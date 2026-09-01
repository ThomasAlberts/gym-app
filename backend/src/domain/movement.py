from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Enum as SAEnum

from .enums import MovementPattern

if TYPE_CHECKING:
    from .exercise_definition import ExerciseDefinition

class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # "Bench Press", "Squat", etc.

    movement_pattern: MovementPattern = Field(
        sa_column=SAEnum(MovementPattern, name="movement_pattern_enum")
    )

    exercises: List["ExerciseDefinition"] = Relationship(back_populates="movement")