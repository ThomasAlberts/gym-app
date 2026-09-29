from backend.src.domain.entities.movement import Movement as DomainMovement
from backend.src.domain.entities.exercise_definition import ExerciseDefinition as DomainExerciseDefinition
from backend.src.domain.value_objects.muscle_emphasis import MuscleEmphasis
from backend.src.adapters.database.models.movement import Movement as ORMMovement
from backend.src.adapters.database.models.exercise_definition import ExerciseDefinition as ORMExerciseDefinition


def movement_to_domain(orm: ORMMovement) -> DomainMovement:
    return DomainMovement(id=orm.id, name=orm.name, movement_pattern=orm.movement_pattern)


def exercise_definition_to_domain(orm: ORMExerciseDefinition) -> DomainExerciseDefinition:
    return DomainExerciseDefinition(
        id=orm.id,
        name=orm.name,
        movement=movement_to_domain(orm.movement),
        equipment_type=orm.equipment_type,
        grip_type=orm.grip_type,
        angle=orm.angle,
        muscles=[
            MuscleEmphasis(muscle=link.muscle, emphasis=link.emphasis)
            for link in orm.muscles
        ],
    )
