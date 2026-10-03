from backend.src.domain.entities.exercise import Exercise
from backend.src.domain.enums import Muscle
from backend.src.domain.value_objects.muscle_emphasis import MuscleEmphasis


def compute_muscle_strain(
    exercises: list[Exercise],
    emphasis_by_definition: dict[int, list[MuscleEmphasis]],
) -> dict[Muscle, float]:
    strain: dict[Muscle, float] = {}
    for exercise in exercises:
        if not exercise.set_count:
            continue
        for item in emphasis_by_definition.get(exercise.exercise_definition_id, []):
            strain[item.muscle] = strain.get(item.muscle, 0.0) + exercise.set_count * item.emphasis
    return strain
