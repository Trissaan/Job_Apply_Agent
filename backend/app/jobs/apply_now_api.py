from fastapi import APIRouter, Depends, HTTPException
from app.auth.deps import decode_token
from app.db.mongo import users_collection
from app.jobs.scrapers.seek import scrape_seek_jobs
from app.resume.logic.gpt_utils import tailor_resume_with_claude, generate_cover_letter
from app.resume.logic.export_utils import generate_pdf_from_text
from bots.utils.job_logger import log_application
from bots.apply_engine import apply_to_job, detect_platform
import os
import tempfile
import traceback
import asyncio

router = APIRouter()

@router.post("/apply-now")
def apply_now(user_id: str = Depends(decode_token)):
    try:
        # 🔍 Fetch user preferences
        user = users_collection.find_one({"user_id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User preferences not found")

        job_title = user.get("job_title")
        location = user.get("location")

        if not job_title or not location:
            raise HTTPException(status_code=400, detail="Incomplete preferences")

        # 🧠 Load base resume
        resume_txt_path = f"temp/{user_id}_base_resume.txt"
        if not os.path.exists(resume_txt_path):
            raise HTTPException(status_code=400, detail="Base resume not found")

        with open(resume_txt_path, "r", encoding="utf-8") as f:
            base_resume = f.read()

        # 🔍 Scrape matching jobs
        jobs = asyncio.run(scrape_seek_jobs(job_title, location))
        if not jobs:
            return {"message": "No jobs found"}

        applied_jobs = []

        for job in jobs:
            try:
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

                applied_jobs.append(job["job_title"])

            except Exception as job_error:
                print(f"❌ Failed to apply: {job_error}")
                traceback.print_exc()

        return {
            "status": "success",
            "message": f"Applied to {len(applied_jobs)} jobs",
            "titles": applied_jobs
        }

    except Exception as e:
        print(f"🔥 Apply-now internal error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Apply-now failed. See logs.")
