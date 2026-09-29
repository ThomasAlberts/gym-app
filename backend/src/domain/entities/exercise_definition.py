from dataclasses import dataclass, field
from typing import Optional, List

from backend.src.domain.enums import EquipmentType, GripType, AngleType
from backend.src.domain.entities.movement import Movement
from backend.src.domain.value_objects.muscle_emphasis import MuscleEmphasis


@dataclass
class ExerciseDefinition:
    id: Optional[int]
    name: str
    movement: Movement
    equipment_type: EquipmentType
    grip_type: Optional[GripType] = None
    angle: Optional[AngleType] = None
    muscles: List[MuscleEmphasis] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        parts = []
        if self.angle:
            parts.append(self.angle.value.capitalize())
        if self.equipment_type:
            parts.append(self.equipment_type.value.replace("_", " ").capitalize())
        parts.append(self.movement.name)
        return " ".join(parts)
