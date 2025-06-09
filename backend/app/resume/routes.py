from fastapi import APIRouter, File, UploadFile, Form
from app.storage.upload import upload_resume_to_s3
from pydantic import BaseModel
from app.resume.gpt_utils import generate_cover_letter

router = APIRouter()

@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    try:
        url = upload_resume_to_s3(file.file, file.filename, user_id)
        return {"resume_url": url}
    except Exception as e:
        return {"error": str(e)}
    
class TailorRequest(BaseModel):
    resume_text: str
    jd_text: str
    job_title: str

@router.post("/generate-cover-letter")
def generate_cover_letter_api(data: TailorRequest):
    try:
        result = generate_cover_letter(data.jd_text, data.resume_text, data.job_title)
        return {"cover_letter": result}
    except Exception as e:
        return {"error": str(e)}