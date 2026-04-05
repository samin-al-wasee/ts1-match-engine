from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MatchupProfile:
    """
    Layer 3 — Matchup Layer output.

    Edges are expressed from Team A perspective:
      -1.0 = strong advantage Team B
       0.0 = neutral
      +1.0 = strong advantage Team A
    """

    # Possession / buildup vs pressure
    buildup_edge: float = 0.0

    # Pressing effectiveness (A press vs B press resistance)
    pressing_edge: float = 0.0

    # Route / chance creation lanes
    wide_edge: float = 0.0
    central_edge: float = 0.0

    # Transitions
    transition_edge: float = 0.0

    # Aerial / set-piece leaning proxy (until dedicated set-piece fields exist)
    aerial_edge: float = 0.0

    def summary(self) -> str:
        return (
            f"Buildup Edge: {self.buildup_edge:+.2f}\n"
            f"Pressing Edge: {self.pressing_edge:+.2f}\n"
            f"Wide Edge: {self.wide_edge:+.2f}\n"
            f"Central Edge: {self.central_edge:+.2f}\n"
            f"Transition Edge: {self.transition_edge:+.2f}\n"
            f"Aerial Edge: {self.aerial_edge:+.2f}"
        )
