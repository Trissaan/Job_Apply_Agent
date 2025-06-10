from playwright.sync_api import sync_playwright
import time

def scrape_seek_jobs(job_title, location):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to True later
        page = browser.new_page()

        # Format search URL
        search_url = f"https://www.seek.com.au/{job_title.replace(' ', '-')}-jobs/in-{location.replace(' ', '-')}"
        page.goto(search_url)
        time.sleep(3)

        job_links = page.locator('a[data-automation="jobTitle"]').all()

        for job in job_links[:5]:  # limit for testing
            job.click()
            time.sleep(2)
            page.wait_for_load_state("load")
            
            job_title = page.locator('h1[data-automation="job-detail-title"]').text_content()
            company = page.locator('span[data-automation="advertiser-name"]').text_content()
            jd = page.locator('div[data-automation="jobAdDetails"]').text_content()

            try:
                apply_button = page.locator('a[data-automation="applyButton"]').get_attribute('href')
            except:
                apply_button = "No Apply Button Found"

            jobs.append({
                "title": job_title,
                "company": company,
                "description": jd[:300],  # shortened
                "apply_link": apply_button
            })

            page.go_back()
            time.sleep(1)

        browser.close()
    
    return jobs
