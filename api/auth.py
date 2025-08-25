import os
from fastapi import Request, HTTPException
from jose import jwt, JWTError
import requests

# Azure AD Settings (replace with your values)
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
ISSUER = os.getenv("ISSUER")
JWKS_URL = os.getenv("JWKS_URL")

ALLOWED_AUDIENCES = f"api://{CLIENT_ID}"
ALLOWED_ISSUERS = [
    f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
    f"https://sts.windows.net/{TENANT_ID}/"
]

signing_keys = requests.get(JWKS_URL).json()["keys"]

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            signing_keys,
            algorithms=["RS256"],
            audience=ALLOWED_AUDIENCES,
            issuer=ALLOWED_ISSUERS
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")