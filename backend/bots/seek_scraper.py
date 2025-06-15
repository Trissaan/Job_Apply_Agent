from playwright.sync_api import sync_playwright
import time
import traceback


def scrape_seek_jobs(job_title: str, location: str) -> list[dict]:
    jobs = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path="C:/Users/triss/AppData/Local/ms-playwright/chromium-1169/chrome-win/chrome.exe",
                headless=False
            )
            page = browser.new_page()

            search_url = f"https://www.seek.com.au/{job_title.replace(' ', '-')}-jobs/in-{location.replace(' ', '-')}"
            print(f" Navigating to: {search_url}")
            page.goto(search_url, timeout=20000)
            page.wait_for_selector('a[data-automation="jobTitle"]', timeout=15000)

            job_links = page.locator('a[data-automation="jobTitle"]').all()
            print(f" Found {len(job_links)} job cards")

            job_hrefs = [link.get_attribute("href") for link in job_links[:5] if link.get_attribute("href")]

            for idx, href in enumerate(job_hrefs):
                try:
                    job_url = f"https://www.seek.com.au{href}"
                    print(f"\n Visiting job {idx + 1}: {job_url}")
                    page.goto(job_url, timeout=15000)
                    page.wait_for_selector('h1[data-automation="job-detail-title"]', timeout=10000)

                    title = page.locator('h1[data-automation="job-detail-title"]').text_content() or "N/A"
                    company = page.locator('span[data-automation="advertiser-name"]').text_content() or "N/A"
                    jd = page.locator('div[data-automation="jobAdDetails"]').text_content() or "N/A"

                    try:
                        apply_button = page.locator('a[data-automation="applyButton"]').get_attribute('href')
                    except:
                        apply_button = None

                    if not apply_button:
                        apply_button = job_url

                    jobs.append({
                        "job_title": title.strip(),
                        "company": company.strip(),
                        "job_description": jd.strip()[:300],
                        "apply_url": apply_button,
                    })

                    # Reload original job search page
                    page.goto(search_url, timeout=20000)
                    page.wait_for_selector('a[data-automation="jobTitle"]', timeout=15000)
                except Exception as job_error:
                    print(f"Skipped job {idx + 1} due to error:")
                    traceback.print_exc()
                    continue

            browser.close()

    except Exception as outer_error:
        print("Outer error during scrape_seek_jobs:")
        traceback.print_exc()
        raise outer_error

    return jobs
