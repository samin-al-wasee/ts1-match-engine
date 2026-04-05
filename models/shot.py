from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from models.chance import ChanceType


class ShotResult(StrEnum):
    SHOT = "shot"
    GOAL = "goal"


@dataclass(frozen=True)
class ShotOutcome:
    minute: int
    side: str  # "home" or "away"
    chance_type: ChanceType
    xg: float
    result: ShotResult
