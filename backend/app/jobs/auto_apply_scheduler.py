from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.user.preferences import get_user_preferences
from app.services.credentials import get_decrypted_credentials
from app.resume.logic.gpt_utils import tailor_resume_with_claude, generate_cover_letter
from app.resume.logic.export_utils import generate_pdf_from_text
from bots.utils.job_logger import log_application, has_already_applied, log_failed_application
from bots.utils.upload_handler import upload_resume_to_s3
from bots.apply_engine import apply_to_job, detect_platform
from app.jobs.scrapers.seek import scrape_seek_jobs
from playwright.async_api import async_playwright
import os
import tempfile
import traceback

scheduler = AsyncIOScheduler()

async def login_to_seek(page, email, password):
    await page.goto("https://www.seek.com.au/login")
    await page.fill('input[type="email"]', email)
    await page.fill('input[type="password"]', password)
    await page.click('button[type="submit"]')
    await page.wait_for_load_state("networkidle")
    assert "seek.com.au" in page.url
    print("✅ Logged into Seek.")

async def auto_apply_job_agent():
    print(r"[Scheduler] Running auto-apply job...")

    try:
        all_users = get_user_preferences()
        print(f"Found {len(all_users)} users with preferences")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            for user in all_users:
                if not user.get("auto_apply", True):
                    print(f"[Skip] Auto-apply disabled for user: {user.get('user_id')}")
                    continue

                user_id = user.get("user_id")
                job_title = user.get("job_title")
                location = user.get("location")

                try:
                    creds = await get_decrypted_credentials(user_id, "seek")
                    await login_to_seek(page, creds["email"], creds["password"])

                    jobs = await scrape_seek_jobs(page, user_id=user_id, job_title=job_title, location=location)
                    print(f"[{user_id}] Scraped {len(jobs)} jobs")

                    for idx, job in enumerate(jobs):
                        try:
                            print(f"[{user_id}] Applying to {job['job_title']} at {job['company']}")

                            # 🛑 Check if already applied
                            if has_already_applied(user_id=user_id, job_url=job["apply_url"]):
                                print(f"[{user_id}] Skipping already-applied job: {job['job_title']}")
                                continue

                            # 📄 Load resume
                            resume_txt_path = f"temp/{user_id}_base_resume.txt"
                            if not os.path.exists(resume_txt_path):
                                print(f"[{user_id}] No resume found at {resume_txt_path}")
                                continue

                            with open(resume_txt_path, "r", encoding="utf-8") as f:
                                base_resume = f.read()

                            # ✍️ Tailor + cover letter
                            tailored = tailor_resume_with_claude(base_resume, job["job_description"], job["job_title"])
                            cover_letter = generate_cover_letter(job["job_description"], tailored, job["job_title"])

                            # 📄 Export PDF
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                                generate_pdf_from_text(tailored, temp_pdf.name)
                                resume_path = temp_pdf.name

                            # 🚀 Apply
                            apply_to_job(job["apply_url"], resume_path, user)

                            # ☁️ Upload (optional)
                            upload_resume_to_s3(resume_path, user_id=user_id)

                            # 🪵 Log success
                            log_application(
                                user_id=user_id,
                                job_title=job["job_title"],
                                company=job["company"],
                                job_description=job["job_description"],
                                cover_letter_text=cover_letter,
                                platform=detect_platform(job["apply_url"]),
                                job_url=job["apply_url"],
                                tags=[]
                            )

                        except Exception as job_err:
                            print(f"[{user_id}] ❌ Job {idx} failed: {job_err}")
                            traceback.print_exc()
                            log_failed_application(user_id=user_id, job=job, error=str(job_err))

                except Exception as user_err:
                    print(f"[{user_id}] ❌ User block failed: {user_err}")
                    traceback.print_exc()

            await browser.close()

    except Exception as e:
        print("❌ Scheduler crashed:", e)
        traceback.print_exc()

# Start async scheduler every 10 minutes
scheduler.add_job(auto_apply_job_agent, 'interval', minutes=10)
scheduler.start()

print("✅ Async Scheduler started (every 10 mins)")
