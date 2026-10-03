from datetime import datetime, timezone
from typing import Callable, Optional

from backend.src.domain.entities.exercise import Exercise
from backend.src.domain.entities.workout_session import WorkoutSession
from backend.src.domain.errors import UnknownExerciseDefinition
from backend.src.domain.repositories import (
    ExerciseDefinitionRepository,
    WorkoutSessionRepository,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class WorkoutSessionService:
    def __init__(
        self,
        workout_sessions: WorkoutSessionRepository,
        exercise_definitions: ExerciseDefinitionRepository,
        clock: Callable[[], datetime] = _utcnow,
    ):
        self._workout_sessions = workout_sessions
        self._exercise_definitions = exercise_definitions
        self._clock = clock


    def create_workout_session(
        self,
        user_id: int,
        started_at: Optional[datetime] = None,
        name: Optional[str] = None,
        ended_at: Optional[datetime] = None,
        exercises: Optional[list[Exercise]] = None,
    ) -> WorkoutSession:
        exercises = exercises or []
        self._ensure_definitions_exist(exercises)
        workout_session = WorkoutSession.create(
            user_id=user_id,
            name=name,
            started_at=started_at or self._clock(),   # no start time sent = starts now
            ended_at=ended_at,
            exercises=exercises,
        )
        return self._workout_sessions.save(workout_session)


    def update_workout_session(
        self,
        user_id: int,
        workout_session_id: int,
        changes: dict,
        exercises: Optional[list[Exercise]] = None,
    ) -> Optional[WorkoutSession]:
        workout_session = self._get_owned(user_id, workout_session_id)
        if workout_session is None:
            return None

        # validate everything before touching the aggregate
        if exercises is not None:
            self._ensure_definitions_exist(exercises)

        workout_session.apply_changes(**changes)
        if exercises is not None:
            workout_session.replace_exercises(exercises)
        return self._workout_sessions.save(workout_session)


    def delete_workout_session(self, user_id: int, workout_session_id: int) -> bool:
        if self._get_owned(user_id, workout_session_id) is None:
            return False
        self._workout_sessions.delete(workout_session_id)
        return True


    def get_workout_session(self, user_id: int, workout_session_id: int) -> Optional[WorkoutSession]:
        return self._get_owned(user_id, workout_session_id)


    def get_all_workout_sessions(self, user_id: int) -> list[WorkoutSession]:
        return self._workout_sessions.list_for_user(user_id)


    def _get_owned(self, user_id: int, workout_session_id: int) -> Optional[WorkoutSession]:
        """Someone else's workout session looks exactly like a missing one."""
        workout_session = self._workout_sessions.get_by_id(workout_session_id)
        if workout_session is None or not workout_session.belongs_to(user_id):
            return None
        return workout_session


    def _ensure_definitions_exist(self, exercises: list[Exercise]) -> None:
        ids = {ex.exercise_definition_id for ex in exercises}
        if not ids:
            return
        missing = self._exercise_definitions.find_missing_ids(ids)   # one query, not one per exercise
        if missing:
            raise UnknownExerciseDefinition(missing)
