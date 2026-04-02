from models.player import Player
from models.tactic import TeamTactic
from models.team import Team


def main():
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

    striker = Player(
        id=9, name="Alex Storm", position="ST", role="Pressing Forward", duty="Attack"
    )

    team = Team(
        name="Redchester FC", formation="4-3-3", tactic=tactic, starting_xi=[striker]
    )

    print("Football Manager Engine V1")
    print(team.summary())
    print(striker.overall_summary())
    print(team.tactic.summary())


if __name__ == "__main__":
    main()
