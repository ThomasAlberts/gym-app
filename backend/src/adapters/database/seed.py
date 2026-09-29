from sqlmodel import Session, select

from backend.src.adapters.database.models import (
    Movement,
    ExerciseDefinition,
    MuscleEmphasis
)
from backend.src.domain.enums import (
    MovementPattern,
    AngleType,
    GripType,
    EquipmentType,
    Muscle,
)

# (id, name, movement_pattern)
MOVEMENTS = [
    # Squat
    (1, "Back squat", MovementPattern.SQUAT),
    (2, "Front squat", MovementPattern.SQUAT),
    (3, "Goblet squat", MovementPattern.SQUAT),
    # Hinge
    (4, "Conventional deadlift", MovementPattern.HINGE),
    (5, "Romanian deadlift", MovementPattern.HINGE),
    (6, "Kettlebell swing", MovementPattern.HINGE),
    # Lunge
    (7, "Walking lunge", MovementPattern.LUNGE),
    (8, "Reverse lunge", MovementPattern.LUNGE),
    (9, "Bulgarian split squat", MovementPattern.LUNGE),
    # Horizontal push
    (10, "Bench press", MovementPattern.HORIZONTAL_PUSH),
    (11, "Incline bench press", MovementPattern.HORIZONTAL_PUSH),
    (12, "Decline bench press", MovementPattern.HORIZONTAL_PUSH),
    (13, "Push-up", MovementPattern.HORIZONTAL_PUSH),
    (14, "Dumbbell floor press", MovementPattern.HORIZONTAL_PUSH),
    # Vertical push
    (15, "Overhead press (strict press)", MovementPattern.VERTICAL_PUSH),
    (16, "Push press", MovementPattern.VERTICAL_PUSH),
    (17, "Seated dumbbell shoulder press", MovementPattern.VERTICAL_PUSH),
    (18, "Machine shoulder press", MovementPattern.VERTICAL_PUSH),
    # Horizontal pull
    (19, "Bent-over barbell row", MovementPattern.HORIZONTAL_PULL),
    (20, "Chest-supported row", MovementPattern.HORIZONTAL_PULL),
    (21, "Seated cable row", MovementPattern.HORIZONTAL_PULL),
    (22, "Inverted row (TRX/bar)", MovementPattern.HORIZONTAL_PULL),
    # Vertical pull
    (23, "Pull-up", MovementPattern.VERTICAL_PULL),
    (24, "Chin-up", MovementPattern.VERTICAL_PULL),
    (25, "Lat pull-down", MovementPattern.VERTICAL_PULL),
    (26, "Assisted pull-up", MovementPattern.VERTICAL_PULL),
    # Carry
    (27, "Farmer's carry", MovementPattern.CARRY),
    (28, "Suitcase carry", MovementPattern.CARRY),
    (29, "Rack carry", MovementPattern.CARRY),
    # Rotation / anti-rotation
    (30, "Cable woodchop", MovementPattern.ROTATION),
    (31, "Pallof press", MovementPattern.ROTATION),
    (32, "Russian twist", MovementPattern.ROTATION),
]

# (id, name, movement_id, equipment_type, grip_type, angle)
EXERCISE_DEFINITIONS = [
    # Squats
    (1, "Barbell back squat", 1, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    (2, "Barbell front squat", 2, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    (3, "Goblet squat", 3, EquipmentType.KETTLEBELL, GripType.NEUTRAL, None),
    # Hinges
    (4, "Conventional deadlift", 4, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    (5, "Romanian deadlift", 5, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    (6, "Kettlebell swing", 6, EquipmentType.KETTLEBELL, GripType.NEUTRAL, None),
    # Lunges
    (7, "Walking dumbbell lunge", 7, EquipmentType.DUMBBELL, GripType.NEUTRAL, None),
    (8, "Reverse dumbbell lunge", 8, EquipmentType.DUMBBELL, GripType.NEUTRAL, None),
    (9, "Bulgarian split squat (dumbbells)", 9, EquipmentType.DUMBBELL, GripType.NEUTRAL, None),
    # Horizontal push
    (10, "Barbell bench press", 10, EquipmentType.BARBELL, GripType.NEUTRAL, AngleType.FLAT),
    (11, "Barbell incline bench press", 11, EquipmentType.BARBELL, GripType.NEUTRAL, AngleType.INCLINE),
    (12, "Barbell decline bench press", 12, EquipmentType.BARBELL, GripType.NEUTRAL, AngleType.DECLINE),
    (13, "Push-up", 13, EquipmentType.BODYWEIGHT, GripType.NEUTRAL, AngleType.FLAT),
    (14, "Dumbbell floor press", 14, EquipmentType.DUMBBELL, GripType.NEUTRAL, AngleType.FLAT),
    # Vertical push
    (15, "Barbell overhead press", 15, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    (16, "Push press", 16, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    (17, "Seated dumbbell shoulder press", 17, EquipmentType.DUMBBELL, GripType.NEUTRAL, None),
    (18, "Machine shoulder press", 18, EquipmentType.MACHINE, GripType.NEUTRAL, None),
    # Horizontal pull
    (19, "Bent-over barbell row", 19, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    (20, "Chest-supported dumbbell row", 20, EquipmentType.DUMBBELL, GripType.NEUTRAL, None),
    (21, "Seated cable row (V-bar)", 21, EquipmentType.CABLE_V_BAR, GripType.NEUTRAL, None),
    (22, "Inverted row", 22, EquipmentType.BODYWEIGHT, GripType.NEUTRAL, None),
    # Vertical pull
    (23, "Pull-up", 23, EquipmentType.BODYWEIGHT, GripType.PRONATED, None),
    (24, "Chin-up", 24, EquipmentType.BODYWEIGHT, GripType.SUPINATED, None),
    (25, "Lat pull-down (wide grip)", 25, EquipmentType.CABLE_LAT_PULLDOWN_BAR, GripType.WIDE, None),
    (26, "Assisted pull-up (machine)", 26, EquipmentType.MACHINE, GripType.NEUTRAL, None),
    # Carry
    (27, "Farmer's carry (dumbbells)", 27, EquipmentType.DUMBBELL, GripType.NEUTRAL, None),
    (28, "Suitcase carry (single dumbbell)", 28, EquipmentType.DUMBBELL, GripType.NEUTRAL, None),
    (29, "Rack carry (barbell)", 29, EquipmentType.BARBELL, GripType.NEUTRAL, None),
    # Rotation
    (30, "Cable woodchop (high to low)", 30, EquipmentType.CABLE_SINGLE_D_HANDLE, GripType.NEUTRAL, None),
    (31, "Pallof press", 31, EquipmentType.CABLE, GripType.NEUTRAL, None),
    (32, "Russian twist (medicine ball)", 32, EquipmentType.MEDICINE_BALL, GripType.NEUTRAL, None),
]

# exercise_definition_id -> [(muscle, emphasis), ...]
MUSCLE_EMPHASIS = {
    # Squats
    1: [(Muscle.QUADS, 1.0), (Muscle.GLUTES, 1.0), (Muscle.HAMSTRINGS, 0.5), (Muscle.LOWER_BACK, 0.5), (Muscle.ABS, 0.25)],
    2: [(Muscle.QUADS, 1.0), (Muscle.GLUTES, 0.75), (Muscle.ABS, 0.75), (Muscle.LOWER_BACK, 0.5), (Muscle.HAMSTRINGS, 0.25)],
    3: [(Muscle.QUADS, 1.0), (Muscle.GLUTES, 0.75), (Muscle.ABS, 0.5), (Muscle.ADDUCTORS, 0.25)],
    # Hinges
    4: [(Muscle.HAMSTRINGS, 1.0), (Muscle.GLUTES, 1.0), (Muscle.LOWER_BACK, 1.0), (Muscle.TRAPS, 0.5), (Muscle.FOREARMS, 0.5), (Muscle.ABS, 0.5)],
    5: [(Muscle.HAMSTRINGS, 1.0), (Muscle.GLUTES, 1.0), (Muscle.LOWER_BACK, 0.5), (Muscle.FOREARMS, 0.25)],
    6: [(Muscle.HAMSTRINGS, 1.0), (Muscle.GLUTES, 1.0), (Muscle.LOWER_BACK, 0.5), (Muscle.ABS, 0.5), (Muscle.FRONT_DELTS, 0.25)],
    # Lunges
    7: [(Muscle.QUADS, 1.0), (Muscle.GLUTES, 0.75), (Muscle.HAMSTRINGS, 0.5), (Muscle.CALVES, 0.25), (Muscle.ABS, 0.25)],
    8: [(Muscle.QUADS, 1.0), (Muscle.GLUTES, 0.75), (Muscle.HAMSTRINGS, 0.5), (Muscle.CALVES, 0.25)],
    9: [(Muscle.QUADS, 1.0), (Muscle.GLUTES, 1.0), (Muscle.HAMSTRINGS, 0.5), (Muscle.ABS, 0.25)],
    # Horizontal push
    10: [(Muscle.CHEST_MID, 1.0), (Muscle.TRICEPS, 0.75), (Muscle.FRONT_DELTS, 0.5), (Muscle.CHEST_UPPER, 0.25)],
    11: [(Muscle.CHEST_UPPER, 1.0), (Muscle.FRONT_DELTS, 0.75), (Muscle.TRICEPS, 0.5), (Muscle.CHEST_MID, 0.25)],
    12: [(Muscle.CHEST_LOWER, 1.0), (Muscle.TRICEPS, 0.75), (Muscle.FRONT_DELTS, 0.5), (Muscle.CHEST_MID, 0.25)],
    13: [(Muscle.CHEST_MID, 1.0), (Muscle.TRICEPS, 0.75), (Muscle.FRONT_DELTS, 0.5), (Muscle.ABS, 0.25)],
    14: [(Muscle.CHEST_MID, 1.0), (Muscle.TRICEPS, 0.75), (Muscle.FRONT_DELTS, 0.5)],
    # Vertical push
    15: [(Muscle.FRONT_DELTS, 1.0), (Muscle.TRICEPS, 0.75), (Muscle.CHEST_UPPER, 0.5), (Muscle.SIDE_DELTS, 0.25), (Muscle.ABS, 0.25)],
    16: [(Muscle.FRONT_DELTS, 1.0), (Muscle.TRICEPS, 0.75), (Muscle.GLUTES, 0.5), (Muscle.QUADS, 0.25)],
    17: [(Muscle.FRONT_DELTS, 1.0), (Muscle.SIDE_DELTS, 0.75), (Muscle.TRICEPS, 0.5), (Muscle.UPPER_TRAPS, 0.25)],
    18: [(Muscle.FRONT_DELTS, 1.0), (Muscle.SIDE_DELTS, 0.75), (Muscle.TRICEPS, 0.5)],
    # Horizontal pull
    19: [(Muscle.LATS, 1.0), (Muscle.RHOMBOIDS, 0.75), (Muscle.MID_TRAPS, 0.5), (Muscle.REAR_DELTS, 0.5), (Muscle.BICEPS, 0.5), (Muscle.LOWER_BACK, 0.5)],
    20: [(Muscle.LATS, 1.0), (Muscle.RHOMBOIDS, 0.75), (Muscle.REAR_DELTS, 0.5), (Muscle.BICEPS, 0.5)],
    21: [(Muscle.LATS, 1.0), (Muscle.RHOMBOIDS, 0.75), (Muscle.MID_TRAPS, 0.5), (Muscle.BICEPS, 0.5), (Muscle.REAR_DELTS, 0.25)],
    22: [(Muscle.LATS, 1.0), (Muscle.RHOMBOIDS, 0.75), (Muscle.REAR_DELTS, 0.5), (Muscle.BICEPS, 0.5), (Muscle.ABS, 0.25)],
    # Vertical pull
    23: [(Muscle.LATS, 1.0), (Muscle.RHOMBOIDS, 0.5), (Muscle.REAR_DELTS, 0.5), (Muscle.BICEPS, 0.5), (Muscle.FOREARMS, 0.25)],
    24: [(Muscle.LATS, 1.0), (Muscle.BICEPS, 0.75), (Muscle.RHOMBOIDS, 0.5), (Muscle.REAR_DELTS, 0.25)],
    25: [(Muscle.LATS, 1.0), (Muscle.RHOMBOIDS, 0.5), (Muscle.REAR_DELTS, 0.5), (Muscle.BICEPS, 0.5)],
    26: [(Muscle.LATS, 1.0), (Muscle.BICEPS, 0.5), (Muscle.RHOMBOIDS, 0.5), (Muscle.REAR_DELTS, 0.25)],
    # Carry
    27: [(Muscle.FOREARMS, 1.0), (Muscle.TRAPS, 0.75), (Muscle.ABS, 0.75), (Muscle.LOWER_BACK, 0.5), (Muscle.CALVES, 0.25)],
    28: [(Muscle.FOREARMS, 1.0), (Muscle.OBLIQUES, 1.0), (Muscle.ABS, 0.75), (Muscle.LOWER_BACK, 0.5)],
    29: [(Muscle.FRONT_DELTS, 0.75), (Muscle.TRAPS, 0.75), (Muscle.ABS, 0.75), (Muscle.FOREARMS, 0.5), (Muscle.LOWER_BACK, 0.5)],
    # Rotation
    30: [(Muscle.OBLIQUES, 1.0), (Muscle.ABS, 0.75), (Muscle.LATS, 0.5), (Muscle.FRONT_DELTS, 0.25)],
    31: [(Muscle.OBLIQUES, 1.0), (Muscle.ABS, 1.0), (Muscle.FRONT_DELTS, 0.5)],
    32: [(Muscle.OBLIQUES, 1.0), (Muscle.ABS, 0.75), (Muscle.HIP_FLEXORS, 0.25)],
}


def _movements() -> list[Movement]:
    return [
        Movement(id=id_, name=name, movement_pattern=pattern)
        for id_, name, pattern in MOVEMENTS
    ]


def _exercise_definitions() -> list[ExerciseDefinition]:
    return [
        ExerciseDefinition(
            id=id_,
            name=name,
            movement_id=movement_id,
            equipment_type=equipment,
            grip_type=grip,
            angle=angle,
        )
        for id_, name, movement_id, equipment, grip, angle in EXERCISE_DEFINITIONS
    ]


def _exercise_muscle_links() -> list[MuscleEmphasis]:
    return [
        MuscleEmphasis(
            exercise_definition_id=definition_id,
            muscle=muscle,
            emphasis=emphasis,
        )
        for definition_id, items in MUSCLE_EMPHASIS.items()
        for muscle, emphasis in items
    ]


def seed_domain_data(session: Session) -> None:
    """Populate reference data (movements, exercise definitions, muscle links)
    if the database is empty. Safe to call on every app startup."""
    already_seeded = session.exec(select(Movement)).first() is not None
    if already_seeded:
        return

    # Flush in FK order so movements exist before the definitions that use them.
    session.add_all(_movements())
    session.flush()
    session.add_all(_exercise_definitions())
    session.flush()
    session.add_all(_exercise_muscle_links())
    session.commit()