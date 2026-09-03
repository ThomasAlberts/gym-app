from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from backend.src.adapters.database.database import get_database        # your database session dependency
from backend.src.adapters.response.exercise_info_response import ExerciseDefinitionResponse
from backend.src.adapters.response.workout_response import ExerciseWithWorkoutResponse
from backend.src.core.deps import get_current_user
from backend.src.models.user import User
from backend.src.services.exercise_info_service import ExerciseInfoService

## contains all info needed to create exercises: enums, exercise_defintion, movement, muscle, exercise_muscle_link

router = APIRouter(prefix="/exercise_info", tags=["exercise_info"])

@router.get("/exercise_defintion/all", response_model=List[ExerciseDefinitionResponse])
def get_exercise_definitions(
    session: Session = Depends(get_database),
):
    return ExerciseInfoService(session).get_all_exercise_definitions()



def _to_response(ex) -> ExerciseWithWorkoutResponse:
    return ExerciseWithWorkoutResponse(
        id=ex.id,
        exercise_definition_id=ex.exercise_definition_id,
        notes=ex.notes,
        exercise_sets=ex.exercise_sets,
        workout_id=ex.workout_session_id,
        workout_started_at=ex.workout_session.started_at,
    )


@router.get("/exercise/all", response_model=List[ExerciseWithWorkoutResponse])
def get_all_exercises(
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    exercises = ExerciseInfoService(session).get_all_exercises_for_user(user.id)
    return [_to_response(ex) for ex in exercises]


@router.get("/exercise/recent", response_model=List[ExerciseWithWorkoutResponse])
def get_recent_exercises(
    days: int = Query(7, ge=1, le=365),
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    exercises = ExerciseInfoService(session).get_exercises_since(user.id, days)
    return [_to_response(ex) for ex in exercises]


@router.get(
    "/exercise/last/{exercise_definition_id}/history",
    response_model=List[ExerciseWithWorkoutResponse],
)
def get_last_exercises_for_definition(
    exercise_definition_id: int,
    days: int = Query(90, ge=1, le=365),
    exclude_workout_id: Optional[int] = Query(None),
    limit: int = Query(3, ge=1, le=10),
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    exercises = ExerciseInfoService(session).get_last_exercises_for_definition(
        user.id, exercise_definition_id, days, exclude_workout_id, limit
    )
    return [_to_response(ex) for ex in exercises]