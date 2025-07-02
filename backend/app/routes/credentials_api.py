from fastapi import APIRouter, Depends, HTTPException
from app.auth.deps import decode_token as get_current_user_id
from app.db.mongo import get_mongo_db
from app.utils.crypto import encrypt
from pydantic import BaseModel

router = APIRouter()

class CredentialInput(BaseModel):
    platform: str  # e.g., "seek"
    email: str
    password: str

@router.post("/platform-credentials")
async def store_platform_credentials(
    data: CredentialInput,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_mongo_db)
):
    coll = db["platform_credentials"]

    encrypted_email = encrypt(data.email)
    encrypted_password = encrypt(data.password)

    existing = await coll.find_one({"user_id": user_id, "platform": data.platform})
    if existing:
        await coll.update_one(
            {"user_id": user_id, "platform": data.platform},
            {"$set": {"email_encrypted": encrypted_email, "password_encrypted": encrypted_password}}
        )
    else:
        await coll.insert_one({
            "user_id": user_id,
            "platform": data.platform,
            "email_encrypted": encrypted_email,
            "password_encrypted": encrypted_password
        })

    return {"message": "Credentials stored securely."}
