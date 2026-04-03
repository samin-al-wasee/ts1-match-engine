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
    - key: snake_case attribute key (or str(enum_value))
    - default: used when bucket is None or key is missing (V1 default is 50)
    """
    if not bucket:
        return int(default)
    return int(bucket.get(str(key), default))


class TechnicalAttr(StrEnum):
    PASSING = "passing"
    FIRST_TOUCH = "first_touch"
    TECHNIQUE = "technique"
    DRIBBLING = "dribbling"
    CROSSING = "crossing"
    FINISHING = "finishing"
    HEADING = "heading"
    TACKLING = "tackling"
    MARKING = "marking"
    BALL_CONTROL = "ball_control"

    # GK
    GK_HANDLING = "gk_handling"
    GK_REFLEXES = "gk_reflexes"
    GK_ONE_ON_ONES = "gk_one_on_ones"
    GK_KICKING = "gk_kicking"
    GK_COMMAND_OF_AREA = "gk_command_of_area"


class MentalAttr(StrEnum):
    COMPOSURE = "composure"
    DECISIONS = "decisions"
    VISION = "vision"
    OFF_BALL = "off_ball"
    POSITIONING = "positioning"
    TEAMWORK = "teamwork"
    CONCENTRATION = "concentration"
    AGGRESSION = "aggression"
    WORK_RATE = "work_rate"
    LEADERSHIP = "leadership"
    ANTICIPATION = "anticipation"
    BRAVERY = "bravery"


class PhysicalAttr(StrEnum):
    PACE = "pace"
    ACCELERATION = "acceleration"
    STAMINA = "stamina"
    STRENGTH = "strength"
    AGILITY = "agility"
    BALANCE = "balance"
    JUMPING = "jumping"
    INJURY_RESISTANCE = "injury_resistance"


class ConditionAttr(StrEnum):
    MATCH_FITNESS = "match_fitness"
    SHARPNESS = "sharpness"
    MORALE = "morale"
    FATIGUE = "fatigue"
    DISCIPLINE = "discipline"


class HiddenAttr(StrEnum):
    CONSISTENCY = "consistency"
    BIG_MATCHES = "big_matches"
    PROFESSIONALISM = "professionalism"
    AMBITION = "ambition"
    TEMPERAMENT = "temperament"
    LOYALTY = "loyalty"
    ADAPTABILITY = "adaptability"
    INJURY_PRONENESS = "injury_proneness"
