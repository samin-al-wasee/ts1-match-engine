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


def make_sample_tactic() -> TeamTactic:
    return TeamTactic(
        build_up_style=BuildUpStyle.BUILD_FROM_BACK,
        tempo=Tempo.HIGH,
        width=Width.WIDE,
        final_third_focus=FinalThirdFocus.THROUGH_BALL_FOCUS,
        attacking_focus=AttackingFocus.ATTACK_LEFT,
        defensive_line=DefensiveLine.HIGH,
        line_of_engagement=LineOfEngagement.HIGH_BLOCK,
        pressing_intensity=PressingIntensity.HIGH,
        defensive_width=DefensiveWidth.BALANCED,
        marking_style=MarkingStyle.MIXED,
        tackling_aggression=TacklingAggression.AGGRESSIVE,
        transition_on_win=TransitionOnWin.COUNTER_IMMEDIATELY,
        transition_on_loss=TransitionOnLoss.COUNTERPRESS,
        team_mentality=TeamMentality.POSITIVE,
        passing_risk=PassingRisk.RISKY,
        dribbling_risk=DribblingRisk.AGGRESSIVE,
        shooting_policy=ShootingPolicy.SHOOT_MORE,
        compactness=Compactness.COMPACT,
        vertical_stretch=VerticalStretch.STRETCHED,
        overload_focus=OverloadFocus.LEFT_OVERLOAD,
        set_piece_attack=SetPieceAttack.FAR_POST_CORNERS,
        set_piece_defense=SetPieceDefense.MIXED_MARKING,
        free_kick_strategy=FreeKickStrategy.CROSS_INTO_BOX,
    )


def test_team_tactic_stores_all_fields_exactly():
    tactic = make_sample_tactic()

    assert tactic.build_up_style == BuildUpStyle.BUILD_FROM_BACK
    assert tactic.tempo == Tempo.HIGH
    assert tactic.width == Width.WIDE
    assert tactic.final_third_focus == FinalThirdFocus.THROUGH_BALL_FOCUS
    assert tactic.attacking_focus == AttackingFocus.ATTACK_LEFT

    assert tactic.defensive_line == DefensiveLine.HIGH
    assert tactic.line_of_engagement == LineOfEngagement.HIGH_BLOCK
    assert tactic.pressing_intensity == PressingIntensity.HIGH
    assert tactic.defensive_width == DefensiveWidth.BALANCED
    assert tactic.marking_style == MarkingStyle.MIXED
    assert tactic.tackling_aggression == TacklingAggression.AGGRESSIVE

    assert tactic.transition_on_win == TransitionOnWin.COUNTER_IMMEDIATELY
    assert tactic.transition_on_loss == TransitionOnLoss.COUNTERPRESS

    assert tactic.team_mentality == TeamMentality.POSITIVE
    assert tactic.passing_risk == PassingRisk.RISKY
    assert tactic.dribbling_risk == DribblingRisk.AGGRESSIVE
    assert tactic.shooting_policy == ShootingPolicy.SHOOT_MORE

    assert tactic.compactness == Compactness.COMPACT
    assert tactic.vertical_stretch == VerticalStretch.STRETCHED
    assert tactic.overload_focus == OverloadFocus.LEFT_OVERLOAD

    assert tactic.set_piece_attack == SetPieceAttack.FAR_POST_CORNERS
    assert tactic.set_piece_defense == SetPieceDefense.MIXED_MARKING
    assert tactic.free_kick_strategy == FreeKickStrategy.CROSS_INTO_BOX


def test_team_tactic_summary_contains_all_sections_and_values():
    tactic = make_sample_tactic()
    summary = tactic.summary()

    expected_lines = [
        "Build-Up Style: Build From Back",
        "Tempo: High",
        "Width: Wide",
        "Final Third Focus: Through Ball Focus",
        "Attacking Focus: Attack Left",
        "Defensive Line: High",
        "Line of Engagement: High Block",
        "Pressing Intensity: High",
        "Defensive Width: Balanced",
        "Marking Style: Mixed",
        "Tackling Aggression: Aggressive",
        "Transition on Win: Counter Immediately",
        "Transition on Loss: Counterpress",
        "Team Mentality: Positive",
        "Passing Risk: Risky",
        "Dribbling Risk: Aggressive",
        "Shooting Policy: Shoot More",
        "Compactness: Compact",
        "Vertical Stretch: Stretched",
        "Overload Focus: Left overload",
        "Set Piece Attack: Far-post corners",
        "Set Piece Defense: Mixed marking",
        "Free Kick Strategy: Cross into box",
    ]

    for line in expected_lines:
        assert line in summary


def test_team_tactic_summary_has_expected_line_count():
    summary = make_sample_tactic().summary()
    lines = summary.splitlines()
    assert len(lines) == 23
