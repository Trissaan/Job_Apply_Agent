from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["job_apply_ai"]
users_collection = db["users"]

# --- Create a new user ---
def create_user(user_id: str, email: str):
    users_collection.insert_one({
        "_id": user_id,
        "email": email,
        "preferences": {
            "job_title": "",
            "location": ""
        },
        "auto_apply": True  # Default is enabled
    })

# --- Get all users ---
def get_all_users():
    return list(users_collection.find())

# --- Toggle auto_apply status ---
def set_auto_apply(user_id: str, enabled: bool):
    result = users_collection.update_one(
        {"_id": user_id},
        {"$set": {"auto_apply": enabled}}
    )
    return result.modified_count > 0

# --- Optional: Get single user by ID ---
def get_user(user_id: str):
    return users_collection.find_one({"_id": user_id})
