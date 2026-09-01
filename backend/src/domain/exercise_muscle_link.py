from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SAEnum
from .enums import Muscle

if TYPE_CHECKING:
    from .exercise_definition import ExerciseDefinition

class ExerciseMuscleLink(SQLModel, table=True):
    __tablename__ = "exercise_muscle_link"

    exercise_definition_id: Optional[int] = Field(
        foreign_key="exercise_definition.id", primary_key=True
    )
    muscle: Muscle = Field(
        sa_column=Column("muscle", SAEnum(Muscle, name="muscle_enum"), primary_key=True)
    )
    emphasis: float = Field(default=1.0)

    exercise_definition: "ExerciseDefinition" = Relationship(back_populates="muscles")