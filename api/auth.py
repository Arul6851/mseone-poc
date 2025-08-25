from fastapi import Request, HTTPException
from jose import jwt, JWTError
import requests

# Azure AD Settings (replace with your values)
TENANT_ID = "becdf9d3-b3e3-4fde-9aa5-e67ce0b5f957"
CLIENT_ID = "7125c2cc-bbc1-48b8-9e0d-e0d18946a0a6"
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/"
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

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