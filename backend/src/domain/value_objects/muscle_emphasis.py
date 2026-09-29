from dataclasses import dataclass
from backend.src.domain.enums import Muscle


@dataclass(frozen=True)
class MuscleEmphasis:
    muscle: Muscle
    emphasis: float = 1.0
