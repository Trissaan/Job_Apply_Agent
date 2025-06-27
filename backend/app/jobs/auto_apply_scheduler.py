from apscheduler.schedulers.background import BackgroundScheduler
from app.user.preferences import get_user_preferences
from app.jobs.scrapers.seek import scrape_seek_jobs
from app.resume.logic.gpt_utils import tailor_resume_with_claude, generate_cover_letter
from app.resume.logic.export_utils import generate_pdf_from_text
from bots.utils.job_logger import log_application
from app.storage.upload import upload_resume_to_s3
from bots.apply_engine import apply_to_job, detect_platform
import os
import tempfile
import traceback
import asyncio

scheduler = BackgroundScheduler()

def auto_apply_job_agent():
    print(r"[Scheduler] Running auto-apply job...")

    try:
        all_users = get_user_preferences()
        print(f"Found {len(all_users)} users with preferences")

        for user in all_users:
            if not user.get("auto_apply", True):  # Skip if explicitly disabled
                print(f"[Skip] Auto-apply disabled for user: {user.get('user_id')}")
                continue

            user_id = user.get("user_id")
            job_title = user.get("job_title")
            location = user.get("location")

            try:
                jobs = asyncio.run(scrape_seek_jobs(job_title, location))
                print(f"Scraped {len(jobs)} jobs for {user_id} ({job_title})")

                for idx, job in enumerate(jobs):
                    try:
                        print(f"Applying to {job['job_title']} at {job['company']}")

                        # Load resume
                        resume_txt_path = f"temp/{user_id}_base_resume.txt"
                        if not os.path.exists(resume_txt_path):
                            print(f"No resume found for {user_id}")
                            continue

                        with open(resume_txt_path, "r", encoding="utf-8") as f:
                            base_resume = f.read()

                        tailored = tailor_resume_with_claude(base_resume, job["job_description"], job["job_title"])
                        cover_letter = generate_cover_letter(job["job_description"], tailored, job["job_title"])

                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                            generate_pdf_from_text(tailored, temp_pdf.name)
                            resume_path = temp_pdf.name

                        apply_to_job(job["apply_url"], resume_path, user)

                        log_application(
                            job_title=job["job_title"],
                            company=job["company"],
                            job_description=job["job_description"],
                            cover_letter_text=cover_letter,
                            platform=detect_platform(job["apply_url"]),
                            job_url=job["apply_url"],
                            tags=[]
                        )

                    except Exception as job_err:
                        print(f"Failed on job {idx}: {job_err}")
                        traceback.print_exc()

            except Exception as user_err:
                print(f"Failed user {user_id}: {user_err}")
                traceback.print_exc()

    except Exception as e:
        print("Scheduler failed:", e)

# Schedule every 10 mins (adjust as needed)
scheduler.add_job(auto_apply_job_agent, 'interval', minutes=10)
scheduler.start()

print("Scheduler started (running every 10 mins)")
