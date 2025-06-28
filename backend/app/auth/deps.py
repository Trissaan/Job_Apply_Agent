import requests
from jose import jwt
from fastapi import Depends, HTTPException, Header
from app.config import COGNITO_CLIENT_ID, AWS_REGION, COGNITO_USER_POOL_ID

COGNITO_ISSUER = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"

def get_cognito_public_keys():
    jwks_url = f"{COGNITO_ISSUER}/.well-known/jwks.json"
    try:
        resp = requests.get(jwks_url)
        resp.raise_for_status()
        jwks = resp.json()
        return jwks["keys"]
    except Exception as e:
        print("❌ Failed to fetch or parse Cognito JWKs:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch JWKs")

def decode_token(authorization: str = Header(..., alias="Authorization")) -> str:
    try:
        print("🔐 Raw Authorization:", authorization)

        # Handle Swagger sending "Bearer Bearer <token>" or just "<token>"
        parts = authorization.split()
        if len(parts) >= 2 and parts[0] == "Bearer":
            token = parts[-1]
        else:
            raise HTTPException(status_code=401, detail="Malformed Authorization header")

        print("✅ Cleaned token:", token[:30], "...")

        unverified_header = jwt.get_unverified_header(token)
        print("📌 JWT Header:", unverified_header)

        keys = get_cognito_public_keys()
        key = next(k for k in keys if k["kid"] == unverified_header["kid"])
        print("🔑 Matching key found")

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=COGNITO_CLIENT_ID,
            issuer=COGNITO_ISSUER,
        )
        print("🎯 Token valid. Payload:", payload)

        return payload["sub"]  # or "username" if that's how you ID users

    except Exception as e:
        print("❌ Token validation failed:", str(e))
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
