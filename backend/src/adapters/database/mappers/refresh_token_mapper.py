from typing import Optional

from backend.src.domain.entities.refresh_token import RefreshToken as DomainRefreshToken
from backend.src.adapters.database.models.refresh_token import RefreshToken as ORMRefreshToken


def to_domain(orm_token: ORMRefreshToken) -> DomainRefreshToken:
    return DomainRefreshToken(
        id=orm_token.id,
        user_id=orm_token.user_id,
        token_hash=orm_token.token_hash,
        expires_at=orm_token.expires_at,
        revoked=orm_token.revoked,
        created_at=orm_token.created_at,
    )


def to_orm(token: DomainRefreshToken, existing: Optional[ORMRefreshToken] = None) -> ORMRefreshToken:
    orm_token = existing or ORMRefreshToken()
    orm_token.id = token.id
    orm_token.user_id = token.user_id
    orm_token.token_hash = token.token_hash
    orm_token.expires_at = token.expires_at
    orm_token.revoked = token.revoked
    orm_token.created_at = token.created_at
    return orm_token
