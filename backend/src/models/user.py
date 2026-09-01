from sqlmodel import SQLModel, Field
from typing import Optional

from backend.src.core.roles import Role


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    first_name: Optional[str] = Field(default=None, nullable=True)
    last_name: Optional[str] = Field(default=None, nullable=True)
    role: Role = Field(default=Role.user)