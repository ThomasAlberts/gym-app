from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from backend.src.adapters.response.workout_response import ExerciseWithWorkoutResponse
from backend.src.domain.enums import EquipmentType, GripType, AngleType

class ExerciseDefinitionResponse(BaseModel):
    id: int
    name: str
    movement_id: int
    equipment_type: "EquipmentType"  # of str als je enums niet direct wilt
    grip_type: "GripType"
    angle: Optional["AngleType"] = None

    model_config = ConfigDict(from_attributes=True)


class ExerciseMuscleLinkResponse(BaseModel):
    muscle: str
    emphasis: float


class ExercisesSinceMondayResponse(BaseModel):
    exercises: list[ExerciseWithWorkoutResponse]
    muscle_links: dict[int, list[ExerciseMuscleLinkResponse]]
    muscle_strain: dict[str, float]
