from enum import StrEnum


# -------------------------
# Team Tactics: Attacking Tactics (SPEC Part 2.A)
# -------------------------
class BuildUpStyle(StrEnum):
    BUILD_FROM_BACK = "Build From Back"
    MIXED_BUILD_UP = "Mixed Build-Up"
    DIRECT_PROGRESSION = "Direct Progression"
    LONG_BALL = "Long Ball"
    COUNTER_BUILD_UP = "Counter Build-Up"


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
    WORK_BALL_INTO_BOX = "Work Ball Into Box"
    MIXED_ATTACKING = "Mixed Attacking"
    SHOOT_ON_SIGHT = "Shoot On Sight"
    CROSS_EARLY = "Cross Early"
    OVERLAP_WIDE = "Overlap Wide"
    UNDERLAP_INSIDE = "Underlap Inside"
    THROUGH_BALL_FOCUS = "Through Ball Focus"
    DRIBBLE_MORE = "Dribble More"
    HOLD_POSSESSION = "Hold Possession"


class AttackingFocus(StrEnum):
    ATTACK_LEFT = "Attack Left"
    ATTACK_RIGHT = "Attack Right"
    ATTACK_CENTRE = "Attack Centre"
    MIXED = "Mixed"
    SWITCH_FLANKS_OFTEN = "Switch Flanks Often"
    TARGET_HALF_SPACES = "Target Half-Spaces"


# -------------------------
# Team Tactics: Defensive Tactics (SPEC Part 2.B)
# -------------------------
class DefensiveLine(StrEnum):
    VERY_DEEP = "Very Deep"
    DEEP = "Deep"
    STANDARD = "Standard"
    HIGH = "High"
    VERY_HIGH = "Very High"


class LineOfEngagement(StrEnum):
    LOW_BLOCK = "Low Block"
    MID_BLOCK = "Mid Block"
    HIGH_BLOCK = "High Block"
    FULL_PRESS = "Full Press"


class PressingIntensity(StrEnum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    BALANCED = "Balanced"
    HIGH = "High"
    EXTREME = "Extreme"


class DefensiveWidth(StrEnum):
    VERY_NARROW = "Very Narrow"
    NARROW = "Narrow"
    BALANCED = "Balanced"
    WIDE = "Wide"
    VERY_WIDE = "Very Wide"


class MarkingStyle(StrEnum):
    ZONAL = "Zonal"
    MIXED = "Mixed"
    TIGHT_MAN_ORIENTED = "Tight Man-Oriented"


class TacklingAggression(StrEnum):
    STAY_ON_FEET = "Stay On Feet"
    BALANCED = "Balanced"
    AGGRESSIVE = "Aggressive"
    VERY_AGGRESSIVE = "Very Aggressive"


# -------------------------
# Team Tactics: Transition Tactics (SPEC Part 2.C)
# -------------------------
class TransitionOnWin(StrEnum):
    COUNTER_IMMEDIATELY = "Counter Immediately"
    PROGRESS_SAFELY = "Progress Safely"
    HOLD_SHAPE = "Hold Shape"
    FEED_PLAYMAKER = "Feed Playmaker"
    FEED_WINGER = "Feed Winger"
    GO_LONG_TO_STRIKER = "Go Long To Striker"
    ATTACK_WEAK_SIDE = "Attack Weak Side"


class TransitionOnLoss(StrEnum):
    COUNTERPRESS = "Counterpress"
    DELAY = "Delay"
    REGROUP = "Regroup"
    TACTICAL_FOUL = "Tactical Foul"
    DROP_DEEP_IMMEDIATELY = "Drop Deep Immediately"


# -------------------------
# Team Tactics: Mentality / Match Approach (SPEC Part 2.D)
# -------------------------
class TeamMentality(StrEnum):
    VERY_DEFENSIVE = "Very Defensive"
    DEFENSIVE = "Defensive"
    CAUTIOUS = "Cautious"
    BALANCED = "Balanced"
    POSITIVE = "Positive"
    ATTACKING = "Attacking"
    VERY_ATTACKING = "Very Attacking"


# -------------------------
# Team Tactics: Risk Management (SPEC Part 2.E)
# -------------------------
class PassingRisk(StrEnum):
    VERY_SAFE = "Very Safe"
    SAFE = "Safe"
    BALANCED = "Balanced"
    RISKY = "Risky"
    VERY_RISKY = "Very Risky"


class DribblingRisk(StrEnum):
    VERY_CONSERVATIVE = "Very Conservative"
    BALANCED = "Balanced"
    AGGRESSIVE = "Aggressive"


class ShootingPolicy(StrEnum):
    SHOOT_LESS = "Shoot Less"
    BALANCED = "Balanced"
    SHOOT_MORE = "Shoot More"
    SHOOT_AGGRESSIVELY = "Shoot Aggressively"


# -------------------------
# Team Tactics: Space Control (SPEC Part 2.F)
# -------------------------
class Compactness(StrEnum):
    VERY_COMPACT = "Very Compact"
    COMPACT = "Compact"
    BALANCED = "Balanced"
    LOOSE = "Loose"
    VERY_LOOSE = "Very Loose"


class VerticalStretch(StrEnum):
    COMPRESSED = "Compressed"
    BALANCED = "Balanced"
    STRETCHED = "Stretched"


class OverloadFocus(StrEnum):
    LEFT_OVERLOAD = "Left overload"
    RIGHT_OVERLOAD = "Right overload"
    CENTRAL_OVERLOAD = "Central overload"
    NO_SPECIFIC_OVERLOAD = "No specific overload"


# -------------------------
# Set Piece Control System (SPEC Part 5)
# -------------------------
class SetPieceAttack(StrEnum):
    NEAR_POST_CORNERS = "Near-post corners"
    FAR_POST_CORNERS = "Far-post corners"
    MIXED_CORNERS = "Mixed corners"
    SHORT_CORNERS = "Short corners"
    CROWD_GOALKEEPER = "Crowd goalkeeper"
    EDGE_OF_BOX_SETUP = "Edge-of-box setup"
    TALL_PLAYER_TARGETING = "Tall-player targeting"
    REBOUND_HUNTING = "Rebound hunting"


class SetPieceDefense(StrEnum):
    ZONAL_MARKING = "Zonal marking"
    MIXED_MARKING = "Mixed marking"
    MAN_MARKING = "Man marking"
    LEAVE_PLAYERS_UP = "Leave players up"
    FULL_RETREAT = "Full retreat"
    COUNTER_SETUP = "Counter setup"
    NEAR_POST_GUARD = "Near-post guard"


class FreeKickStrategy(StrEnum):
    SHOOT_DIRECT = "Shoot direct"
    CROSS_INTO_BOX = "Cross into box"
    SHORT_ROUTINE = "Short routine"
    FAST_RESTART = "Fast restart"
