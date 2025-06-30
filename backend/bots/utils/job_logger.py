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
LOG_PATH = "logs/applications.json"

def has_already_applied(user_id: str, job_url: str) -> bool:
    if not os.path.exists(LOG_PATH):
        return False
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            try:
                entry = json.loads(line)
                if entry.get("user_id") == user_id and entry.get("job_url") == job_url:
                    return True
            except json.JSONDecodeError:
                continue
    except Exception as e:
        print(f"Error checking deduplication log: {e}")
    return False

def get_user_applications(user_id: str):
    log_path = "logs/applications.json"
    if not os.path.exists(log_path):
        return []

    applications = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                if record.get("user_id") == user_id:
                    applications.append(record)
            except json.JSONDecodeError:
                continue
    return applications
FAILED_LOG_PATH = "logs/failed_jobs.json"

def log_failed_application(user_id: str, job: dict, error: str):
    entry = {
        "user_id": user_id,
        "job_title": job.get("job_title"),
        "company": job.get("company"),
        "job_url": job.get("apply_url"),
        "error": error,
        "timestamp": datetime.utcnow().isoformat()
    }

    os.makedirs(os.path.dirname(FAILED_LOG_PATH), exist_ok=True)
    with open(FAILED_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")