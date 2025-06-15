import os
import json
from datetime import datetime

LOG_PATH = "logs/applications.json"

def ensure_log_file():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

def log_application(
    job_title: str,
    company: str,
    job_description: str,
    cover_letter_text: str,
    platform: str,
    status: str = "submitted",
    job_url: str = "",
    tags: list = None
):
    ensure_log_file()

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "job_title": job_title.strip(),
        "company": company.strip() or "Unknown",
        "platform": platform.strip(),
        "job_url": job_url,
        "status": status,
        "tags": tags or [],
        "job_description_snippet": job_description[:300].strip() + "...",
        "cover_letter": cover_letter_text.strip()
    }

    # Load existing logs
    with open(LOG_PATH, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        # Avoid duplicates: same title + platform + company
        is_duplicate = any(
            entry["job_title"].lower() == log_entry["job_title"].lower() and
            entry["company"].lower() == log_entry["company"].lower() and
            entry["platform"].lower() == log_entry["platform"].lower()
            for entry in data
        )

        if not is_duplicate:
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            print(f"📝 Logged application: {job_title} at {company} [{platform}]")
        else:
            print(f"⚠️ Skipped logging (duplicate): {job_title} at {company} [{platform}]")
