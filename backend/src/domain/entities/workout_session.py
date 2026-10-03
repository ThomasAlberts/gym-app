from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, Optional

from backend.src.domain.entities.exercise import Exercise
from backend.src.domain.errors import InvalidWorkoutSession

_EDITABLE_FIELDS = {"name", "started_at", "ended_at"}


def _as_utc(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


def _as_utc_or_none(value: Optional[datetime]) -> Optional[datetime]:
    return None if value is None else _as_utc(value)


def _check_dates(started_at: datetime, ended_at: Optional[datetime]) -> None:
    if ended_at is not None and _as_utc(ended_at) < _as_utc(started_at):
        raise InvalidWorkoutSession("ended_at cannot be before started_at")


@dataclass
class WorkoutSession:
    user_id: int
    started_at: datetime
    name: Optional[str] = None
    ended_at: Optional[datetime] = None
    id: Optional[int] = None
    exercises: list[Exercise] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        user_id: int,
        started_at: datetime,
        name: Optional[str] = None,
        ended_at: Optional[datetime] = None,
        exercises: Optional[Iterable[Exercise]] = None,
    ) -> "WorkoutSession":
        started_at, ended_at = _as_utc(started_at), _as_utc_or_none(ended_at)
        _check_dates(started_at, ended_at)
        return cls(
            user_id=user_id,
            name=name,
            started_at=started_at,
            ended_at=ended_at,
            exercises=list(exercises or []),
        )

    def belongs_to(self, user_id: int) -> bool:
        return self.user_id == user_id

    def apply_changes(self, **changes) -> None:
        unknown = set(changes) - _EDITABLE_FIELDS
        if unknown:
            raise InvalidWorkoutSession(f"cannot change: {sorted(unknown)}")
        if "started_at" in changes and changes["started_at"] is None:
            raise InvalidWorkoutSession("started_at cannot be null")
        for key in ("started_at", "ended_at"):
            if key in changes:
                changes[key] = _as_utc_or_none(changes[key])
        _check_dates(
            changes.get("started_at", self.started_at),
            changes.get("ended_at", self.ended_at),
        )
        for key, value in changes.items():
            setattr(self, key, value)

    def replace_exercises(self, exercises: Iterable[Exercise]) -> None:
        self.exercises = list(exercises)
