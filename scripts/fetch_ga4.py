
# fetch_ga4.py

import os
import pandas as pd
from datetime import datetime, timedelta, timezone
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Metric,
    Dimension,
    RunReportRequest
)
from google.oauth2 import service_account

# === CONFIGURATION ===
GA4_PROPERTY_ID = "473367988"
DATA_PATH = os.path.join("data", "ga4")
CREDENTIALS_PATH = "config/tracker-ai-core-58a5e68590e5.json"
OUTPUT_FILE = os.path.join(DATA_PATH, "master_ga4.csv")

# === AUTH ===
def get_ga4_client():
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    return BetaAnalyticsDataClient(credentials=credentials)

# === UTILITIES ===
def get_latest_date(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, parse_dates=["date"])
        return df["date"].max().date()
    return datetime(2025, 8, 1, tzinfo=timezone.utc).date() - timedelta(days=1)

# === DATA FETCHING ===
def fetch_daily_stats(client, start_date, end_date):
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="country"),
            Dimension(name="city"),
            Dimension(name="deviceCategory"),
        ],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="sessions"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="engagedSessions"),
            Metric(name="engagementRate"),
            Metric(name="eventCount"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=25000
    )

    response = client.run_report(request)
    records = []

    for row in response.rows:
        record = {
            "date": row.dimension_values[0].value,
            "country": row.dimension_values[1].value,
            "city": row.dimension_values[2].value,
            "deviceCategory": row.dimension_values[3].value,
            "activeUsers": int(row.metric_values[0].value),
            "newUsers": int(row.metric_values[1].value),
            "sessions": int(row.metric_values[2].value),
            "bounceRate": float(row.metric_values[3].value),
            "avgSessionDuration": float(row.metric_values[4].value),
            "engagedSessions": int(row.metric_values[5].value),
            "engagementRate": float(row.metric_values[6].value),
            "eventCount": int(row.metric_values[7].value),
        }
        records.append(record)

    return records

# === SAVE RESULTS ===
def save_to_csv(records, file_path):
    if not records:
        print("[ ] No new GA4 data.")
        return

    df_new = pd.DataFrame(records)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df_new]).drop_duplicates()
    else:
        df_combined = df_new

    df_combined.to_csv(file_path, index=False)
    print(f"[✓] Updated GA4 data with {len(df_new)} new rows.")

# === MAIN ENTRYPOINT ===
def run_ga4():
    client = get_ga4_client()
    today = datetime.now(timezone.utc).date()
    last_date = get_latest_date(OUTPUT_FILE)
    next_day = last_date + timedelta(days=1)

    if next_day >= today:
        print("[ ] No new GA4 data.")
        return

    print(f"[•] Fetching GA4 data from {next_day} to {today - timedelta(days=1)}")
    records = fetch_daily_stats(client, str(next_day), str(today - timedelta(days=1)))
    save_to_csv(records, OUTPUT_FILE)
