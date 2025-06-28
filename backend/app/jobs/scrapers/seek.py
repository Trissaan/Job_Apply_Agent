from playwright.async_api import async_playwright
import traceback
import os
import re

os.makedirs("temp", exist_ok=True)  # Ensure debug screenshot directory exists

async def scrape_seek_jobs(job_title: str, location: str) -> list[dict]:
    jobs = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            search_url = f"https://www.seek.com.au/{job_title.replace(' ', '-')}-jobs/in-{location.replace(' ', '-')}"
            print(f"Navigating to: {search_url}")
            await page.goto(search_url, timeout=20000, wait_until="domcontentloaded")

            # Dismiss cookie banner if present
            try:
                await page.locator("button:has-text('Accept All')").click(timeout=3000)
            except:
                pass

            await page.wait_for_selector('a[data-automation="jobTitle"]', timeout=20000)
            job_links = await page.locator('a[data-automation="jobTitle"]').all()
            print(f"Found {len(job_links)} job cards")

            job_hrefs = [
                await link.get_attribute("href")
                for link in job_links[:5]
                if await link.get_attribute("href")
            ]

            for idx, href in enumerate(job_hrefs):
                try:
                    job_url = f"https://www.seek.com.au{href}"
                    print(f"\nVisiting job {idx + 1}: {job_url}")
                    await page.goto(job_url, timeout=15000)

                    await page.wait_for_selector('h1[data-automation="job-detail-title"]', timeout=10000)

                    title = await page.locator('h1[data-automation="job-detail-title"]').text_content() or "N/A"
                    company = await page.locator('span[data-automation="advertiser-name"]').text_content() or "N/A"

                    # FULL job description
                    raw_html = await page.inner_html('div[data-automation="jobAdDetails"]')
                    description = re.sub("<[^>]+>", "", raw_html).strip()

                    # Get apply button or fallback
                    try:
                        apply_button_el = await page.wait_for_selector('[data-automation="applyButton"]', timeout=10000)
                        apply_button = await apply_button_el.get_attribute("href")
                        if apply_button and not apply_button.startswith("http"):
                            apply_button = job_url
                    except:
                        await page.screenshot(path=f"temp/debug_job_{idx+1}.png", full_page=True)
                        apply_button = job_url

                    jobs.append({
                        "job_title": title.strip(),
                        "company": company.strip(),
                        "job_description": description[:2000],
                        "apply_url": apply_button,
                        "source_url": job_url,
                    })

                    # Return to listing
                    await page.goto(search_url, timeout=15000)
                    await page.wait_for_selector('a[data-automation="jobTitle"]')

                except Exception as job_error:
                    print(f"Skipped job {idx + 1} due to error:")
                    traceback.print_exc()
                    continue

            await browser.close()

    except Exception as outer_error:
        print("Outer error during scrape_seek_jobs:")
        traceback.print_exc()

    return jobs
