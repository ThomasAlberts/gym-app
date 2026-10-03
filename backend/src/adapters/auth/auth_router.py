from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlmodel import Session

from backend.src.adapters.database.database import get_database
from backend.src.adapters.database.repositories.refresh_token_repository import SqlRefreshTokenRepository
from backend.src.adapters.database.repositories.user_repository import SqlUserRepository
from backend.src.core.config import settings
from backend.src.core.deps import get_current_user
from backend.src.domain.entities.user import User
from backend.src.services.auth_service import (
    AuthService,
    EmailAlreadyRegistered,
    InvalidCredentials,
    InvalidRefreshToken,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# Add COOKIE_SECURE: bool = False to your Settings; set it True in production (https).
COOKIE_SECURE: bool = getattr(settings, "COOKIE_SECURE", False)


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


def get_auth_service(session: Session = Depends(get_database)) -> AuthService:
    return AuthService(SqlUserRepository(session), SqlRefreshTokenRepository(session))


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/auth",  # only sent to /auth/* endpoints
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, svc: AuthService = Depends(get_auth_service)):
    try:
        user = svc.register(body.email, body.password, body.first_name, body.last_name)
    except EmailAlreadyRegistered:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(body: LoginRequest, response: Response, svc: AuthService = Depends(get_auth_service)):
    try:
        result = svc.login(body.email, body.password)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    _set_auth_cookies(response, result.access_token, result.refresh_token)
    u = result.user
    return {"user": {"id": u.id, "email": u.email, "role": u.role}}


@router.post("/refresh")
def refresh(request: Request, response: Response, svc: AuthService = Depends(get_auth_service)):
    raw = request.cookies.get("refresh_token")
    if not raw:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        result = svc.refresh(raw)
    except InvalidRefreshToken:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    _set_auth_cookies(response, result.access_token, result.refresh_token)
    return {"detail": "Refreshed"}


@router.post("/logout")
def logout(request: Request, response: Response, svc: AuthService = Depends(get_auth_service)):
    svc.logout(request.cookies.get("refresh_token"))
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/auth")
    return {"detail": "Logged out"}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}
