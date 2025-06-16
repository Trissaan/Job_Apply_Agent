from app.jobs.scrapers.seek import scrape_seek_jobs
from bots.apply_engine import apply_to_job
from app.resume.gpt_utils import tailor_resume_with_claude, generate_cover_letter
import os

job_title = "data analyst"
location = "melbourne"

# Load base resume from file
with open("temp/base_resume.txt", "r", encoding="utf-8") as f:
    base_resume = f.read()

user_info = {
    "first_name": "Trissaan",
    "last_name": "Shanmugasundaram",
    "email": "trissaan@gmail.com",
    "phone": "0434549364"
}

jobs = scrape_seek_jobs(job_title, location)

for idx, job in enumerate(jobs):
    print(f"\n📨 Applying to: {job['job_title']} at {job['company']}")

    # Tailor resume
    tailored_resume = tailor_resume_with_claude(
        base_resume, job["job_description"], job["job_title"]
    )

    # Generate cover letter
    cover_letter = generate_cover_letter(
        job["job_description"], tailored_resume, job["job_title"]
    )

    # Save tailored files
    out_dir = "temp/test_user_001"
    os.makedirs(out_dir, exist_ok=True)

    resume_path = os.path.join(out_dir, f"{job_title.replace(' ', '_')}_resume.txt")
    cover_letter_path = os.path.join(out_dir, f"{job_title.replace(' ', '_')}_cover_letter.txt")

    with open(resume_path, "w", encoding="utf-8") as f:
        f.write(tailored_resume)

    with open(cover_letter_path, "w", encoding="utf-8") as f:
        f.write(cover_letter)

    # Apply using the tailored files
    apply_to_job(job["apply_url"], resume_path, user_info)
