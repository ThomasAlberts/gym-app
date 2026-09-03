# backend/src/adapters/database/seed.py
from sqlmodel import Session, select

from backend.src.domain.movement import Movement
from backend.src.domain.exercise_definition import ExerciseDefinition
from backend.src.domain.exercise_muscle_link import ExerciseMuscleLink
from backend.src.domain.enums import MovementPattern, AngleType, GripType, EquipmentType, Muscle

## db fill todo: move use real db

def _movements():
    return [
        Movement(id=1, name="Squat", movement_pattern=MovementPattern.SQUAT),
        Movement(id=2, name="Overhead press", movement_pattern=MovementPattern.VERTICAL_PUSH),
        Movement(id=3, name="Bench press", movement_pattern=MovementPattern.VERTICAL_PUSH),
        Movement(id=4, name="pull-down", movement_pattern=MovementPattern.VERTICAL_PULL),
    ]


def _exercise_definitions():
    return [
        ExerciseDefinition(id=1, name="Barbell squat", movement_id=1, equipment_type=EquipmentType.BARBELL, grip_type=GripType.NEUTRAL),
        ExerciseDefinition(id=2, name="Barbell overhead press", movement_id=2, equipment_type=EquipmentType.BARBELL, grip_type=GripType.NEUTRAL),
        ExerciseDefinition(id=3, name="Barbell bench press", movement_id=3, equipment_type=EquipmentType.BARBELL, grip_type=GripType.NEUTRAL, angle=AngleType.FLAT),
        ExerciseDefinition(id=4, name="Barbell incline bench press", movement_id=3, equipment_type=EquipmentType.BARBELL, grip_type=GripType.NEUTRAL, angle=AngleType.INCLINE),
        ExerciseDefinition(id=5, name="Lat pull-down", movement_id=4, equipment_type=EquipmentType.CABLE_LAT_PULLDOWN_BAR, grip_type=GripType.NEUTRAL),
    ]


def _exercise_muscle_links():
    links = []
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.GLUTES, emphasis=1.5),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.QUADS, emphasis=1.5),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.HAMSTRINGS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.ABS, emphasis=0.8),
    ])
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.FRONT_DELTS, emphasis=1.4),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.TRICEPS, emphasis=1.2),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.CHEST_UPPER, emphasis=0.9),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.REAR_DELTS, emphasis=0.7),
    ])
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.CHEST_MID, emphasis=1.5),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.TRICEPS, emphasis=1.3),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.FRONT_DELTS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.CHEST_UPPER, emphasis=0.8),
    ])
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.CHEST_UPPER, emphasis=1.5),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.FRONT_DELTS, emphasis=1.3),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.TRICEPS, emphasis=1.1),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.CHEST_MID, emphasis=0.8),
    ])
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.LATS, emphasis=1.5),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.RHOMBOIDS, emphasis=1.2),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.BICEPS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.REAR_DELTS, emphasis=0.8),
    ])
    return links


def seed_domain_data(session: Session) -> None:
    """Populate reference data (movements, exercise definitions, muscle links)
    if the database is empty. Safe to call on every app startup."""
    already_seeded = session.exec(select(Movement)).first() is not None
    if already_seeded:
        return

    session.add_all(_movements())
    session.add_all(_exercise_definitions())
    session.add_all(_exercise_muscle_links())
    session.commit()