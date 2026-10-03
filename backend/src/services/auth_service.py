from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from backend.src.core.config import settings
from backend.src.core.jwt import create_access_token, create_refresh_token
from backend.src.core.security import hash_password, verify_password, hash_token
from backend.src.domain.auth_repositories import RefreshTokenRepository, UserRepository
from backend.src.domain.entities.refresh_token import RefreshToken
from backend.src.domain.entities.user import User


class EmailAlreadyRegistered(Exception): ...
class InvalidCredentials(Exception): ...
class InvalidRefreshToken(Exception): ...


@dataclass(frozen=True)
class AuthTokens:
    user: User
    access_token: str
    refresh_token: str


class AuthService:
    def __init__(self, users: UserRepository, tokens: RefreshTokenRepository):
        self._users = users
        self._tokens = tokens

    def register(
        self,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> User:
        if self._users.get_by_email(email):
            raise EmailAlreadyRegistered()
        return self._users.save(
            User(
                id=None,
                email=email,
                hashed_password=hash_password(password),
                first_name=first_name,
                last_name=last_name,
            )
        )

    def login(self, email: str, password: str) -> AuthTokens:
        user = self._users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentials()
        return self._issue(user)

    def refresh(self, raw_token: str) -> AuthTokens:
        record = self._tokens.get_by_hash(hash_token(raw_token))
        if not record or not record.is_valid():
            raise InvalidRefreshToken()
        user = self._users.get_by_id(record.user_id)
        if not user:
            raise InvalidRefreshToken()
        record.revoke()  # rotation: old token is single-use
        self._tokens.save(record)
        return self._issue(user)

    def logout(self, raw_token: Optional[str]) -> None:
        if not raw_token:
            return
        record = self._tokens.get_by_hash(hash_token(raw_token))
        if record:
            record.revoke()
            self._tokens.save(record)

    def _issue(self, user: User) -> AuthTokens:
        access = create_access_token(
            {"sub": str(user.id)},
            secret=settings.JWT_SECRET,
            expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            algorithm=settings.JWT_ALGORITHM,
        )
        raw = create_refresh_token()
        self._tokens.save(
            RefreshToken(
                id=None,
                user_id=user.id,
                token_hash=hash_token(raw),
                expires_at=datetime.now(timezone.utc)
                + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
        )
        return AuthTokens(user, access, raw)
