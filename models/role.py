from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    """
    V1 player roles (flat list). Names match docs exactly.
    """

    SHOT_STOPPER = "Shot Stopper"
    SWEEPER_KEEPER = "Sweeper Keeper"

    FULL_BACK = "Full Back"
    WING_BACK = "Wing Back"
    INVERTED_FULL_BACK = "Inverted Full Back"
    DEFENSIVE_FULL_BACK = "Defensive Full Back"

    CENTRAL_DEFENDER = "Central Defender"
    STOPPER = "Stopper"
    BALL_PLAYING_DEFENDER = "Ball Playing Defender"
    WIDE_BACK = "Wide Back"

    ANCHOR_HOLDING_MIDFIELDER = "Anchor / Holding Midfielder"
    BALL_WINNING_MIDFIELDER = "Ball-Winning Midfielder"
    DEEP_LYING_PLAYMAKER_REGISTA = "Deep-Lying Playmaker (Regista)"
    HALF_BACK = "Half Back"

    BOX_TO_BOX_MIDFIELDER = "Box-to-Box Midfielder"
    MEZZALA_ADVANCED_WIDE_MIDFIELDER = "Mezzala (Advanced Wide Midfielder)"
    CARRILERO_SHUTTLING_MIDFIELDER = "Carrilero (Shuttling Midfielder)"
    BOX_CRASHER = "Box Crasher"

    SHADOW_STRIKER = "Shadow Striker"
    TREQUARTISTA_PLAYMAKER_FREE_ATTACKING_MIDFIELDER = (
        "Trequartista (Playmaker / Free Attacking Midfielder)"
    )
    ENGANCHE_HOOK_CLASSIC_NUMBER_10 = "Enganche (Hook / Classic Number 10)"
    HALF_WINGER_WIDE_AM = "Half Winger / Wide AM"

    WINGER = "Winger"
    INVERTED_WINGER = "Inverted Winger"
    WIDE_PLAYMAKER = "Wide Playmaker"
    DEFENSIVE_WINGER = "Defensive Winger"

    TARGET_MAN = "Target Man"
    POACHER = "Poacher"
    SECONDARY_STRIKER = "Secondary Striker"
    ADVANCED_FORWARD = "Advanced Forward"
    FALSE_NINE = "False Nine"
