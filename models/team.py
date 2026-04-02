from dataclasses import dataclass, field
from typing import List

from models.player import Player
from models.tactic import TeamTactic


@dataclass
class Team:
    name: str
    formation: str
    tactic: TeamTactic

    starting_xi: List[Player] = field(default_factory=list)
    bench: List[Player] = field(default_factory=list)

    chemistry: float = 75.0
    morale: float = 75.0

    def squad_size(self) -> int:
        return len(self.starting_xi) + len(self.bench)

    def summary(self) -> str:
        return f"{self.name} | Formation: {self.formation} | Squad: {self.squad_size()}"

    def set_starting_xi(self, players: List[Player]):
        self.starting_xi = players
