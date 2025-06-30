from app.utils.crypto import decrypt
from app.db.mongo import get_mongo_db

async def get_decrypted_credentials(user_id: str, platform: str):
    db = await get_mongo_db()
    record = await db["platform_credentials"].find_one({"user_id": user_id, "platform": platform})
    if not record:
        raise Exception(f"No credentials found for user {user_id} on platform {platform}")
    return {
        "email": decrypt(record["email_encrypted"]),
        "password": decrypt(record["password_encrypted"])
    }
