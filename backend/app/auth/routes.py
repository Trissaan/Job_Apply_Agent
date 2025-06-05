from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .cognito import signup_user, confirm_user, login_user

router = APIRouter()

class AuthSchema(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(data: AuthSchema):
    try:
        response = signup_user(data.email, data.password)
        return {"message": "Signup successful, check your email for the confirmation code"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/confirm")
def confirm(data: AuthSchema, code: str):
    try:
        confirm_user(data.email, data.code)
        return {"message": "User confirmed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: AuthSchema):
    try:
        response = login_user(data.email, data.password)
        return {
            "access_token": response['AuthenticationResult']['AccessToken'],
            "refresh_token": response['AuthenticationResult']['RefreshToken']
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

