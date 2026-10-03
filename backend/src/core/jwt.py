import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt


def create_access_token(
    data: dict,
    secret: str,
    expires_minutes: int = 15,
    algorithm: str = "HS256",
):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["type"] = "access"
    return jwt.encode(payload, secret, algorithm=algorithm)


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)
