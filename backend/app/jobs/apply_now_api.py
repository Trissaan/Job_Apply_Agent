from fastapi import APIRouter, Depends, HTTPException
from app.auth.deps import decode_token
from app.db.mongo import users_collection
from app.jobs.scrapers.seek import scrape_seek_jobs
from app.resume.logic.gpt_utils import tailor_resume_with_claude, generate_cover_letter
from app.resume.logic.export_utils import generate_pdf_from_text
from bots.utils.job_logger import log_application, has_already_applied, log_failed_application
from bots.utils.claude_client import extract_tags_from_jd
from bots.seek_apply import apply_to_seek_job
from playwright.async_api import async_playwright
import os
import tempfile
import traceback
import asyncio

router = APIRouter()

async def get_seek_jobs(user_id, job_title, location):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 800}
        )

        page = await context.new_page()
        jobs = await scrape_seek_jobs(page, user_id, job_title, location)
        await browser.close()
        return jobs


@router.post("/apply-now")
async def apply_now(user_id: str = Depends(decode_token), dry_run: bool = True):
    try:
        # 🔍 Fetch user preferences
        user = users_collection.find_one({"user_id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User preferences not found")

        job_title = user.get("job_title")
        location = user.get("location")
        full_name = user.get("full_name", "Your Name")
        email = user.get("email", "you@example.com")

        if not job_title or not location:
            raise HTTPException(status_code=400, detail="Incomplete preferences")

        # 🧠 Load base resume
        resume_txt_path = f"temp/{user_id}_base_resume.txt"
        if not os.path.exists(resume_txt_path):
            raise HTTPException(status_code=400, detail="Base resume not found")

        with open(resume_txt_path, "r", encoding="utf-8") as f:
            base_resume = f.read()

        # 🔍 Scrape matching jobs from Seek
        jobs = asyncio.run(get_seek_jobs(user_id, job_title, location))
        if not jobs:
            return {"message": "No jobs found"}

        applied_jobs = []

        for job in jobs:
            try:
                if has_already_applied(user_id=user_id, job_url=job["apply_url"]):
                    print(f"[{user_id}] Skipping already-applied job: {job['job_title']} at {job['company']}")
                    continue

                print(f"💡 Processing: {job['job_title']}")
                tailored = tailor_resume_with_claude(base_resume, job["job_description"], job["job_title"])
                cover_letter = generate_cover_letter(job["job_description"], tailored, job["job_title"])

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                    generate_pdf_from_text(tailored, temp_pdf.name)
                    resume_path = temp_pdf.name

                if not dry_run:
                    # 🤖 Apply via Playwright (Seek Easy Apply)
                    asyncio.run(apply_to_seek_job(
                        job_url=job["apply_url"],
                        resume_path=resume_path,
                        name=full_name,
                        email=email
                    ))
                else:
                    print(f"[DRY RUN] Would apply to: {job['job_title']} at {job['company']}")

                tags = extract_tags_from_jd(job["job_description"])
                log_application(
                    user_id=user_id,
                    job_title=job["job_title"],
                    company=job["company"],
                    job_description=job["job_description"],
                    cover_letter_text=cover_letter,
                    platform="seek",
                    job_url=job["apply_url"],
                    tags=tags
                )

                applied_jobs.append(job["job_title"])

            except Exception as job_error:
                print(f"❌ Failed to apply for {job['job_title']}: {job_error}")
                traceback.print_exc()
                log_failed_application(user_id=user_id, job=job, error=str(job_error))

        return {
            "status": "success",
            "message": f"Applied to {len(applied_jobs)} jobs",
            "titles": applied_jobs
        }

    except Exception as e:
        print(f"🔥 Apply-now internal error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Apply-now failed. See logs.")