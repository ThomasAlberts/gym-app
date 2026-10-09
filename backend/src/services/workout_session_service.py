from datetime import datetime, timezone
from typing import Callable, Optional

from backend.src.adapters.database.repositories.workout_session_repository import SqlWorkoutSessionRepository
from backend.src.domain.entities.exercise import Exercise
from backend.src.domain.entities.workout_session import WorkoutSession
from backend.src.services.exercise_info_service import ExerciseInfoService


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class WorkoutSessionService:
    def __init__(
        self,
        workout_session_repository: SqlWorkoutSessionRepository,
        exercise_info_service: ExerciseInfoService,
        clock: Callable[[], datetime] = _utcnow,
    ):
        self._workout_session_repository = workout_session_repository
        self._exercise_info_service = exercise_info_service
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
        self._exercise_info_service.ensure_exercise_definitions_exist(exercises)
        workout_session = WorkoutSession.create(
            user_id=user_id,
            name=name,
            started_at=started_at or self._clock(),   # no start time sent = starts now
            ended_at=ended_at,
            exercises=exercises,
        )
        return self._workout_session_repository.save(workout_session)


    def update_workout_session(
        self,
        user_id: int,
        workout_session_id: int,
        changes: dict,
        exercises: Optional[list[Exercise]] = None,
    ) -> Optional[WorkoutSession]:
        workout_session = self._validate_owner(user_id, workout_session_id)
        if workout_session is None:
            return None

        if exercises is not None:
            self._exercise_info_service.ensure_exercise_definitions_exist(exercises)

        workout_session.apply_changes(**changes)
        if exercises is not None:
            workout_session.replace_exercises(exercises)
        return self._workout_session_repository.save(workout_session)


    def delete_workout_session(self, user_id: int, workout_session_id: int) -> bool:
        if self._validate_owner(user_id, workout_session_id) is None:
            return False
        self._workout_session_repository.delete(workout_session_id)
        return True


    def get_workout_session(self, user_id: int, workout_session_id: int) -> Optional[WorkoutSession]:
        return self._validate_owner(user_id, workout_session_id)


    def list_workout_sessions(self, user_id: int) -> list[WorkoutSession]:
        return self._workout_session_repository.list_for_user(user_id)


    def _validate_owner(self, user_id: int, workout_session_id: int) -> Optional[WorkoutSession]:
        """Someone else's workout session looks exactly like a missing one."""
        workout_session = self._workout_session_repository.get_by_id(workout_session_id)
        if workout_session is None or not workout_session.belongs_to(user_id):
            return None
        return workout_session