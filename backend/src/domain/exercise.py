from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.src.domain.exercise_definition import ExerciseDefinition
    from .exercise_set import ExerciseSet
    from .workout_session import WorkoutSession

class Exercise(SQLModel, table=True):
    """
    Exercise instance in a workout session.
    References ExerciseDefinition for canonical exercise info.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # Link to the workout session
    workout_session_id: Optional[int] = Field(
        default=None,
        foreign_key="workout_session.id"
    )

    # Link to the canonical exercise definition
    exercise_definition_id: Optional[int] = Field(
        default=None,
        foreign_key="exercise_definition.id"
    )

    notes: Optional[str] = None

    # Relationships
    workout_session: Optional["WorkoutSession"] = Relationship(
        back_populates="exercises"
    )

    exercise_definition: "ExerciseDefinition" = Relationship(
        back_populates="exercises"
    )

    exercise_sets: List["ExerciseSet"] = Relationship(
        back_populates="exercise",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    # Computed properties
    @property
    def total_work_time(self) -> int:
        """
        Sum of all work durations from sets
        """
        return sum(s.work_time for s in getattr(self, "exercise_sets", []))

    @property
    def total_rest_time(self) -> int:
        """
        Sum of all rest durations from sets
        """
        return sum(s.rest_time for s in getattr(self, "exercise_sets", []))