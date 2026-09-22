from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.src.domain.exercise import Exercise

class ExerciseSet(SQLModel, table=True):
    __tablename__ = "exercise_set"
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")

    reps: Optional[int] = None
    weight: Optional[float] = None
    work_time: Optional[int] = None
    rest_time: Optional[int] = None

    exercise: Optional["Exercise"] = Relationship(back_populates="exercise_sets")

    @property
    def work_duration_sec(self) -> int:
        """Return the total work duration for this set."""
        return self.work_time or 0

    @property
    def rest_duration_sec_safe(self) -> int:
        """Return the rest duration safely (0 if None)."""
        return self.rest_time or 0