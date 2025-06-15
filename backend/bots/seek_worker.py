from seek_scraper import scrape_seek_jobs
import sys
import json

if __name__ == "__main__":
    job_title = sys.argv[1]
    location = sys.argv[2]
    jobs = scrape_seek_jobs(job_title, location)
    print(json.dumps(jobs))
