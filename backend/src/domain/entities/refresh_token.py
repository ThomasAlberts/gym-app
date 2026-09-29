from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class RefreshToken:
    id: Optional[int]
    user_id: int
    token_hash: str
    expires_at: datetime
    revoked: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.expires_at

    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired()

    def revoke(self) -> None:
        self.revoked = True
