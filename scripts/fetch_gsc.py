import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load env vars
load_dotenv()

# Config from .env
GSC_CLIENT_EMAIL = os.getenv("GSC_CLIENT_EMAIL")
GSC_PRIVATE_KEY = os.getenv("GSC_PRIVATE_KEY").replace('\\n', '\n')
PROPERTY_URL = os.getenv("GSC_PROPERTY_URL")
OUTPUT_PATH = 'data/gsc/gsc_overview.csv'


def get_gsc_service():
    creds_info = {
        "type": "service_account",
        "client_email": GSC_CLIENT_EMAIL,
        "private_key": GSC_PRIVATE_KEY,
        "token_uri": "https://oauth2.googleapis.com/token"
    }
    creds = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    return build("searchconsole", "v1", credentials=creds)

def fetch_gsc_overview(start_date, end_date):
    service = get_gsc_service()
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'aggregationType': 'auto',
        'dimensions': [],
    }
    response = service.searchanalytics().query(siteUrl=PROPERTY_URL, body=request).execute()
    if 'rows' not in response:
        return None

    row = response['rows'][0]
    return {
        'date_start': start_date,
        'date_end': end_date,
        'clicks': row.get('clicks', 0),
        'impressions': row.get('impressions', 0),
        'ctr': row.get('ctr', 0),
        'position': row.get('position', 0)
    }

def save_to_csv(data, output_file):
    df = pd.DataFrame([data])
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    if os.path.exists(output_file):
        df.to_csv(output_file, mode='a', header=False, index=False)
    else:
        df.to_csv(output_file, index=False)

def run(start_days_ago=7, end_days_ago=1):
    end_date = datetime.utcnow() - timedelta(days=end_days_ago)
    start_date = datetime.utcnow() - timedelta(days=start_days_ago)
    data = fetch_gsc_overview(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    if data:
        save_to_csv(data, OUTPUT_PATH)
        print(f"[✓] GSC overview data saved: {OUTPUT_PATH}")
    else:
        print("[!] No data returned from GSC API.")

