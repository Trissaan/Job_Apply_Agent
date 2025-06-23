import boto3
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from app.config import COGNITO_CLIENT_ID, AWS_REGION
import requests

COGNITO_ISSUER = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"

def get_cognito_public_keys():
    jwks_url = f"{COGNITO_ISSUER}/.well-known/jwks.json"
    return requests.get(jwks_url).json()["keys"]

def decode_token(token: str = Header(..., alias="Authorization")):
    try:
        token = token.replace("Bearer ", "")
        unverified_header = jwt.get_unverified_header(token)
        keys = get_cognito_public_keys()
        key = next(k for k in keys if k["kid"] == unverified_header["kid"])

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=COGNITO_CLIENT_ID,
            issuer=COGNITO_ISSUER,
        )

        return payload["sub"]  # This is the Cognito User ID

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
