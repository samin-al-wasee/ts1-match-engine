from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PhaseEventType(StrEnum):
    PASS = "pass"
    TURNOVER = "turnover"
    SHOT = "shot"
    GOAL = "goal"


@dataclass(frozen=True)
class MinuteOutcome:
    """
    V1: minimal minute resolution output.
    """

    minute: int
    possessing_side: str  # "home" or "away"
    event_type: PhaseEventType
    xg: float = 0.0  # only meaningful for shots/goals
    description: str = ""
