from models.player_attributes import (
    ConditionAttr,
    Footedness,
    HiddenAttr,
    MentalAttr,
    PhysicalAttr,
    TechnicalAttr,
    get_player_attr,
)


def test_get_player_attr_returns_default_when_bucket_missing_or_key_absent():
    assert get_player_attr(None, TechnicalAttr.CROSSING) == 50
    assert get_player_attr({}, TechnicalAttr.CROSSING, default=42) == 42


def test_get_player_attr_supports_normal_case_and_snake_case_keys():
    bucket = {
        "Short Passing": 78,
        "long_passing": 72,
        "set_piece_delivery": 69,
    }

    assert get_player_attr(bucket, TechnicalAttr.SHORT_PASSING) == 78
    assert get_player_attr(bucket, "long-passing") == 72
    assert get_player_attr(bucket, "Set Piece Delivery") == 69


def test_get_player_attr_keeps_passing_short_passing_backward_compatibility():
    old_bucket = {"passing": 74}
    new_bucket = {"Short Passing": 82}

    assert get_player_attr(old_bucket, "short_passing") == 74
    assert get_player_attr(new_bucket, "passing") == 82


def test_player_attribute_enums_use_normal_case_values():
    assert TechnicalAttr.SHORT_PASSING.value == "Short Passing"
    assert TechnicalAttr.GK_ONE_ON_ONES.value == "GK One On Ones"

    assert MentalAttr.TACTICAL_AWARENESS.value == "Tactical Awareness"
    assert PhysicalAttr.NATURAL_FITNESS.value == "Natural Fitness"
    assert ConditionAttr.MATCH_FITNESS.value == "Match Fitness"
    assert HiddenAttr.CONSISTENCY_UNDER_PRESSURE.value == "Consistency Under Pressure"
    assert Footedness.LEFT.value == "Left"
