from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from backend.src.adapters.database.database import get_database
from backend.src.adapters.response.exercise_info_response import (
    ExerciseDefinitionResponse, ExercisesSinceMondayResponse, ExerciseMuscleLinkResponse,
)
from backend.src.adapters.response.workout_response import (
    ExerciseWithWorkoutResponse,
)
from backend.src.core.deps import get_current_user
from backend.src.domain.user import User
from backend.src.services.exercise_info_service import (
    ExerciseInfoService,
)


# Contains information needed to create exercises:
# exercise definitions, movements, muscles, links, and enums.

router = APIRouter(
    prefix="/exercise_info",
    tags=["exercise_info"],
)


@router.get(
    "/exercise_definition/all",
    response_model=list[ExerciseDefinitionResponse],
)
def get_exercise_definitions(
    session: Session = Depends(get_database),
):
    service = ExerciseInfoService(session)

    return service.get_all_exercise_definitions()


@router.get(
    "/exercise/all",
    response_model=list[ExerciseWithWorkoutResponse],
)
def get_all_exercises(
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    service = ExerciseInfoService(session)

    exercises = service.get_all_exercises_for_user(
        user_id=user.id,
    )

    return [
        _to_response(exercise)
        for exercise in exercises
    ]


@router.get(
    "/exercise/recent",
    response_model=list[ExerciseWithWorkoutResponse],
)
def get_recent_exercises(
    days: int = Query(
        default=7,
        ge=1,
        le=365,
        description="Number of previous days to search.",
    ),
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    service = ExerciseInfoService(session)

    exercises = service.get_exercises_since(
        user_id=user.id,
        days=days,
    )
    for x in exercises:
        print(_to_response(x))
    return [
        _to_response(exercise)
        for exercise in exercises
    ]


@router.get(
    "/exercise/since-monday",
    response_model=ExercisesSinceMondayResponse,
)
def get_exercises_since_monday(
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    service = ExerciseInfoService(session)

    exercises = service.get_exercises_since_monday(
        user_id=user.id,
    )

    muscle_links_by_definition = service.get_muscle_links_by_definition_id(exercises)
    muscle_strain = service.compute_muscle_strain(
        exercises, muscle_links_by_definition
    )

    return ExercisesSinceMondayResponse(
        exercises=[_to_response(exercise) for exercise in exercises],
        muscle_links={
            definition_id: [
                ExerciseMuscleLinkResponse(muscle=link.muscle, emphasis=link.emphasis)
                for link in links
            ]
            for definition_id, links in muscle_links_by_definition.items()
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
    session: Session = Depends(get_database),
    user: User = Depends(get_current_user),
):
    service = ExerciseInfoService(session)

    try:
        exercises = (
            service.get_last_exercises_for_definition(
                user_id=user.id,
                exercise_definition_id=(
                    exercise_definition_id
                ),
                limit=limit,
                exclude_workout_session_id=(
                    exclude_workout_session_id
                ),
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return [
        _to_response(exercise)
        for exercise in exercises
    ]


def _to_response(
    exercise,
) -> ExerciseWithWorkoutResponse:
    return ExerciseWithWorkoutResponse(
        id=exercise.id,
        exercise_definition_id=(
            exercise.exercise_definition_id
        ),
        notes=exercise.notes,
        exercise_sets=exercise.exercise_sets,
        workout_id=exercise.workout_session_id,
        workout_started_at=(
            exercise.workout_session.started_at
        ),
    )
