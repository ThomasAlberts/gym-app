from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SAEnum
from backend.src.domain.enums import Muscle

if TYPE_CHECKING:
    from .exercise_definition import ExerciseDefinition


class MuscleEmphasis(SQLModel, table=True):
    __tablename__ = "muscle_emphasis"

    exercise_definition_id: Optional[int] = Field(
        foreign_key="exercise_definition.id", primary_key=True
    )
    muscle: Muscle = Field(
        sa_column=Column("muscle", SAEnum(Muscle, name="muscle_enum"), primary_key=True)
    )
    emphasis: float = Field(default=1.0)

    exercise_definition: "ExerciseDefinition" = Relationship(back_populates="muscles")
