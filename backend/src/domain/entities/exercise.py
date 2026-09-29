from dataclasses import dataclass, field
from typing import Optional, List
from backend.src.domain.entities.exercise_set import ExerciseSet


@dataclass
class Exercise:
    id: Optional[int]
    workout_session_id: Optional[int]
    exercise_definition_id: int
    notes: Optional[str] = None
    exercise_sets: List[ExerciseSet] = field(default_factory=list)

    @property
    def total_work_time(self) -> int:
        return sum(s.work_time or 0 for s in self.exercise_sets)

    @property
    def total_rest_time(self) -> int:
        return sum(s.rest_time or 0 for s in self.exercise_sets)

    def add_set(self, exercise_set: ExerciseSet) -> None:
        self.exercise_sets.append(exercise_set)
