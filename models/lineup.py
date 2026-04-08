from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence

from models.duty import Duty
from models.formation import FormationShape
from models.player import Player
from models.role import Role


@dataclass(frozen=True)
class RoleAssignment:
    """Role intent of a starter inside a slot."""

    role_name: Role
    duty: Duty


@dataclass(frozen=True)
class LineupSlotAssignment:
    """Mapping between one formation slot and one player role assignment."""

    slot_id: str
    player_id: int
    role_assignment: RoleAssignment


@dataclass
class MatchLineup:
    """Matchday lineup structure with formation and slot assignments."""

    formation: FormationShape
    slot_assignments: List[LineupSlotAssignment] = field(default_factory=list)
    bench: List[Player] = field(default_factory=list)
    reserves: List[Player] = field(default_factory=list)
    captain_id: int | None = None

    def starter_ids(self) -> List[int]:
        return [assignment.player_id for assignment in self.slot_assignments]

    def validate(self) -> None:
        slot_ids = {slot.slot_id for slot in self.formation.slot_definitions}
        assigned_slots = [assignment.slot_id for assignment in self.slot_assignments]

        if len(set(assigned_slots)) != len(assigned_slots):
            raise ValueError("Duplicate slot assignment detected in lineup.")

        unknown_slots = [
            slot_id for slot_id in assigned_slots if slot_id not in slot_ids
        ]
        if unknown_slots:
            raise ValueError(f"Unknown formation slot ids: {unknown_slots}")

        if len(set(self.starter_ids())) != len(self.starter_ids()):
            raise ValueError("Same player was assigned to multiple formation slots.")

    def to_player_lookup(self, players: Sequence[Player]) -> Dict[int, Player]:
        return {player.id: player for player in players}

    def ordered_starter_players(self, players: Sequence[Player]) -> List[Player]:
        by_id = self.to_player_lookup(players)
        ordered: List[Player] = []
        for slot in self.formation.slot_definitions:
            assignment = next(
                (
                    a
                    for a in self.slot_assignments
                    if a.slot_id == slot.slot_id and a.player_id in by_id
                ),
                None,
            )
            if assignment is not None:
                ordered.append(by_id[assignment.player_id])
        return ordered

    def clone(self) -> "MatchLineup":
        return MatchLineup(
            formation=self.formation,
            slot_assignments=list(self.slot_assignments),
            bench=list(self.bench),
            reserves=list(self.reserves),
            captain_id=self.captain_id,
        )

    @staticmethod
    def from_players(
        formation: FormationShape,
        players: Sequence[Player],
        bench: Iterable[Player] | None = None,
        reserves: Iterable[Player] | None = None,
        captain_id: int | None = None,
    ) -> "MatchLineup":
        """
        Best-effort slot assignment for backward compatibility paths.

        Selection order:
        1) unassigned player matching one of slot preferred positions
        2) next unassigned player
        """
        unassigned = list(players)
        assignments: List[LineupSlotAssignment] = []

        for slot in formation.slot_definitions:
            chosen_idx = -1
            for idx, player in enumerate(unassigned):
                if (
                    slot.preferred_positions
                    and player.position in slot.preferred_positions
                ):
                    chosen_idx = idx
                    break
            if chosen_idx < 0 and unassigned:
                chosen_idx = 0
            if chosen_idx < 0:
                break

            player = unassigned.pop(chosen_idx)
            assignments.append(
                LineupSlotAssignment(
                    slot_id=slot.slot_id,
                    player_id=player.id,
                    role_assignment=RoleAssignment(
                        role_name=player.role, duty=player.duty
                    ),
                )
            )

        lineup = MatchLineup(
            formation=formation,
            slot_assignments=assignments,
            bench=list(bench or []),
            reserves=list(reserves or []),
            captain_id=captain_id,
        )
        lineup.validate()
        return lineup
