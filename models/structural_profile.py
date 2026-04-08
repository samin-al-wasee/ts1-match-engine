from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralProfile:
    """
    Engine-facing structural summary derived from formation + lineup + role expression.

    All fields are normalized to 0..1.
    """

    width_coverage: float = 0.5
    central_density: float = 0.5
    support_network_quality: float = 0.5
    box_presence: float = 0.5
    rest_defense_stability: float = 0.5
    press_shape_cohesion: float = 0.5
    transition_protection: float = 0.5
    half_space_access: float = 0.5
    flank_isolation_risk: float = 0.5
    slot_fit_score: float = 0.5
    role_coherence: float = 0.5
