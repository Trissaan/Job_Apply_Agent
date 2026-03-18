import json
import imaplib
import email
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils.resume_utils import tailor_resume_with_claude, generate_cover_letter_with_claude, export_tailored_resume_to_pdf
from utils.pdf_utils import extract_text_from_pdf
from utils.form_filler import generate_form_plan_with_claude
from datetime import datetime
import os

# CONFIG
CREDENTIALS_PATH = Path("credentials/seek_creds.json")
HTML_SNAPSHOT_PATH = "seek_code_page.html"

def get_seek_login_code(gmail_user, app_password, timeout=180):
    print("⏳ Holding for 5 seconds to wait for fresh email to arrive...")
    time.sleep(5)

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(gmail_user, app_password)
    mail.select("inbox")

    print("\n📩 Waiting for code email...")
    t0 = time.time()
    seen_ids = set()

    while time.time() - t0 < timeout:
        print("📡 Polling Gmail inbox for SEEK codes...")
        result, data = mail.search(None, 'SUBJECT "code for SEEK"')
        if data[0]:
            for msg_id in reversed(data[0].split()[-5:]):
                if msg_id in seen_ids:
                    continue
                seen_ids.add(msg_id)

                result, msg_data = mail.fetch(msg_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = msg.get("Subject", "No subject")
                print(f"📨 Checking: {subject}")

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                        elif part.get_content_type() == "text/html":
                            html = part.get_payload(decode=True).decode(errors="ignore")
                            soup = BeautifulSoup(html, "html.parser")
                            body = soup.get_text()
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                match = re.search(r"\b(\d{6})\b", body)
                if match:
                    code = match.group(1)
                    print(f"✅ Found login code: {code}")
                    return code

        time.sleep(5)

    raise TimeoutError("❌ Seek sign-in code not received in time.")


async def apply_to_job(page, tailored_resume_path: str, cover_letter_text: str, job_title: str, resume_text: str):
    try:
        print("🧠 Asking Claude how to apply on this page...")
        html = await page.content()
        try:
            form_plan = generate_form_plan_with_claude(html, job_title, resume_text)
        except Exception as e:
            print("⚠️ Failed to parse Claude's form response:", e)
            print("Claude raw output:\n", html[:1000])
            form_plan = {"inputs": {}, "checkboxes": []}

        click_text = form_plan.get("click_button_text", "Apply")
        try:
            print(f"🔘 Clicking button: {click_text}")
            await page.get_by_text(click_text).click(timeout=8000)
            await page.wait_for_timeout(2000)
        except:
            print(f"⚠️ Could not click button with text '{click_text}'")

        resume_selector = form_plan.get("resume_upload_selector", "")
        if resume_selector and resume_selector != "none":
            try:
                await page.set_input_files(resume_selector, tailored_resume_path)
                print("📎 Resume uploaded.")
            except:
                print(f"⚠️ Resume upload field '{resume_selector}' not found.")
        else:
            print("⚠️ No resume upload field provided.")

        cl_selector = form_plan.get("cover_letter_selector", "")
        if cl_selector and cl_selector != "none":
            try:
                await page.fill(cl_selector, cover_letter_text)
                print("✍️ Cover letter pasted.")
            except:
                print(f"⚠️ Cover letter field '{cl_selector}' not found.")
        else:
            print("⚠️ No cover letter field found.")

        for selector, value in form_plan.get("inputs", {}).items():
            try:
                await page.fill(selector, value)
                print(f"📝 Filled: {selector}")
            except:
                print(f"⚠️ Failed to fill: {selector}")

        for checkbox in form_plan.get("checkboxes", []):
            try:
                await page.check(checkbox)
                print(f"☑️ Checked: {checkbox}")
            except:
                print(f"⚠️ Failed to check: {checkbox}")

        submit_text = form_plan.get("submit_button_text", "Submit")
        try:
            await page.get_by_text(submit_text).click(timeout=8000)
            await page.wait_for_timeout(3000)
            print("✅ Application submitted.")
        except:
            print(f"⚠️ Could not click submit button with text '{submit_text}'")

        await page.screenshot(path="applied_confirmation.png", full_page=True)

    except Exception as e:
        print(f"❌ Error during dynamic application: {e}")


async def login_and_scrape_jobs(job_title="Data Analyst", location="Melbourne"):
    with open(CREDENTIALS_PATH) as f:
        creds = json.load(f)

    email_addr = creds["email"]
    gmail_app_password = creds["gmail_app_password"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("🌐 Navigating to SEEK...")
        await page.goto("https://www.seek.com.au/", timeout=60000)
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(2000)

        print("🔒 Clicking sign-in...")
        signin_links = await page.locator("a[href*='/oauth/login']").all()
        for link in signin_links:
            try:
                await link.click(force=True)
                break
            except:
                continue

        await page.wait_for_selector("input#emailAddress")
        await page.fill("input#emailAddress", email_addr)
        await page.click("button:has-text('Email me a sign in code')")

        print("⏳ Waiting for code input field...")
        try:
            await page.wait_for_selector("input[aria-label='verification input']", timeout=30000)
            print("✅ Code input field is ready.")
        except:
            html = await page.content()
            with open("seek_debug_failed_code_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            raise TimeoutError("🛑 Failed to detect code input field.")

        code = get_seek_login_code(email_addr, gmail_app_password)
        print(f"📨 Using login code: {code}")
        await page.fill("input[aria-label='verification input']", code)

        try:
            submit_btn = page.locator("button:has-text('Sign in')")
            await submit_btn.wait_for(state="attached", timeout=10000)
            await submit_btn.wait_for(state="visible")
            await submit_btn.wait_for(state="enabled")
            await submit_btn.click()
        except:
            print("⚠️ Button already gone — likely auto-signed in.")

        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(2000)

        search_url = f"https://www.seek.com.au/{job_title.replace(' ', '-')}-jobs/in-{location.replace(' ', '-')}"
        await page.goto(search_url)
        await page.wait_for_selector("article[data-automation='normalJob']", timeout=15000)

        job_cards = await page.locator("article[data-automation='normalJob']").all()
        print(f"🧾 Found {len(job_cards)} job cards.")

        jobs_data = []
        for job in job_cards[:5]:
            try:
                job_title_el = job.locator("a[data-automation='jobTitle']")
                title = await job_title_el.inner_text(timeout=5000)
                link = await job_title_el.get_attribute("href", timeout=5000)
                jobs_data.append((title, link))
            except:
                continue

        for i, (title, link) in enumerate(jobs_data):
            try:
                print(f"\n🔍 Processing job {i+1}/{len(jobs_data)}...")

                full_link = "https://www.seek.com.au" + link
                await page.goto(full_link)
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(2000)

                try:
                    job_description_html = await page.inner_html("main", timeout=5000)
                except:
                    print("⚠️ <main> not found, falling back to <body>")
                    job_description_html = await page.inner_html("body", timeout=5000)

                soup = BeautifulSoup(job_description_html, "html.parser")
                job_description = soup.get_text(separator="\n").strip()

                base_resume_text = extract_text_from_pdf(r"D:\JobApply\job_agent\Trissaan_Resume.pdf")
                tailored_resume = tailor_resume_with_claude(base_resume_text, job_description)
                cover_letter = generate_cover_letter_with_claude(base_resume_text, job_description, "Unknown Company")

                formatted_resume_path = "Trissaan_Tailored_Resume_Formatted.pdf"
                export_tailored_resume_to_pdf(tailored_resume, formatted_resume_path)

                await apply_to_job(
                    page,
                    tailored_resume_path=formatted_resume_path,
                    cover_letter_text=cover_letter,
                    job_title=title,
                    resume_text=base_resume_text
                )

                log_entry = {
                    "title": title,
                    "company": "Unknown Company",
                    "url": full_link,
                    "applied_at": datetime.now().isoformat(),
                    "cover_letter": cover_letter
                }

                log_path = "applied_jobs.json"
                if os.path.exists(log_path):
                    with open(log_path, "r") as f:
                        log_data = json.load(f)
                else:
                    log_data = []

                log_data.append(log_entry)
                with open(log_path, "w") as f:
                    json.dump(log_data, f, indent=2)

                print(f"✅ Applied to: {title} at Unknown Company")

            except Exception as e:
                print(f"⚠️ Failed to process job {i+1}: {e}")

        await browser.close()
        return []