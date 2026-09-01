# dto/workout_dto.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ExerciseSetCreate(BaseModel):
    reps: Optional[int] = None
    weight: Optional[float] = None
    work_time: int = Field(0)
    rest_time: int = Field(0)

    class Config:
        populate_by_name = True


class ExerciseCreate(BaseModel):
    exercise_definition_id: int
    notes: Optional[str] = None
    exercise_sets: List[ExerciseSetCreate] = []


class WorkoutCreate(BaseModel):
    name: Optional[str] = None
    exercises: List[ExerciseCreate] = []
    started_at: datetime
    ended_at: Optional[datetime] = None


class WorkoutUpdate(BaseModel):
    name: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    exercises: Optional[List[ExerciseCreate]] = None