from backend.src.adapters.dto.ai_request_dto import SuggestionOut
from backend.src.domain.entities.exercise import Exercise
from backend.src.domain.entities.exercise_set import ExerciseSet
from backend.src.services.ai_suggestion_service import LoggedExercise, LoggedSet, Suggestion


def exercise_from_dto(dto) -> Exercise:
    return Exercise(
        exercise_definition_id=dto.exercise_definition_id,
        notes=dto.notes,
        exercise_sets=[
            ExerciseSet(
                reps=s.reps,
                weight=s.weight,
                work_time=s.work_time,
                rest_time=s.rest_time,
            )
            for s in dto.exercise_sets
        ],
    )


def exercises_from_dto(items) -> list[Exercise]:
    return [exercise_from_dto(e) for e in items]


def logged_exercises_from_dto(items) -> list[LoggedExercise]:
    return [
        LoggedExercise(
            name=e.name,
            equipment_type=e.equipment_type,
            grip_type=e.grip_type,
            sets=[LoggedSet(reps=s.reps, weight=s.weight) for s in e.exercise_sets],
        )
        for e in items
    ]


def suggestion_to_dto(s: Suggestion) -> SuggestionOut:
    return SuggestionOut(
        id=s.id,
        name=s.name,
        equipment_type=s.equipment_type,
        grip_type=s.grip_type,
        reason=s.reason,
    )
