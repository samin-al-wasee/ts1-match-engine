from dataclasses import FrozenInstanceError

import pytest

from models.tactical_identity import TacticalIdentity


def test_tactical_identity_defaults_match_model_contract():
    identity = TacticalIdentity()

    assert identity.risk_taking == 0.50
    assert identity.directness_bias == 0.50
    assert identity.vertical_progression_bias == 0.50
    assert identity.short_pass_bias == 0.50
    assert identity.width_bias == 0.50

    assert identity.attack_left_bias == 0.33
    assert identity.attack_central_bias == 0.34
    assert identity.attack_right_bias == 0.33

    assert identity.through_ball_bias == 0.35
    assert identity.cross_bias == 0.30
    assert identity.cutback_bias == 0.25
    assert identity.dribble_creation_bias == 0.25
    assert identity.long_shot_bias == 0.20
    assert identity.shot_patience == 0.50

    assert identity.defensive_line_height == 0.50
    assert identity.press_intensity_bias == 0.50
    assert identity.press_trigger_rate == 0.50
    assert identity.defensive_width_bias == 0.50
    assert identity.compactness_bias == 0.50
    assert identity.marking_bias == 0.00
    assert identity.tackling_aggression_bias == 0.50

    assert identity.counter_trigger_bias == 0.50
    assert identity.counterpress_bias == 0.50
    assert identity.counter_speed_bias == 0.50

    assert identity.set_piece_attacking_bias == 0.50
    assert identity.set_piece_defensive_bias == 0.00

    assert identity.possession_tilt == 0.0
    assert identity.pass_weight_mult == 1.0
    assert identity.turnover_weight_mult == 1.0
    assert identity.shot_weight_mult == 1.0
    assert identity.shot_conversion_delta == 0.0


def test_tactical_identity_allows_custom_values_at_initialization():
    identity = TacticalIdentity(
        risk_taking=0.78,
        width_bias=0.72,
        attack_central_bias=0.61,
        press_intensity_bias=0.83,
        possession_tilt=0.12,
        shot_weight_mult=1.18,
    )

    assert identity.risk_taking == 0.78
    assert identity.width_bias == 0.72
    assert identity.attack_central_bias == 0.61
    assert identity.press_intensity_bias == 0.83
    assert identity.possession_tilt == 0.12
    assert identity.shot_weight_mult == 1.18


def test_tactical_identity_is_frozen_dataclass():
    identity = TacticalIdentity()

    with pytest.raises(FrozenInstanceError):
        identity.risk_taking = 0.9
