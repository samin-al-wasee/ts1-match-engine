from enum import StrEnum


# -------------------------
# Core identity
# -------------------------
class Mentality(StrEnum):
    ULTRA_DEFENSIVE = "Ultra Defensive"
    DEFENSIVE = "Defensive"
    BALANCED = "Balanced"
    ATTACKING = "Attacking"
    ULTRA_ATTACKING = "Ultra Attacking"


class BuildUpStyle(StrEnum):
    BUILD_FROM_BACK = "Build From Back"
    MIXED_BUILD_UP = "Mixed Build Up"
    DIRECT_BUILD_UP = "Direct Build Up"
    LONG_BALL = "Long Ball"


class Tempo(StrEnum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    BALANCED = "Balanced"
    HIGH = "High"
    VERY_HIGH = "Very High"


class Width(StrEnum):
    VERY_NARROW = "Very Narrow"
    NARROW = "Narrow"
    BALANCED = "Balanced"
    WIDE = "Wide"
    VERY_WIDE = "Very Wide"


class FinalThirdFocus(StrEnum):
    THROUGH_BALL_FOCUS = "Through Ball Focus"
    CROSSING_FOCUS = "Crossing Focus"
    CUTBACK_FOCUS = "Cutback Focus"
    DRIBBLE_FOCUS = "Dribble Focus"
    SHOOTING_FOCUS = "Shooting Focus"
    MIXED = "Mixed"


class PassingDirectness(StrEnum):
    VERY_SHORT = "Very Short"
    SHORT = "Short"
    MIXED = "Mixed"
    DIRECT = "Direct"
    VERY_DIRECT = "Very Direct"


class ChanceCreationStyle(StrEnum):
    PATIENT_COMBINATIONS = "Patient Combinations"
    FAST_VERTICAL = "Fast Vertical"
    WIDE_OVERLOADS = "Wide Overloads"
    ISOLATIONS_1V1 = "Isolations 1v1"
    SECOND_BALLS = "Second Balls"
    MIXED = "Mixed"


class CrossingStyle(StrEnum):
    EARLY_CROSSES = "Early Crosses"
    MIXED_CROSSES = "Mixed Crosses"
    BYLINE_CUTBACKS = "Byline Cutbacks"


class ShootingTendency(StrEnum):
    WORK_BALL_INTO_BOX = "Work Ball Into Box"
    MIXED_SHOOTING = "Mixed Shooting"
    SHOOT_ON_SIGHT = "Shoot On Sight"


class DribblingTendency(StrEnum):
    RARELY = "Rarely"
    SITUATIONAL = "Situational"
    OFTEN = "Often"


# -------------------------
# Out of possession
# -------------------------
class DefensiveLine(StrEnum):
    VERY_DEEP = "Very Deep"
    DEEP = "Deep"
    STANDARD = "Standard"
    HIGH = "High"
    VERY_HIGH = "Very High"


class PressingIntensity(StrEnum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    STANDARD = "Standard"
    HIGH = "High"
    VERY_HIGH = "Very High"


class PressTrigger(StrEnum):
    RARE = "Rare"
    STANDARD = "Standard"
    AGGRESSIVE = "Aggressive"
    CONSTANT = "Constant"


class DefensiveWidth(StrEnum):
    VERY_NARROW = "Very Narrow"
    NARROW = "Narrow"
    STANDARD = "Standard"
    WIDE = "Wide"
    VERY_WIDE = "Very Wide"


class LineCompactness(StrEnum):
    VERY_LOOSE = "Very Loose"
    LOOSE = "Loose"
    STANDARD = "Standard"
    COMPACT = "Compact"
    VERY_COMPACT = "Very Compact"


class MarkingStyle(StrEnum):
    ZONAL = "Zonal"
    MIXED = "Mixed"
    MAN = "Man"


class TacklingStyle(StrEnum):
    CAUTIOUS = "Cautious"
    NORMAL = "Normal"
    AGGRESSIVE = "Aggressive"


# -------------------------
# Transitions
# -------------------------
class TransitionOnWin(StrEnum):
    COUNTER_IMMEDIATELY = "Counter Immediately"
    COUNTER_IF_ON = "Counter If On"
    HOLD_POSSESSION = "Hold Possession"
    RESET_SHAPE = "Reset Shape"


class TransitionOnLoss(StrEnum):
    COUNTERPRESS = "Counterpress"
    COUNTERPRESS_IF_ON = "Counterpress If On"
    REGROUP = "Regroup"
    FALL_BACK = "Fall Back"


class CounterSpeed(StrEnum):
    SLOW = "Slow"
    NORMAL = "Normal"
    FAST = "Fast"
    VERY_FAST = "Very Fast"


# -------------------------
# Set pieces
# -------------------------
class SetPieceAttackingStyle(StrEnum):
    SHORT_ROUTINES = "Short Routines"
    MIXED_ROUTINES = "Mixed Routines"
    DELIVERY_TO_BOX = "Delivery To Box"


class SetPieceDefensiveStyle(StrEnum):
    ZONAL = "Zonal"
    MIXED = "Mixed"
    MAN = "Man"
