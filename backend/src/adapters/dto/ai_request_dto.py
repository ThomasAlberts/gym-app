from typing import Optional

from pydantic import BaseModel


class SetIn(BaseModel):
    reps: Optional[int] = None
    weight: Optional[float] = None


class ExerciseIn(BaseModel):
    name: str
    equipment_type: str
    grip_type: str = "none"
    exercise_sets: list[SetIn] = []


class SuggestRequest(BaseModel):
    current_exercises: list[ExerciseIn]
    exclude_definition_ids: list[int] = []


class SuggestionOut(BaseModel):
    id: int
    name: str
    equipment_type: str
    grip_type: str
    reason: str