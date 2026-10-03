from typing import Optional
from sqlmodel import Session, select

from backend.src.domain.entities.refresh_token import RefreshToken
from backend.src.adapters.database.models.refresh_token import RefreshToken as ORMRefreshToken
from backend.src.adapters.database.mappers.refresh_token_mapper import to_domain, to_orm


class SqlRefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        row = self.session.exec(
            select(ORMRefreshToken).where(ORMRefreshToken.token_hash == token_hash)
        ).first()
        return to_domain(row) if row else None

    def save(self, token: RefreshToken) -> RefreshToken:
        existing = self.session.get(ORMRefreshToken, token.id) if token.id else None
        row = to_orm(token, existing)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return to_domain(row)
