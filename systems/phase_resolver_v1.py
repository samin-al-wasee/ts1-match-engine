from __future__ import annotations

import random

from models.match_state import MatchState
from models.matchup import MatchupProfile
from models.phase import MinuteOutcome, PhaseEventType
from models.team_strength import TeamStrengthProfile
from models.tactical_identity import TacticalIdentityV1
from systems.weighted_sampler import weighted_choice


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _clamp01(x: float) -> float:
    return _clamp(x, 0.0, 1.0)


class PhaseResolverV1:
    """
    Layer 5 — Phase Resolution (V1 minute-loop).

    Resolves a single minute into one primary event:
    - pass (retains possession)
    - turnover (possession changes)
    - shot (may become goal)

    Inputs are layered:
    - L1: TacticalIdentityV1 (small multipliers/deltas)
    - L2: TeamStrengthProfile (capability)
    - L3: MatchupProfile (A vs B edges)
    - L4: MatchState (momentum/urgency/fatigue/score context)
    """

    @staticmethod
    def resolve_minute(
        *,
        minute: int,
        possessing_side: str,  # "home" or "away"
        state: MatchState,
        home_strength: TeamStrengthProfile,
        away_strength: TeamStrengthProfile,
        home_id: TacticalIdentityV1,
        away_id: TacticalIdentityV1,
        matchup_home_vs_away: MatchupProfile,  # edges from home perspective
        rng: random.Random | None = None,
    ) -> MinuteOutcome:
        rng = rng or random  # type: ignore

        # Pick attacker/defender context based on possessing side.
        if possessing_side == "home":
            atk_strength, def_strength = home_strength, away_strength
            atk_id, _def_id = home_id, away_id
            atk_team_state, _def_team_state = state.home, state.away
            # Convert matchup edges to attacker perspective
            pressing_edge = matchup_home_vs_away.pressing_edge
            buildup_edge = matchup_home_vs_away.buildup_edge
        else:
            atk_strength, def_strength = away_strength, home_strength
            atk_id, _def_id = away_id, home_id
            atk_team_state, _def_team_state = state.away, state.home
            # flip edges (home vs away -> away vs home)
            pressing_edge = -matchup_home_vs_away.pressing_edge
            buildup_edge = -matchup_home_vs_away.buildup_edge

        # --- Base weights (tuned later) ---
        # Interpreting: "pass" = harmless circulation, "turnover" = lose ball, "shot" = attempt created.
        pass_w = 1.00
        turnover_w = 0.55
        shot_w = 0.35

        # --- Layer 1 modifiers (V1 tactical identity multipliers) ---
        pass_w *= atk_id.pass_weight_mult
        turnover_w *= atk_id.turnover_weight_mult
        shot_w *= atk_id.shot_weight_mult

        # --- Layer 2/3 influence (strength + matchup edges) ---
        # Buildup edge boosts pass retention and reduces turnovers.
        pass_w *= 1.0 + 0.20 * _clamp(buildup_edge, -1.0, 1.0)
        turnover_w *= 1.0 - 0.25 * _clamp(buildup_edge, -1.0, 1.0)

        # Pressing edge for defender increases turnover chance for attacker.
        turnover_w *= 1.0 + 0.30 * _clamp(
            -pressing_edge, -1.0, 1.0
        )  # if defender has pressing advantage => negative attacker edge
        pass_w *= 1.0 - 0.10 * _clamp(-pressing_edge, -1.0, 1.0)

        # Strength influence: build_up_quality vs pressing_force shapes turnover baseline.
        # Keep small in V1 so identity still matters.
        rel_buildup = (
            atk_strength.build_up_quality - def_strength.pressing_force
        ) / 50.0  # ~[-2,+2]
        turnover_w *= 1.0 - 0.10 * _clamp(rel_buildup, -1.0, 1.0)
        pass_w *= 1.0 + 0.05 * _clamp(rel_buildup, -1.0, 1.0)

        # Chance creation ability slightly increases shot weight.
        rel_creativity = (
            atk_strength.central_creativity - def_strength.defensive_compactness
        ) / 60.0
        shot_w *= 1.0 + 0.12 * _clamp(rel_creativity, -1.0, 1.0)

        # --- Layer 4 modifiers (match state) ---
        # Urgency: increases shot attempts but also turnovers.
        urgency = _clamp01(atk_team_state.urgency)
        shot_w *= 1.0 + 0.25 * (urgency - 0.5)
        turnover_w *= 1.0 + 0.20 * (urgency - 0.5)
        pass_w *= 1.0 - 0.10 * (urgency - 0.5)

        # Fatigue: reduces passing/press-resistance, increases turnovers, reduces shots slightly.
        fatigue = _clamp01(atk_team_state.fatigue)
        pass_w *= 1.0 - 0.18 * fatigue
        turnover_w *= 1.0 + 0.25 * fatigue
        shot_w *= 1.0 - 0.10 * fatigue

        # Momentum: small boost to creating shots and avoiding turnovers.
        momentum = _clamp01(atk_team_state.momentum)
        shot_w *= 1.0 + 0.10 * (momentum - 0.5)
        turnover_w *= 1.0 - 0.08 * (momentum - 0.5)

        # Clamp to avoid negative weights
        pass_w = max(0.01, pass_w)
        turnover_w = max(0.01, turnover_w)
        shot_w = max(0.01, shot_w)

        event = weighted_choice(
            items=[PhaseEventType.PASS, PhaseEventType.TURNOVER, PhaseEventType.SHOT],
            weights=[pass_w, turnover_w, shot_w],
            rng=rng,
        )

        # --- Resolve event ---
        if event == PhaseEventType.PASS:
            return MinuteOutcome(
                minute=minute,
                possessing_side=possessing_side,
                event_type=PhaseEventType.PASS,
                description="Recycles possession.",
            )

        if event == PhaseEventType.TURNOVER:
            return MinuteOutcome(
                minute=minute,
                possessing_side=possessing_side,
                event_type=PhaseEventType.TURNOVER,
                description="Loses the ball under pressure.",
            )

        # Shot event:
        # Create a very simple xG from relative attacking vs defending + identity conversion delta.
        base_xg = 0.08  # V1 baseline shot quality
        xg = base_xg + 0.03 * _clamp(rel_creativity, -1.0, 1.0)
        xg = _clamp01(xg)

        # Conversion probability nudged by identity (V1)
        conv_p = _clamp01(xg + atk_id.shot_conversion_delta)

        is_goal = rng.random() < conv_p  # type: ignore
        return MinuteOutcome(
            minute=minute,
            possessing_side=possessing_side,
            event_type=PhaseEventType.GOAL if is_goal else PhaseEventType.SHOT,
            xg=xg,
            description="Scores!" if is_goal else "Takes a shot.",
        )
