"""Garmin Connect running activity data collection module.

Collects activity records, HR zone distribution, weekly volume as markdown.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Garmin Forerunner 965 HR zone boundaries (user-configured)
# Z1: 96-114, Z2: 115-133, Z3: 134-154, Z4: 155-171, Z5: 172+
HR_ZONES = {
    "Z1 (Recovery)": (0, 115),
    "Z2 (Easy)": (115, 134),
    "Z3 (Tempo)": (134, 155),
    "Z4 (Threshold)": (155, 172),
    "Z5 (VO2max)": (172, 999),
}


def get_running_activities(
    client, start: str, end: str
) -> List[Dict]:
    """Get running activities for a date range.

    Args:
        start: Start date (YYYY-MM-DD)
        end: End date (YYYY-MM-DD)

    Returns:
        List of running activity dicts (newest first)
    """
    activities = client.get_activities_by_date(start, end, "running")
    return activities or []


def get_activity_detail(client, activity_id: int) -> Dict:
    """Get activity details (HR zones, laps, etc.)."""
    return client.get_activity_details(activity_id)


def get_hr_zones(client, activity_id: int) -> List[Dict]:
    """Get HR zone time distribution for an activity."""
    return client.get_activity_hr_in_timezones(activity_id)


def format_pace(speed_mps: Optional[float]) -> str:
    """Convert m/s to M'SS"/km pace."""
    if not speed_mps or speed_mps <= 0:
        return "--"
    pace_sec = 1000 / speed_mps
    minutes = int(pace_sec // 60)
    seconds = int(pace_sec % 60)
    return f"{minutes}'{seconds:02d}\"/km"


def format_duration(seconds: Optional[float]) -> str:
    """Convert seconds to HH:MM:SS or MM:SS."""
    if not seconds:
        return "--"
    s = int(seconds)
    h, remainder = divmod(s, 3600)
    m, sec = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


def classify_hr_zone(avg_hr: Optional[float]) -> str:
    """Classify HR zone by average heart rate."""
    if not avg_hr:
        return "N/A"
    for zone_name, (low, high) in HR_ZONES.items():
        if low <= avg_hr < high:
            return zone_name
    return "N/A"


def calc_zone_distribution(hr_zones_data: List[Dict]) -> Dict[str, float]:
    """Calculate zone time percentages from HR zone data.

    Returns:
        {"Z1": 10.5, "Z2": 65.3, ...} (percentages)
    """
    if not hr_zones_data:
        return {}

    total_secs = 0
    zone_secs = {}

    for zone in hr_zones_data:
        zone_num = zone.get("zoneNumber", 0)
        secs = zone.get("secsInZone", 0)
        zone_name = f"Z{zone_num}"
        zone_secs[zone_name] = secs
        total_secs += secs

    if total_secs == 0:
        return {}

    return {k: round(v / total_secs * 100, 1) for k, v in zone_secs.items()}


def calc_easy_hard_ratio(zone_dist: Dict[str, float]) -> Dict[str, float]:
    """Calculate Easy/Hard ratio from zone distribution.

    Easy = Z1 + Z2, Hard = Z3 + Z4 + Z5
    """
    easy = zone_dist.get("Z1", 0) + zone_dist.get("Z2", 0)
    hard = zone_dist.get("Z3", 0) + zone_dist.get("Z4", 0) + zone_dist.get("Z5", 0)
    return {"easy": round(easy, 1), "hard": round(hard, 1)}


def format_activity_md(activity: Dict, hr_zones_data: Optional[List] = None) -> str:
    """Format a single activity as markdown."""
    name = activity.get("activityName", "Running")
    distance_m = activity.get("distance", 0)
    distance_km = round(distance_m / 1000, 2) if distance_m else 0
    duration = activity.get("duration", 0)
    avg_speed = activity.get("averageSpeed", 0)
    avg_hr = activity.get("averageHR")
    max_hr = activity.get("maxHR")
    cadence = activity.get("averageRunningCadenceInStepsPerMinute")
    calories = activity.get("calories", 0)
    start_time = activity.get("startTimeLocal", "")
    elevation_gain = activity.get("elevationGain")
    avg_stride = activity.get("avgStrideLength")
    training_effect = activity.get("aerobicTrainingEffect")
    vo2max = activity.get("vO2MaxValue")

    lines = []
    lines.append(f"### {name}")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("|------|-------|")
    lines.append(f"| Start | {start_time} |")
    lines.append(f"| Distance | {distance_km} km |")
    lines.append(f"| Duration | {format_duration(duration)} |")
    lines.append(f"| Avg Pace | {format_pace(avg_speed)} |")
    if avg_hr:
        lines.append(f"| Avg HR | {avg_hr} bpm |")
    if max_hr:
        lines.append(f"| Max HR | {max_hr} bpm |")
    if cadence:
        lines.append(f"| Cadence | {round(cadence)} spm |")
    if avg_stride:
        lines.append(f"| Avg Stride | {round(avg_stride, 1)} cm |")
    if elevation_gain:
        lines.append(f"| Elevation Gain | {round(elevation_gain)} m |")
    lines.append(f"| Calories | {calories} kcal |")
    if training_effect:
        lines.append(f"| Aerobic TE | {round(training_effect, 1)} |")
    if vo2max:
        lines.append(f"| VO2max | {vo2max} |")
    if avg_hr:
        lines.append(f"| HR Zone | {classify_hr_zone(avg_hr)} |")

    # HR zone distribution
    if hr_zones_data:
        zone_dist = calc_zone_distribution(hr_zones_data)
        if zone_dist:
            ratio = calc_easy_hard_ratio(zone_dist)
            lines.append("")
            lines.append("**HR Zone Distribution**")
            lines.append("")
            lines.append("| Zone | % |")
            lines.append("|------|---|")
            for z, pct in sorted(zone_dist.items()):
                lines.append(f"| {z} | {pct}% |")
            lines.append(f"| **Easy/Hard** | **{ratio['easy']}% / {ratio['hard']}%** |")

            if ratio["easy"] < 75:
                lines.append("")
                lines.append(f"> Warning: Easy ratio {ratio['easy']}% - below 80/20 target!")

    return "\n".join(lines)


def calc_weekly_volume(activities: List[Dict]) -> Dict:
    """Aggregate weekly volume from activities.

    Returns:
        {"total_km": 35.2, "sessions": 5, "avg_hr": 128, ...}
    """
    total_distance = 0
    total_duration = 0
    total_calories = 0
    hr_sum = 0
    hr_count = 0

    for a in activities:
        d = a.get("distance", 0) or 0
        total_distance += d
        total_duration += a.get("duration", 0) or 0
        total_calories += a.get("calories", 0) or 0
        hr = a.get("averageHR")
        if hr:
            hr_sum += hr
            hr_count += 1

    return {
        "total_km": round(total_distance / 1000, 1),
        "sessions": len(activities),
        "total_duration": format_duration(total_duration),
        "total_calories": round(total_calories),
        "avg_hr": round(hr_sum / hr_count) if hr_count else None,
    }


def check_volume_rule(current_km: float, previous_km: float) -> Dict:
    """Check 10% rule for weekly volume increase.

    Returns:
        {"change_pct": 15.2, "violation": True, "message": "..."}
    """
    if previous_km == 0:
        return {"change_pct": 0, "violation": False, "message": "No previous week data"}

    change = ((current_km - previous_km) / previous_km) * 100
    violation = change > 10
    msg = f"{change:+.1f}% ({'WARNING: 10% rule violation!' if violation else 'OK'})"
    return {"change_pct": round(change, 1), "violation": violation, "message": msg}
