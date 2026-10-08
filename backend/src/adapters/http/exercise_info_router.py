from fastapi import APIRouter, Depends, HTTPException, Query

from backend.src.adapters.http.dependencies import get_exercise_info_service
from backend.src.adapters.response.exercise_info_response import (
    ExerciseDefinitionResponse,
    ExercisesSinceMondayResponse,
    MuscleEmphasisResponse,
)
from backend.src.adapters.response.workout_response import ExerciseWithWorkoutResponse
from backend.src.core.deps import get_current_user
from backend.src.domain.entities.exercise import Exercise
from backend.src.domain.entities.user import User
from backend.src.services.exercise_info_service import ExerciseInfoService


router = APIRouter(
    prefix="/exercise_info",
    tags=["exercise_info"],
)


@router.get(
    "/exercise_definition/all",
    response_model=list[ExerciseDefinitionResponse],
)
def get_all_exercise_definition(
    service: ExerciseInfoService = Depends(get_exercise_info_service),
):
    return [
        ExerciseDefinitionResponse.model_validate(definition, from_attributes=True)
        for definition in service.list_exercise_definitions()
    ]


@router.get(
    "/exercise/all",
    response_model=list[ExerciseWithWorkoutResponse],
)
def get_all_exercises(
    service: ExerciseInfoService = Depends(get_exercise_info_service),
    user: User = Depends(get_current_user),
):
    items = service.get_all_exercises_for_user(user_id=user.id)
    return [_to_response(*item) for item in items]


@router.get(
    "/exercise/recent",
    response_model=list[ExerciseWithWorkoutResponse],
)
def list_recent_exercises(
    days: int = Query(
        default=7,
        ge=1,
        le=365,
        description="Number of previous days to search.",
    ),
    service: ExerciseInfoService = Depends(get_exercise_info_service),
    user: User = Depends(get_current_user),
):
    items = service.list_recent_exercises(user_id=user.id, days=days)
    return [_to_response(*item) for item in items]


@router.get(
    "/exercise/since-monday",
    response_model=ExercisesSinceMondayResponse,
)
def get_exercises_since_monday(
    service: ExerciseInfoService = Depends(get_exercise_info_service),
    user: User = Depends(get_current_user),
):
    items = service.get_exercises_since_monday(user_id=user.id)
    emphasis_by_definition = service.get_muscle_emphasis_by_exercise_definition_id(items)
    muscle_strain = service.compute_muscle_strain(items, emphasis_by_definition)

    return ExercisesSinceMondayResponse(
        exercises=[_to_response(*item) for item in items],
        muscle_links={
            definition_id: [
                MuscleEmphasisResponse(muscle=m.muscle, emphasis=m.emphasis)
                for m in muscles
            ]
            for definition_id, muscles in emphasis_by_definition.items()
        },
        muscle_strain=muscle_strain,
    )


@router.get(
    "/exercise/history/{exercise_definition_id}",
    response_model=list[ExerciseWithWorkoutResponse],
)
def get_last_exercises_for_definition(
    exercise_definition_id: int,
    limit: int = Query(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of exercises to return.",
    ),
    exclude_workout_session_id: int | None = Query(
        default=None,
        description=(
            "Workout session ID to exclude, for example "
            "the workout currently being edited."
        ),
    ),
    service: ExerciseInfoService = Depends(get_exercise_info_service),
    user: User = Depends(get_current_user),
):
    try:
        items = service.list_exercises_for_definition(
            user_id=user.id,
            exercise_definition_id=exercise_definition_id,
            limit=limit,
            exclude_workout_session_id=exclude_workout_session_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return [_to_response(*item) for item in items]


def _to_response(exercise: Exercise, workout_started_at) -> ExerciseWithWorkoutResponse:
    return ExerciseWithWorkoutResponse(
        id=exercise.id,
        exercise_definition_id=exercise.exercise_definition_id,
        notes=exercise.notes,
        exercise_sets=exercise.exercise_sets,
        workout_id=exercise.workout_session_id,
        workout_started_at=workout_started_at,
    )
