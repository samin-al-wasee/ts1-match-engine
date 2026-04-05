from __future__ import annotations

import random

from models.chance import ChanceType
from models.match_state import TeamMatchState
from models.matchup import MatchupProfile
from models.shot import ShotOutcome, ShotResult
from models.team_strength import TeamStrengthProfile
from models.tactical_identity import TacticalIdentity
from systems.tactical_identity_adapter import TacticalIdentityAdapter


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _clamp01(x: float) -> float:
    return _clamp(x, 0.0, 1.0)


class ShotResolverV1:
    """
    Step 5 — Chance quality + conversion (SHOT vs GOAL).

    Uses current TeamStrengthProfile fields as proxies:
      - finishing proxy: central_creativity (not ideal but usable)
      - wide delivery proxy: wide_attack
      - defensive resistance: defensive_compactness
      - pressing force: pressing_force (pressure lowers xG a bit)
    """

    # Base xG by chance type (tune later)
    _BASE_XG: dict[ChanceType, float] = {
        ChanceType.THROUGH_BALL: 0.18,
        ChanceType.CUTBACK: 0.14,
        ChanceType.CROSS: 0.10,
        ChanceType.DRIBBLE: 0.12,
        ChanceType.LONG_SHOT: 0.05,
    }

    @staticmethod
    def resolve(
        *,
        minute: int,
        side: str,  # "home" or "away"
        chance_type: ChanceType,
        atk_strength: TeamStrengthProfile,
        def_strength: TeamStrengthProfile,
        matchup_atk_vs_def: MatchupProfile,  # already oriented attacker vs defender
        atk_identity_full: TacticalIdentity,
        atk_state: TeamMatchState,
        def_state: TeamMatchState,
        rng: random.Random | None = None,
    ) -> ShotOutcome:
        rng = rng or random  # type: ignore

        base_xg = ShotResolverV1._BASE_XG[chance_type]

        # --- Strength proxies (replace later with finishing/goalkeeping fields) ---
        # attack quality proxy depends on chance type:
        if chance_type in (ChanceType.CROSS, ChanceType.CUTBACK):
            atk_quality = atk_strength.wide_attack
        elif chance_type == ChanceType.LONG_SHOT:
            atk_quality = atk_strength.central_creativity * 0.7
        else:
            atk_quality = atk_strength.central_creativity

        # defender quality proxy:
        def_quality = (
            0.70 * def_strength.defensive_compactness
            + 0.30 * def_strength.pressing_force
        )

        # contest signal ~[-1, +1] (roughly)
        contest = _clamp((atk_quality - def_quality) / 40.0, -1.0, 1.0)

        # matchup edges amplify the relevant chance family slightly
        edge_boost = 0.0
        if chance_type in (ChanceType.CROSS, ChanceType.CUTBACK, ChanceType.DRIBBLE):
            edge_boost += 0.04 * _clamp(matchup_atk_vs_def.wide_edge, -1.0, 1.0)
        if chance_type in (ChanceType.THROUGH_BALL, ChanceType.LONG_SHOT):
            edge_boost += 0.04 * _clamp(matchup_atk_vs_def.central_edge, -1.0, 1.0)

        # --- Match state effects ---
        # Fatigue reduces execution quality
        fatigue_penalty = 0.05 * _clamp01(atk_state.fatigue)
        # Momentum slightly increases composure/finishing
        momentum_boost = 0.03 * (_clamp01(atk_state.momentum) - 0.5)
        # Urgency increases shot forcing -> slightly worse shot quality (but more shots earlier step)
        urgency_penalty = 0.03 * (_clamp01(atk_state.urgency) - 0.5)

        # --- Identity effects (full) ---
        # shot_patience: more patient -> better shot selection quality, but fewer shots (handled earlier)
        patience_boost = 0.05 * (_clamp01(atk_identity_full.shot_patience) - 0.5)
        # risk_taking: more risk -> slightly worse average shot quality
        risk_penalty = 0.04 * (_clamp01(atk_identity_full.risk_taking) - 0.5)

        # Compose xG
        xg = base_xg
        xg += 0.06 * contest
        xg += edge_boost
        xg += patience_boost
        xg += momentum_boost
        xg -= fatigue_penalty
        xg -= urgency_penalty
        xg -= risk_penalty

        # extra: long shots are more sensitive to forcing
        if chance_type == ChanceType.LONG_SHOT:
            xg -= 0.03 * (_clamp01(atk_state.urgency) - 0.5)

        xg = _clamp01(xg)

        # Conversion probability: start from xG and apply derived V1 delta (backward compat knob)
        v1 = TacticalIdentityAdapter.to_v1(atk_identity_full)
        conv_p = _clamp01(xg + v1.shot_conversion_delta)

        is_goal = rng.random() < conv_p  # type: ignore
        return ShotOutcome(
            minute=minute,
            side=side,
            chance_type=chance_type,
            xg=float(xg),
            result=ShotResult.GOAL if is_goal else ShotResult.SHOT,
        )
