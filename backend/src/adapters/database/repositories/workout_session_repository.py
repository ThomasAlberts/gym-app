from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from backend.src.adapters.database.mappers.workout_session_mapper import (
    workout_session_to_domain,
    workout_session_to_orm,
)
from backend.src.adapters.database.models import (
    Exercise as ORMExercise,
    WorkoutSession as ORMWorkoutSession,
)
from backend.src.domain.entities.workout_session import WorkoutSession

_EAGER = selectinload(ORMWorkoutSession.exercises).selectinload(ORMExercise.exercise_sets)


class SqlWorkoutSessionRepository:  # satisfies domain WorkoutSessionRepository
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, workout_session_id: int) -> Optional[WorkoutSession]:
        orm = self._load(workout_session_id)
        return workout_session_to_domain(orm) if orm else None

    def list_for_user(self, user_id: int) -> list[WorkoutSession]:
        statement = (
            select(ORMWorkoutSession)
            .where(ORMWorkoutSession.user_id == user_id)
            .order_by(ORMWorkoutSession.started_at.desc())
            .options(_EAGER)
        )
        return [workout_session_to_domain(o) for o in self._session.exec(statement).all()]

    def save(self, workout_session: WorkoutSession) -> WorkoutSession:
        existing = (
            self._load(workout_session.id) if workout_session.id is not None else None
        )
        orm = workout_session_to_orm(workout_session, existing)
        self._session.add(orm)
        self._session.commit()
        return self.get_by_id(orm.id)

    def delete(self, workout_session_id: int) -> None:
        orm = self._session.get(ORMWorkoutSession, workout_session_id)
        if orm is not None:
            self._session.delete(orm)
            self._session.commit()

    def _load(self, workout_session_id: int) -> Optional[ORMWorkoutSession]:
        statement = (
            select(ORMWorkoutSession)
            .where(ORMWorkoutSession.id == workout_session_id)
            .options(_EAGER)
        )
        return self._session.exec(statement).first()
