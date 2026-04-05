from __future__ import annotations

from dataclasses import replace

from models.matchup import MatchupProfile
from models.team_strength import TeamStrengthProfile
from models.tactical_identity import TacticalIdentity


def _clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _safe_div(n: float, d: float, default: float = 0.0) -> float:
    return n / d if abs(d) > 1e-9 else default


def _edge_from_strength_diff(
    a: float,
    b: float,
    scale: float = 20.0,
) -> float:
    """
    Convert a raw strength diff (often around 0..100-ish) to an edge [-1, +1].

    scale=20 means:
      diff=+20 -> +1.0 (strong)
      diff=+10 -> +0.5 (moderate)
    """
    return _clamp(_safe_div(a - b, scale))


class MatchupCalculator:
    """
    Layer 3 — Matchup Layer.

    Produces per-domain matchup edges by combining:
    - Layer 2: TeamStrengthProfile (players/chemistry/morale derived capability)
    - Layer 1: TacticalIdentity (intent/biases that nudge probabilities)

    This is V1: it intentionally uses only currently available strength fields.
    As you expand TeamStrengthProfile (finishing, set pieces, etc.), you can
    upgrade the formulas here without changing the consumer interface.
    """

    @staticmethod
    def calculate(
        strength_a: TeamStrengthProfile,
        identity_a: TacticalIdentity,
        strength_b: TeamStrengthProfile,
        identity_b: TacticalIdentity,
    ) -> MatchupProfile:
        # --- Base edges from strength differences ---
        # Buildup vs pressure: A buildup quality vs B pressing force
        buildup_edge = _edge_from_strength_diff(
            strength_a.build_up_quality,
            strength_b.pressing_force,
            scale=18.0,
        )

        # Pressing edge: A pressing force vs B press resistance
        pressing_edge = _edge_from_strength_diff(
            strength_a.pressing_force,
            strength_b.press_resistance,
            scale=18.0,
        )

        # Wide / central: compare attack strengths vs opponent ability to stay compact
        # (proxy until you add wide_defending / box_defending / etc.)
        wide_edge = _edge_from_strength_diff(
            strength_a.wide_attack,
            strength_b.defensive_compactness,
            scale=20.0,
        )

        central_edge = _edge_from_strength_diff(
            strength_a.central_creativity,
            strength_b.defensive_compactness,
            scale=20.0,
        )

        # Transitions: A transition threat vs B compactness (proxy for transition defense)
        transition_edge = _edge_from_strength_diff(
            strength_a.transition_threat,
            strength_b.defensive_compactness,
            scale=20.0,
        )

        # Aerial: A aerial threat vs B compactness (proxy until set_piece_defense exists)
        aerial_edge = _edge_from_strength_diff(
            strength_a.aerial_threat,
            strength_b.defensive_compactness,
            scale=22.0,
        )

        profile = MatchupProfile(
            buildup_edge=buildup_edge,
            pressing_edge=pressing_edge,
            wide_edge=wide_edge,
            central_edge=central_edge,
            transition_edge=transition_edge,
            aerial_edge=aerial_edge,
        )

        # --- Tactical identity nudges (small, clamped) ---
        # Pressing: if A is more intense than B, increase pressing edge slightly.
        press_nudge = _clamp(
            (identity_a.press_intensity_bias - identity_b.press_intensity_bias) * 0.30
        )
        trigger_nudge = _clamp(
            (identity_a.press_trigger_rate - identity_b.press_trigger_rate) * 0.20
        )
        profile = replace(
            profile,
            pressing_edge=_clamp(profile.pressing_edge + press_nudge + trigger_nudge),
        )

        # Buildup: directness and short-pass bias interplay with opponent press.
        # If A is very short-pass vs a strong press profile, reduce buildup edge slightly.
        short_vs_press_penalty = (
            identity_a.short_pass_bias * identity_b.press_intensity_bias
        ) * 0.15
        profile = replace(
            profile,
            buildup_edge=_clamp(profile.buildup_edge - short_vs_press_penalty),
        )

        # Wide/Central: route bias should amplify the team’s advantage in that lane a bit.
        # (This does not create advantage; it only helps you express it.)
        wide_route_amp = (identity_a.width_bias - 0.5) * 0.20
        central_route_amp = (
            identity_a.attack_central_bias - identity_b.attack_central_bias
        ) * 0.20
        profile = replace(
            profile,
            wide_edge=_clamp(profile.wide_edge + wide_route_amp),
            central_edge=_clamp(profile.central_edge + central_route_amp),
        )

        # Transition: counter bias boosts the ability to exploit transition edge.
        counter_amp = (
            identity_a.counter_trigger_bias - identity_b.counterpress_bias
        ) * 0.25
        speed_amp = (
            identity_a.counter_speed_bias - identity_b.counter_speed_bias
        ) * 0.10
        profile = replace(
            profile,
            transition_edge=_clamp(profile.transition_edge + counter_amp + speed_amp),
        )

        # Aerial/set piece: use set-piece biases as slight amplifiers.
        # (Still a proxy until you add set_piece_attack/set_piece_defense strengths.)
        sp_amp = (
            identity_a.set_piece_attacking_bias - identity_b.set_piece_defensive_bias
        ) * 0.20
        profile = replace(
            profile,
            aerial_edge=_clamp(profile.aerial_edge + sp_amp),
        )

        return profile
