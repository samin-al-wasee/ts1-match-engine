from dataclasses import dataclass, field
from typing import List

from models.player import Player
from models.tactic import TeamTactic
from models.tactical_identity import TacticalIdentity
from models.team_strength import TeamStrengthProfile
from systems.tactical_identity_builder import TacticalIdentityBuilder
from systems.strength_calculator import StrengthCalculator


@dataclass
class Team:
    name: str
    formation: str
    tactic: TeamTactic

    starting_xi: List[Player] = field(default_factory=list)
    bench: List[Player] = field(default_factory=list)
    reserves: List[Player] = field(default_factory=list)

    def squad_size(self) -> int:
        return len(self.starting_xi) + len(self.bench) + len(self.reserves)

    def summary(self) -> str:
        return f"{self.name} | Formation: {self.formation} | Squad: {self.squad_size()}"

    def set_starting_xi(self, players: List[Player]):
        self.starting_xi = players

    @property
    def tactical_identity(self) -> TacticalIdentity:
        tactical_identity: TacticalIdentity = TacticalIdentityBuilder.build_full(
            self.tactic
        )

        return tactical_identity

    @property
    def strength_profile(self) -> TeamStrengthProfile:
        strength_profile: TeamStrengthProfile = StrengthCalculator.calculate(self)

        return strength_profile

    @property
    def matchday_copy(self) -> "Team":
        """
        Create a copy of the team for matchday use, which can be modified
        (e.g., for injuries, fatigue) without affecting the original team data.
        """
        return Team(
            name=self.name,
            formation=self.formation,
            tactic=self.tactic,
            starting_xi=list(self.starting_xi),
            bench=list(self.bench),
            reserves=list(self.reserves),
        )
