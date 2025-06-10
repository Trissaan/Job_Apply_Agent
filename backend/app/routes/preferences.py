from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.db.mongo import users_collection

router = APIRouter()

class Preferences(BaseModel):
    user_id: str
    job_title: str
    jd_text: str
    location: str
    industry: Optional[str] = None
    experience_level: Optional[str] = None

@router.post("/save-preferences")
def save_preferences(prefs: Preferences):
    users_collection.update_one(
        {"user_id": prefs.user_id},
        {"$set": prefs.dict()},
        upsert=True
    )
    return {"message": "Preferences saved"}
