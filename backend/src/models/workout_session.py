from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .exercise import Exercise


class WorkoutSession(SQLModel, table=True):
    __tablename__ = "workout_session"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: Optional[str] = Field(default=None, max_length=100)

    user_id: int = Field(foreign_key="user.id")

    started_at: Optional[datetime] = None

    ended_at: Optional[datetime] = None

    exercises: List["Exercise"] = Relationship(
        back_populates="workout_session",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    @property
    def exercise_count(self) -> int:
        return len(self.exercises or [])

    @property
    def total_work_sec(self) -> int:
        return sum(e.total_work_time for e in self.exercises or [])

    @property
    def total_rest_sec(self) -> int:
        return sum(e.total_rest_time for e in self.exercises or [])

    @property
    def total_duration_sec(self) -> int:
        return self.total_work_sec + self.total_rest_sec