from fastapi import APIRouter
from pydantic import BaseModel
from app.db.mongo import users_collection

router = APIRouter()

class Preferences(BaseModel):
    user_id: str
    job_title: str
    location: str
    industry: str
    experience_level: str

@router.post("/save-preferences")
def save_preferences(prefs: Preferences):
    users_collection.update_one(
        {"user_id": prefs.user_id},
        {"$set": prefs.dict()},
        upsert=True
    )
    return {"message": "Preferences saved"}
