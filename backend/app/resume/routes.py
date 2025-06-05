from fastapi import APIRouter, File, UploadFile, Form
from app.storage.upload import upload_resume_to_s3

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
