from datetime import datetime, time, timedelta, timezone
from typing import Callable, Optional

from backend.src.domain.entities.exercise_definition import ExerciseDefinition
from backend.src.domain.entities.exercise import Exercise
from backend.src.domain.enums import Muscle
from backend.src.domain.muscle_strain import compute_muscle_strain as _compute_muscle_strain
from backend.src.domain.repositories import ExerciseDefinitionRepository, ExerciseRepository
from backend.src.domain.value_objects.muscle_emphasis import MuscleEmphasis


HISTORY_WINDOW_DAYS = 60


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def start_of_week(now: datetime) -> datetime:
    monday = now.date() - timedelta(days=now.weekday())
    return datetime.combine(monday, time.min, tzinfo=timezone.utc)


class ExerciseInfoService:
    def __init__(
        self,
        exercises: ExerciseRepository,
        exercise_definitions: ExerciseDefinitionRepository,
        clock: Callable[[], datetime] = _utcnow,
    ):
        self._exercises = exercises
        self._exercise_definitions = exercise_definitions
        self._clock = clock


    def get_all_exercise_definitions(self) -> list[ExerciseDefinition]:
        return self._exercise_definitions.list_all()


    def get_all_exercises_for_user(self, user_id: int) -> list[tuple[Exercise, Optional[datetime]]]:
        return self._exercises.list_for_user(user_id)


    def get_exercises_since(self, user_id: int, days: int) -> list[tuple[Exercise, Optional[datetime]]]:
        now = self._clock()
        return self._exercises.list_for_user_between(user_id, now - timedelta(days=days), now)


    def get_exercises_since_monday(self, user_id: int) -> list[tuple[Exercise, Optional[datetime]]]:
        now = self._clock()
        return self._exercises.list_for_user_between(user_id, start_of_week(now), now)


    def get_muscle_emphasis_by_definition_id(
        self, items: list[tuple[Exercise, Optional[datetime]]]
    ) -> dict[int, list[MuscleEmphasis]]:
        ids = {exercise.exercise_definition_id for exercise, _ in items}
        if not ids:
            return {}
        return self._exercise_definitions.get_muscle_emphasis(ids)


    def compute_muscle_strain(
        self,
        items: list[tuple[Exercise, Optional[datetime]]],
        emphasis_by_definition: dict[int, list[MuscleEmphasis]],
    ) -> dict[Muscle, float]:
        return _compute_muscle_strain([exercise for exercise, _ in items], emphasis_by_definition)


    def get_last_exercises_for_definition(
        self,
        user_id: int,
        exercise_definition_id: int,
        limit: int = 3,
        exclude_workout_session_id: Optional[int] = None,
    ) -> list[tuple[Exercise, Optional[datetime]]]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        now = self._clock()
        return self._exercises.list_for_definition_between(
            user_id,
            exercise_definition_id,
            now - timedelta(days=HISTORY_WINDOW_DAYS),
            now,
            limit,
            exclude_workout_session_id,
        )
