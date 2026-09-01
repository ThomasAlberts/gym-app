from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.src.adapters.database.database import get_database        # your database session dependency
from backend.src.adapters.response.workout_response import WorkoutResponse
from backend.src.models.user import User
from backend.src.adapters.dto.workout_dto import WorkoutCreate, WorkoutUpdate  # the Pydantic/SQLModel schema for input
from backend.src.core.deps import get_current_user  # dependency to get logged-in user
from backend.src.services.workout_service import WorkoutService

router = APIRouter(prefix="/workout", tags=["workout"])

@router.post("/create_new", status_code=201)
def create_workout(
    dto: WorkoutCreate,
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    workout = WorkoutService(session).create_workout(user.id, dto)
    return workout


@router.patch("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: int,
    dto: WorkoutUpdate,
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    workout = WorkoutService(session).get_workout(workout_id)
    if workout is None or workout.user_id != user.id:
        raise HTTPException(404, "Workout not found")

    updated = WorkoutService(session).update_workout(workout_id, dto)
    return updated


@router.delete("/{workout_id}", status_code=204)
def delete_workout(
    workout_id: int,
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    deleted = WorkoutService(session).delete_workout(workout_id, user.id)
    if not deleted:
        raise HTTPException(404, "Workout not found")


@router.get("/all", response_model=List[WorkoutResponse])
def get_all_workouts(
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    return WorkoutService(session).get_all_workouts(user.id)


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: int,
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    workout = WorkoutService(session).get_workout(workout_id)
    if workout is None:
        raise HTTPException(404, "Workout not found")
    return workout


