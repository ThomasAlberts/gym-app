from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Enum as SAEnum

from .enums import EquipmentType, GripType, AngleType

if TYPE_CHECKING:
    from .movement import Movement  # used only for type hints
    from .exercise_muscle_link import ExerciseMuscleLink
    from backend.src.domain.exercise import Exercise

class ExerciseDefinition(SQLModel, table=True):
    __tablename__ = "exercise_definition"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # generated display name

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

    # relationships
    movement: "Movement" = Relationship(back_populates="exercises")
    muscles: List["ExerciseMuscleLink"] = Relationship(back_populates="exercise_definition")
    exercises: List["Exercise"] = Relationship(back_populates="exercise_definition")

    @property
    def display_name(self) -> str:
        parts = []
        if self.angle:
            parts.append(self.angle.value.capitalize())
        if self.equipment_type:
            parts.append(self.equipment_type.value.replace("_", " ").capitalize())
        parts.append(self.movement.name)
        return " ".join(parts)