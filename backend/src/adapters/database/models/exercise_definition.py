from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Enum as SAEnum

from backend.src.domain.enums import EquipmentType, GripType, AngleType

if TYPE_CHECKING:
    from .muscle_emphasis import MuscleEmphasis
    from .exercise import Exercise


class ExerciseDefinition(SQLModel, table=True):
    __tablename__ = "exercise_definition"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str

    movement_id: int = Field(foreign_key="movement.id")

    equipment_type: EquipmentType = Field(
        sa_column=SAEnum(EquipmentType, name="equipment_type_enum")
    )
    grip_type: Optional[GripType] = Field(
        default=None,
        sa_column=SAEnum(GripType, name="grip_type_enum")
    )
    angle: Optional[AngleType] = Field(
        default=None,
        sa_column=SAEnum(AngleType, name="angle_type_enum")
    )

    muscles: List["MuscleEmphasis"] = Relationship(back_populates="exercise_definition")

    exercises: List["Exercise"] = Relationship(back_populates="exercise_definition")