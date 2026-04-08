from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from models.position import Position


@dataclass(frozen=True)
class FormationSlot:
    """Structural slot inside a formation shape."""

    slot_id: str
    base_zone: str
    line: str
    lateral_band: str
    vertical_band: str
    preferred_positions: Tuple[Position, ...] = tuple()
    adjacency_slots: Tuple[str, ...] = tuple()
    support_links: Tuple[str, ...] = tuple()
    attacking_lane_access: Tuple[str, ...] = tuple()
    defensive_responsibility: Tuple[str, ...] = tuple()


@dataclass(frozen=True)
class FormationShape:
    """
    Formation as a structural football object.

    code: canonical label such as 4-3-3.
    slot_definitions: ordered list of structural slots.
    structural_tags: lightweight metadata for shape behavior.
    """

    code: str
    slot_definitions: Tuple[FormationSlot, ...]
    structural_tags: Dict[str, float] = field(default_factory=dict)

    def slot_ids(self) -> List[str]:
        return [slot.slot_id for slot in self.slot_definitions]

    def slot_by_id(self, slot_id: str) -> FormationSlot | None:
        for slot in self.slot_definitions:
            if slot.slot_id == slot_id:
                return slot
        return None
