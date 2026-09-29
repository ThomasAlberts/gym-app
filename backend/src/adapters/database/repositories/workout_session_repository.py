from typing import Optional, List
from sqlmodel import Session, select

from backend.src.domain.entities.workout_session import WorkoutSession
from backend.src.adapters.database.models.workout_session import WorkoutSession as ORMWorkoutSession
from backend.src.adapters.database.mappers.workout_mapper import (
    workout_session_to_domain,
    workout_session_to_orm,
)


class SqlWorkoutSessionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, session_id: int) -> Optional[WorkoutSession]:
        orm_session = self.session.get(ORMWorkoutSession, session_id)
        return workout_session_to_domain(orm_session) if orm_session else None

    def list_for_user(self, user_id: int) -> List[WorkoutSession]:
        orm_sessions = self.session.exec(
            select(ORMWorkoutSession).where(ORMWorkoutSession.user_id == user_id)
        ).all()
        return [workout_session_to_domain(s) for s in orm_sessions]

    def save(self, session: WorkoutSession) -> WorkoutSession:
        existing = self.session.get(ORMWorkoutSession, session.id) if session.id else None
        orm_session = workout_session_to_orm(session, existing)
        self.session.add(orm_session)
        self.session.commit()
        self.session.refresh(orm_session)
        return workout_session_to_domain(orm_session)
