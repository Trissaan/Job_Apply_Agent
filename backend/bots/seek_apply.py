from playwright.async_api import async_playwright
import traceback
import os

async def apply_to_seek_job(job_url: str, resume_path: str, name: str, email: str):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(job_url, timeout=20000)
            print(f"Visiting job: {job_url}")

            # 1. Click the Apply button
            try:
                apply_button = await page.wait_for_selector('[data-automation="applyButton"]', timeout=8000)
                await apply_button.click()
                await page.wait_for_timeout(3000)
            except Exception as e:
                print("❌ Could not find Apply button")
                raise e

            # 2. Upload resume (if available)
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(resume_path)
                print(f"✅ Uploaded resume from: {resume_path}")
            else:
                print("⚠️ Resume upload input not found.")

            # 3. Fill name/email if asked (some Seek forms do, some don’t)
            try:
                name_input = await page.query_selector('input[name="name"]')
                if name_input:
                    await name_input.fill(name)

                email_input = await page.query_selector('input[name="email"]')
                if email_input:
                    await email_input.fill(email)
            except:
                print("⚠️ Optional fields not present.")

            # 4. Submit
            try:
                submit_button = await page.query_selector('button[type="submit"]')
                if submit_button:
                    await submit_button.click()
                    print("✅ Application submitted")
            except:
                print("⚠️ Submit button not found")

            await page.wait_for_timeout(3000)
            await browser.close()

    except Exception:
        print("❌ Failed to apply to Seek job")
        traceback.print_exc()
