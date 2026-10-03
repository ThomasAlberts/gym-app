from dataclasses import dataclass, field
from typing import Optional

from backend.src.domain.entities.exercise_set import ExerciseSet


@dataclass
class Exercise:
    exercise_definition_id: int
    notes: Optional[str] = None
    exercise_sets: list[ExerciseSet] = field(default_factory=list)
    id: Optional[int] = None
    workout_session_id: Optional[int] = None

    @property
    def set_count(self) -> int:
        return len(self.exercise_sets)
