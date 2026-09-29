from typing import Optional
from sqlmodel import Session, select

from backend.src.domain.entities.user import User
from backend.src.adapters.database.models.user import User as ORMUser
from backend.src.adapters.database.mappers.user_mapper import to_domain, to_orm


class SqlUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        orm_user = self.session.get(ORMUser, user_id)
        return to_domain(orm_user) if orm_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        orm_user = self.session.exec(select(ORMUser).where(ORMUser.email == email)).first()
        return to_domain(orm_user) if orm_user else None

    def save(self, user: User) -> User:
        existing = self.session.get(ORMUser, user.id) if user.id else None
        orm_user = to_orm(user, existing)
        self.session.add(orm_user)
        self.session.commit()
        self.session.refresh(orm_user)
        return to_domain(orm_user)
