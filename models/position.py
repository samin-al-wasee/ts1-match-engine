from __future__ import annotations

from enum import StrEnum


class Position(StrEnum):
    """
    Normalized base-slot player positions (V1).

    Keep this list small and stable. Variations belong in Role (+ Duty).
    """

    GK = "GK"
    RB = "RB"
    CB = "CB"
    LB = "LB"
    DM = "DM"
    CM = "CM"
    AM = "AM"
    RW = "RW"
    LW = "LW"
    ST = "ST"


# Optional helper for input cleanup (use in editors/importers, not engine core).
_POSITION_ALIASES: dict[str, Position] = {
    "CDM": Position.DM,
    "CAM": Position.AM,
    "RCM": Position.CM,
    "LCM": Position.CM,
    "RAM": Position.AM,
    "LAM": Position.AM,
    "RM": Position.RW,
    "LM": Position.LW,
    "CF": Position.ST,
    "RF": Position.ST,
    "LF": Position.ST,
    "RWB": Position.RB,
    "LWB": Position.LB,
}


def normalize_position(value: str | Position) -> Position:
    """
    Normalize common aliases (e.g. CDM -> DM, CAM -> AM) into canonical V1 Position.
    """
    if isinstance(value, Position):
        return value
    v = value.strip().upper()
    return _POSITION_ALIASES.get(v, Position(v))
