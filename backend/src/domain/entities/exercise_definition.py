from dataclasses import dataclass, field
from typing import Optional, List

from backend.src.domain.enums import EquipmentType, GripType, AngleType
from backend.src.domain.value_objects.muscle_emphasis import MuscleEmphasis


@dataclass
class ExerciseDefinition:
    id: Optional[int]
    name: str
    movement_id: int
    equipment_type: EquipmentType
    grip_type: Optional[GripType] = None
    angle: Optional[AngleType] = None
    muscles: List[MuscleEmphasis] = field(default_factory=list)