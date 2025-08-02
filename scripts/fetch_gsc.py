# Code/scripts/fetch_gsc.py

import os
import pandas as pd
from datetime import datetime, timezone, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_PATH = "config/tracker-ai-core-58a5e68590e5.json"
PROPERTY_URL = "https://www.maisonguida.com/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
DATA_PATH = "data/gsc/"
DIMENSIONS = ["query", "page", "country", "device", "date"]

def get_gsc_service():
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds)

def get_latest_date(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, parse_dates=["date"])
        latest = df["date"].max().date()
        return latest + timedelta(days=1)
    else:
        return datetime.now(timezone.utc).date() - timedelta(days=3)

def fetch_and_append(service, dimension):
    output_file = os.path.join(DATA_PATH, f"master_{dimension}s.csv")
    file_path = output_file
    start_date = get_latest_date(file_path)
    end_date = datetime.now(timezone.utc).date() - timedelta(days=2)  # GSC delay
    current_date = start_date
    all_records = []

    while current_date <= end_date:
        request = {
            "startDate": current_date.strftime("%Y-%m-%d"),
            "endDate": current_date.strftime("%Y-%m-%d"),
            "dimensions": [] if dimension == "date" else [dimension],
            "rowLimit": 25000
        }

        response = service.searchanalytics().query(siteUrl=PROPERTY_URL, body=request).execute()
        rows = response.get("rows", [])

        for row in rows:
            record = {
                "date": current_date.strftime("%Y-%m-%d"),
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": row.get("ctr", 0),
                "position": row.get("position", 0)
            }
            if dimension != "date":
                record[dimension] = row["keys"][0]
            all_records.append(record)

        current_date += timedelta(days=1)

    if all_records:
        df_new = pd.DataFrame(all_records)
        os.makedirs(DATA_PATH, exist_ok=True)

        if os.path.exists(output_file):
            df_existing = pd.read_csv(output_file)
            dedupe_key = ["date"] if dimension == "date" else ["date", dimension]
            df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=dedupe_key)
        else:
            df_combined = df_new

        df_combined.to_csv(output_file, index=False)
        print(f"[✓] Updated {output_file} with {len(df_new)} new rows.")
    else:
        print(f"[ ] No new data for {dimension}.")


