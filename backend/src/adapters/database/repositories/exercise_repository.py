from datetime import datetime
from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from backend.src.adapters.database.mappers.workout_session_mapper import exercise_to_domain
from backend.src.adapters.database.models import (
    Exercise as ORMExercise,
    WorkoutSession as ORMWorkoutSession,
)
from backend.src.domain.entities.exercise import Exercise


class SqlExerciseRepository:
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def _for_user(user_id: int):
        return (
            select(ORMExercise, ORMWorkoutSession.started_at)
            .join(ORMWorkoutSession, ORMExercise.workout_session_id == ORMWorkoutSession.id)
            .where(ORMWorkoutSession.user_id == user_id)
            .options(selectinload(ORMExercise.exercise_sets))
        )

    def _run(self, statement) -> list[tuple[Exercise, Optional[datetime]]]:
        return [
            (exercise_to_domain(row), started_at)
            for row, started_at in self._session.exec(statement).all()
        ]

    def list_for_user(self, user_id: int) -> list[tuple[Exercise, Optional[datetime]]]:
        statement = self._for_user(user_id).order_by(ORMWorkoutSession.started_at.desc())
        return self._run(statement)

    def list_for_user_between(
        self, user_id: int, start: datetime, end: datetime
    ) -> list[tuple[Exercise, Optional[datetime]]]:
        statement = (
            self._for_user(user_id)
            .where(ORMWorkoutSession.started_at >= start, ORMWorkoutSession.started_at <= end)
            .order_by(ORMWorkoutSession.started_at.desc())
        )
        return self._run(statement)

    def list_for_definition_between(
        self,
        user_id: int,
        definition_id: int,
        start: datetime,
        end: datetime,
        limit: int,
        exclude_workout_session_id: Optional[int] = None,
    ) -> list[tuple[Exercise, Optional[datetime]]]:
        statement = self._for_user(user_id).where(
            ORMExercise.exercise_definition_id == definition_id,
            ORMWorkoutSession.started_at >= start,
            ORMWorkoutSession.started_at <= end,
        )
        if exclude_workout_session_id is not None:
            statement = statement.where(ORMExercise.workout_session_id != exclude_workout_session_id)
        statement = statement.order_by(ORMWorkoutSession.started_at.desc()).limit(limit)
        return self._run(statement)
