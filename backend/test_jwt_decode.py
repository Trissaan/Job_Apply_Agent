import requests
from jose import jwt

# --- ENV values from your .env ---
COGNITO_USER_POOL_ID = "ap-southeast-2_vSonBphuP"
AWS_REGION = "ap-southeast-2"
COGNITO_CLIENT_ID = "5t0v819upem1uner0ur5r96m4k"
COGNITO_ISSUER = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"

# 👇 Paste your Cognito JWT token here (either IdToken or AccessToken)
token = "eyJraWQiOiJQYjJUMmp0SDdqSk5pRTdcL09HMnZ2WWhqR3U5UVFxd05wb25kRzJIRUpaND0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJjOTFlZTQxOC03MGMxLTcwZTMtMGQwOC1mNTBkYWNlNTY4ODYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGhlYXN0LTIuYW1hem9uYXdzLmNvbVwvYXAtc291dGhlYXN0LTJfdlNvbkJwaHVQIiwiY2xpZW50X2lkIjoiNXQwdjgxOXVwZW0xdW5lcjB1cjVyOTZtNGsiLCJvcmlnaW5fanRpIjoiYmMxYWFmZmMtMWIyMS00NGJmLWE0OGItZGJjODI2NTQ2YzdiIiwiZXZlbnRfaWQiOiIyNjZjMDQ2MS02OTI2LTQ1ZTAtODQ0Zi1jYjMyN2I4MWFjNGIiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNzUxMDcyMDE0LCJleHAiOjE3NTEwNzU2MTQsImlhdCI6MTc1MTA3MjAxNCwianRpIjoiNzcxZDZiYzMtNGZmNC00Mjg3LWIwYzktMzJiZTRjNzhlZWU5IiwidXNlcm5hbWUiOiJjOTFlZTQxOC03MGMxLTcwZTMtMGQwOC1mNTBkYWNlNTY4ODYifQ.Ecc87JYFoaKxAI7r6eCQ0W-5vfswFkU_scblx7dORIdkfuMEMNb47ei6ePPRCXbcro_IC6qxp3RuxhJXWZKX9AJhj65_m1l-ymjyf0B8RhWFnn7hvvql6vPa7-i6S37eTl73-eDvK5KMUj_8T-Qenr3FIH2GRmME9C2D_LIHYlqznM2qw5ZCXZylzWdK1S-dvGvBbLTYrR0RBYCrvjx6QDs5Dp20PxvkuivfRKXYxMvJGJoSkq2AAW_YPU0WI0sLo_UR2CrpNY5ioHRJVEjeSIi5Y6OXR5hFeQfM4IU93sJo3COJrUDc8HwHLgAs9Zc7MMXQc0deltThKznZ95EyYA"

# --- Decode and print ---
try:
    keys = requests.get(f"{COGNITO_ISSUER}/.well-known/jwks.json").json()["keys"]
    header = jwt.get_unverified_header(token)
    key = next(k for k in keys if k["kid"] == header["kid"])

    payload = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=COGNITO_CLIENT_ID,
        issuer=COGNITO_ISSUER
    )

    print("✅ Token payload:", payload)

except Exception as e:
    print("❌ Token validation failed:", str(e))
