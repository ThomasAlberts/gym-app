from dataclasses import dataclass
from typing import Optional
from backend.src.domain.enums import MovementPattern


@dataclass
class Movement:
    id: Optional[int]
    name: str
    movement_pattern: MovementPattern