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


def _enum_values_are_unique(enum_cls) -> None:
    values = [member.value for member in enum_cls]
    assert len(values) == len(set(values))


def test_attacking_enums_have_expected_spec_values():
    assert BuildUpStyle.BUILD_FROM_BACK.value == "Build From Back"
    assert BuildUpStyle.MIXED_BUILD_UP.value == "Mixed Build-Up"
    assert BuildUpStyle.DIRECT_PROGRESSION.value == "Direct Progression"
    assert BuildUpStyle.LONG_BALL.value == "Long Ball"
    assert BuildUpStyle.COUNTER_BUILD_UP.value == "Counter Build-Up"

    assert Tempo.VERY_LOW.value == "Very Low"
    assert Tempo.VERY_HIGH.value == "Very High"

    assert Width.VERY_NARROW.value == "Very Narrow"
    assert Width.VERY_WIDE.value == "Very Wide"

    assert FinalThirdFocus.THROUGH_BALL_FOCUS.value == "Through Ball Focus"
    assert FinalThirdFocus.DRIBBLE_MORE.value == "Dribble More"

    assert AttackingFocus.ATTACK_CENTRE.value == "Attack Centre"
    assert AttackingFocus.TARGET_HALF_SPACES.value == "Target Half-Spaces"


def test_defensive_enums_have_expected_spec_values():
    assert DefensiveLine.VERY_DEEP.value == "Very Deep"
    assert DefensiveLine.VERY_HIGH.value == "Very High"

    assert LineOfEngagement.LOW_BLOCK.value == "Low Block"
    assert LineOfEngagement.FULL_PRESS.value == "Full Press"

    assert PressingIntensity.EXTREME.value == "Extreme"

    assert DefensiveWidth.NARROW.value == "Narrow"
    assert DefensiveWidth.VERY_WIDE.value == "Very Wide"

    assert MarkingStyle.TIGHT_MAN_ORIENTED.value == "Tight Man-Oriented"

    assert TacklingAggression.STAY_ON_FEET.value == "Stay On Feet"
    assert TacklingAggression.VERY_AGGRESSIVE.value == "Very Aggressive"


def test_transition_risk_space_and_set_piece_enums_have_expected_values():
    assert TransitionOnWin.COUNTER_IMMEDIATELY.value == "Counter Immediately"
    assert TransitionOnWin.ATTACK_WEAK_SIDE.value == "Attack Weak Side"

    assert TransitionOnLoss.COUNTERPRESS.value == "Counterpress"
    assert TransitionOnLoss.DROP_DEEP_IMMEDIATELY.value == "Drop Deep Immediately"

    assert TeamMentality.VERY_DEFENSIVE.value == "Very Defensive"
    assert TeamMentality.VERY_ATTACKING.value == "Very Attacking"

    assert PassingRisk.VERY_SAFE.value == "Very Safe"
    assert PassingRisk.VERY_RISKY.value == "Very Risky"

    assert DribblingRisk.VERY_CONSERVATIVE.value == "Very Conservative"
    assert DribblingRisk.AGGRESSIVE.value == "Aggressive"

    assert ShootingPolicy.SHOOT_LESS.value == "Shoot Less"
    assert ShootingPolicy.SHOOT_AGGRESSIVELY.value == "Shoot Aggressively"

    assert Compactness.VERY_COMPACT.value == "Very Compact"
    assert Compactness.VERY_LOOSE.value == "Very Loose"

    assert VerticalStretch.COMPRESSED.value == "Compressed"
    assert VerticalStretch.STRETCHED.value == "Stretched"

    assert OverloadFocus.LEFT_OVERLOAD.value == "Left overload"
    assert OverloadFocus.NO_SPECIFIC_OVERLOAD.value == "No specific overload"

    assert SetPieceAttack.NEAR_POST_CORNERS.value == "Near-post corners"
    assert SetPieceAttack.REBOUND_HUNTING.value == "Rebound hunting"

    assert SetPieceDefense.ZONAL_MARKING.value == "Zonal marking"
    assert SetPieceDefense.COUNTER_SETUP.value == "Counter setup"

    assert FreeKickStrategy.SHOOT_DIRECT.value == "Shoot direct"
    assert FreeKickStrategy.FAST_RESTART.value == "Fast restart"


def test_all_tactic_attribute_enums_have_unique_values():
    for enum_cls in (
        BuildUpStyle,
        Tempo,
        Width,
        FinalThirdFocus,
        AttackingFocus,
        DefensiveLine,
        LineOfEngagement,
        PressingIntensity,
        DefensiveWidth,
        MarkingStyle,
        TacklingAggression,
        TransitionOnWin,
        TransitionOnLoss,
        TeamMentality,
        PassingRisk,
        DribblingRisk,
        ShootingPolicy,
        Compactness,
        VerticalStretch,
        OverloadFocus,
        SetPieceAttack,
        SetPieceDefense,
        FreeKickStrategy,
    ):
        _enum_values_are_unique(enum_cls)
