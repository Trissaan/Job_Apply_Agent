from seek_scraper import scrape_seek_jobs

if __name__ == "__main__":
    jobs = scrape_seek_jobs("data analyst", "Melbourne VIC")

    for job in jobs:
        print("\n" + "="*60)
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Description Snippet: {job['description'][:200]}...")
        print(f"Apply Link: {job['apply_link']}")
