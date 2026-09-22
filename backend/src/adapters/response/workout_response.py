from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class ExerciseSetResponse(BaseModel):
        id: int
        reps: Optional[int]
        weight: Optional[float]
        work_time: Optional[int]
        rest_time: Optional[int]

        model_config = ConfigDict(from_attributes=True)


class ExerciseResponse(BaseModel):
    id: int
    exercise_definition_id: int
    notes: Optional[str]
    exercise_sets: List[ExerciseSetResponse] = []

    model_config = ConfigDict(from_attributes=True)


class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    name: Optional[str]
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    exercises: List[ExerciseResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ExerciseWithWorkoutResponse(ExerciseResponse):
    workout_id: int
    workout_started_at: Optional[datetime]