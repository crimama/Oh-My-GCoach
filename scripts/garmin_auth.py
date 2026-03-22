"""Garmin Connect authentication module.

Uses garth OAuth to authenticate, then makes direct API calls with Bearer token.
Workaround for garth's session passing bug.
"""

import os
import sys
from pathlib import Path
from getpass import getpass

import requests
from dotenv import load_dotenv
from garth import Client as GarthClient

SCRIPT_DIR = Path(__file__).parent
ENV_FILE = SCRIPT_DIR / ".env"
TOKEN_DIR = Path.home() / ".garminconnect"
API_BASE = "https://connectapi.garmin.com"

load_dotenv(ENV_FILE)


class GarminClient:
    """Lightweight Garmin Connect client.

    Authenticates via garth, then calls API directly with Bearer token.
    """

    def __init__(self, garth_client: GarthClient):
        self.garth = garth_client
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {garth_client.oauth2_token.access_token}",
            "DI-Backend": "connectapi.garmin.com",
            "User-Agent": "GarminConnect/5.0",
        })

    def _get(self, path: str, params: dict = None):
        resp = self.session.get(f"{API_BASE}{path}", params=params, timeout=30)
        resp.raise_for_status()
        if resp.status_code == 204:
            return None
        return resp.json()

    # === Activities ===

    def get_activities(self, start: int = 0, limit: int = 20):
        return self._get(
            "/activitylist-service/activities/search/activities",
            {"start": start, "limit": limit},
        )

    def get_activities_by_date(self, start_date: str, end_date: str,
                                activity_type: str = None):
        params = {"startDate": start_date, "endDate": end_date}
        if activity_type:
            params["activityType"] = activity_type
        return self._get(
            "/activitylist-service/activities/search/activities",
            params,
        )

    def get_activity_details(self, activity_id: int):
        return self._get(f"/activity-service/activity/{activity_id}")

    def get_activity_hr_in_timezones(self, activity_id: int):
        return self._get(
            f"/activity-service/activity/{activity_id}/hrTimeInZones"
        )

    def get_activity_splits(self, activity_id: int):
        return self._get(f"/activity-service/activity/{activity_id}/splits")

    # === Health Metrics ===

    def get_stats(self, date: str):
        return self._get(f"/usersummary-service/usersummary/daily/{date}")

    def get_daily_weigh_ins(self, date: str):
        return self._get(f"/weight-service/weight/dayview/{date}")

    def get_weigh_ins(self, start_date: str, end_date: str):
        return self._get(
            "/weight-service/weight/dateRange",
            {"startDate": start_date, "endDate": end_date},
        )

    def get_body_composition(self, start_date: str, end_date: str = None):
        params = {"startDate": start_date}
        if end_date:
            params["endDate"] = end_date
        return self._get("/weight-service/weight/dateRange", params)

    def get_sleep_data(self, date: str):
        return self._get(
            "/wellness-service/wellness/dailySleep",
            {"date": date},
        )

    def get_hrv_data(self, date: str):
        return self._get(f"/hrv-service/hrv/{date}")

    def get_rhr_day(self, date: str):
        """Resting heart rate from dailyHeartRate endpoint."""
        return self._get(
            "/wellness-service/wellness/dailyHeartRate",
            {"date": date},
        )

    def get_heart_rates(self, date: str):
        return self._get(
            "/wellness-service/wellness/dailyHeartRate",
            {"date": date},
        )

    def get_all_day_stress(self, date: str):
        return self._get(f"/wellness-service/wellness/dailyStress/{date}")

    def get_body_battery(self, date: str):
        """Body battery - endpoint may not be available for all devices."""
        try:
            return self._get(
                "/wellness-service/wellness/bodyBattery/reports/daily",
                {"date": date},
            )
        except Exception:
            return None

    def get_training_readiness(self, date: str):
        return self._get(f"/metrics-service/metrics/trainingreadiness/{date}")

    def get_training_status(self, date: str):
        return self._get(
            f"/metrics-service/metrics/trainingstatus/aggregated/{date}"
        )

    def get_max_metrics(self, date: str):
        return self._get(f"/metrics-service/metrics/maxmet/daily/{date}")

    def get_race_predictions(self):
        return self._get(
            "/metrics-service/metrics/racepredictions/latest/all"
        )

    # === Device / Profile ===

    def get_devices(self):
        return self._get("/device-service/deviceregistration/devices")

    def get_full_name(self):
        return self._get("/userprofile-service/socialProfile")


def get_client() -> GarminClient:
    """Return an authenticated GarminClient."""

    # 1) Try saved token
    if TOKEN_DIR.exists():
        try:
            garth = GarthClient()
            garth.load(str(TOKEN_DIR))
            client = GarminClient(garth)
            client.get_devices()  # connection test
            return client
        except Exception:
            print("Saved token expired. Re-authenticating...")

    # 2) New login
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")

    if not email or not password:
        if sys.stdin.isatty():
            email = email or input("Garmin email: ")
            password = password or getpass("Garmin password: ")
        else:
            print("ERROR: Garmin credentials not found.")
            print("  Set in scripts/.env:")
            print("  GARMIN_EMAIL=your@email.com")
            print("  GARMIN_PASSWORD=yourpassword")
            sys.exit(1)

    garth = GarthClient()
    garth.login(email, password)
    garth.dump(str(TOKEN_DIR))
    print(f"Token saved: {TOKEN_DIR}")

    return GarminClient(garth)


if __name__ == "__main__":
    c = get_client()
    devices = c.get_devices()
    print(f"Login OK! Devices: {[d.get('displayName', d.get('applicationKey')) for d in devices]}")
