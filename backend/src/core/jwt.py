import secrets
from datetime import datetime, timedelta
from jose import jwt

def create_access_token(data: dict, secret: str, expires_minutes: int = 15):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload["type"] = "access"
    return jwt.encode(payload, secret, algorithm="HS256")

def create_refresh_token() -> str:
    # random opaque string i.p.v. JWT — hoeft geen payload te bevatten,
    # we zoeken 'm toch op in de database
    return secrets.token_urlsafe(64)