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

    # Exercise 1: squat-pattern lift.
    # Quads and glutes are both prime movers in a squat; hamstrings assist
    # the hip extension; abs are stabilizing, not driving the movement.
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.GLUTES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.QUADS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.HAMSTRINGS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.ABS, emphasis=0.25),
    ])

    # Exercise 2: overhead/shoulder press.
    # Front delts are the target; triceps and upper chest assist the press;
    # rear delts only stabilize the shoulder blade, minor role.
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.FRONT_DELTS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.TRICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.CHEST_UPPER, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.REAR_DELTS, emphasis=0.25),
    ])

    # Exercise 3: flat bench press.
    # Mid chest is the target; triceps and front delts assist the press;
    # upper chest gets minor spillover from a flat (non-incline) angle.
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.CHEST_MID, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.TRICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.FRONT_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.CHEST_UPPER, emphasis=0.25),
    ])

    # Exercise 4: incline press.
    # Upper chest is the target; front delts and triceps assist; mid chest
    # gets minor spillover from the incline angle.
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.CHEST_UPPER, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.FRONT_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.TRICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.CHEST_MID, emphasis=0.25),
    ])

    # Exercise 5: row/pulldown pattern.
    # Lats are the target; rhomboids and biceps assist the pull; rear delts
    # only stabilize, minor role.
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.RHOMBOIDS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.BICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.REAR_DELTS, emphasis=0.25),
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