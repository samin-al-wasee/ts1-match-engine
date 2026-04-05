from models.tactic import TeamTactic
from models.tactic_attributes import (
    AttackingFocus,
    BuildUpStyle,
    Compactness,
    DefensiveLine,
    DefensiveWidth,
    DribblingRisk,
    FinalThirdFocus,
    FreeKickStrategy,
    LineOfEngagement,
    MarkingStyle,
    OverloadFocus,
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
    VerticalStretch,
    Width,
)
from models.tactical_identity import TacticalIdentity
from systems.tactical_identity_builder import TacticalIdentityBuilder


def make_tactic(
    *,
    build_up_style: BuildUpStyle = BuildUpStyle.MIXED_BUILD_UP,
    tempo: Tempo = Tempo.BALANCED,
    width: Width = Width.BALANCED,
    final_third_focus: FinalThirdFocus = FinalThirdFocus.MIXED_ATTACKING,
    attacking_focus: AttackingFocus = AttackingFocus.MIXED,
    defensive_line: DefensiveLine = DefensiveLine.STANDARD,
    line_of_engagement: LineOfEngagement = LineOfEngagement.MID_BLOCK,
    pressing_intensity: PressingIntensity = PressingIntensity.BALANCED,
    defensive_width: DefensiveWidth = DefensiveWidth.BALANCED,
    marking_style: MarkingStyle = MarkingStyle.MIXED,
    tackling_aggression: TacklingAggression = TacklingAggression.BALANCED,
    transition_on_win: TransitionOnWin = TransitionOnWin.PROGRESS_SAFELY,
    transition_on_loss: TransitionOnLoss = TransitionOnLoss.REGROUP,
    team_mentality: TeamMentality = TeamMentality.BALANCED,
    passing_risk: PassingRisk = PassingRisk.BALANCED,
    dribbling_risk: DribblingRisk = DribblingRisk.BALANCED,
    shooting_policy: ShootingPolicy = ShootingPolicy.BALANCED,
    compactness: Compactness = Compactness.BALANCED,
    vertical_stretch: VerticalStretch = VerticalStretch.BALANCED,
    overload_focus: OverloadFocus = OverloadFocus.NO_SPECIFIC_OVERLOAD,
    set_piece_attack: SetPieceAttack = SetPieceAttack.MIXED_CORNERS,
    set_piece_defense: SetPieceDefense = SetPieceDefense.MIXED_MARKING,
    free_kick_strategy: FreeKickStrategy = FreeKickStrategy.CROSS_INTO_BOX,
) -> TeamTactic:
    return TeamTactic(
        build_up_style=build_up_style,
        tempo=tempo,
        width=width,
        final_third_focus=final_third_focus,
        attacking_focus=attacking_focus,
        defensive_line=defensive_line,
        line_of_engagement=line_of_engagement,
        pressing_intensity=pressing_intensity,
        defensive_width=defensive_width,
        marking_style=marking_style,
        tackling_aggression=tackling_aggression,
        transition_on_win=transition_on_win,
        transition_on_loss=transition_on_loss,
        team_mentality=team_mentality,
        passing_risk=passing_risk,
        dribbling_risk=dribbling_risk,
        shooting_policy=shooting_policy,
        compactness=compactness,
        vertical_stretch=vertical_stretch,
        overload_focus=overload_focus,
        set_piece_attack=set_piece_attack,
        set_piece_defense=set_piece_defense,
        free_kick_strategy=free_kick_strategy,
    )


def test_build_full_returns_tactical_identity_instance():
    identity = TacticalIdentityBuilder.build_full(make_tactic())
    assert isinstance(identity, TacticalIdentity)


def test_engine_knobs_exact_values_for_known_profile():
    tactic = make_tactic(
        build_up_style=BuildUpStyle.BUILD_FROM_BACK,
        tempo=Tempo.HIGH,
        pressing_intensity=PressingIntensity.HIGH,
        team_mentality=TeamMentality.BALANCED,
    )

    identity = TacticalIdentityBuilder.build_full(tactic)

    assert identity.possession_tilt == 0.09
    assert identity.pass_weight_mult == 1.08
    assert identity.turnover_weight_mult == 1.06
    assert identity.shot_weight_mult == 1.02
    assert identity.shot_conversion_delta == -0.02


def test_engine_knobs_clamp_in_extreme_case():
    tactic = make_tactic(
        build_up_style=BuildUpStyle.LONG_BALL,
        tempo=Tempo.VERY_HIGH,
        pressing_intensity=PressingIntensity.EXTREME,
        team_mentality=TeamMentality.VERY_ATTACKING,
    )

    identity = TacticalIdentityBuilder.build_full(tactic)

    assert -0.20 <= identity.possession_tilt <= 0.20
    assert 0.80 <= identity.pass_weight_mult <= 1.20
    assert 0.80 <= identity.turnover_weight_mult <= 1.20
    assert 0.80 <= identity.shot_weight_mult <= 1.25
    assert -0.10 <= identity.shot_conversion_delta <= 0.10

    # Deterministic clamp outcome for turnover multiplier in this combo.
    assert identity.turnover_weight_mult == 1.2


def test_risk_taking_clamps_to_zero_for_ultra_safe_setup():
    tactic = make_tactic(
        passing_risk=PassingRisk.VERY_SAFE,
        dribbling_risk=DribblingRisk.VERY_CONSERVATIVE,
        team_mentality=TeamMentality.VERY_DEFENSIVE,
    )

    identity = TacticalIdentityBuilder.build_full(tactic)
    assert identity.risk_taking == 0.0


def test_risk_taking_clamps_to_one_for_ultra_risky_setup():
    tactic = make_tactic(
        passing_risk=PassingRisk.VERY_RISKY,
        dribbling_risk=DribblingRisk.AGGRESSIVE,
        team_mentality=TeamMentality.VERY_ATTACKING,
    )

    identity = TacticalIdentityBuilder.build_full(tactic)
    assert identity.risk_taking == 1.0


def test_attacking_focus_maps_to_directional_biases():
    left = TacticalIdentityBuilder.build_full(
        make_tactic(attacking_focus=AttackingFocus.ATTACK_LEFT)
    )
    centre = TacticalIdentityBuilder.build_full(
        make_tactic(attacking_focus=AttackingFocus.ATTACK_CENTRE)
    )
    right = TacticalIdentityBuilder.build_full(
        make_tactic(attacking_focus=AttackingFocus.ATTACK_RIGHT)
    )

    assert (
        left.attack_left_bias,
        left.attack_central_bias,
        left.attack_right_bias,
    ) == (
        0.55,
        0.25,
        0.20,
    )
    assert (
        centre.attack_left_bias,
        centre.attack_central_bias,
        centre.attack_right_bias,
    ) == (0.20, 0.60, 0.20)
    assert (
        right.attack_left_bias,
        right.attack_central_bias,
        right.attack_right_bias,
    ) == (0.20, 0.25, 0.55)


def test_final_third_focus_influences_chance_type_biases():
    through = TacticalIdentityBuilder.build_full(
        make_tactic(final_third_focus=FinalThirdFocus.THROUGH_BALL_FOCUS)
    )
    cross = TacticalIdentityBuilder.build_full(
        make_tactic(
            final_third_focus=FinalThirdFocus.CROSS_EARLY, width=Width.VERY_WIDE
        )
    )
    dribble = TacticalIdentityBuilder.build_full(
        make_tactic(
            final_third_focus=FinalThirdFocus.DRIBBLE_MORE,
            dribbling_risk=DribblingRisk.AGGRESSIVE,
        )
    )

    assert through.through_ball_bias > cross.through_ball_bias
    assert cross.cross_bias > through.cross_bias
    assert dribble.dribble_creation_bias > through.dribble_creation_bias


def test_set_piece_bias_mapping_matches_expected_levels():
    direct = TacticalIdentityBuilder.build_full(
        make_tactic(
            set_piece_attack=SetPieceAttack.TALL_PLAYER_TARGETING,
            set_piece_defense=SetPieceDefense.MAN_MARKING,
        )
    )
    short = TacticalIdentityBuilder.build_full(
        make_tactic(
            set_piece_attack=SetPieceAttack.SHORT_CORNERS,
            set_piece_defense=SetPieceDefense.ZONAL_MARKING,
        )
    )

    assert direct.set_piece_attacking_bias == 0.9
    assert direct.set_piece_defensive_bias == 1.0

    assert short.set_piece_attacking_bias == 0.2
    assert short.set_piece_defensive_bias == 0.0


def test_all_bias_outputs_stay_in_normalized_ranges():
    identity = TacticalIdentityBuilder.build_full(
        make_tactic(
            build_up_style=BuildUpStyle.COUNTER_BUILD_UP,
            tempo=Tempo.VERY_HIGH,
            width=Width.VERY_WIDE,
            final_third_focus=FinalThirdFocus.SHOOT_ON_SIGHT,
            attacking_focus=AttackingFocus.TARGET_HALF_SPACES,
            defensive_line=DefensiveLine.VERY_HIGH,
            pressing_intensity=PressingIntensity.EXTREME,
            defensive_width=DefensiveWidth.VERY_WIDE,
            marking_style=MarkingStyle.TIGHT_MAN_ORIENTED,
            tackling_aggression=TacklingAggression.VERY_AGGRESSIVE,
            transition_on_win=TransitionOnWin.COUNTER_IMMEDIATELY,
            transition_on_loss=TransitionOnLoss.COUNTERPRESS,
            team_mentality=TeamMentality.VERY_ATTACKING,
            passing_risk=PassingRisk.VERY_RISKY,
            dribbling_risk=DribblingRisk.AGGRESSIVE,
            shooting_policy=ShootingPolicy.SHOOT_AGGRESSIVELY,
            compactness=Compactness.VERY_COMPACT,
            set_piece_attack=SetPieceAttack.CROWD_GOALKEEPER,
            set_piece_defense=SetPieceDefense.MAN_MARKING,
        )
    )

    normalized_fields = [
        identity.risk_taking,
        identity.directness_bias,
        identity.vertical_progression_bias,
        identity.short_pass_bias,
        identity.width_bias,
        identity.attack_left_bias,
        identity.attack_central_bias,
        identity.attack_right_bias,
        identity.through_ball_bias,
        identity.cross_bias,
        identity.cutback_bias,
        identity.dribble_creation_bias,
        identity.long_shot_bias,
        identity.shot_patience,
        identity.defensive_line_height,
        identity.press_intensity_bias,
        identity.press_trigger_rate,
        identity.defensive_width_bias,
        identity.compactness_bias,
        identity.marking_bias,
        identity.tackling_aggression_bias,
        identity.counter_trigger_bias,
        identity.counterpress_bias,
        identity.counter_speed_bias,
        identity.set_piece_attacking_bias,
        identity.set_piece_defensive_bias,
    ]

    assert all(0.0 <= value <= 1.0 for value in normalized_fields)
