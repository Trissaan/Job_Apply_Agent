import asyncio
from seekers.seek_scraper import login_and_scrape_jobs

if __name__ == "__main__":
    jobs = asyncio.run(login_and_scrape_jobs())
    for job in jobs:
        print(f"\n🔎 {job['title']} at {job['company']}")
        print(f"🔗 {job['link']}")
        print(f"📝 {job['snippet']}")
