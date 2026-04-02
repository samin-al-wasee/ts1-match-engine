from models.player import Player
from models.tactic import TeamTactic
from models.team import Team
from systems.strength_calculator import StrengthCalculator
from models.team_strength import TeamStrengthProfile


def make_test_player(player_id: int, name: str) -> Player:
    return Player(
        id=player_id,
        name=name,
        position="CM",
        role="Box-to-Box",
        duty="Support",
        technical={
            "passing": 70,
            "first_touch": 68,
            "dribbling": 66,
            "crossing": 60,
            "technique": 69,
            "heading": 62,
            "marking": 64,
            "tackling": 67,
        },
        mental={
            "composure": 71,
            "decisions": 72,
            "vision": 70,
            "off_ball": 68,
            "positioning": 69,
            "teamwork": 74,
            "concentration": 67,
            "work_rate": 75,
            "aggression": 66,
        },
        physical={
            "balance": 68,
            "agility": 69,
            "pace": 72,
            "acceleration": 71,
            "jumping": 65,
            "strength": 70,
            "stamina": 76,
        },
    )


def make_test_team(
    width="Balanced",
    pressing="Balanced",
    build_up="Mixed Build-Up",
    transition="Hold Shape",
) -> Team:
    tactic = TeamTactic(
        mentality="Balanced",
        build_up_style=build_up,
        tempo="Balanced",
        width=width,
        attacking_focus="Mixed",
        defensive_line="Standard",
        pressing_intensity=pressing,
        transition_on_win=transition,
        transition_on_loss="Regroup",
    )

    players = [make_test_player(i, f"Player {i}") for i in range(1, 12)]

    return Team(
        name="Redchester FC",
        formation="4-3-3",
        tactic=tactic,
        starting_xi=players,
        chemistry=80,
        morale=80,
    )


def test_strength_profile_is_created():
    team = make_test_team()
    profile = StrengthCalculator.calculate(team)

    assert isinstance(profile, TeamStrengthProfile)


def test_strength_values_are_numeric():
    team = make_test_team()
    profile = StrengthCalculator.calculate(team)

    assert isinstance(profile.build_up_quality, float)
    assert isinstance(profile.press_resistance, float)
    assert isinstance(profile.wide_attack, float)
    assert isinstance(profile.central_creativity, float)
    assert isinstance(profile.aerial_threat, float)
    assert isinstance(profile.defensive_compactness, float)
    assert isinstance(profile.transition_threat, float)
    assert isinstance(profile.pressing_force, float)


def test_wide_tactic_increases_wide_attack():
    balanced_team = make_test_team(width="Balanced")
    wide_team = make_test_team(width="Wide")

    balanced_profile = StrengthCalculator.calculate(balanced_team)
    wide_profile = StrengthCalculator.calculate(wide_team)

    assert wide_profile.wide_attack > balanced_profile.wide_attack


def test_high_press_increases_pressing_force():
    balanced_team = make_test_team(pressing="Balanced")
    high_press_team = make_test_team(pressing="High")

    balanced_profile = StrengthCalculator.calculate(balanced_team)
    high_press_profile = StrengthCalculator.calculate(high_press_team)

    assert high_press_profile.pressing_force > balanced_profile.pressing_force


def test_build_from_back_increases_build_up_quality():
    mixed_team = make_test_team(build_up="Mixed Build-Up")
    build_from_back_team = make_test_team(build_up="Build From Back")

    mixed_profile = StrengthCalculator.calculate(mixed_team)
    build_from_back_profile = StrengthCalculator.calculate(build_from_back_team)

    assert build_from_back_profile.build_up_quality > mixed_profile.build_up_quality


def test_counter_immediately_increases_transition_threat():
    hold_shape_team = make_test_team(transition="Hold Shape")
    counter_team = make_test_team(transition="Counter Immediately")

    hold_shape_profile = StrengthCalculator.calculate(hold_shape_team)
    counter_profile = StrengthCalculator.calculate(counter_team)

    assert counter_profile.transition_threat > hold_shape_profile.transition_threat
