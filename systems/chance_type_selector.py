from __future__ import annotations

from dataclasses import dataclass

from models.chance import ChanceType
from models.match_state import TeamMatchState
from models.matchup import MatchupProfile
from models.phase_v2 import Route
from models.tactical_identity import TacticalIdentity
from systems.weighted_sampler import weighted_choice


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass(frozen=True)
class ChanceSelection:
    chance_type: ChanceType
    weights: dict[str, float]


class ChanceTypeSelector:
    """
    Step 4 — Convert progression into a chance type.

    Base weights come from TacticalIdentity biases:
      through_ball_bias, cross_bias, cutback_bias, dribble_creation_bias, long_shot_bias

    Then apply small situational nudges:
      - route: wide routes boost cross/cutback/dribble; central boosts through balls/long shots
      - matchup: wide_edge/central_edge amplifies chances that match the lane advantage
      - match state: urgency increases long_shot a bit; low momentum increases long_shot (forcing)
    """

    @staticmethod
    def select(
        *,
        route: Route,
        identity_atk: TacticalIdentity,
        matchup_atk_vs_def: MatchupProfile,
        atk_state: TeamMatchState,
        rng=None,
    ) -> ChanceSelection:
        # Start from identity biases (0..1). Convert to positive weights.
        w_through = 0.20 + 1.20 * _clamp01(identity_atk.through_ball_bias)
        w_cross = 0.20 + 1.20 * _clamp01(identity_atk.cross_bias)
        w_cutback = 0.20 + 1.20 * _clamp01(identity_atk.cutback_bias)
        w_dribble = 0.20 + 1.20 * _clamp01(identity_atk.dribble_creation_bias)
        w_long = 0.15 + 1.10 * _clamp01(identity_atk.long_shot_bias)

        # --- Route nudges ---
        if route in (Route.LEFT, Route.RIGHT):
            w_cross *= 1.25
            w_cutback *= 1.20
            w_dribble *= 1.10
            w_through *= 0.90
            w_long *= 0.95
        else:  # CENTRAL
            w_through *= 1.25
            w_long *= 1.10
            w_cross *= 0.90
            w_cutback *= 0.95

        # --- Matchup nudges (lane advantage) ---
        # If you have a wide edge, increase cross/cutback/dribble slightly.
        wide_edge = matchup_atk_vs_def.wide_edge
        central_edge = matchup_atk_vs_def.central_edge

        w_cross *= 1.0 + 0.15 * wide_edge
        w_cutback *= 1.0 + 0.12 * wide_edge
        w_dribble *= 1.0 + 0.10 * wide_edge

        w_through *= 1.0 + 0.15 * central_edge
        w_long *= 1.0 + 0.10 * central_edge

        # --- Match state nudges ---
        urgency = _clamp01(atk_state.urgency)
        momentum = _clamp01(atk_state.momentum)

        # High urgency -> more "forcing" and lower patience => a bit more long shots & crosses.
        w_long *= 1.0 + 0.15 * (urgency - 0.5)
        w_cross *= 1.0 + 0.08 * (urgency - 0.5)

        # Low momentum -> more desperation shots
        w_long *= 1.0 + 0.10 * (0.5 - momentum)

        # Prepare weights dict
        weights = {
            ChanceType.THROUGH_BALL: float(max(0.01, w_through)),
            ChanceType.CROSS: float(max(0.01, w_cross)),
            ChanceType.CUTBACK: float(max(0.01, w_cutback)),
            ChanceType.DRIBBLE: float(max(0.01, w_dribble)),
            ChanceType.LONG_SHOT: float(max(0.01, w_long)),
        }

        ct = weighted_choice(
            items=list(weights.keys()),
            weights=list(weights.values()),
            rng=rng,
        )

        return ChanceSelection(
            chance_type=ct,  # type: ignore
            weights={k.value: v for k, v in weights.items()},
        )
