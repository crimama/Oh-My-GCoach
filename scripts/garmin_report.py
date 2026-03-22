"""Weekly report generation module.

Weekly volume, zone distribution, 80/20 check, 10% rule, health metrics summary.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from garmin_activities import (
    get_running_activities,
    get_hr_zones,
    calc_weekly_volume,
    calc_zone_distribution,
    calc_easy_hard_ratio,
    check_volume_rule,
    format_pace,
    format_duration,
    classify_hr_zone,
)
from garmin_health import (
    get_weight_range,
    get_sleep,
    get_resting_hr,
    get_hrv,
    calc_weight_moving_avg,
)


def get_week_range(date: str) -> tuple:
    """Get Monday-Sunday range for the week containing the given date."""
    dt = datetime.strptime(date, "%Y-%m-%d")
    monday = dt - timedelta(days=dt.weekday())
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def get_prev_week_range(date: str) -> tuple:
    """Get previous week's date range."""
    dt = datetime.strptime(date, "%Y-%m-%d")
    monday = dt - timedelta(days=dt.weekday())
    prev_sunday = monday - timedelta(days=1)
    prev_monday = prev_sunday - timedelta(days=6)
    return prev_monday.strftime("%Y-%m-%d"), prev_sunday.strftime("%Y-%m-%d")


def generate_weekly_report(client, date: str) -> str:
    """Generate weekly report as markdown.

    Args:
        date: Any date within the target week (YYYY-MM-DD)
    """
    week_start, week_end = get_week_range(date)
    prev_start, prev_end = get_prev_week_range(date)

    dt = datetime.strptime(week_start, "%Y-%m-%d")
    iso_year, iso_week, _ = dt.isocalendar()

    # Running data
    activities = get_running_activities(client, week_start, week_end)
    volume = calc_weekly_volume(activities)

    # Previous week volume (10% rule check)
    prev_activities = get_running_activities(client, prev_start, prev_end)
    prev_volume = calc_weekly_volume(prev_activities)
    vol_check = check_volume_rule(volume["total_km"], prev_volume["total_km"])

    # Weekly HR zone aggregation
    all_zone_secs = {}
    for act in activities:
        act_id = act.get("activityId")
        if not act_id:
            continue
        try:
            hr_data = get_hr_zones(client, act_id)
            if hr_data:
                for zone in hr_data:
                    zn = f"Z{zone.get('zoneNumber', 0)}"
                    all_zone_secs[zn] = all_zone_secs.get(zn, 0) + zone.get("secsInZone", 0)
        except Exception:
            continue

    total_zone_secs = sum(all_zone_secs.values())
    zone_dist = {}
    if total_zone_secs > 0:
        zone_dist = {k: round(v / total_zone_secs * 100, 1) for k, v in sorted(all_zone_secs.items())}

    easy_hard = calc_easy_hard_ratio(zone_dist) if zone_dist else None

    # Health metrics (weekly average)
    weight_7d_start = (datetime.strptime(week_end, "%Y-%m-%d") - timedelta(days=6)).strftime("%Y-%m-%d")
    weights = get_weight_range(client, weight_7d_start, week_end)
    weight_avg = calc_weight_moving_avg(weights) if weights else None

    sleep_scores = []
    sleep_totals = []
    rhr_values = []
    hrv_values = []

    current = datetime.strptime(week_start, "%Y-%m-%d")
    end_dt = datetime.strptime(week_end, "%Y-%m-%d")
    while current <= end_dt:
        d = current.strftime("%Y-%m-%d")
        s = get_sleep(client, d)
        if s:
            sleep_totals.append(s["total_min"])
            if s.get("score"):
                sleep_scores.append(s["score"])
        rhr = get_resting_hr(client, d)
        if rhr:
            rhr_values.append(rhr)
        h = get_hrv(client, d)
        if h and h.get("last_night"):
            hrv_values.append(h["last_night"])
        current += timedelta(days=1)

    # Build report
    lines = []
    lines.append(f"# Weekly Report - {iso_year}-W{iso_week:02d}")
    lines.append(f"> {week_start} ~ {week_end}")
    lines.append("")

    # Volume summary
    lines.append("## Running Volume")
    lines.append("")
    lines.append("| Metric | This Week | Last Week |")
    lines.append("|--------|-----------|-----------|")
    lines.append(f"| Distance | **{volume['total_km']} km** | {prev_volume['total_km']} km |")
    lines.append(f"| Sessions | {volume['sessions']} | {prev_volume['sessions']} |")
    lines.append(f"| Duration | {volume['total_duration']} | {prev_volume['total_duration']} |")
    lines.append(f"| Calories | {volume['total_calories']} kcal | {prev_volume['total_calories']} kcal |")
    lines.append(f"| 10% Rule | {vol_check['message']} | |")
    lines.append("")

    # Zone distribution
    if zone_dist:
        lines.append("## HR Zone Distribution (Weekly)")
        lines.append("")
        lines.append("| Zone | % |")
        lines.append("|------|---|")
        for z, pct in sorted(zone_dist.items()):
            lines.append(f"| {z} | {pct}% |")
        if easy_hard:
            lines.append(f"| **Easy/Hard** | **{easy_hard['easy']}% / {easy_hard['hard']}%** |")
            lines.append("")
            if easy_hard["easy"] >= 78:
                lines.append("> 80/20 OK (Easy {:.0f}%)".format(easy_hard["easy"]))
            else:
                lines.append("> WARNING: 80/20 violation! Easy {}% - keep easy runs HR <= 140".format(easy_hard["easy"]))
        lines.append("")

    # Health metrics
    lines.append("## Health Metrics (Weekly Avg)")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    if weight_avg:
        lines.append(f"| Weight (7d avg) | {weight_avg} kg |")
    if weights:
        latest = sorted(weights, key=lambda x: x["date"])[-1]
        lines.append(f"| Latest Weight | {latest['weight_kg']} kg ({latest['date']}) |")
    if rhr_values:
        lines.append(f"| Resting HR (avg) | {round(sum(rhr_values)/len(rhr_values))} bpm |")
    if sleep_totals:
        avg_sleep = sum(sleep_totals) / len(sleep_totals)
        h, m = divmod(round(avg_sleep), 60)
        lines.append(f"| Sleep (avg) | {h}h {m}m |")
        if avg_sleep < 450:
            lines.append(f"| | Warning: Weekly avg sleep deficit (<7.5h) |")
    if sleep_scores:
        lines.append(f"| Sleep Score (avg) | {round(sum(sleep_scores)/len(sleep_scores))} |")
    if hrv_values:
        lines.append(f"| HRV (avg) | {round(sum(hrv_values)/len(hrv_values))} ms |")
    lines.append("")

    # Activity list
    lines.append("## Activities")
    lines.append("")
    lines.append("| Date | Distance | Duration | Pace | Avg HR | Zone |")
    lines.append("|------|----------|----------|------|--------|------|")
    for act in sorted(activities, key=lambda x: x.get("startTimeLocal", "")):
        d = act.get("startTimeLocal", "")[:10]
        dist = round((act.get("distance", 0) or 0) / 1000, 1)
        dur = format_duration(act.get("duration"))
        pace = format_pace(act.get("averageSpeed"))
        hr = act.get("averageHR", "--")
        zone = classify_hr_zone(act.get("averageHR"))
        lines.append(f"| {d} | {dist}km | {dur} | {pace} | {hr} | {zone} |")

    return "\n".join(lines)
