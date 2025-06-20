from app.jobs.scrapers.seek import scrape_seek_jobs
from bots.apply_engine import apply_to_job, detect_platform
from app.resume.logic.gpt_utils import tailor_resume_with_claude, generate_cover_letter
from bots.utils.job_logger import log_application
from app.resume.logic.export_utils import generate_pdf_from_text
from app.db.mongo import users_collection
from app.storage.upload import upload_resume_to_s3
from app.resume.logic.export_utils import extract_text_from_pdf

import os
from datetime import datetime


def run_for_user(user_id: str, dry_run: bool = False):
    # Step 1: Load user info and preferences
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        print(f"User not found: {user_id}")
        return

    user_info = {
        "first_name": user.get("first_name", "Unknown"),
        "last_name": user.get("last_name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", "")
    }

    job_title = user.get("job_title", "data analyst")
    location = user.get("location", "melbourne")
    resume_pdf_path = user.get("resume_path", "")  # assume stored after upload

    if not resume_pdf_path or not os.path.exists(resume_pdf_path):
        print(f"Resume file not found for user: {user_id}")
        return

    base_resume = extract_text_from_pdf(resume_pdf_path)
    if not base_resume:
        print(" Failed to extract resume text.")
        return

    # Step 2: Scrape jobs from Seek
    jobs = scrape_seek_jobs(job_title, location)
    if not jobs:
        print("No jobs found.")
        return

    out_dir = f"temp/{user_id}"
    os.makedirs(out_dir, exist_ok=True)

    # Step 3: Apply to each job
    for idx, job in enumerate(jobs):
        try:
            print(f"\n Applying to: {job['job_title']} at {job['company']}")

            # Tailor resume and generate cover letter
            tailored_resume = tailor_resume_with_claude(base_resume, job["job_description"], job["job_title"])
            cover_letter = generate_cover_letter(job["job_description"], tailored_resume, job["job_title"])

            # Save tailored resume as PDF
            resume_path = os.path.join(out_dir, f"resume_{idx}.pdf")
            generate_pdf_from_text(tailored_resume, filename=f"resume_{idx}.pdf", out_dir=out_dir)

            # Save cover letter as text (for logs)
            cover_letter_path = os.path.join(out_dir, f"cover_letter_{idx}.txt")
            with open(cover_letter_path, "w", encoding="utf-8") as f:
                f.write(cover_letter)

            # Detect platform and apply
            platform = detect_platform(job["apply_url"])

            if dry_run:
                print(f"[DRY RUN] Would apply on {platform.upper()} using resume: {resume_path}")
            else:
                apply_to_job(job["apply_url"], resume_path, user_info)

            # Log the application
            log_application(
                job_title=job["job_title"],
                company=job["company"],
                job_description=job["job_description"],
                cover_letter_text=cover_letter,
                platform=platform,
                job_url=job["apply_url"],
                tags=[]  # You can plug in tag extraction here if needed
            )

        except Exception as e:
            print(f"Failed to apply to {job['job_title']} at {job['company']}: {e}")
            continue


# ✅ For dev testing
if __name__ == "__main__":
    run_for_user(user_id="test_user_001", dry_run=True)  # Change to False to enable real applying
