from datetime import datetime, timezone
from typing import Optional

from backend.src.domain.entities.refresh_token import RefreshToken
from backend.src.adapters.database.models.refresh_token import RefreshToken as ORMRefreshToken


def _ensure_utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _to_naive_utc(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt


def to_domain(row: ORMRefreshToken) -> RefreshToken:
    return RefreshToken(
        id=row.id,
        user_id=row.user_id,
        token_hash=row.token_hash,
        expires_at=_ensure_utc(row.expires_at),
        revoked=row.revoked,
        created_at=_ensure_utc(row.created_at),
    )


def to_orm(token: RefreshToken, existing: Optional[ORMRefreshToken] = None) -> ORMRefreshToken:
    row = existing or ORMRefreshToken()
    row.user_id = token.user_id
    row.token_hash = token.token_hash
    row.expires_at = _to_naive_utc(token.expires_at)
    row.revoked = token.revoked
    row.created_at = _to_naive_utc(token.created_at)
    return row
