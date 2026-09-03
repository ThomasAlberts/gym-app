# services/workout_service.py
import datetime
from datetime import datetime, timedelta
from sqlmodel import Session, select

from backend.src.domain.exercise_definition import ExerciseDefinition
from backend.src.models.exercise import Exercise
from backend.src.models.workout_session import WorkoutSession


class ExerciseInfoService:
    def __init__(self, session: Session):
        self.session = session


    def get_all_exercise_definitions(self):
        return self.session.query(ExerciseDefinition).all()


    def get_all_exercises_for_user(self, user_id: int) -> list[Exercise]:
        statement = (
            select(Exercise)
            .join(WorkoutSession, Exercise.workout_session_id == WorkoutSession.id)
            .where(WorkoutSession.user_id == user_id)
            .order_by(WorkoutSession.started_at.desc())
        )
        return self.session.exec(statement).all()


    def get_exercises_since(self, user_id: int, days: int) -> list[Exercise]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        statement = (
            select(Exercise)
            .join(WorkoutSession, Exercise.workout_session_id == WorkoutSession.id)
            .where(WorkoutSession.user_id == user_id)
            .where(WorkoutSession.started_at >= cutoff)
            .order_by(WorkoutSession.started_at.desc())
        )
        return self.session.exec(statement).all()

    def get_last_exercises_for_definition(
            self,
            user_id: int,
            exercise_definition_id: int,
            days: int = 90,
            exclude_workout_session_id: int | None = None,
            limit: int = 3,
    ) -> list[Exercise]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        statement = (
            select(Exercise)
            .join(WorkoutSession, Exercise.workout_session_id == WorkoutSession.id)
            .where(WorkoutSession.user_id == user_id)
            .where(Exercise.exercise_definition_id == exercise_definition_id)
            .where(WorkoutSession.started_at >= cutoff)
        )
        if exclude_workout_session_id is not None:
            statement = statement.where(
                Exercise.workout_session_id != exclude_workout_session_id
            )
        statement = statement.order_by(WorkoutSession.started_at.desc()).limit(limit)
        return self.session.exec(statement).all()