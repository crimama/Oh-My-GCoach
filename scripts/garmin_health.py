"""Garmin Connect health metrics collection module.

Collects weight, sleep, HRV, resting HR, stress data.
"""

from typing import Dict, List, Optional


def get_weight(client, date: str) -> Optional[Dict]:
    """Get weight data for a specific date."""
    try:
        data = client.get_daily_weigh_ins(date)
        if not data:
            return None
        entries = data.get("dateWeightList", [])
        if not entries:
            return None
        entry = entries[0]
        weight_g = entry.get("weight", 0)
        if not weight_g:
            return None
        weight_kg = round(weight_g / 1000, 1) if weight_g > 1000 else round(weight_g, 1)
        return {
            "weight_kg": weight_kg,
            "bmi": round(entry["bmi"], 1) if entry.get("bmi") else None,
            "body_fat_pct": round(entry["bodyFat"], 1) if entry.get("bodyFat") else None,
        }
    except Exception:
        return None


def get_weight_range(client, start: str, end: str) -> List[Dict]:
    """Get weight data for a date range."""
    try:
        data = client.get_weigh_ins(start, end)
        entries = data.get("dateWeightList", [])
        results = []
        for entry in entries:
            w = entry.get("weight", 0)
            if w and w > 0:
                date_ts = entry.get("date")
                if isinstance(date_ts, (int, float)):
                    from datetime import datetime
                    date_str = datetime.fromtimestamp(date_ts / 1000).strftime("%Y-%m-%d")
                else:
                    date_str = str(date_ts)[:10]
                results.append({
                    "date": date_str,
                    "weight_kg": round(w / 1000, 1) if w > 1000 else round(w, 1),
                })
        return results
    except Exception:
        return []


def get_sleep(client, date: str) -> Optional[Dict]:
    """Get sleep data."""
    try:
        data = client.get_sleep_data(date)
        if not data or not isinstance(data, dict):
            return None

        def to_min(seconds):
            return round(seconds / 60) if seconds else 0

        total = data.get("sleepTimeSeconds")
        if not total:
            return None

        scores = data.get("sleepScores", {})
        overall = scores.get("overall", {})
        score = overall.get("value") if isinstance(overall, dict) else None

        return {
            "total_min": to_min(total),
            "deep_min": to_min(data.get("deepSleepSeconds")),
            "light_min": to_min(data.get("lightSleepSeconds")),
            "rem_min": to_min(data.get("remSleepSeconds")),
            "awake_min": to_min(data.get("awakeSleepSeconds")),
            "score": score,
        }
    except Exception:
        return None


def get_hrv(client, date: str) -> Optional[Dict]:
    """Get HRV data."""
    try:
        data = client.get_hrv_data(date)
        if not data:
            return None
        summary = data.get("hrvSummary", {})
        if not summary:
            return None
        return {
            "weekly_avg": summary.get("weeklyAvg"),
            "last_night": summary.get("lastNightAvg"),
            "status": summary.get("status"),
            "baseline_low": summary.get("baselineLowUpper"),
            "baseline_high": summary.get("baselineBalancedUpper"),
        }
    except Exception:
        return None


def get_resting_hr(client, date: str) -> Optional[int]:
    """Get resting heart rate."""
    try:
        data = client.get_rhr_day(date)
        if not data or not isinstance(data, dict):
            return None
        rhr = data.get("restingHeartRate")
        return round(rhr) if rhr else None
    except Exception:
        return None


def get_stress(client, date: str) -> Optional[Dict]:
    """Get stress data."""
    try:
        data = client.get_all_day_stress(date)
        if not data or not isinstance(data, dict):
            return None

        avg = data.get("avgStressLevel")
        max_val = data.get("maxStressLevel")
        if avg is None:
            return None

        return {
            "avg": round(avg),
            "max": max_val,
        }
    except Exception:
        return None


def get_body_battery(client, date: str) -> Optional[Dict]:
    """Get body battery data."""
    try:
        data = client.get_body_battery(date)
        if not data:
            return None

        if isinstance(data, list):
            values = [e.get("bodyBatteryLevel", 0) for e in data
                      if isinstance(e, dict) and e.get("bodyBatteryLevel")]
        elif isinstance(data, dict):
            values = [data.get("highBB"), data.get("lowBB")]
            values = [v for v in values if v]
        else:
            return None

        if not values:
            return None
        return {
            "high": max(values),
            "low": min(values),
            "drain": max(values) - min(values),
        }
    except Exception:
        return None


def get_training_readiness(client, date: str) -> Optional[Dict]:
    """Get training readiness score."""
    try:
        data = client.get_training_readiness(date)
        if not data:
            return None

        if isinstance(data, list):
            if not data:
                return None
            entry = data[0]
        else:
            entry = data

        return {
            "score": entry.get("score"),
            "level": entry.get("level"),
        }
    except Exception:
        return None


def get_race_predictions(client, date: str = None) -> Optional[Dict]:
    """Get race time predictions."""
    try:
        data = client.get_race_predictions()
        if not data or not isinstance(data, dict):
            return None

        def fmt_time(secs):
            if not secs:
                return None
            s = int(secs)
            h, r = divmod(s, 3600)
            m, sec = divmod(r, 60)
            if h > 0:
                return f"{h}:{m:02d}:{sec:02d}"
            return f"{m}:{sec:02d}"

        return {
            "5k": fmt_time(data.get("time5K")),
            "10k": fmt_time(data.get("time10K")),
            "hm": fmt_time(data.get("timeHalfMarathon")),
            "fm": fmt_time(data.get("timeMarathon")),
        }
    except Exception:
        return None


def format_daily_health_md(date: str, weight=None, sleep=None, hrv=None,
                           rhr=None, stress=None, battery=None,
                           readiness=None) -> str:
    """Format daily health metrics as markdown."""
    lines = []
    lines.append(f"## {date} Health Metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")

    if weight:
        lines.append(f"| Weight | {weight['weight_kg']} kg |")
        if weight.get("bmi"):
            lines.append(f"| BMI | {weight['bmi']} |")
        if weight.get("body_fat_pct"):
            lines.append(f"| Body Fat | {weight['body_fat_pct']}% |")

    if rhr:
        lines.append(f"| Resting HR | {rhr} bpm |")

    if sleep:
        h, m = divmod(sleep["total_min"], 60)
        lines.append(f"| Sleep | {h}h {m}m |")
        if sleep.get("score"):
            lines.append(f"| Sleep Score | {sleep['score']} |")
        lines.append(f"| Deep Sleep | {sleep['deep_min']}m |")
        lines.append(f"| REM Sleep | {sleep['rem_min']}m |")

        if sleep["total_min"] < 450:  # 7.5h = 450min
            lines.append(f"| | Warning: Sleep deficit ({h}h {m}m < 7.5h) |")

    if hrv:
        if hrv.get("last_night"):
            lines.append(f"| HRV (last night) | {hrv['last_night']} ms |")
        if hrv.get("weekly_avg"):
            lines.append(f"| HRV (weekly avg) | {hrv['weekly_avg']} ms |")
        if hrv.get("status"):
            lines.append(f"| HRV Status | {hrv['status']} |")

    if stress:
        lines.append(f"| Stress (avg) | {stress['avg']} |")
        if stress.get("max"):
            lines.append(f"| Stress (max) | {stress['max']} |")

    if battery:
        lines.append(f"| Body Battery | {battery['low']}-{battery['high']} |")

    if readiness:
        if readiness.get("score"):
            lines.append(f"| Training Readiness | {readiness['score']} ({readiness.get('level', '')}) |")

    return "\n".join(lines)


def calc_weight_moving_avg(weights: List[Dict], window: int = 7) -> Optional[float]:
    """Calculate 7-day moving average weight."""
    if len(weights) < window:
        return None
    recent = sorted(weights, key=lambda x: x["date"])[-window:]
    avg = sum(w["weight_kg"] for w in recent) / window
    return round(avg, 1)
