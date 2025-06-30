from fastapi import APIRouter, Depends
from app.auth.deps import decode_token
from fastapi.responses import FileResponse
from fastapi import Query
from bots.utils.job_logger import get_user_applications
import json
import os

router = APIRouter()

@router.get("/dashboard/history")
def get_application_history(user_id: str = Depends(decode_token)):
    try:
        log_path = "./logs/applications.json"
        if not os.path.exists(log_path):
            return {"jobs": []}

        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Filter by user_id
        user_jobs = [entry for entry in data if entry.get("user_id") == user_id]

        return {"jobs": user_jobs}

    except Exception as e:
        return {"error": str(e)}

@router.get("/download")
def download_file(path: str = Query(..., description="Full path to file")):
    try:
        return FileResponse(path, filename=path.split("/")[-1], media_type="application/octet-stream")
    except Exception as e:
        return {"error": str(e)}
@router.get("/application-logs")
def get_application_logs(user_id: str = Depends(decode_token)):
    logs = get_user_applications(user_id)
    return {"user_id": user_id, "applications": logs}

