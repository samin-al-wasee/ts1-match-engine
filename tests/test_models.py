from models.player import Player
from models.tactic import TeamTactic
from models.team import Team
from models.match_state import MatchState


def test_player_summary():
    player = Player(
        id=1, name="Alex Storm", position="ST", role="Pressing Forward", duty="Attack"
    )
    assert player.overall_summary() == "Alex Storm (ST) - Pressing Forward [Attack]"


def test_tactic_summary():
    tactic = TeamTactic(
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
    assert "Mentality: Balanced" in tactic.summary()


def test_team_summary_and_size():
    tactic = TeamTactic(
        mentality="Balanced",
        build_up_style="Mixed Build-Up",
        tempo="Balanced",
        width="Balanced",
        attacking_focus="Mixed",
        defensive_line="Standard",
        pressing_intensity="Balanced",
        transition_on_win="Hold Shape",
        transition_on_loss="Regroup",
    )

    player = Player(
        id=1, name="Alex Storm", position="ST", role="Advanced Forward", duty="Attack"
    )

    team = Team(
        name="Redchester FC",
        formation="4-3-3",
        tactic=tactic,
        starting_xi=[player],
        bench=[],
    )

    assert team.squad_size() == 1
    assert "Redchester FC" in team.summary()


def test_match_state_events_and_scoreline():
    state = MatchState()
    state.home_score = 2
    state.away_score = 1
    state.add_event("12' Goal for Redchester FC")

    assert state.scoreline() == "2 - 1"
    assert len(state.visible_events) == 1
