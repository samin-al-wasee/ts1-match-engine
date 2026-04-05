from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ScoreState(StrEnum):
    LEADING = "leading"
    DRAWING = "drawing"
    TRAILING = "trailing"


@dataclass
class TeamMatchState:
    """
    Team-specific dynamic match context (Layer 4).
    Values should be lightweight, updated every minute/event.
    """

    goals_for: int = 0
    goals_against: int = 0

    # 0..1 (consumer clamps)
    momentum: float = 0.50  # confidence / flow; 0=bad, 1=great
    urgency: float = 0.50  # willingness to force play; 0=slow it, 1=push hard
    discipline: float = 0.70  # foul/card risk control; 0=chaotic, 1=disciplined
    fatigue: float = 0.00  # 0=fresh, 1=exhausted

    def goal_diff(self) -> int:
        return self.goals_for - self.goals_against

    def score_state(self) -> ScoreState:
        gd = self.goal_diff()
        if gd > 0:
            return ScoreState.LEADING
        if gd < 0:
            return ScoreState.TRAILING
        return ScoreState.DRAWING


@dataclass
class MatchState:
    """
    Global match context (Layer 4).
    """

    minute: int = 0
    max_minutes: int = 90

    home: TeamMatchState = TeamMatchState()
    away: TeamMatchState = TeamMatchState()

    def is_late_game(self) -> bool:
        return self.minute >= int(self.max_minutes * 0.75)
