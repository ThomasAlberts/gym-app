from sqlmodel import Session, select

from backend.src.domain.movement import Movement
from backend.src.domain.exercise_definition import ExerciseDefinition
from backend.src.domain.exercise_muscle_link import ExerciseMuscleLink
from backend.src.domain.enums import (
    MovementPattern,
    AngleType,
    GripType,
    EquipmentType,
    Muscle,
)


def _movements():
    return [
        # Squat pattern
        Movement(id=1, name="Back squat", movement_pattern=MovementPattern.SQUAT),
        Movement(id=2, name="Front squat", movement_pattern=MovementPattern.SQUAT),
        Movement(id=3, name="Goblet squat", movement_pattern=MovementPattern.SQUAT),

        # Hinge pattern
        Movement(id=4, name="Conventional deadlift", movement_pattern=MovementPattern.HINGE),
        Movement(id=5, name="Romanian deadlift", movement_pattern=MovementPattern.HINGE),
        Movement(id=6, name="Kettlebell swing", movement_pattern=MovementPattern.HINGE),

        # Lunge pattern
        Movement(id=7, name="Walking lunge", movement_pattern=MovementPattern.LUNGE),
        Movement(id=8, name="Reverse lunge", movement_pattern=MovementPattern.LUNGE),
        Movement(id=9, name="Bulgarian split squat", movement_pattern=MovementPattern.LUNGE),

        # Horizontal push
        Movement(id=10, name="Bench press", movement_pattern=MovementPattern.HORIZONTAL_PUSH),
        Movement(id=11, name="Incline bench press", movement_pattern=MovementPattern.HORIZONTAL_PUSH),
        Movement(id=12, name="Decline bench press", movement_pattern=MovementPattern.HORIZONTAL_PUSH),
        Movement(id=13, name="Push-up", movement_pattern=MovementPattern.HORIZONTAL_PUSH),
        Movement(id=14, name="Dumbbell floor press", movement_pattern=MovementPattern.HORIZONTAL_PUSH),

        # Vertical push
        Movement(id=15, name="Overhead press (strict press)", movement_pattern=MovementPattern.VERTICAL_PUSH),
        Movement(id=16, name="Push press", movement_pattern=MovementPattern.VERTICAL_PUSH),
        Movement(id=17, name="Seated dumbbell shoulder press", movement_pattern=MovementPattern.VERTICAL_PUSH),
        Movement(id=18, name="Machine shoulder press", movement_pattern=MovementPattern.VERTICAL_PUSH),

        # Horizontal pull
        Movement(id=19, name="Bent-over barbell row", movement_pattern=MovementPattern.HORIZONTAL_PULL),
        Movement(id=20, name="Chest-supported row", movement_pattern=MovementPattern.HORIZONTAL_PULL),
        Movement(id=21, name="Seated cable row", movement_pattern=MovementPattern.HORIZONTAL_PULL),
        Movement(id=22, name="Inverted row (TRX/bar)", movement_pattern=MovementPattern.HORIZONTAL_PULL),

        # Vertical pull
        Movement(id=23, name="Pull-up", movement_pattern=MovementPattern.VERTICAL_PULL),
        Movement(id=24, name="Chin-up", movement_pattern=MovementPattern.VERTICAL_PULL),
        Movement(id=25, name="Lat pull-down", movement_pattern=MovementPattern.VERTICAL_PULL),
        Movement(id=26, name="Assisted pull-up", movement_pattern=MovementPattern.VERTICAL_PULL),

        # Carry
        Movement(id=27, name="Farmer's carry", movement_pattern=MovementPattern.CARRY),
        Movement(id=28, name="Suitcase carry", movement_pattern=MovementPattern.CARRY),
        Movement(id=29, name="Rack carry", movement_pattern=MovementPattern.CARRY),

        # Rotation / anti-rotation
        Movement(id=30, name="Cable woodchop", movement_pattern=MovementPattern.ROTATION),
        Movement(id=31, name="Pallof press", movement_pattern=MovementPattern.ROTATION),
        Movement(id=32, name="Russian twist", movement_pattern=MovementPattern.ROTATION),
    ]


def _exercise_definitions():
    return [
        # Squats
        ExerciseDefinition(
            id=1,
            name="Barbell back squat",
            movement_id=1,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=2,
            name="Barbell front squat",
            movement_id=2,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=3,
            name="Goblet squat",
            movement_id=3,
            equipment_type=EquipmentType.KETTLEBELL,
            grip_type=GripType.NEUTRAL,
        ),

        # Hinges
        ExerciseDefinition(
            id=4,
            name="Conventional deadlift",
            movement_id=4,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=5,
            name="Romanian deadlift",
            movement_id=5,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=6,
            name="Kettlebell swing",
            movement_id=6,
            equipment_type=EquipmentType.KETTLEBELL,
            grip_type=GripType.NEUTRAL,
        ),

        # Lunges
        ExerciseDefinition(
            id=7,
            name="Walking dumbbell lunge",
            movement_id=7,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=8,
            name="Reverse dumbbell lunge",
            movement_id=8,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=9,
            name="Bulgarian split squat (dumbbells)",
            movement_id=9,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
        ),

        # Horizontal push
        ExerciseDefinition(
            id=10,
            name="Barbell bench press",
            movement_id=10,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
            angle=AngleType.FLAT,
        ),
        ExerciseDefinition(
            id=11,
            name="Barbell incline bench press",
            movement_id=11,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
            angle=AngleType.INCLINE,
        ),
        ExerciseDefinition(
            id=12,
            name="Barbell decline bench press",
            movement_id=12,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
            angle=AngleType.DECLINE,
        ),
        ExerciseDefinition(
            id=13,
            name="Push-up",
            movement_id=13,
            equipment_type=EquipmentType.BODYWEIGHT,
            grip_type=GripType.NEUTRAL,
            angle=AngleType.FLAT,
        ),
        ExerciseDefinition(
            id=14,
            name="Dumbbell floor press",
            movement_id=14,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
            angle=AngleType.FLAT,
        ),

        # Vertical push
        ExerciseDefinition(
            id=15,
            name="Barbell overhead press",
            movement_id=15,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=16,
            name="Push press",
            movement_id=16,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=17,
            name="Seated dumbbell shoulder press",
            movement_id=17,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=18,
            name="Machine shoulder press",
            movement_id=18,
            equipment_type=EquipmentType.MACHINE,
            grip_type=GripType.NEUTRAL,
        ),

        # Horizontal pull
        ExerciseDefinition(
            id=19,
            name="Bent-over barbell row",
            movement_id=19,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=20,
            name="Chest-supported dumbbell row",
            movement_id=20,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=21,
            name="Seated cable row (V-bar)",
            movement_id=21,
            equipment_type=EquipmentType.CABLE_V_BAR,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=22,
            name="Inverted row",
            movement_id=22,
            equipment_type=EquipmentType.BODYWEIGHT,
            grip_type=GripType.NEUTRAL,
        ),

        # Vertical pull
        ExerciseDefinition(
            id=23,
            name="Pull-up",
            movement_id=23,
            equipment_type=EquipmentType.BODYWEIGHT,
            grip_type=GripType.PRONATED,
        ),
        ExerciseDefinition(
            id=24,
            name="Chin-up",
            movement_id=24,
            equipment_type=EquipmentType.BODYWEIGHT,
            grip_type=GripType.SUPINATED,
        ),
        ExerciseDefinition(
            id=25,
            name="Lat pull-down (wide grip)",
            movement_id=25,
            equipment_type=EquipmentType.CABLE_LAT_PULLDOWN_BAR,
            grip_type=GripType.WIDE,
        ),
        ExerciseDefinition(
            id=26,
            name="Assisted pull-up (machine)",
            movement_id=26,
            equipment_type=EquipmentType.MACHINE,
            grip_type=GripType.NEUTRAL,
        ),

        # Carry
        ExerciseDefinition(
            id=27,
            name="Farmer's carry (dumbbells)",
            movement_id=27,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=28,
            name="Suitcase carry (single dumbbell)",
            movement_id=28,
            equipment_type=EquipmentType.DUMBBELL,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=29,
            name="Rack carry (barbell)",
            movement_id=29,
            equipment_type=EquipmentType.BARBELL,
            grip_type=GripType.NEUTRAL,
        ),

        # Rotation
        ExerciseDefinition(
            id=30,
            name="Cable woodchop (high to low)",
            movement_id=30,
            equipment_type=EquipmentType.CABLE_SINGLE_D_HANDLE,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=31,
            name="Pallof press",
            movement_id=31,
            equipment_type=EquipmentType.CABLE,
            grip_type=GripType.NEUTRAL,
        ),
        ExerciseDefinition(
            id=32,
            name="Russian twist (medicine ball)",
            movement_id=32,
            equipment_type=EquipmentType.MEDICINE_BALL,
            grip_type=GripType.NEUTRAL,
        ),
    ]


def _exercise_muscle_links():
    links = []

    # ---------- Squats ----------
    # Back squat
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.QUADS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.GLUTES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.HAMSTRINGS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.LOWER_BACK, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=1, muscle=Muscle.ABS, emphasis=0.25),
    ])

    # Front squat (more quad-dominant, still heavy glutes/core)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.QUADS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.GLUTES, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.ABS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.LOWER_BACK, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=2, muscle=Muscle.HAMSTRINGS, emphasis=0.25),
    ])

    # Goblet squat
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.QUADS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.GLUTES, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.ABS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=3, muscle=Muscle.ADDUCTORS, emphasis=0.25),  # if you add ADDUCTORS enum
    ])

    # ---------- Hinges ----------
    # Conventional deadlift
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.HAMSTRINGS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.GLUTES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.LOWER_BACK, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.TRAPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.FOREARMS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=4, muscle=Muscle.ABS, emphasis=0.5),
    ])

    # Romanian deadlift
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.HAMSTRINGS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.GLUTES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.LOWER_BACK, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=5, muscle=Muscle.FOREARMS, emphasis=0.25),
    ])

    # Kettlebell swing
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=6, muscle=Muscle.HAMSTRINGS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=6, muscle=Muscle.GLUTES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=6, muscle=Muscle.LOWER_BACK, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=6, muscle=Muscle.ABS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=6, muscle=Muscle.FRONT_DELTS, emphasis=0.25),
    ])

    # ---------- Lunges ----------
    # Walking lunge
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=7, muscle=Muscle.QUADS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=7, muscle=Muscle.GLUTES, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=7, muscle=Muscle.HAMSTRINGS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=7, muscle=Muscle.CALVES, emphasis=0.25),
        ExerciseMuscleLink(exercise_definition_id=7, muscle=Muscle.ABS, emphasis=0.25),
    ])

    # Reverse lunge
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=8, muscle=Muscle.QUADS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=8, muscle=Muscle.GLUTES, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=8, muscle=Muscle.HAMSTRINGS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=8, muscle=Muscle.CALVES, emphasis=0.25),
    ])

    # Bulgarian split squat
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=9, muscle=Muscle.QUADS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=9, muscle=Muscle.GLUTES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=9, muscle=Muscle.HAMSTRINGS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=9, muscle=Muscle.ABS, emphasis=0.25),
    ])

    # ---------- Horizontal push ----------
    # Barbell bench press (flat)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=10, muscle=Muscle.CHEST_MID, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=10, muscle=Muscle.TRICEPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=10, muscle=Muscle.FRONT_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=10, muscle=Muscle.CHEST_UPPER, emphasis=0.25),
    ])

    # Incline bench press
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=11, muscle=Muscle.CHEST_UPPER, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=11, muscle=Muscle.FRONT_DELTS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=11, muscle=Muscle.TRICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=11, muscle=Muscle.CHEST_MID, emphasis=0.25),
    ])

    # Decline bench press
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=12, muscle=Muscle.CHEST_LOWER, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=12, muscle=Muscle.TRICEPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=12, muscle=Muscle.FRONT_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=12, muscle=Muscle.CHEST_MID, emphasis=0.25),
    ])

    # Push-up
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=13, muscle=Muscle.CHEST_MID, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=13, muscle=Muscle.TRICEPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=13, muscle=Muscle.FRONT_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=13, muscle=Muscle.ABS, emphasis=0.25),
    ])

    # Dumbbell floor press
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=14, muscle=Muscle.CHEST_MID, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=14, muscle=Muscle.TRICEPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=14, muscle=Muscle.FRONT_DELTS, emphasis=0.5),
    ])

    # ---------- Vertical push ----------
    # Barbell overhead press
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=15, muscle=Muscle.FRONT_DELTS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=15, muscle=Muscle.TRICEPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=15, muscle=Muscle.CHEST_UPPER, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=15, muscle=Muscle.SIDE_DELTS, emphasis=0.25),
        ExerciseMuscleLink(exercise_definition_id=15, muscle=Muscle.ABS, emphasis=0.25),
    ])

    # Push press
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=16, muscle=Muscle.FRONT_DELTS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=16, muscle=Muscle.TRICEPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=16, muscle=Muscle.GLUTES, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=16, muscle=Muscle.QUADS, emphasis=0.25),
    ])

    # Seated dumbbell shoulder press
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=17, muscle=Muscle.FRONT_DELTS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=17, muscle=Muscle.SIDE_DELTS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=17, muscle=Muscle.TRICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=17, muscle=Muscle.UPPER_TRAPS, emphasis=0.25),  # if you add UPPER_TRAPS
    ])

    # Machine shoulder press
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=18, muscle=Muscle.FRONT_DELTS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=18, muscle=Muscle.SIDE_DELTS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=18, muscle=Muscle.TRICEPS, emphasis=0.5),
    ])

    # ---------- Horizontal pull ----------
    # Bent-over barbell row
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=19, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=19, muscle=Muscle.RHOMBOIDS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=19, muscle=Muscle.MID_TRAPS, emphasis=0.5),  # or TRAPS
        ExerciseMuscleLink(exercise_definition_id=19, muscle=Muscle.REAR_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=19, muscle=Muscle.BICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=19, muscle=Muscle.LOWER_BACK, emphasis=0.5),
    ])

    # Chest-supported dumbbell row
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=20, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=20, muscle=Muscle.RHOMBOIDS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=20, muscle=Muscle.REAR_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=20, muscle=Muscle.BICEPS, emphasis=0.5),
    ])

    # Seated cable row (V-bar)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=21, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=21, muscle=Muscle.RHOMBOIDS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=21, muscle=Muscle.MID_TRAPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=21, muscle=Muscle.BICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=21, muscle=Muscle.REAR_DELTS, emphasis=0.25),
    ])

    # Inverted row
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=22, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=22, muscle=Muscle.RHOMBOIDS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=22, muscle=Muscle.REAR_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=22, muscle=Muscle.BICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=22, muscle=Muscle.ABS, emphasis=0.25),
    ])

    # ---------- Vertical pull ----------
    # Pull-up (pronated)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=23, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=23, muscle=Muscle.RHOMBOIDS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=23, muscle=Muscle.REAR_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=23, muscle=Muscle.BICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=23, muscle=Muscle.FOREARMS, emphasis=0.25),
    ])

    # Chin-up (supinated, more biceps)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=24, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=24, muscle=Muscle.BICEPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=24, muscle=Muscle.RHOMBOIDS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=24, muscle=Muscle.REAR_DELTS, emphasis=0.25),
    ])

    # Lat pull-down (wide grip)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=25, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=25, muscle=Muscle.RHOMBOIDS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=25, muscle=Muscle.REAR_DELTS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=25, muscle=Muscle.BICEPS, emphasis=0.5),
    ])

    # Assisted pull-up
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=26, muscle=Muscle.LATS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=26, muscle=Muscle.BICEPS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=26, muscle=Muscle.RHOMBOIDS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=26, muscle=Muscle.REAR_DELTS, emphasis=0.25),
    ])

    # ---------- Carry ----------
    # Farmer's carry
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=27, muscle=Muscle.FOREARMS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=27, muscle=Muscle.TRAPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=27, muscle=Muscle.ABS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=27, muscle=Muscle.LOWER_BACK, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=27, muscle=Muscle.CALVES, emphasis=0.25),
    ])

    # Suitcase carry (anti-lateral flexion, obliques)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=28, muscle=Muscle.FOREARMS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=28, muscle=Muscle.OBLIQUES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=28, muscle=Muscle.ABS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=28, muscle=Muscle.LOWER_BACK, emphasis=0.5),
    ])

    # Rack carry (front rack, more upper back)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=29, muscle=Muscle.FRONT_DELTS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=29, muscle=Muscle.TRAPS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=29, muscle=Muscle.ABS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=29, muscle=Muscle.FOREARMS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=29, muscle=Muscle.LOWER_BACK, emphasis=0.5),
    ])

    # ---------- Rotation ----------
    # Cable woodchop
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=30, muscle=Muscle.OBLIQUES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=30, muscle=Muscle.ABS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=30, muscle=Muscle.LATS, emphasis=0.5),
        ExerciseMuscleLink(exercise_definition_id=30, muscle=Muscle.FRONT_DELTS, emphasis=0.25),
    ])

    # Pallof press (anti-rotation)
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=31, muscle=Muscle.OBLIQUES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=31, muscle=Muscle.ABS, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=31, muscle=Muscle.FRONT_DELTS, emphasis=0.5),
    ])

    # Russian twist
    links.extend([
        ExerciseMuscleLink(exercise_definition_id=32, muscle=Muscle.OBLIQUES, emphasis=1.0),
        ExerciseMuscleLink(exercise_definition_id=32, muscle=Muscle.ABS, emphasis=0.75),
        ExerciseMuscleLink(exercise_definition_id=32, muscle=Muscle.HIP_FLEXORS, emphasis=0.25),  # if you add HIP_FLEXORS
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