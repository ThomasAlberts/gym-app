from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .exercise_definition import ExerciseDefinition
    from .exercise_set import ExerciseSet
    from .workout_session import WorkoutSession


class Exercise(SQLModel, table=True):
    __tablename__ = "exercise"

    id: Optional[int] = Field(default=None, primary_key=True)
    workout_session_id: Optional[int] = Field(default=None, foreign_key="workout_session.id")
    exercise_definition_id: Optional[int] = Field(default=None, foreign_key="exercise_definition.id")
    notes: Optional[str] = None

    workout_session: Optional["WorkoutSession"] = Relationship(back_populates="exercises")
    exercise_definition: "ExerciseDefinition" = Relationship(back_populates="exercises")
    exercise_sets: List["ExerciseSet"] = Relationship(
        back_populates="exercise",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
