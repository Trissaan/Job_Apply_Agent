from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["job_apply_ai"]
users_collection = db["users"]
