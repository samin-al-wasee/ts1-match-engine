from models.tactic import TeamTactic
from systems.tactical_identity_builder import TacticalIdentityBuilder


def _base_tactic(**overrides) -> TeamTactic:
    """
    Create a baseline tactic with known values so tests are deterministic.
    """
    base = dict(
        mentality="Balanced",
        build_up_style="Build From Back",
        tempo="High",
        width="Wide",
        attacking_focus="Attack Left",
        defensive_line="High",
        pressing_intensity="High",
        transition_on_win="Counter Immediately",
        transition_on_loss="Counterpress",
    )
    base.update(overrides)
    return TeamTactic(**base)


def test_build_v1_returns_identity_with_expected_fields():
    tactic = _base_tactic()
    ident = TacticalIdentityBuilder.build_v1(tactic)

    # Existence / type checks
    assert hasattr(ident, "possession_tilt")
    assert hasattr(ident, "pass_weight_mult")
    assert hasattr(ident, "turnover_weight_mult")
    assert hasattr(ident, "shot_weight_mult")
    assert hasattr(ident, "shot_conversion_delta")

    assert isinstance(ident.possession_tilt, float)
    assert isinstance(ident.pass_weight_mult, float)
    assert isinstance(ident.turnover_weight_mult, float)
    assert isinstance(ident.shot_weight_mult, float)
    assert isinstance(ident.shot_conversion_delta, float)


def test_build_v1_baseline_mapping_build_from_back_high_press_high_tempo():
    """
    This matches the baseline tactic in main.py:
    - Build From Back
    - High tempo
    - High pressing
    - Balanced mentality

    We don't assert exact values too tightly unless you want hard guarantees;
    we assert directionality and that values are within clamps.
    """
    tactic = _base_tactic(
        build_up_style="Build From Back",
        tempo="High",
        pressing_intensity="High",
        mentality="Balanced",
    )
    ident = TacticalIdentityBuilder.build_v1(tactic)

    # Directional expectations based on docs:
    assert ident.possession_tilt > 0.0  # build from back + pressing
    assert ident.pass_weight_mult > 1.0  # build from back nudges passing up
    assert ident.turnover_weight_mult >= 1.0  # high tempo/press add chaos
    assert ident.shot_weight_mult >= 1.0  # high tempo nudges shots up
    assert ident.shot_conversion_delta <= 0.0  # high tempo reduces conversion slightly

    # Clamp expectations
    assert -0.20 <= ident.possession_tilt <= 0.20
    assert 0.80 <= ident.pass_weight_mult <= 1.20
    assert 0.80 <= ident.turnover_weight_mult <= 1.20
    assert 0.80 <= ident.shot_weight_mult <= 1.25
    assert -0.10 <= ident.shot_conversion_delta <= 0.10


def test_build_v1_long_ball_is_more_direct_and_lower_possession():
    tactic = _base_tactic(
        build_up_style="Long Ball", tempo="High", pressing_intensity="Low"
    )
    ident = TacticalIdentityBuilder.build_v1(tactic)

    assert ident.possession_tilt < 0.0
    assert ident.pass_weight_mult < 1.0
    assert (
        ident.shot_weight_mult > 1.0
    )  # long ball increases shots weight in V1 mapping


def test_build_v1_positive_mentality_increases_shot_and_conversion():
    tactic = _base_tactic(mentality="Positive", tempo="Low")
    ident = TacticalIdentityBuilder.build_v1(tactic)

    assert ident.shot_weight_mult > 1.0
    assert ident.shot_conversion_delta > 0.0


def test_build_v1_clamps_values_to_safe_ranges():
    """
    Construct a tactic combo likely to push values toward extremes
    and ensure clamps prevent out-of-range results.
    """
    tactic = _base_tactic(
        build_up_style="Build From Back",
        tempo="High",
        pressing_intensity="Extreme",
        mentality="Positive",
    )
    ident = TacticalIdentityBuilder.build_v1(tactic)

    assert -0.20 <= ident.possession_tilt <= 0.20
    assert 0.80 <= ident.pass_weight_mult <= 1.20
    assert 0.80 <= ident.turnover_weight_mult <= 1.20
    assert 0.80 <= ident.shot_weight_mult <= 1.25
    assert -0.10 <= ident.shot_conversion_delta <= 0.10
