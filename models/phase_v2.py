from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from models.chance import ChanceType
from models.shot import ShotResult


class InitiativeResult(StrEnum):
    HOME = "home"
    AWAY = "away"


class Route(StrEnum):
    LEFT = "left"
    CENTRAL = "central"
    RIGHT = "right"


class ProgressionResult(StrEnum):
    ADVANCE = "advance"
    STALLED = "stalled"
    TURNOVER = "turnover"


@dataclass(frozen=True)
class PhaseFrame:
    minute: int
    initiative: InitiativeResult
    route: Route
    progression: ProgressionResult

    # Step 4 (only meaningful when progression == ADVANCE)
    chance_type: Optional[ChanceType] = None
    chance_type_weights: Optional[dict[str, float]] = None

    initiative_p_home: float = 0.5
    route_weights: dict[str, float] = None  # type: ignore
    progression_p_advance: float = 0.0
    progression_p_turnover: float = 0.0

    xg: Optional[float] = None
    shot_result: Optional[ShotResult] = None
