from fastapi import APIRouter, File, UploadFile, Depends
from pydantic import BaseModel
from app.resume.logic.gpt_utils import generate_cover_letter, tailor_resume_with_claude
from app.resume.logic.export_utils import generate_pdf_from_text, save_resume_as_text, extract_text_from_pdf
from app.auth.deps import decode_token
import os

router = APIRouter()

# --- Upload Base Resume (PDF → Text) ---
@router.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):
    try:
        user_id = "trissaan_demo_001"  # hardcoded identity for demo

        os.makedirs("./temp", exist_ok=True)

        # Save uploaded PDF
        pdf_path = f"./temp/{user_id}_base_resume.pdf"
        with open(pdf_path, "wb") as f:
            f.write(file.file.read())

        # Extract text for tailoring
        resume_text = extract_text_from_pdf(pdf_path)

        # Save text version
        txt_path = f"./temp/{user_id}_base_resume.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(resume_text)

        return {
            "message": "Base resume uploaded successfully.",
            "resume_text_preview": resume_text[:300] + "..."
        }

    except Exception as e:
        return {"error": str(e)}

"""def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Depends(decode_token)
):
    try:
        os.makedirs("./temp", exist_ok=True)

        # Save uploaded PDF
        pdf_path = f"./temp/{user_id}_base_resume.pdf"
        with open(pdf_path, "wb") as f:
            f.write(file.file.read())

        # Extract text for tailoring
        resume_text = extract_text_from_pdf(pdf_path)

        # Save text version
        txt_path = f"./temp/{user_id}_base_resume.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(resume_text)

        return {
            "message": "Base resume uploaded successfully.",
            "resume_text_preview": resume_text[:300] + "..."
        }

    except Exception as e:
        return {"error": str(e)}
"""
# --- Request Model for Tailoring ---
class TailorRequest(BaseModel):
    resume_text: str
    jd_text: str
    job_title: str
    user_id: str  # TEMP for dev; will use JWT later

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
        # 1. Tailor resume using Claude
        tailored_text = tailor_resume_with_claude(
            base_resume=data.resume_text,
            jd_text=data.jd_text,
            job_title=data.job_title
        )

        out_dir = f"./temp/{data.user_id}"
        base_name = data.job_title.replace(' ', '_').lower()
        pdf_file = f"{base_name}_resume.pdf"
        txt_file = f"{base_name}_resume.txt"
        os.makedirs(out_dir, exist_ok=True)

        # 2. Save tailored resume as PDF and TXT
        pdf_path = generate_pdf_from_text(tailored_text, filename=pdf_file, out_dir=out_dir)
        txt_path = save_resume_as_text(tailored_text, filename=txt_file, out_dir=out_dir)

        return {
            "tailored_resume_text": tailored_text,
            "files": {
                "pdf": pdf_path,
                "txt": txt_path
            }
        }

    except Exception as e:
        return {"error": str(e)}

