from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app.db.mongo import users_collection

router = APIRouter()

class Preferences(BaseModel):
    job_title: str
    jd_text: Optional[str] = ""
    location: str
    industry: Optional[str] = None
    experience_level: Optional[str] = None

@router.post("/save-preferences")
def save_preferences(prefs: Preferences):
    user_id = "trissaan_demo_001"  # Hardcoded for local testing
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {**prefs.dict(), "user_id": user_id}},
        upsert=True
    )
    return {"message": "Preferences saved"}

@router.get("/preferences")
def get_preferences():
    user_id = "trissaan_demo_001"
    prefs = users_collection.find_one({"user_id": user_id}, {"_id": 0})
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return prefs

@router.post("/user/auto-apply")
def toggle_auto_apply(enabled: bool = Form(...)):
    user_id = "trissaan_demo_001"
    try:
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"auto_apply": enabled}}
        )
        return {"success": True, "new_value": enabled}
    except Exception as e:
        return {"error": str(e)}

def get_user_preferences():
    # Helper for background scraping — gets all saved user prefs
    return list(users_collection.find({}, {"_id": 0}))
