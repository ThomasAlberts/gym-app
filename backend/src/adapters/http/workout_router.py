from typing import List

from fastapi import APIRouter, Depends, HTTPException

from backend.src.adapters.dto.workout_session_dto import WorkoutCreate, WorkoutUpdate
from backend.src.adapters.http.dependencies import get_workout_session_service
from backend.src.adapters.http.mappers import exercises_from_dto
from backend.src.adapters.response.workout_response import WorkoutResponse
from backend.src.core.deps import get_current_user
from backend.src.domain.entities.user import User
from backend.src.services.workout_session_service import WorkoutSessionService

router = APIRouter(prefix="/workout", tags=["workout"])


@router.post("/create_new", status_code=201)
def create_workout(
    dto: WorkoutCreate,
    service: WorkoutSessionService = Depends(get_workout_session_service),
    user: User = Depends(get_current_user),
):
    return service.create_workout_session(
        user_id=user.id,
        started_at=dto.started_at,
        name=dto.name,
        ended_at=dto.ended_at,
        exercises=exercises_from_dto(dto.exercises),
    )


@router.patch("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: int,
    dto: WorkoutUpdate,
    service: WorkoutSessionService = Depends(get_workout_session_service),
    user: User = Depends(get_current_user),
):
    updated = service.update_workout_session(
        user_id=user.id,
        workout_session_id=workout_id,
        changes=dto.model_dump(exclude_unset=True, exclude={"exercises"}),
        exercises=None if dto.exercises is None else exercises_from_dto(dto.exercises),
    )
    if updated is None:
        raise HTTPException(404, "Workout not found")
    return updated


@router.delete("/{workout_id}", status_code=204)
def delete_workout(
    workout_id: int,
    service: WorkoutSessionService = Depends(get_workout_session_service),
    user: User = Depends(get_current_user),
):
    if not service.delete_workout_session(user.id, workout_id):
        raise HTTPException(404, "Workout not found")


@router.get("/all", response_model=List[WorkoutResponse])
def get_all_workouts(
    service: WorkoutSessionService = Depends(get_workout_session_service),
    user: User = Depends(get_current_user),
):
    return service.get_all_workout_sessions(user.id)


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: int,
    service: WorkoutSessionService = Depends(get_workout_session_service),
    user: User = Depends(get_current_user),
):
    workout = service.get_workout_session(user.id, workout_id)
    if workout is None:
        raise HTTPException(404, "Workout not found")
    return workout
