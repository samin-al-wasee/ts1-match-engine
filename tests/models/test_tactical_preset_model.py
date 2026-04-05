import pytest

from models.tactic import TeamTactic
from models.tactic_attributes import (
    BuildUpStyle,
    FinalThirdFocus,
    LineOfEngagement,
    PressingIntensity,
    TeamMentality,
)
from models.tactical_preset import TacticalPreset, TacticalPresetFactory


def test_factory_lists_include_expected_groupings():
    generic = TacticalPresetFactory.generic_presets()
    popular = TacticalPresetFactory.popular_presets()
    all_presets = TacticalPresetFactory.all_presets()

    assert TacticalPreset.POSSESSION_CONTROL in generic
    assert TacticalPreset.SET_PIECE_FOCUS in generic
    assert TacticalPreset.COMPACT_TRANSITIONS in generic
    assert TacticalPreset.POSITIONAL_PRESS in generic

    assert TacticalPreset.TIKI_TAKA in popular
    assert TacticalPreset.JOGA_BONITO in popular

    assert len(all_presets) == len(generic) + len(popular)


def test_factory_create_accepts_enum_and_string_forms():
    from_enum = TacticalPresetFactory.create(TacticalPreset.HIGH_PRESS)
    from_label = TacticalPresetFactory.create("High Press")
    from_slug = TacticalPresetFactory.create("high_press")
    from_kebab = TacticalPresetFactory.create("high-press")

    assert isinstance(from_enum, TeamTactic)
    assert from_enum.pressing_intensity == PressingIntensity.EXTREME

    assert from_label.pressing_intensity == PressingIntensity.EXTREME
    assert from_slug.pressing_intensity == PressingIntensity.EXTREME
    assert from_kebab.pressing_intensity == PressingIntensity.EXTREME


def test_factory_returns_new_tactic_instances_each_call():
    first = TacticalPresetFactory.create(TacticalPreset.BALANCED)
    second = TacticalPresetFactory.create(TacticalPreset.BALANCED)

    assert first is not second
    first.team_mentality = TeamMentality.ATTACKING
    assert second.team_mentality == TeamMentality.BALANCED


def test_factory_raises_helpful_error_for_unknown_preset():
    with pytest.raises(ValueError) as err:
        TacticalPresetFactory.create("ultra unknown profile")

    message = str(err.value)
    assert "Unknown tactical preset" in message
    assert "Available presets" in message


def test_selected_presets_map_to_expected_identity_shape():
    tiki = TacticalPresetFactory.create(TacticalPreset.TIKI_TAKA)
    counter = TacticalPresetFactory.create(TacticalPreset.COUNTER_ATTACK)
    joga = TacticalPresetFactory.create(TacticalPreset.JOGA_BONITO)

    assert tiki.build_up_style == BuildUpStyle.BUILD_FROM_BACK
    assert tiki.final_third_focus == FinalThirdFocus.WORK_BALL_INTO_BOX

    assert counter.build_up_style == BuildUpStyle.COUNTER_BUILD_UP
    assert counter.line_of_engagement == LineOfEngagement.MID_BLOCK

    assert joga.final_third_focus == FinalThirdFocus.DRIBBLE_MORE
    assert joga.line_of_engagement == LineOfEngagement.HIGH_BLOCK
