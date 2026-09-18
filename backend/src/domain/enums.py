from enum import Enum

# Movement patterns
class MovementPattern(str, Enum):
    HORIZONTAL_PUSH = "horizontal_push"
    VERTICAL_PUSH = "vertical_push"
    HORIZONTAL_PULL = "horizontal_pull"
    VERTICAL_PULL = "vertical_pull"
    SQUAT = "squat"
    HINGE = "hinge"
    LUNGE = "lunge"
    CARRY = "carry"
    ROTATION = "rotation"

# Grip type
class GripType(str, Enum):
    PRONATED = "pronated"
    SUPINATED = "supinated"
    NEUTRAL = "neutral"
    CLOSE = "close"
    WIDE = "wide"

# Angle type
class AngleType(str, Enum):
    FLAT = "flat"
    INCLINE = "incline"
    DECLINE = "decline"

# Muscle groups (more detailed)
class Muscle(str, Enum):
    CHEST_UPPER = "chest_upper"
    CHEST_MID = "chest_mid"
    CHEST_LOWER = "chest_lower"
    FRONT_DELTS = "front_delts"
    SIDE_DELTS = "side_delts"
    REAR_DELTS = "rear_delts"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    FOREARMS = "forearms"
    LATS = "lats"
    RHOMBOIDS = "rhomboids"
    TRAPS = "traps"
    UPPER_TRAPS = "upper_traps"
    MID_TRAPS = "mid_traps"
    QUADS = "quads"
    HAMSTRINGS = "hamstrings"
    GLUTES = "glutes"
    CALVES = "calves"
    ABS = "abs"
    OBLIQUES = "obliques"
    LOWER_BACK = "lower_back"
    HIP_FLEXORS = "hip_flexors"
    ADDUCTORS = "adductors"
    ABDUCTORS = "abductors"

# Equipment
class EquipmentType(str, Enum):
    BARBELL = "barbell"
    DUMBBELL = "dumbbell"
    Z_BAR = "z-bar"
    SMITH_MACHINE = "smith_machine"
    MACHINE = "machine"
    CABLE = "cable"
    BODYWEIGHT = "bodyweight"
    KETTLEBELL = "kettlebell"
    RESISTANCE_BAND = "resistance_band"
    MEDICINE_BALL = "medicine_ball"
    BOSU = "bosu"
    TRX = "trx"
    CABLE_STRAIGHT_BAR = "cable_straight_bar"
    STRAIGHT_BAR = "straight_bar"
    CABLE_Z_BAR = "cable_z_bar"
    CABLE_ROPE_ATTACHMENT = "cable_rope_attachment"
    ROPE_ATTACHMENT = "rope_attachment"
    CABLE_V_BAR = "cable_v_bar"
    V_BAR = "v_bar"
    CABLE_SINGLE_D_HANDLE = "cable_single_d_handle"
    SINGLE_D_HANDLE = "single_d_handle"
    CABLE_DOUBLE_D_HANDLE = "cable_double_d_handle"
    DOUBLE_D_HANDLE = "double_d_handle"
    CABLE_LAT_PULLDOWN_BAR = "cable_lat_pulldown_bar"