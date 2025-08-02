# TRACKER-AI-CORE

TRACKER-AI-CORE is a lightweight tracking system that collects and stores daily analytics from both **Google Search Console (GSC)** and **Google Analytics 4 (GA4)**. It provides a consistent CSV-based dataset for SEO-AI or marketing intelligence apps to work with real performance data.

---

## ✅ Features

- **Google Search Console (GSC)**:
  - Collects daily stats for:
    - Queries
    - Pages
    - Countries
    - Devices
    - Dates (summary)

- **Google Analytics 4 (GA4)**:
  - Collects daily stats for:
    - Active Users
    - New Users
    - Sessions
    - Bounce Rate
    - Session Duration
    - Engaged Sessions
    - Engagement Rate
    - Event Count
  - Breakdowns by:
    - Country
    - City
    - Device Category

---

## 📂 File Structure

```
Code/
├── run_tracker.py                  # CLI entrypoint
├── scripts/
│   ├── fetch_gsc.py               # Handles GSC downloads
│   └── fetch_ga4.py               # Handles GA4 downloads
├── config/
│   └── tracker-ai-core-xxx.json   # Your Google service account credentials
└── data/
    ├── ga4/
    │   └── master_ga4.csv         # Daily enhanced GA4 dataset
    └── gsc/
        ├── master_dates.csv       # Daily GSC summary
        ├── master_queries.csv
        ├── master_pages.csv
        ├── master_countries.csv
        └── master_devices.csv
```

---

## 🚀 Usage

### 1. Setup

Install dependencies in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place your **Google Service Account JSON key** in `config/` and update `CREDENTIALS_PATH` in both fetch scripts.

### 2. Fetch Data

Run the following:

#### ✅ Update both GSC + GA4 daily:
```bash
python run_tracker.py --update
python run_tracker.py --ga4
```

#### 🧪 Check that data is being written:
```bash
cat data/ga4/master_ga4.csv
cat data/gsc/master_queries.csv
```

---

## 📊 Use Cases

- Feed real performance metrics into SEO-AI for keyword validation.
- Measure actual engagement by geography, device, and session type.
- Correlate GSC keyword positions with bounce rate or session time.
- Detect campaign or drop performance shifts quickly.

---

## 🛠 Roadmap Ideas

- Automatic daily CRON runner
- API wrapper to export to Google Sheets
- Add UTM-based campaign tracking in GA4
- Slack/email alerts on anomalies

---

## 🤖 Author

Built with ❤️ by [John Watkinson] and ChatGPT for real-world SEO + analytics tracking.

