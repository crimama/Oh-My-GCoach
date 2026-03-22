#!/usr/bin/env python3
"""Garmin Connect data sync main script.

Usage:
    python garmin_sync.py                     # Today's data
    python garmin_sync.py --date 2026-03-17   # Specific date
    python garmin_sync.py --week              # This week's report
    python garmin_sync.py --week --date 2026-03-17  # Week report for date
    python garmin_sync.py --range 2026-03-01 2026-03-17  # Date range activities
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from garmin_auth import get_client
from garmin_activities import (
    get_running_activities,
    get_hr_zones,
    format_activity_md,
    calc_weekly_volume,
    calc_zone_distribution,
    calc_easy_hard_ratio,
)
from garmin_health import (
    get_weight,
    get_sleep,
    get_hrv,
    get_resting_hr,
    get_stress,
    get_body_battery,
    get_training_readiness,
    get_race_predictions,
    format_daily_health_md,
)
from garmin_report import generate_weekly_report, get_week_range

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TRAINING_DIR = DATA_DIR / "training"
HEALTH_DIR = DATA_DIR / "health"


def sync_daily(client, date: str):
    """Sync running + health data for a specific date."""
    print(f"\n{'='*50}")
    print(f"[{date}] Syncing data...")
    print(f"{'='*50}")

    # Running activities
    print("\nFetching running activities...")
    activities = get_running_activities(client, date, date)
    all_hr_zones = {}

    if activities:
        print(f"  {len(activities)} activities found")
        for act in activities:
            act_id = act.get("activityId")
            act_hr_zones = None
            if act_id:
                try:
                    act_hr_zones = get_hr_zones(client, act_id)
                    all_hr_zones[act_id] = act_hr_zones
                except Exception:
                    pass

            md = format_activity_md(act, act_hr_zones)
            print(f"\n{md}")

            if act_hr_zones:
                zone_dist = calc_zone_distribution(act_hr_zones)
                if zone_dist:
                    ratio = calc_easy_hard_ratio(zone_dist)
                    print(f"\n  -> Easy/Hard: {ratio['easy']}% / {ratio['hard']}%", end="")
                    if ratio["easy"] < 78:
                        print(" WARNING: Below 80/20!")
                    else:
                        print(" OK")
    else:
        print("  No running activities")

    # Health metrics
    print("\nFetching health metrics...")
    weight = get_weight(client, date)
    sleep = get_sleep(client, date)
    hrv = get_hrv(client, date)
    rhr = get_resting_hr(client, date)
    stress = get_stress(client, date)
    battery = get_body_battery(client, date)
    readiness = get_training_readiness(client, date)

    health_md = format_daily_health_md(
        date, weight=weight, sleep=sleep, hrv=hrv,
        rhr=rhr, stress=stress, battery=battery,
        readiness=readiness,
    )
    print(f"\n{health_md}")

    # Race predictions
    predictions = get_race_predictions(client, date)
    if predictions:
        print("\nRace Predictions:")
        for dist, time in predictions.items():
            if time:
                print(f"  {dist}: {time}")

    # Save to file
    save_daily(date, activities, all_hr_zones, health_md)


def save_daily(date: str, activities, hr_zones, health_md: str):
    """Save daily data to files."""
    dt = datetime.strptime(date, "%Y-%m-%d")
    month_str = dt.strftime("%Y-%m")

    HEALTH_DIR.mkdir(parents=True, exist_ok=True)

    recovery_file = HEALTH_DIR / f"{month_str}-recovery.md"
    header = f"# {dt.strftime('%Y-%m')} Recovery Metrics\n\n"

    if recovery_file.exists():
        content = recovery_file.read_text(encoding="utf-8")
        marker = f"## {date} Health Metrics"
        if marker in content:
            start = content.index(marker)
            next_section = content.find("\n## ", start + 1)
            if next_section == -1:
                content = content[:start] + health_md + "\n"
            else:
                content = content[:start] + health_md + "\n\n" + content[next_section:]
        else:
            content = content.rstrip() + "\n\n" + health_md + "\n"
    else:
        content = header + health_md + "\n"

    recovery_file.write_text(content, encoding="utf-8")
    print(f"\nSaved: {recovery_file}")


def sync_week(client, date: str):
    """Generate weekly report."""
    print(f"\nGenerating weekly report ({date})...")
    report = generate_weekly_report(client, date)
    print(f"\n{report}")

    week_start, week_end = get_week_range(date)
    dt = datetime.strptime(week_start, "%Y-%m-%d")
    iso_year, iso_week, _ = dt.isocalendar()
    filename = f"{iso_year}-W{iso_week:02d}-weekly-report.md"

    TRAINING_DIR.mkdir(parents=True, exist_ok=True)
    report_file = TRAINING_DIR / filename
    report_file.write_text(report, encoding="utf-8")
    print(f"\nSaved: {report_file}")


def sync_range(client, start: str, end: str):
    """List running activities for a date range."""
    print(f"\n{start} ~ {end} Activities")
    activities = get_running_activities(client, start, end)

    if not activities:
        print("  No activities")
        return

    volume = calc_weekly_volume(activities)
    print(f"\nTotal: {volume['sessions']} sessions | {volume['total_km']}km | {volume['total_duration']}")
    print(f"\n| Date | Distance | Duration | Pace | Avg HR |")
    print(f"|------|----------|----------|------|--------|")

    from garmin_activities import format_pace, format_duration
    for act in sorted(activities, key=lambda x: x.get("startTimeLocal", "")):
        d = act.get("startTimeLocal", "")[:10]
        dist = round((act.get("distance", 0) or 0) / 1000, 1)
        dur = format_duration(act.get("duration"))
        pace = format_pace(act.get("averageSpeed"))
        hr = act.get("averageHR", "--")
        print(f"| {d} | {dist}km | {dur} | {pace} | {hr} |")


def main():
    parser = argparse.ArgumentParser(description="Garmin Connect Data Sync")
    parser.add_argument("--date", "-d", help="Date (YYYY-MM-DD, default: today)")
    parser.add_argument("--week", "-w", action="store_true", help="Generate weekly report")
    parser.add_argument("--range", "-r", nargs=2, metavar=("START", "END"),
                        help="Date range (YYYY-MM-DD YYYY-MM-DD)")
    args = parser.parse_args()

    date = args.date or datetime.now().strftime("%Y-%m-%d")

    print("Logging into Garmin Connect...")
    client = get_client()
    print("Login successful!")

    if args.range:
        sync_range(client, args.range[0], args.range[1])
    elif args.week:
        sync_week(client, date)
    else:
        sync_daily(client, date)

    print("\nSync complete!")


if __name__ == "__main__":
    main()
