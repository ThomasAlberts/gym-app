from dataclasses import dataclass
from typing import Optional


@dataclass
class ExerciseSet:
    id: Optional[int]
    exercise_id: Optional[int]
    reps: Optional[int] = None
    weight: Optional[float] = None
    work_time: Optional[int] = None
    rest_time: Optional[int] = None

    @property
    def work_duration_sec(self) -> int:
        return self.work_time or 0

    @property
    def rest_duration_sec_safe(self) -> int:
        return self.rest_time or 0
