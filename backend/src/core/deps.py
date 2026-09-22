from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlmodel import Session

from backend.src.adapters.database.database import get_database
from backend.src.domain.user import User
from backend.src.core.config import settings
from backend.src.core.roles import Role


def get_current_user(
    request: Request,
    session: Session = Depends(get_database),
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_role(*allowed_roles: Role):
    return Depends(
        lambda user=Depends(get_current_user): (
            user if user.role in allowed_roles
            else HTTPException(status_code=403, detail="Forbidden")
        )
    )