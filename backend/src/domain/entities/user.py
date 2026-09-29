from dataclasses import dataclass
from typing import Optional

# NOTE: adjust this import to match your actual project root package name.
from backend.src.core.roles import Role


@dataclass
class User:
    id: Optional[int]
    email: str
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Role = Role.user

    @property
    def full_name(self) -> str:
        parts = [p for p in (self.first_name, self.last_name) if p]
        return " ".join(parts) if parts else self.email
