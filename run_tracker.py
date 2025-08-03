from scripts.fetch_gsc import fetch_and_append, get_gsc_service
from scripts.fetch_ga4 import run_ga4

# GSC dimensions to track
DIMENSIONS = ["query", "page", "country", "device", "date"]

def run():
    service = get_gsc_service()
    for dim in DIMENSIONS:
        fetch_and_append(service, dim)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run GSC Tracker")
    parser.add_argument("--gsc", action="store_true", help="Fetch and append new GSC data")
    parser.add_argument("--ga4", action="store_true", help="Fetch and append new GA4 data")

    args = parser.parse_args()

    if args.ga4:
        run_ga4()
    elif args.update:
        run()
    else:
        print("Use --gsc (GSC) or --ga4 (Analytics) to fetch data.")
