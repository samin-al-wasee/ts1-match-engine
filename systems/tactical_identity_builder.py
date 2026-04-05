from models.tactic import TeamTactic
from models.tactic_attributes import (
    AttackingFocus,
    BuildUpStyle,
    Compactness,
    DefensiveLine,
    DefensiveWidth,
    DribblingRisk,
    FinalThirdFocus,
    MarkingStyle,
    PassingRisk,
    PressingIntensity,
    SetPieceAttack,
    SetPieceDefense,
    ShootingPolicy,
    TacklingAggression,
    TeamMentality,
    Tempo,
    TransitionOnLoss,
    TransitionOnWin,
    Width,
)
from models.tactical_identity import TacticalIdentity


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _clamp01(x: float) -> float:
    return _clamp(x, 0.0, 1.0)


class TacticalIdentityBuilder:
    """
    Builds TacticalIdentity from TeamTactic based on SPEC Part 2 controls.

    - build_full(): full identity mapping (includes current minute-loop knobs)
    """

    @staticmethod
    def _compute_engine_knobs(tactic: TeamTactic) -> dict[str, float]:
        """
        Computes current minute-loop engine knobs from TeamTactic.
        """
        possession_tilt = 0.0
        pass_mult = 1.0
        turnover_mult = 1.0
        shot_mult = 1.0
        shot_conv_delta = 0.0

        # Build-up style
        if tactic.build_up_style == BuildUpStyle.BUILD_FROM_BACK:
            possession_tilt += 0.08
            pass_mult += 0.08
            turnover_mult -= 0.03
            shot_mult -= 0.02
        elif tactic.build_up_style == BuildUpStyle.LONG_BALL:
            possession_tilt -= 0.10
            pass_mult -= 0.06
            turnover_mult += 0.05
            shot_mult += 0.06
        elif tactic.build_up_style == BuildUpStyle.COUNTER_BUILD_UP:
            possession_tilt -= 0.04
            turnover_mult += 0.03
            shot_mult += 0.03

        # Tempo
        if tactic.tempo == Tempo.VERY_HIGH:
            possession_tilt -= 0.05
            turnover_mult += 0.08
            shot_mult += 0.06
            shot_conv_delta -= 0.03
        elif tactic.tempo == Tempo.HIGH:
            possession_tilt -= 0.03
            turnover_mult += 0.06
            shot_mult += 0.04
            shot_conv_delta -= 0.02
        elif tactic.tempo == Tempo.LOW:
            possession_tilt += 0.03
            turnover_mult -= 0.05
            pass_mult += 0.05
            shot_mult -= 0.02
            shot_conv_delta += 0.01
        elif tactic.tempo == Tempo.VERY_LOW:
            possession_tilt += 0.05
            turnover_mult -= 0.08
            pass_mult += 0.07
            shot_mult -= 0.04
            shot_conv_delta += 0.02

        # Pressing intensity
        if tactic.pressing_intensity == PressingIntensity.EXTREME:
            possession_tilt += 0.06
            turnover_mult += 0.06
            shot_mult += 0.02
            shot_conv_delta -= 0.01
        elif tactic.pressing_intensity == PressingIntensity.HIGH:
            possession_tilt += 0.04
            turnover_mult += 0.03
        elif tactic.pressing_intensity == PressingIntensity.LOW:
            possession_tilt -= 0.04
        elif tactic.pressing_intensity == PressingIntensity.VERY_LOW:
            possession_tilt -= 0.06

        # Team mentality
        if tactic.team_mentality == TeamMentality.VERY_ATTACKING:
            shot_mult += 0.10
            shot_conv_delta += 0.03
            turnover_mult += 0.02
        elif tactic.team_mentality == TeamMentality.ATTACKING:
            shot_mult += 0.08
            shot_conv_delta += 0.02
        elif tactic.team_mentality == TeamMentality.POSITIVE:
            shot_mult += 0.04
            shot_conv_delta += 0.01
        elif tactic.team_mentality == TeamMentality.DEFENSIVE:
            shot_mult -= 0.05
            shot_conv_delta -= 0.01
            possession_tilt += 0.02
        elif tactic.team_mentality == TeamMentality.VERY_DEFENSIVE:
            shot_mult -= 0.08
            shot_conv_delta -= 0.02
            possession_tilt += 0.03

        # Clamp values for safe engine behavior
        possession_tilt = _clamp(possession_tilt, -0.20, 0.20)
        pass_mult = _clamp(pass_mult, 0.80, 1.20)
        turnover_mult = _clamp(turnover_mult, 0.80, 1.20)
        shot_mult = _clamp(shot_mult, 0.80, 1.25)
        shot_conv_delta = _clamp(shot_conv_delta, -0.10, 0.10)

        return {
            "possession_tilt": float(possession_tilt),
            "pass_weight_mult": float(pass_mult),
            "turnover_weight_mult": float(turnover_mult),
            "shot_weight_mult": float(shot_mult),
            "shot_conversion_delta": float(shot_conv_delta),
        }

    @staticmethod
    def build_full(tactic: TeamTactic) -> TacticalIdentity:
        """
        Full mapping from TeamTactic -> TacticalIdentity.
        """
        engine_knobs = TacticalIdentityBuilder._compute_engine_knobs(tactic)

        width_bias = _clamp01(
            {
                Width.VERY_NARROW: 0.0,
                Width.NARROW: 0.25,
                Width.BALANCED: 0.5,
                Width.WIDE: 0.75,
                Width.VERY_WIDE: 1.0,
            }[tactic.width]
        )

        defensive_line_height = _clamp01(
            {
                DefensiveLine.VERY_DEEP: 0.0,
                DefensiveLine.DEEP: 0.25,
                DefensiveLine.STANDARD: 0.5,
                DefensiveLine.HIGH: 0.75,
                DefensiveLine.VERY_HIGH: 1.0,
            }[tactic.defensive_line]
        )

        press_intensity_bias = _clamp01(
            {
                PressingIntensity.VERY_LOW: 0.0,
                PressingIntensity.LOW: 0.25,
                PressingIntensity.BALANCED: 0.5,
                PressingIntensity.HIGH: 0.75,
                PressingIntensity.EXTREME: 1.0,
            }[tactic.pressing_intensity]
        )

        defensive_width_bias = _clamp01(
            {
                DefensiveWidth.VERY_NARROW: 0.0,
                DefensiveWidth.NARROW: 0.25,
                DefensiveWidth.BALANCED: 0.5,
                DefensiveWidth.WIDE: 0.75,
                DefensiveWidth.VERY_WIDE: 1.0,
            }[tactic.defensive_width]
        )

        compactness_bias = _clamp01(
            {
                Compactness.VERY_LOOSE: 0.0,
                Compactness.LOOSE: 0.25,
                Compactness.BALANCED: 0.5,
                Compactness.COMPACT: 0.75,
                Compactness.VERY_COMPACT: 1.0,
            }[tactic.compactness]
        )

        marking_bias = _clamp01(
            {
                MarkingStyle.ZONAL: 0.0,
                MarkingStyle.MIXED: 0.5,
                MarkingStyle.TIGHT_MAN_ORIENTED: 1.0,
            }[tactic.marking_style]
        )

        tackling_aggression_bias = _clamp01(
            {
                TacklingAggression.STAY_ON_FEET: 0.2,
                TacklingAggression.BALANCED: 0.5,
                TacklingAggression.AGGRESSIVE: 0.8,
                TacklingAggression.VERY_AGGRESSIVE: 1.0,
            }[tactic.tackling_aggression]
        )

        risk_taking = _clamp01(
            0.5
            + {
                PassingRisk.VERY_SAFE: -0.25,
                PassingRisk.SAFE: -0.10,
                PassingRisk.BALANCED: 0.0,
                PassingRisk.RISKY: 0.12,
                PassingRisk.VERY_RISKY: 0.22,
            }[tactic.passing_risk]
            + {
                DribblingRisk.VERY_CONSERVATIVE: -0.08,
                DribblingRisk.BALANCED: 0.0,
                DribblingRisk.AGGRESSIVE: 0.10,
            }[tactic.dribbling_risk]
            + {
                TeamMentality.VERY_DEFENSIVE: -0.18,
                TeamMentality.DEFENSIVE: -0.10,
                TeamMentality.CAUTIOUS: -0.05,
                TeamMentality.BALANCED: 0.0,
                TeamMentality.POSITIVE: 0.05,
                TeamMentality.ATTACKING: 0.12,
                TeamMentality.VERY_ATTACKING: 0.20,
            }[tactic.team_mentality]
        )

        directness_bias = _clamp01(
            {
                BuildUpStyle.BUILD_FROM_BACK: 0.20,
                BuildUpStyle.MIXED_BUILD_UP: 0.50,
                BuildUpStyle.DIRECT_PROGRESSION: 0.75,
                BuildUpStyle.LONG_BALL: 1.00,
                BuildUpStyle.COUNTER_BUILD_UP: 0.85,
            }[tactic.build_up_style]
        )

        vertical_progression_bias = _clamp01(
            {
                Tempo.VERY_LOW: 0.20,
                Tempo.LOW: 0.35,
                Tempo.BALANCED: 0.50,
                Tempo.HIGH: 0.75,
                Tempo.VERY_HIGH: 0.95,
            }[tactic.tempo]
        )

        short_pass_bias = _clamp01(1.0 - (0.70 * directness_bias + 0.30 * risk_taking))

        shot_patience = _clamp01(
            {
                ShootingPolicy.SHOOT_LESS: 0.80,
                ShootingPolicy.BALANCED: 0.50,
                ShootingPolicy.SHOOT_MORE: 0.30,
                ShootingPolicy.SHOOT_AGGRESSIVELY: 0.15,
            }[tactic.shooting_policy]
        )

        through_ball_bias = _clamp01(
            0.25
            + 0.40
            * (
                1.0
                if tactic.final_third_focus == FinalThirdFocus.THROUGH_BALL_FOCUS
                else 0.0
            )
            + 0.10
            * (1.0 if tactic.attacking_focus == AttackingFocus.ATTACK_CENTRE else 0.0)
            + 0.10 * (1.0 - width_bias)
        )

        cross_bias = _clamp01(
            0.25
            + 0.35
            * (
                1.0
                if tactic.final_third_focus
                in (FinalThirdFocus.CROSS_EARLY, FinalThirdFocus.OVERLAP_WIDE)
                else 0.0
            )
            + 0.20 * width_bias
        )

        cutback_bias = _clamp01(
            0.20
            + 0.35
            * (
                1.0
                if tactic.final_third_focus == FinalThirdFocus.UNDERLAP_INSIDE
                else 0.0
            )
            + 0.10 * width_bias
        )

        dribble_creation_bias = _clamp01(
            0.20
            + 0.45
            * (1.0 if tactic.final_third_focus == FinalThirdFocus.DRIBBLE_MORE else 0.0)
            + 0.20
            * {
                DribblingRisk.VERY_CONSERVATIVE: 0.0,
                DribblingRisk.BALANCED: 0.5,
                DribblingRisk.AGGRESSIVE: 1.0,
            }[tactic.dribbling_risk]
        )

        long_shot_bias = _clamp01(
            0.15
            + 0.45
            * (
                1.0
                if tactic.final_third_focus == FinalThirdFocus.SHOOT_ON_SIGHT
                else 0.0
            )
            + 0.25 * (1.0 - shot_patience)
        )

        if tactic.attacking_focus == AttackingFocus.ATTACK_LEFT:
            attack_left_bias, attack_central_bias, attack_right_bias = 0.55, 0.25, 0.20
        elif tactic.attacking_focus == AttackingFocus.ATTACK_RIGHT:
            attack_left_bias, attack_central_bias, attack_right_bias = 0.20, 0.25, 0.55
        elif tactic.attacking_focus == AttackingFocus.ATTACK_CENTRE:
            attack_left_bias, attack_central_bias, attack_right_bias = 0.20, 0.60, 0.20
        elif tactic.attacking_focus == AttackingFocus.TARGET_HALF_SPACES:
            attack_left_bias, attack_central_bias, attack_right_bias = 0.30, 0.40, 0.30
        else:
            attack_left_bias, attack_central_bias, attack_right_bias = 0.33, 0.34, 0.33

        press_trigger_rate = _clamp01(
            {
                TransitionOnLoss.COUNTERPRESS: 0.90,
                TransitionOnLoss.DELAY: 0.60,
                TransitionOnLoss.REGROUP: 0.35,
                TransitionOnLoss.TACTICAL_FOUL: 0.75,
                TransitionOnLoss.DROP_DEEP_IMMEDIATELY: 0.15,
            }[tactic.transition_on_loss]
            * (0.7 + 0.6 * press_intensity_bias)
        )

        counter_trigger_bias = _clamp01(
            {
                TransitionOnWin.COUNTER_IMMEDIATELY: 0.90,
                TransitionOnWin.PROGRESS_SAFELY: 0.45,
                TransitionOnWin.HOLD_SHAPE: 0.15,
                TransitionOnWin.FEED_PLAYMAKER: 0.55,
                TransitionOnWin.FEED_WINGER: 0.65,
                TransitionOnWin.GO_LONG_TO_STRIKER: 0.80,
                TransitionOnWin.ATTACK_WEAK_SIDE: 0.70,
            }[tactic.transition_on_win]
        )

        counterpress_bias = _clamp01(
            {
                TransitionOnLoss.COUNTERPRESS: 0.95,
                TransitionOnLoss.DELAY: 0.60,
                TransitionOnLoss.REGROUP: 0.30,
                TransitionOnLoss.TACTICAL_FOUL: 0.75,
                TransitionOnLoss.DROP_DEEP_IMMEDIATELY: 0.10,
            }[tactic.transition_on_loss]
        )

        counter_speed_bias = _clamp01(
            0.5
            + 0.25
            * (
                1.0
                if tactic.transition_on_win
                in (
                    TransitionOnWin.COUNTER_IMMEDIATELY,
                    TransitionOnWin.GO_LONG_TO_STRIKER,
                )
                else 0.0
            )
            + 0.15 * (1.0 if tactic.tempo in (Tempo.HIGH, Tempo.VERY_HIGH) else 0.0)
            - 0.20
            * (1.0 if tactic.transition_on_win == TransitionOnWin.HOLD_SHAPE else 0.0)
        )

        set_piece_attacking_bias = _clamp01(
            {
                SetPieceAttack.SHORT_CORNERS: 0.20,
                SetPieceAttack.MIXED_CORNERS: 0.50,
                SetPieceAttack.NEAR_POST_CORNERS: 0.70,
                SetPieceAttack.FAR_POST_CORNERS: 0.70,
                SetPieceAttack.CROWD_GOALKEEPER: 0.80,
                SetPieceAttack.EDGE_OF_BOX_SETUP: 0.45,
                SetPieceAttack.TALL_PLAYER_TARGETING: 0.90,
                SetPieceAttack.REBOUND_HUNTING: 0.65,
            }[tactic.set_piece_attack]
        )

        set_piece_defensive_bias = _clamp01(
            {
                SetPieceDefense.ZONAL_MARKING: 0.0,
                SetPieceDefense.MIXED_MARKING: 0.5,
                SetPieceDefense.MAN_MARKING: 1.0,
                SetPieceDefense.LEAVE_PLAYERS_UP: 0.3,
                SetPieceDefense.FULL_RETREAT: 0.2,
                SetPieceDefense.COUNTER_SETUP: 0.4,
                SetPieceDefense.NEAR_POST_GUARD: 0.3,
            }[tactic.set_piece_defense]
        )

        return TacticalIdentity(
            risk_taking=float(risk_taking),
            directness_bias=float(directness_bias),
            vertical_progression_bias=float(vertical_progression_bias),
            short_pass_bias=float(short_pass_bias),
            width_bias=float(width_bias),
            attack_left_bias=float(attack_left_bias),
            attack_central_bias=float(attack_central_bias),
            attack_right_bias=float(attack_right_bias),
            through_ball_bias=float(through_ball_bias),
            cross_bias=float(cross_bias),
            cutback_bias=float(cutback_bias),
            dribble_creation_bias=float(dribble_creation_bias),
            long_shot_bias=float(long_shot_bias),
            shot_patience=float(shot_patience),
            defensive_line_height=float(defensive_line_height),
            press_intensity_bias=float(press_intensity_bias),
            press_trigger_rate=float(press_trigger_rate),
            defensive_width_bias=float(defensive_width_bias),
            compactness_bias=float(compactness_bias),
            marking_bias=float(marking_bias),
            tackling_aggression_bias=float(tackling_aggression_bias),
            counter_trigger_bias=float(counter_trigger_bias),
            counterpress_bias=float(counterpress_bias),
            counter_speed_bias=float(counter_speed_bias),
            set_piece_attacking_bias=float(set_piece_attacking_bias),
            set_piece_defensive_bias=float(set_piece_defensive_bias),
            possession_tilt=engine_knobs["possession_tilt"],
            pass_weight_mult=engine_knobs["pass_weight_mult"],
            turnover_weight_mult=engine_knobs["turnover_weight_mult"],
            shot_weight_mult=engine_knobs["shot_weight_mult"],
            shot_conversion_delta=engine_knobs["shot_conversion_delta"],
        )
