from dataclasses import dataclass, field
from typing import List


@dataclass
class MatchState:
    minute: int = 0
    home_score: int = 0
    away_score: int = 0

    home_momentum: float = 0.0
    away_momentum: float = 0.0

    possession_side: str = "neutral"
    visible_events: List[str] = field(default_factory=list)

    def scoreline(self) -> str:
        return f"{self.home_score} - {self.away_score}"

    def add_event(self, event: str) -> None:
        self.visible_events.append(event)
