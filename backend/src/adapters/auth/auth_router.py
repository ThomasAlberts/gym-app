from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlmodel import Session, select
from pydantic import BaseModel

from backend.src.adapters.database.database import get_database
from backend.src.models.user import User
from backend.src.models.refresh_token import RefreshToken
from backend.src.core.security import hash_password, verify_password, hash_token
from backend.src.core.jwt import create_access_token, create_refresh_token
from backend.src.core.config import settings
from backend.src.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,       # True zodra je https gebruikt (productie!)
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,       # True in productie
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/auth",       # alleen meesturen naar /auth/* endpoints, niet nodig elders
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, session: Session = Depends(get_database)):
    existing = session.exec(select(User).where(User.email == request.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=request.email,
        hashed_password=hash_password(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(request: LoginRequest, response: Response, session: Session = Depends(get_database)):
    user = session.exec(select(User).where(User.email == request.email)).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": str(user.id)},
        secret=settings.JWT_SECRET,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    refresh_token = create_refresh_token()

    # Refresh token opslaan (gehashed) zodat we 'm kunnen intrekken
    record = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    session.add(record)
    session.commit()

    _set_auth_cookies(response, access_token, refresh_token)

    return {"user": {"id": user.id, "email": user.email, "role": user.role}}


@router.post("/refresh")
def refresh(request: Request, response: Response, session: Session = Depends(get_database)):
    raw_token = request.cookies.get("refresh_token")
    if not raw_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    token_hash = hash_token(raw_token)
    record = session.exec(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    ).first()

    if (
        not record
        or record.revoked
        or record.expires_at < datetime.utcnow()
    ):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = session.get(User, record.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Rotatie: oude refresh token intrekken, nieuwe uitgeven
    record.revoked = True
    new_refresh_token = create_refresh_token()
    new_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(new_refresh_token),
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    session.add(record)
    session.add(new_record)
    session.commit()

    new_access_token = create_access_token(
        {"sub": str(user.id)},
        secret=settings.JWT_SECRET,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    _set_auth_cookies(response, new_access_token, new_refresh_token)

    return {"detail": "Refreshed"}


@router.post("/logout")
def logout(request: Request, response: Response, session: Session = Depends(get_database)):
    raw_token = request.cookies.get("refresh_token")
    if raw_token:
        record = session.exec(
            select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw_token))
        ).first()
        if record:
            record.revoked = True
            session.add(record)
            session.commit()

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/auth")
    return {"detail": "Logged out"}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}