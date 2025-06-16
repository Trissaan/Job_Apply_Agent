from seek_scraper import scrape_seek_jobs
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing job_title or location arguments"}))
        sys.exit(1)

    job_title = sys.argv[1]
    location = sys.argv[2]

    try:
        jobs = scrape_seek_jobs(job_title, location)
        print(json.dumps(jobs, ensure_ascii=False, indent=2))  # ✅ formatted + non-escaped
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
