from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from backend.src.domain.entities.exercise import Exercise


@dataclass
class WorkoutSession:
    id: Optional[int]
    user_id: int
    name: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    exercises: List[Exercise] = field(default_factory=list)

    @property
    def exercise_count(self) -> int:
        return len(self.exercises)

    @property
    def total_work_sec(self) -> int:
        return sum(e.total_work_time for e in self.exercises)

    @property
    def total_rest_sec(self) -> int:
        return sum(e.total_rest_time for e in self.exercises)

    @property
    def total_duration_sec(self) -> int:
        return self.total_work_sec + self.total_rest_sec

    def end(self, ended_at: Optional[datetime] = None) -> None:
        if self.started_at is None:
            raise ValueError("Cannot end a session that hasn't started")
        if self.ended_at is not None:
            raise ValueError("Session is already ended")
        self.ended_at = ended_at or datetime.utcnow()
