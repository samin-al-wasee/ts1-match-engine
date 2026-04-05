from __future__ import annotations

import random

from models.match_state import MatchState
from models.matchup import MatchupProfile
from models.phase_v2 import InitiativeResult, ProgressionResult, Route, PhaseFrame
from models.team_strength import TeamStrengthProfile
from models.tactical_identity import TacticalIdentity
from systems.weighted_sampler import weighted_choice
from systems.chance_type_selector import ChanceTypeSelector
from systems.tactical_identity_adapter import TacticalIdentityAdapter
from systems.shot_resolver import ShotResolverV1


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _clamp01(x: float) -> float:
    return _clamp(x, 0.0, 1.0)


def _sigmoid(x: float) -> float:
    # cheap sigmoid-ish squashing, good enough for V1
    return 1.0 / (1.0 + (2.718281828 ** (-x)))


class PhaseResolverStepwiseV1:
    """
    Layer 5 — Stepwise Phase Resolver (Steps 1-3).

    Step 1: Initiative (who controls this minute)
    Step 2: Route selection (left/central/right)
    Step 3: Progression resolution (advance/stall/turnover)
    """

    @staticmethod
    def resolve_frame(
        *,
        minute: int,
        state: MatchState,
        home_strength: TeamStrengthProfile,
        away_strength: TeamStrengthProfile,
        home_id_full: TacticalIdentity,
        away_id_full: TacticalIdentity,
        matchup_home_vs_away: MatchupProfile,
        rng: random.Random | None = None,
    ) -> PhaseFrame:
        rng = rng or random  # type: ignore

        home_id_v1 = TacticalIdentityAdapter.to_v1(home_id_full)
        away_id_v1 = TacticalIdentityAdapter.to_v1(away_id_full)

        # -------------------
        # (1) Initiative
        # -------------------
        # Base 50/50 + Layer 1 possession tilt + small matchup + match state momentum/urgency effects.
        # possession_tilt is already clamped [-0.2, +0.2].
        tilt = _clamp(
            home_id_v1.possession_tilt - away_id_v1.possession_tilt, -0.40, 0.40
        )

        # Matchup: if home has buildup advantage, slightly increase initiative chance.
        matchup_push = 0.10 * _clamp(matchup_home_vs_away.buildup_edge, -1.0, 1.0)

        # Match state: momentum helps control; urgency can reduce control (more forced play = more chaos)
        mom_push = 0.10 * _clamp(state.home.momentum - state.away.momentum, -1.0, 1.0)
        urg_push = -0.06 * _clamp(state.home.urgency - state.away.urgency, -1.0, 1.0)

        # Strength: build-up quality vs pressing force as a slight initiative driver
        strength_push = 0.10 * _clamp(
            (home_strength.build_up_quality - away_strength.pressing_force) / 60.0,
            -1.0,
            1.0,
        )

        # Convert to probability. Keep it mild.
        x = (tilt * 2.2) + matchup_push + mom_push + urg_push + strength_push
        p_home = _clamp01(0.50 + 0.22 * _clamp(x, -1.0, 1.0))

        initiative = (
            InitiativeResult.HOME if rng.random() < p_home else InitiativeResult.AWAY  # type: ignore
        )

        # -------------------
        # (2) Route selection
        # -------------------
        # V1 route selection uses matchup edges only (wide/central) because TacticalIdentityV1
        # doesn't have left/central/right biases. We'll upgrade to full TacticalIdentity later.
        if initiative == InitiativeResult.HOME:
            wide_edge = matchup_home_vs_away.wide_edge
            central_edge = matchup_home_vs_away.central_edge
        else:
            wide_edge = -matchup_home_vs_away.wide_edge
            central_edge = -matchup_home_vs_away.central_edge

        # Make route weights from edges:
        # - if central edge high => more central
        # - if wide edge high => more left/right
        # Keep left/right symmetric in V1.
        w_central = 1.0 + 0.60 * _clamp(central_edge, -1.0, 1.0)
        w_wide = 1.0 + 0.60 * _clamp(wide_edge, -1.0, 1.0)

        w_left = w_wide / 2.0
        w_right = w_wide / 2.0

        route_str = weighted_choice(
            items=[Route.LEFT, Route.CENTRAL, Route.RIGHT],
            weights=[w_left, w_central, w_right],
            rng=rng,
        )

        route_weights = {
            "left": float(w_left),
            "central": float(w_central),
            "right": float(w_right),
        }

        # -------------------
        # (3) Resolve progression
        # -------------------
        # Progression contest: attacker progression ability vs defender resistance.
        # Use different strength proxies depending on route.
        if initiative == InitiativeResult.HOME:
            atk_s, def_s = home_strength, away_strength
            atk_id, _def_id = home_id_full, away_id_full
            atk_state, def_state = state.home, state.away
            pressing_edge = matchup_home_vs_away.pressing_edge
        else:
            atk_s, def_s = away_strength, home_strength
            atk_id, _def_id = away_id_full, home_id_full
            atk_state, def_state = state.away, state.home
            pressing_edge = -matchup_home_vs_away.pressing_edge

        if route_str in (Route.LEFT, Route.RIGHT):
            atk_prog = atk_s.wide_attack
        else:
            atk_prog = atk_s.central_creativity

        # Defender resistance proxy: compactness + (pressing impact)
        def_resist = 0.65 * def_s.defensive_compactness + 0.35 * def_s.pressing_force

        # Raw contest signal
        contest = (atk_prog - def_resist) / 25.0  # ~[-4,+4] if 0..100 scale
        contest += 0.50 * _clamp(
            pressing_edge, -1.0, 1.0
        )  # pressing edge helps defender (if negative for attacker)

        # State modifiers
        # Attacker fatigue hurts progression, defender fatigue helps attacker.
        contest += 0.60 * (def_state.fatigue - atk_state.fatigue)
        # Momentum helps progression
        contest += 0.35 * (atk_state.momentum - def_state.momentum)
        # Urgency increases turnover risk (forcing play)
        urgency = _clamp01(atk_state.urgency)
        force_risk = urgency - 0.5

        # Convert contest to probabilities.
        # Base: advance vs stall vs turnover
        p_adv = _clamp01(0.40 + 0.20 * _clamp(contest, -1.0, 1.0))
        p_tov = _clamp01(0.18 - 0.08 * _clamp(contest, -1.0, 1.0) + 0.10 * force_risk)

        # Tactical identity V1 affects turnover and pass retention, so apply it here:
        # Higher turnover_weight_mult means you're more turnover-prone in general.
        atk_id_v1 = TacticalIdentityAdapter.to_v1(atk_id)

        p_tov *= _clamp(atk_id_v1.turnover_weight_mult, 0.80, 1.20)
        p_adv *= _clamp(atk_id_v1.pass_weight_mult, 0.80, 1.20)

        # Normalize and derive stall
        p_adv = _clamp01(p_adv)
        p_tov = _clamp01(p_tov)
        # ensure sum <= 1
        max_sum = min(0.98, p_adv + p_tov)
        if max_sum > 0.98:
            # scale down proportionally
            scale = 0.98 / max_sum
            p_adv *= scale
            p_tov *= scale

        _p_stall = _clamp01(1.0 - (p_adv + p_tov))

        r = rng.random()  # type: ignore
        if r < p_tov:
            prog = ProgressionResult.TURNOVER
        elif r < p_tov + p_adv:
            prog = ProgressionResult.ADVANCE
        else:
            prog = ProgressionResult.STALLED

        chance_type = None
        chance_weights = None

        shot_xg = None
        shot_result = None

        if prog == ProgressionResult.ADVANCE:
            if initiative == InitiativeResult.HOME:
                identity_atk = home_id_full
                matchup_atk_vs_def = matchup_home_vs_away
                atk_state = state.home
            else:
                identity_atk = away_id_full
                # flip wide/central edges for away attack
                matchup_atk_vs_def = MatchupProfile(
                    buildup_edge=-matchup_home_vs_away.buildup_edge,
                    pressing_edge=-matchup_home_vs_away.pressing_edge,
                    wide_edge=-matchup_home_vs_away.wide_edge,
                    central_edge=-matchup_home_vs_away.central_edge,
                    transition_edge=-matchup_home_vs_away.transition_edge,
                    aerial_edge=-matchup_home_vs_away.aerial_edge,
                )
                atk_state = state.away

            sel = ChanceTypeSelector.select(
                route=route_str,  # type: ignore
                identity_atk=identity_atk,
                matchup_atk_vs_def=matchup_atk_vs_def,
                atk_state=atk_state,
                rng=rng,
            )
            chance_type = sel.chance_type
            chance_weights = sel.weights

            if chance_type is not None:
                if initiative == InitiativeResult.HOME:
                    side = "home"
                    atk_strength, def_strength = home_strength, away_strength
                    atk_id_full = home_id_full
                    atk_state, def_state = state.home, state.away
                    matchup_atk_vs_def = matchup_home_vs_away
                else:
                    side = "away"
                    atk_strength, def_strength = away_strength, home_strength
                    atk_id_full = away_id_full
                    atk_state, def_state = state.away, state.home
                    matchup_atk_vs_def = MatchupProfile(
                        buildup_edge=-matchup_home_vs_away.buildup_edge,
                        pressing_edge=-matchup_home_vs_away.pressing_edge,
                        wide_edge=-matchup_home_vs_away.wide_edge,
                        central_edge=-matchup_home_vs_away.central_edge,
                        transition_edge=-matchup_home_vs_away.transition_edge,
                        aerial_edge=-matchup_home_vs_away.aerial_edge,
                    )

                shot = ShotResolverV1.resolve(
                    minute=minute,
                    side=side,
                    chance_type=chance_type,
                    atk_strength=atk_strength,
                    def_strength=def_strength,
                    matchup_atk_vs_def=matchup_atk_vs_def,
                    atk_identity_full=atk_id_full,
                    atk_state=atk_state,
                    def_state=def_state,
                    rng=rng,
                )
                shot_xg = shot.xg
                shot_result = shot.result

        return PhaseFrame(
            minute=minute,
            initiative=initiative,
            route=route_str,  # type: ignore
            progression=prog,
            initiative_p_home=float(p_home),
            route_weights=route_weights,
            progression_p_advance=float(p_adv),
            progression_p_turnover=float(p_tov),
            chance_type=chance_type,
            chance_type_weights=chance_weights,
            xg=shot_xg,
            shot_result=shot_result,
        )
