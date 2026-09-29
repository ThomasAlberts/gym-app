from typing import Optional
from sqlmodel import Session, select

from backend.src.domain.entities.refresh_token import RefreshToken
from backend.src.adapters.database.models.refresh_token import RefreshToken as ORMRefreshToken
from backend.src.adapters.database.mappers.refresh_token_mapper import to_domain, to_orm


class SqlRefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        orm_token = self.session.exec(
            select(ORMRefreshToken).where(ORMRefreshToken.token_hash == token_hash)
        ).first()
        return to_domain(orm_token) if orm_token else None

    def save(self, token: RefreshToken) -> RefreshToken:
        existing = self.session.get(ORMRefreshToken, token.id) if token.id else None
        orm_token = to_orm(token, existing)
        self.session.add(orm_token)
        self.session.commit()
        self.session.refresh(orm_token)
        return to_domain(orm_token)

    def revoke_all_for_user(self, user_id: int) -> None:
        orm_tokens = self.session.exec(
            select(ORMRefreshToken).where(ORMRefreshToken.user_id == user_id)
        ).all()
        for orm_token in orm_tokens:
            orm_token.revoked = True
            self.session.add(orm_token)
        self.session.commit()
