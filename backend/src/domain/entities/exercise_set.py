from dataclasses import dataclass
from typing import Optional


@dataclass
class ExerciseSet:
    reps: Optional[int] = None
    weight: Optional[float] = None
    work_time: int = 0
    rest_time: int = 0
    id: Optional[int] = None
    exercise_id: Optional[int] = None   # filled when loaded from the DB; the ORM relationship sets it on write
