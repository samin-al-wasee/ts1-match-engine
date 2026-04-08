from dataclasses import dataclass, field
from typing import List

from models.lineup import MatchLineup
from models.player import Player
from models.structural_profile import StructuralProfile
from models.tactic import TeamTactic
from models.tactical_identity import TacticalIdentity
from models.team_strength import TeamStrengthProfile
from systems.formation_factory import FormationFactory
from systems.structural_profile_builder import StructuralProfileBuilder


@dataclass
class Team:
    name: str
    tactic: TeamTactic

    # Primary structural object for match behavior derivation.
    lineup: MatchLineup | None = None

    # Full available player pool.
    squad: List[Player] = field(default_factory=list)

    # Deprecated compatibility mirrors kept for migration-safe behavior.
    formation: str = "4-3-3"
    starting_xi: List[Player] = field(default_factory=list)
    bench: List[Player] = field(default_factory=list)
    reserves: List[Player] = field(default_factory=list)

    # Legacy non-structural team context still accepted where provided.
    chemistry: float | None = None
    morale: float | None = None

    def __post_init__(self) -> None:
        if self.lineup is None:
            formation_shape = FormationFactory.by_code(self.formation)
            self.lineup = MatchLineup.from_players(
                formation=formation_shape,
                players=self.starting_xi,
                bench=self.bench,
                reserves=self.reserves,
            )
        else:
            self.formation = self.lineup.formation.code

        self.starting_xi = self.lineup.ordered_starter_players(self.all_players)
        self.bench = list(self.lineup.bench)
        self.reserves = list(self.lineup.reserves)

        if not self.squad:
            self.squad = self.all_players

    @property
    def all_players(self) -> List[Player]:
        players: List[Player] = []
        seen: set[int] = set()
        for player in self.starting_xi + self.bench + self.reserves + self.squad:
            if player.id in seen:
                continue
            seen.add(player.id)
            players.append(player)
        return players

    def squad_size(self) -> int:
        return len(self.starting_xi) + len(self.bench) + len(self.reserves)

    def summary(self) -> str:
        formation_code = self.lineup.formation.code if self.lineup else self.formation
        return f"{self.name} | Formation: {formation_code} | Squad: {self.squad_size()}"

    def set_starting_xi(self, players: List[Player]):
        formation_shape = FormationFactory.by_code(self.formation)
        self.lineup = MatchLineup.from_players(
            formation=formation_shape,
            players=players,
            bench=self.bench,
            reserves=self.reserves,
        )
        self.starting_xi = list(players)

    def set_lineup(self, lineup: MatchLineup) -> None:
        lineup.validate()
        self.lineup = lineup
        self.formation = lineup.formation.code
        self.bench = list(lineup.bench)
        self.reserves = list(lineup.reserves)
        self.starting_xi = lineup.ordered_starter_players(self.all_players)

    @property
    def structural_profile(self) -> StructuralProfile:
        return StructuralProfileBuilder.build(self.lineup, self.all_players)  # type: ignore

    @property
    def tactical_identity(self) -> TacticalIdentity:
        from systems.tactical_identity_builder import TacticalIdentityBuilder

        return TacticalIdentityBuilder.build_for_team(self)

    @property
    def strength_profile(self) -> TeamStrengthProfile:
        from systems.strength_calculator import StrengthCalculator

        return StrengthCalculator.calculate(self)

    @property
    def matchday_copy(self) -> "Team":
        """
        Create a copy of the team for matchday use, which can be modified
        (e.g., for injuries, fatigue) without affecting the original team data.
        """
        return Team(
            name=self.name,
            tactic=self.tactic,
            lineup=self.lineup.clone() if self.lineup else None,
            formation=self.formation,
            starting_xi=list(self.starting_xi),
            bench=list(self.bench),
            reserves=list(self.reserves),
            squad=list(self.squad),
            chemistry=self.chemistry,
            morale=self.morale,
        )
