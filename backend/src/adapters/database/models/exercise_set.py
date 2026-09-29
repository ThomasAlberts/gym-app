from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .exercise import Exercise


class ExerciseSet(SQLModel, table=True):
    __tablename__ = "exercise_set"
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")

    reps: Optional[int] = None
    weight: Optional[float] = None
    work_time: Optional[int] = None
    rest_time: Optional[int] = None

    exercise: Optional["Exercise"] = Relationship(back_populates="exercise_sets")