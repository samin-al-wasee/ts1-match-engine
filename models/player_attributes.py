from __future__ import annotations

from enum import StrEnum
from typing import Mapping


DEFAULT_ATTR: int = 50


def get_player_attr(
    bucket: Mapping[str, int] | None, key: str, default: int = DEFAULT_ATTR
) -> int:
    """
    Safe attribute getter for Player attribute dicts.

    - bucket: e.g., player.technical / player.mental / player.physical / player.hidden / player.condition
    - key: attribute key in snake_case or normal case (or str(enum_value))
    - default: used when bucket is None or key is missing (V1 default is 50)
    """
    if not bucket:
        return int(default)

    key_str = str(key).strip()
    if key_str in bucket:
        return int(bucket[key_str])

    snake_key = "_".join(key_str.lower().replace("-", " ").split())
    title_key = snake_key.replace("_", " ").title()

    if snake_key in bucket:
        return int(bucket[snake_key])
    if title_key in bucket:
        return int(bucket[title_key])

    # Backward compatibility for passing -> short_passing migration.
    if snake_key == "short_passing":
        if "passing" in bucket:
            return int(bucket["passing"])
        if "Passing" in bucket:
            return int(bucket["Passing"])
    if snake_key == "passing":
        if "short_passing" in bucket:
            return int(bucket["short_passing"])
        if "Short Passing" in bucket:
            return int(bucket["Short Passing"])

    return int(default)


class TechnicalAttr(StrEnum):
    # Ball retention and first contact
    FIRST_TOUCH = "First Touch"
    TECHNIQUE = "Technique"
    BALL_CONTROL = "Ball Control"

    # Ball carrying and 1v1 progression
    DRIBBLING = "Dribbling"
    FLAIR = "Flair"

    # Delivery and chance creation
    SHORT_PASSING = "Short Passing"
    PASSING = "Short Passing"
    CROSSING = "Crossing"
    LONG_PASSING = "Long Passing"
    SET_PIECE_DELIVERY = "Set Piece Delivery"

    # Shooting and end-product
    FINISHING = "Finishing"
    LONG_SHOTS = "Long Shots"
    SHOT_POWER = "Shot Power"
    HEADING = "Heading"
    VOLLEYS = "Volleys"
    WEAK_FOOT_ACCURACY = "Weak Foot Accuracy"

    # Defensive technique
    TACKLING = "Tackling"
    MARKING = "Marking"
    INTERCEPTING = "Intercepting"

    # Goalkeeper technique
    GK_HANDLING = "GK Handling"
    GK_REFLEXES = "GK Reflexes"
    GK_ONE_ON_ONES = "GK One On Ones"
    GK_KICKING = "GK Kicking"
    GK_COMMAND_OF_AREA = "GK Command Of Area"
    GK_AERIAL_REACH = "GK Aerial Reach"
    GK_THROWING = "GK Throwing"
    GK_POSITIONING = "GK Positioning"
    GK_COMMUNICATION = "GK Communication"


class MentalAttr(StrEnum):
    # Decision quality and game reading
    COMPOSURE = "Composure"
    DECISIONS = "Decisions"
    ANTICIPATION = "Anticipation"
    CONCENTRATION = "Concentration"

    # Creativity and attacking movement
    VISION = "Vision"
    OFF_BALL = "Off Ball"
    CREATIVITY = "Creativity"

    # Team and structure discipline
    POSITIONING = "Positioning"
    TEAMWORK = "Teamwork"
    DISCIPLINE = "Discipline"
    TACTICAL_AWARENESS = "Tactical Awareness"

    # Competitive and personality traits
    AGGRESSION = "Aggression"
    WORK_RATE = "Work Rate"
    LEADERSHIP = "Leadership"
    BRAVERY = "Bravery"
    DETERMINATION = "Determination"
    PRESS_RESISTANCE = "Press Resistance"


class PhysicalAttr(StrEnum):
    # Speed and mobility
    PACE = "Pace"
    ACCELERATION = "Acceleration"
    AGILITY = "Agility"
    BALANCE = "Balance"

    # Endurance and repeatability
    STAMINA = "Stamina"

    # Physical duels and contact
    STRENGTH = "Strength"
    JUMPING = "Jumping"
    NATURAL_FITNESS = "Natural Fitness"

    # Durability and recovery
    INJURY_RESISTANCE = "Injury Resistance"
    RECOVERY = "Recovery"


class ConditionAttr(StrEnum):
    # Match readiness
    MATCH_FITNESS = "Match Fitness"
    SHARPNESS = "Sharpness"

    # Mental and emotional state
    MORALE = "Morale"

    # Load and availability
    FATIGUE = "Fatigue"
    INJURY_RISK = "Injury Risk"

    # Behavioral stability
    DISCIPLINE = "Discipline"
    FOCUS = "Focus"


class HiddenAttr(StrEnum):
    # Reliability and pressure performance
    CONSISTENCY = "Consistency"
    BIG_MATCHES = "Big Matches"

    # Professional profile
    PROFESSIONALISM = "Professionalism"
    AMBITION = "Ambition"
    ADAPTABILITY = "Adaptability"

    # Personality and dressing-room fit
    TEMPERAMENT = "Temperament"
    LOYALTY = "Loyalty"

    # Availability and resilience tendencies
    INJURY_PRONENESS = "Injury Proneness"
    CONSISTENCY_UNDER_PRESSURE = "Consistency Under Pressure"
    VERSATILITY = "Versatility"


class Footedness(StrEnum):
    LEFT = "Left"
    RIGHT = "Right"
