from models.tactic import TeamTactic
from models.tactic_attributes import (
    BuildUpStyle,
    ChanceCreationStyle,
    CounterSpeed,
    CrossingStyle,
    DefensiveLine,
    DefensiveWidth,
    DribblingTendency,
    FinalThirdFocus,
    LineCompactness,
    MarkingStyle,
    Mentality,
    PassingDirectness,
    PressingIntensity,
    PressTrigger,
    SetPieceAttackingStyle,
    SetPieceDefensiveStyle,
    ShootingTendency,
    TacklingStyle,
    Tempo,
    TransitionOnLoss,
    TransitionOnWin,
    Width,
)
from models.tactical_identity import TacticalIdentity, TacticalIdentityV1


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _clamp01(x: float) -> float:
    return _clamp(x, 0.0, 1.0)


def _is(cond: bool) -> float:
    return 1.0 if cond else 0.0


def _scale_5(value, very_low, low, mid, high, very_high) -> float:
    """
    Map a 5-level enum to [-1, +1]:
      very_low=-1, low=-0.5, mid=0, high=+0.5, very_high=+1
    """
    if value == very_low:
        return -1.0
    if value == low:
        return -0.5
    if value == mid:
        return 0.0
    if value == high:
        return 0.5
    if value == very_high:
        return 1.0
    return 0.0


def _scale_3(value, low, mid, high) -> float:
    """Map a 3-level enum to [-1, 0, +1]."""
    if value == low:
        return -1.0
    if value == mid:
        return 0.0
    if value == high:
        return 1.0
    return 0.0


class TacticalIdentityBuilder:
    """
    Builds tactical identity objects from a TeamTactic.

    - build_v1(): returns TacticalIdentityV1 (wired into current minute-loop engine)
    - build_full(): returns TacticalIdentity (full Concept Layer 1 catalog; not fully wired yet)
    """

    @staticmethod
    def build_v1(tactic: TeamTactic) -> TacticalIdentityV1:
        """
        V1 intentionally maps only fields that the current basic engine can consume:
        - build_up_style
        - tempo
        - pressing_intensity
        - mentality

        Other TeamTactic fields are intentionally ignored in V1.
        """
        possession_tilt = 0.0
        pass_mult = 1.0
        turnover_mult = 1.0
        shot_mult = 1.0
        shot_conv_delta = 0.0

        # build_up_style
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

        # tempo
        if tactic.tempo == Tempo.HIGH:
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

        # pressing_intensity
        if tactic.pressing_intensity == PressingIntensity.HIGH:
            possession_tilt += 0.04
            turnover_mult += 0.03
        elif tactic.pressing_intensity == PressingIntensity.VERY_HIGH:
            # Previously the doc/builder used "Extreme" but the enum has VERY_HIGH
            possession_tilt += 0.06
            turnover_mult += 0.06
            shot_mult += 0.02
            shot_conv_delta -= 0.01
        elif tactic.pressing_intensity == PressingIntensity.LOW:
            possession_tilt -= 0.04

        # mentality
        if tactic.mentality == Mentality.ATTACKING:
            shot_mult += 0.06
            shot_conv_delta += 0.02
        elif tactic.mentality == Mentality.DEFENSIVE:
            shot_mult -= 0.05
            shot_conv_delta -= 0.01
            # for V1 we bias slightly toward control (not ceding)
            possession_tilt += 0.02

        # Clamp values to keep them sane for V1
        possession_tilt = _clamp(possession_tilt, -0.20, 0.20)
        pass_mult = _clamp(pass_mult, 0.80, 1.20)
        turnover_mult = _clamp(turnover_mult, 0.80, 1.20)
        shot_mult = _clamp(shot_mult, 0.80, 1.25)
        shot_conv_delta = _clamp(shot_conv_delta, -0.10, 0.10)

        return TacticalIdentityV1(
            possession_tilt=possession_tilt,
            pass_weight_mult=pass_mult,
            turnover_weight_mult=turnover_mult,
            shot_weight_mult=shot_mult,
            shot_conversion_delta=shot_conv_delta,
        )

    @staticmethod
    def build_full(tactic: TeamTactic) -> TacticalIdentity:
        """
        Full catalog mapping (Concept Layer 1).
        This does not mean the engine uses all of it yet; it just makes the mapping complete and deterministic.
        """
        # --- Common scalars ---
        tempo_factor = _scale_5(
            tactic.tempo,
            Tempo.VERY_LOW,
            Tempo.LOW,
            Tempo.BALANCED,
            Tempo.HIGH,
            Tempo.VERY_HIGH,
        )

        _press_intensity_factor = _scale_5(
            tactic.pressing_intensity,
            PressingIntensity.VERY_LOW,
            PressingIntensity.LOW,
            PressingIntensity.STANDARD,
            PressingIntensity.HIGH,
            PressingIntensity.VERY_HIGH,
        )

        width_bias = _clamp01(
            {
                Width.VERY_NARROW: 0.0,
                Width.NARROW: 0.25,
                Width.BALANCED: 0.5,
                Width.WIDE: 0.75,
                Width.VERY_WIDE: 1.0,
            }.get(tactic.width, 0.5)
        )

        defensive_line_height = _clamp01(
            {
                DefensiveLine.VERY_DEEP: 0.0,
                DefensiveLine.DEEP: 0.25,
                DefensiveLine.STANDARD: 0.5,
                DefensiveLine.HIGH: 0.75,
                DefensiveLine.VERY_HIGH: 1.0,
            }.get(tactic.defensive_line, 0.5)
        )

        defensive_width_bias = _clamp01(
            {
                DefensiveWidth.VERY_NARROW: 0.0,
                DefensiveWidth.NARROW: 0.25,
                DefensiveWidth.STANDARD: 0.5,
                DefensiveWidth.WIDE: 0.75,
                DefensiveWidth.VERY_WIDE: 1.0,
            }.get(tactic.defensive_width, 0.5)
        )

        compactness_bias = _clamp01(
            {
                LineCompactness.VERY_LOOSE: 0.0,
                LineCompactness.LOOSE: 0.25,
                LineCompactness.STANDARD: 0.5,
                LineCompactness.COMPACT: 0.75,
                LineCompactness.VERY_COMPACT: 1.0,
            }.get(tactic.line_compactness, 0.5)
        )

        marking_bias = _clamp01(
            {
                MarkingStyle.ZONAL: 0.0,
                MarkingStyle.MIXED: 0.5,
                MarkingStyle.MAN: 1.0,
            }.get(tactic.marking_style, 0.0)
        )

        tackling_aggression_bias = _clamp01(
            {
                TacklingStyle.CAUTIOUS: 0.2,
                TacklingStyle.NORMAL: 0.5,
                TacklingStyle.AGGRESSIVE: 0.85,
            }.get(tactic.tackling_style, 0.5)
        )

        dribbling_factor = _scale_3(
            tactic.dribbling_tendency,
            DribblingTendency.RARELY,
            DribblingTendency.SITUATIONAL,
            DribblingTendency.OFTEN,
        )
        dribbling_factor_pos = _clamp01(
            (dribbling_factor + 1.0) / 2.0
        )  # [-1,1] -> [0,1]

        passing_directness_factor = {
            PassingDirectness.VERY_SHORT: -1.0,
            PassingDirectness.SHORT: -0.5,
            PassingDirectness.MIXED: 0.0,
            PassingDirectness.DIRECT: 0.5,
            PassingDirectness.VERY_DIRECT: 1.0,
        }.get(tactic.passing_directness, 0.0)

        # mentality factors
        mentality_attack_factor = {
            Mentality.ULTRA_DEFENSIVE: -1.0,
            Mentality.DEFENSIVE: -0.5,
            Mentality.BALANCED: 0.0,
            Mentality.ATTACKING: 0.6,
            Mentality.ULTRA_ATTACKING: 1.0,
        }.get(tactic.mentality, 0.0)

        _mentality_control_factor = {
            Mentality.ULTRA_DEFENSIVE: 0.6,
            Mentality.DEFENSIVE: 0.4,
            Mentality.BALANCED: 0.0,
            Mentality.ATTACKING: -0.2,
            Mentality.ULTRA_ATTACKING: -0.4,
        }.get(tactic.mentality, 0.0)

        # build_up style factors
        build_up_style_factor = {
            BuildUpStyle.BUILD_FROM_BACK: 1.0,
            BuildUpStyle.MIXED_BUILD_UP: 0.3,
            BuildUpStyle.DIRECT_BUILD_UP: -0.3,
            BuildUpStyle.LONG_BALL: -1.0,
        }.get(tactic.build_up_style, 0.0)

        # chance creation style "risk" and "quality" flavors
        chance_creation_risk_factor = {
            ChanceCreationStyle.PATIENT_COMBINATIONS: -0.6,
            ChanceCreationStyle.MIXED: 0.0,
            ChanceCreationStyle.FAST_VERTICAL: 0.8,
            ChanceCreationStyle.SECOND_BALLS: 0.4,
            ChanceCreationStyle.WIDE_OVERLOADS: 0.2,
            ChanceCreationStyle.ISOLATIONS_1V1: 0.3,
        }.get(tactic.chance_creation_style, 0.0)

        _chance_creation_quality_factor = {
            ChanceCreationStyle.PATIENT_COMBINATIONS: 0.5,
            ChanceCreationStyle.WIDE_OVERLOADS: 0.2,
            ChanceCreationStyle.MIXED: 0.0,
            ChanceCreationStyle.FAST_VERTICAL: -0.1,
            ChanceCreationStyle.SECOND_BALLS: -0.2,
            ChanceCreationStyle.ISOLATIONS_1V1: 0.1,
        }.get(tactic.chance_creation_style, 0.0)

        # shooting tendency factor used by "shot patience"
        shot_patience = _clamp01(
            {
                ShootingTendency.WORK_BALL_INTO_BOX: 0.85,
                ShootingTendency.MIXED_SHOOTING: 0.50,
                ShootingTendency.SHOOT_ON_SIGHT: 0.20,
            }.get(tactic.shooting_tendency, 0.50)
        )

        # press trigger base
        base_press_trigger = {
            PressTrigger.RARE: 0.20,
            PressTrigger.STANDARD: 0.50,
            PressTrigger.AGGRESSIVE: 0.75,
            PressTrigger.CONSTANT: 0.95,
        }.get(tactic.press_trigger, 0.50)

        press_intensity_bias = _clamp01(
            {
                PressingIntensity.VERY_LOW: 0.0,
                PressingIntensity.LOW: 0.25,
                PressingIntensity.STANDARD: 0.5,
                PressingIntensity.HIGH: 0.75,
                PressingIntensity.VERY_HIGH: 1.0,
            }.get(tactic.pressing_intensity, 0.5)
        )

        press_trigger_rate = _clamp01(
            base_press_trigger * (0.7 + 0.6 * press_intensity_bias)
        )

        # transitions
        counter_trigger_bias = _clamp01(
            {
                TransitionOnWin.RESET_SHAPE: 0.10,
                TransitionOnWin.HOLD_POSSESSION: 0.30,
                TransitionOnWin.COUNTER_IF_ON: 0.60,
                TransitionOnWin.COUNTER_IMMEDIATELY: 0.90,
            }.get(tactic.transition_on_win, 0.50)
        )

        counterpress_bias = _clamp01(
            {
                TransitionOnLoss.FALL_BACK: 0.10,
                TransitionOnLoss.REGROUP: 0.30,
                TransitionOnLoss.COUNTERPRESS_IF_ON: 0.60,
                TransitionOnLoss.COUNTERPRESS: 0.90,
            }.get(tactic.transition_on_loss, 0.50)
        )

        counter_speed_bias = _clamp01(
            {
                CounterSpeed.SLOW: 0.20,
                CounterSpeed.NORMAL: 0.50,
                CounterSpeed.FAST: 0.75,
                CounterSpeed.VERY_FAST: 0.90,
            }.get(tactic.counter_speed, 0.50)
        )

        # set pieces
        set_piece_attacking_bias = _clamp01(
            {
                SetPieceAttackingStyle.SHORT_ROUTINES: 0.20,
                SetPieceAttackingStyle.MIXED_ROUTINES: 0.50,
                SetPieceAttackingStyle.DELIVERY_TO_BOX: 0.85,
            }.get(tactic.set_piece_attacking_style, 0.50)
        )

        set_piece_defensive_bias = _clamp01(
            {
                SetPieceDefensiveStyle.ZONAL: 0.0,
                SetPieceDefensiveStyle.MIXED: 0.5,
                SetPieceDefensiveStyle.MAN: 1.0,
            }.get(tactic.set_piece_defensive_style, 0.0)
        )

        # --- Build-up/progression outputs ---
        directness_bias = _clamp01(
            0.5 + 0.25 * passing_directness_factor + 0.15 * (-build_up_style_factor)
        )
        vertical_progression_bias = _clamp01(
            0.5 + 0.20 * passing_directness_factor + 0.10 * tempo_factor
        )
        short_pass_bias = _clamp01(1.0 - directness_bias)

        # --- Risk taking ---
        risk_taking = _clamp01(
            0.50
            + 0.18 * tempo_factor
            + 0.16 * passing_directness_factor
            + 0.12 * mentality_attack_factor
            + 0.08 * chance_creation_risk_factor
        )

        # --- Chance type biases ---
        crossing_style_factor = _clamp01(
            {
                CrossingStyle.EARLY_CROSSES: 0.80,
                CrossingStyle.MIXED_CROSSES: 0.50,
                CrossingStyle.BYLINE_CUTBACKS: 0.20,
            }.get(tactic.crossing_style, 0.50)
        )

        final_third_focus = tactic.final_third_focus
        through_ball_bias = _clamp01(
            0.35
            + 0.35 * _is(final_third_focus == FinalThirdFocus.THROUGH_BALL_FOCUS)
            + 0.15
            * _is(tactic.chance_creation_style == ChanceCreationStyle.FAST_VERTICAL)
            + 0.10 * (1.0 - width_bias)
            + 0.05 * _clamp01((passing_directness_factor + 1.0) / 2.0)
        )

        cross_bias = _clamp01(
            0.30
            + 0.35 * _is(final_third_focus == FinalThirdFocus.CROSSING_FOCUS)
            + 0.15 * crossing_style_factor
            + 0.15 * width_bias
            + 0.10
            * _is(tactic.chance_creation_style == ChanceCreationStyle.WIDE_OVERLOADS)
        )

        cutback_bias = _clamp01(
            0.25
            + 0.40 * _is(final_third_focus == FinalThirdFocus.CUTBACK_FOCUS)
            + 0.20 * _is(tactic.crossing_style == CrossingStyle.BYLINE_CUTBACKS)
            + 0.10 * dribbling_factor_pos
            + 0.05 * width_bias
        )

        dribble_creation_bias = _clamp01(
            0.25
            + 0.35 * _is(final_third_focus == FinalThirdFocus.DRIBBLE_FOCUS)
            + 0.20
            * _is(tactic.chance_creation_style == ChanceCreationStyle.ISOLATIONS_1V1)
            + 0.20 * dribbling_factor_pos
        )

        long_shot_bias = _clamp01(
            0.20
            + 0.40 * _is(final_third_focus == FinalThirdFocus.SHOOTING_FOCUS)
            + 0.25 * _is(tactic.shooting_tendency == ShootingTendency.SHOOT_ON_SIGHT)
            + 0.10
            * _is(tactic.chance_creation_style == ChanceCreationStyle.SECOND_BALLS)
        )

        # --- Route biases (left/central/right) ---
        # With no side-specific tactic inputs, derive a central preference from width + through-ball vs crossing.
        central_preference = _clamp01(
            0.50
            + 0.20 * (1.0 - width_bias)
            + 0.15 * _is(final_third_focus == FinalThirdFocus.THROUGH_BALL_FOCUS)
            - 0.15 * _is(final_third_focus == FinalThirdFocus.CROSSING_FOCUS)
        )
        attack_central_bias = central_preference
        side_total = 1.0 - attack_central_bias
        attack_left_bias = side_total / 2.0
        attack_right_bias = side_total / 2.0

        return TacticalIdentity(
            risk_taking=risk_taking,
            directness_bias=directness_bias,
            vertical_progression_bias=vertical_progression_bias,
            short_pass_bias=short_pass_bias,
            width_bias=width_bias,
            attack_left_bias=attack_left_bias,
            attack_central_bias=attack_central_bias,
            attack_right_bias=attack_right_bias,
            through_ball_bias=through_ball_bias,
            cross_bias=cross_bias,
            cutback_bias=cutback_bias,
            dribble_creation_bias=dribble_creation_bias,
            long_shot_bias=long_shot_bias,
            shot_patience=shot_patience,
            defensive_line_height=defensive_line_height,
            press_intensity_bias=press_intensity_bias,
            press_trigger_rate=press_trigger_rate,
            defensive_width_bias=defensive_width_bias,
            compactness_bias=compactness_bias,
            marking_bias=marking_bias,
            tackling_aggression_bias=tackling_aggression_bias,
            counter_trigger_bias=counter_trigger_bias,
            counterpress_bias=counterpress_bias,
            counter_speed_bias=counter_speed_bias,
            set_piece_attacking_bias=set_piece_attacking_bias,
            set_piece_defensive_bias=set_piece_defensive_bias,
        )
