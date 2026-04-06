from datetime import date
from typing import Any

from models.duty import Duty
from models.player import Player
from models.player_attributes import Footedness
from models.position import Position
from models.role import Role


def make_player(**overrides: Any) -> Player:
    return Player(
        id=overrides.get("id", 9),
        name=overrides.get("name", "Alex Striker"),
        date_of_birth=overrides.get("date_of_birth", date(2000, 6, 15)),
        height_cm=overrides.get("height_cm", 182.0),
        weight_kg=overrides.get("weight_kg", 76.0),
        position=overrides.get("position", Position.ST),
        role=overrides.get("role", Role.ADVANCED_FORWARD),
        duty=overrides.get("duty", Duty.ATTACK),
        footedness=overrides.get("footedness", Footedness.LEFT),
        technical=overrides.get("technical", {}),
        mental=overrides.get("mental", {}),
        physical=overrides.get("physical", {}),
        hidden=overrides.get("hidden", {}),
        condition=overrides.get("condition", {}),
    )


def test_player_calculate_age_before_and_after_birthday():
    player = make_player(date_of_birth=date(2000, 6, 15))

    assert player._calculate_age(on_date=date(2026, 6, 14)) == 25
    assert player._calculate_age(on_date=date(2026, 6, 15)) == 26
    assert player._calculate_age(on_date=date(2026, 7, 1)) == 26


def test_player_height_and_weight_helpers_are_converted_correctly():
    player = make_player(height_cm=182.0, weight_kg=76.0)

    assert player.height_m == 1.82
    assert player.height_ft_inch == "5'11\""
    assert player.weight_lb == 167.6


def test_player_overall_summary_includes_core_identity_fields():
    player = make_player(
        name="Maya Creator",
        position=Position.CM,
        role=Role.MEZZALA_ADVANCED_WIDE_MIDFIELDER,
        duty=Duty.SUPPORT,
        footedness=Footedness.RIGHT,
    )

    assert player.overall_summary() == (
        "Maya Creator (CM) - Mezzala (Advanced Wide Midfielder) [Support] - Right"
    )


def test_player_attribute_buckets_use_independent_default_dicts():
    p1 = make_player(id=1)
    p2 = make_player(id=2)

    p1.technical["Short Passing"] = 81

    assert p2.technical == {}
    assert p1.technical["Short Passing"] == 81
