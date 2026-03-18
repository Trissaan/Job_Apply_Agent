from playwright.async_api import async_playwright
import re
import traceback

async def scrape_seek_jobs(page, user_id: str, job_title: str, location: str) -> list[dict]:
    jobs = []

    try:
        search_url = f"https://www.seek.com.au/{job_title.replace(' ', '-')}-jobs/in-{location.replace(' ', '-')}"
        print(f"[{user_id}] Navigating to: {search_url}")
        await page.goto(search_url, timeout=20000, wait_until="domcontentloaded")

        # Add wait buffer and handle cookie banner
        await page.wait_for_timeout(3000)  # Wait 3 seconds for page to stabilize

        try:
            await page.locator("button:has-text('Accept All')").click(timeout=3000)
        except:
            pass

        try:
            await page.wait_for_selector('[data-automation*="jobTitle"]', timeout=20000)
        except Exception as e:
            print(f"[{user_id}] ❌ Selector not found: {e}")
            print(await page.content())  # Print full HTML for debug
            return []

        job_links = await page.locator('[data-automation*="jobTitle"]').all()
        print(f"[{user_id}] Found {len(job_links)} job cards")

        job_hrefs = [
            await link.get_attribute("href")
            for link in job_links[:5]  # limit to 5 jobs for now
            if await link.get_attribute("href")
        ]

        for idx, href in enumerate(job_hrefs):
            try:
                job_url = f"https://www.seek.com.au{href}"
                print(f"[{user_id}] Visiting job {idx + 1}: {job_url}")
                await page.goto(job_url, timeout=15000)
                await page.wait_for_selector('h1[data-automation="job-detail-title"]', timeout=10000)

                title = await page.locator('h1[data-automation="job-detail-title"]').text_content() or "N/A"
                company = await page.locator('span[data-automation="advertiser-name"]').text_content() or "N/A"

                raw_html = await page.inner_html('div[data-automation="jobAdDetails"]')
                description = re.sub("<[^>]+>", "", raw_html).strip()

                try:
                    apply_button_el = await page.wait_for_selector('[data-automation="applyButton"]', timeout=10000)
                    apply_button = await apply_button_el.get_attribute("href")
                    if apply_button and not apply_button.startswith("http"):
                        apply_button = job_url
                except:
                    apply_button = job_url

                jobs.append({
                    "job_title": title.strip(),
                    "company": company.strip(),
                    "job_description": description[:2000],
                    "apply_url": apply_button,
                    "source_url": job_url,
                })

                await page.goto(search_url, timeout=15000)
                await page.wait_for_selector('[data-automation*="jobTitle"]')

            except Exception as job_error:
                print(f"[{user_id}] ❌ Skipped job {idx + 1} due to error:")
                traceback.print_exc()
                continue

    except Exception as outer_error:
        print(f"[{user_id}] ❌ Outer error during scrape_seek_jobs:")
        traceback.print_exc()

    return jobs