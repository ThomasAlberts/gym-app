from typing import Optional

from sqlmodel import Session, select

from backend.src.adapters.database.models import (
    ExerciseDefinition as ORMExerciseDefinition,
    MuscleEmphasis as ORMMuscleEmphasis
)
from backend.src.domain.entities.exercise_definition import ExerciseDefinition
from backend.src.domain.value_objects.muscle_emphasis import MuscleEmphasis


def _definition_to_domain(row: ORMExerciseDefinition) -> ExerciseDefinition:
    return ExerciseDefinition(
        id=row.id,
        name=row.name,
        movement_id=row.movement_id,
        equipment_type=row.equipment_type,
        grip_type=row.grip_type,
        angle=row.angle,
    )


class SqlExerciseDefinitionRepository:  # satisfies domain ExerciseDefinitionRepository
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, definition_id: int) -> Optional[ExerciseDefinition]:
        row = self._session.get(ORMExerciseDefinition, definition_id)
        return _definition_to_domain(row) if row else None

    def list_all(self) -> list[ExerciseDefinition]:
        statement = (
            select(ORMExerciseDefinition)
            .order_by(ORMExerciseDefinition.id)
        )
        return [_definition_to_domain(r) for r in self._session.exec(statement).all()]

    def list_excluding(self, exclude_ids: list[int]) -> list[ExerciseDefinition]:
        statement = (
            select(ORMExerciseDefinition)
            .order_by(ORMExerciseDefinition.id)
        )
        if exclude_ids:
            statement = statement.where(ORMExerciseDefinition.id.notin_(exclude_ids))
        return [_definition_to_domain(r) for r in self._session.exec(statement).all()]

    def find_missing_ids(self, ids: set[int]) -> set[int]:
        if not ids:
            return set()
        statement = select(ORMExerciseDefinition.id).where(ORMExerciseDefinition.id.in_(ids))
        return set(ids) - set(self._session.exec(statement).all())

    def get_muscle_emphasis(self, definition_ids: set[int]) -> dict[int, list[MuscleEmphasis]]:
        if not definition_ids:
            return {}
        statement = select(ORMMuscleEmphasis).where(
            ORMMuscleEmphasis.exercise_definition_id.in_(definition_ids)
        )
        grouped: dict[int, list[MuscleEmphasis]] = {}
        for row in self._session.exec(statement).all():
            emphasis = row.emphasis if row.emphasis is not None else 1.0
            grouped.setdefault(row.exercise_definition_id, []).append(
                MuscleEmphasis(muscle=row.muscle, emphasis=emphasis)
            )
        return grouped
