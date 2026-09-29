from typing import Optional, List
from sqlmodel import Session, select

from backend.src.domain.entities.exercise_definition import ExerciseDefinition
from backend.src.adapters.database.models.exercise_definition import ExerciseDefinition as ORMExerciseDefinition
from backend.src.adapters.database.mappers.catalog_mapper import exercise_definition_to_domain


class SqlExerciseCatalogRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, definition_id: int) -> Optional[ExerciseDefinition]:
        orm = self.session.get(ORMExerciseDefinition, definition_id)
        return exercise_definition_to_domain(orm) if orm else None

    def list_all(self) -> List[ExerciseDefinition]:
        orm_list = self.session.exec(select(ORMExerciseDefinition)).all()
        return [exercise_definition_to_domain(o) for o in orm_list]
