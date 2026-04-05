from __future__ import annotations

from enum import StrEnum


class ChanceType(StrEnum):
    THROUGH_BALL = "through_ball"
    CROSS = "cross"
    CUTBACK = "cutback"
    DRIBBLE = "dribble"
    LONG_SHOT = "long_shot"
