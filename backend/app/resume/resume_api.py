from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel
from app.storage.upload import upload_resume_to_s3
from app.resume.logic.gpt_utils import generate_cover_letter, tailor_resume_with_claude
from app.resume.logic.export_utils import generate_pdf_from_text, save_resume_as_text
import os

router = APIRouter()

# --- Resume Upload Endpoint ---
@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Form(...)  # TEMP for dev, replace later with JWT
):
    try:
        url = upload_resume_to_s3(file.file, file.filename, user_id)
        return {"resume_url": url}
    except Exception as e:
        return {"error": str(e)}

# --- Request Model for Tailoring ---
class TailorRequest(BaseModel):
    resume_text: str
    jd_text: str
    job_title: str
    user_id: str  # TEMP for dev; to be extracted from JWT later

# --- Cover Letter Generation Endpoint ---
@router.post("/generate-cover-letter")
def generate_cover_letter_api(data: TailorRequest):
    try:
        result = generate_cover_letter(data.jd_text, data.resume_text, data.job_title)
        return {"cover_letter": result}
    except Exception as e:
        return {"error": str(e)}

# --- Tailored Resume Generation Endpoint ---
@router.post("/generate-tailored-resume")
def generate_tailored_resume_api(data: TailorRequest):
    try:
        # 1. Generate the tailored resume text using Claude
        tailored_text = tailor_resume_with_claude(
            base_resume=data.resume_text,
            jd_text=data.jd_text,
            job_title=data.job_title
        )

        # TODO: 🔐 Replace 'user_id' with Cognito JWT user ID in production
        out_dir = f"./temp/{data.user_id}"
        base_name = data.job_title.replace(' ', '_').lower()
        pdf_file = f"{base_name}_resume.pdf"
        txt_file = f"{base_name}_resume.txt"

        # 2. Save as PDF and TXT
        pdf_path = generate_pdf_from_text(tailored_text, filename=pdf_file, out_dir=out_dir)
        txt_path = save_resume_as_text(tailored_text, filename=txt_file, out_dir=out_dir)

        # 3. Return structured response
        return {
            "tailored_resume_text": tailored_text,
            "files": {
                "pdf": pdf_path,
                "txt": txt_path
            }
        }

    except Exception as e:
        return {"error": str(e)}
