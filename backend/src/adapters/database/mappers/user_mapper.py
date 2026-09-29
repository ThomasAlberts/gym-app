from typing import Optional

from backend.src.domain.entities.user import User as DomainUser
from backend.src.adapters.database.models.user import User as ORMUser


def to_domain(orm_user: ORMUser) -> DomainUser:
    return DomainUser(
        id=orm_user.id,
        email=orm_user.email,
        hashed_password=orm_user.hashed_password,
        first_name=orm_user.first_name,
        last_name=orm_user.last_name,
        role=orm_user.role,
    )


def to_orm(user: DomainUser, existing: Optional[ORMUser] = None) -> ORMUser:
    orm_user = existing or ORMUser()
    orm_user.id = user.id
    orm_user.email = user.email
    orm_user.hashed_password = user.hashed_password
    orm_user.first_name = user.first_name
    orm_user.last_name = user.last_name
    orm_user.role = user.role
    return orm_user
