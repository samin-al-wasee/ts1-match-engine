from models.player import Player
from models.tactic import TeamTactic
from models.team import Team
from match_engine import Match
from debug.printer import (
    print_panel,
    print_player_details,
    print_starting_xi,
    print_strength_profile,
    print_tactic_summary,
    print_team_summary,
)
from systems.strength_calculator import StrengthCalculator


def main():
    # Tactic for both teams
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

    # Create Home team
    home_players = [
        Player(0, "Vancouver Derwin Server", "GK", "Goalkeeper", "Defend"),
        Player(1, "Kyle Walkerstone", "RB", "Full Back", "Support"),
        Player(2, "Michael Stoneman", "CB", "Central Defender", "Defend"),
        Player(3, "David Ironwood", "CB", "Central Defender", "Defend"),
        Player(4, "Lucas Greenfield", "LB", "Full Back", "Support"),
        Player(5, "James Steelheart", "CDM", "Defensive Midfielder", "Defend"),
        Player(6, "Ryan Thunderstrike", "CDM", "Defensive Midfielder", "Support"),
        Player(7, "Ethan Swiftblade", "CAM", "Attacking Midfielder", "Attack"),
        Player(8, "Oliver Stormrider", "RW", "Winger", "Attack"),
        Player(9, "Benjamin Fireforge", "LW", "Winger", "Attack"),
        Player(10, "Alexander Ironfist", "ST", "Striker", "Attack"),
    ]
    home = Team(
        name="Redchester United",
        formation="4-2-3-1",
        tactic=tactic,
        starting_xi=home_players,
        chemistry=80,
        morale=85,
    )
    home_profile = StrengthCalculator.calculate(home)

    # Create Away team
    away_players = [
        Player(11, "Liam Thunderstone", "GK", "Goalkeeper", "Defend"),
        Player(12, "Noah Stormblade", "RB", "Full Back", "Support"),
        Player(13, "Mason Ironwood", "CB", "Central Defender", "Defend"),
        Player(14, "Logan Steelheart", "CB", "Central Defender", "Defend"),
        Player(15, "Ethan Greenfield", "LB", "Full Back", "Support"),
        Player(16, "Jacob Fireforge", "CDM", "Defensive Midfielder", "Defend"),
        Player(17, "William Swiftblade", "CDM", "Defensive Midfielder", "Support"),
        Player(18, "Michael Stormrider", "CAM", "Attacking Midfielder", "Attack"),
        Player(19, "Alexander Ironfist", "RW", "Winger", "Attack"),
        Player(20, "Daniel Thunderstrike", "LW", "Winger", "Attack"),
        Player(21, "Matthew Steelheart", "ST", "Striker", "Attack"),
    ]
    away = Team(
        name="Bluechester City",
        formation="4-3-3",
        tactic=tactic,
        starting_xi=away_players,
        chemistry=78,
        morale=82,
    )
    away_profile = StrengthCalculator.calculate(away)

    print_panel(
        "⚽ MATCH PREVIEW",
        f"{home.name} vs {away.name}\nFormation: {home.formation} vs {away.formation}",
    )

    # Display team summaries and profiles
    print_team_summary(home)
    print_tactic_summary(home)
    print_starting_xi(home)
    print_player_details(home)
    print_strength_profile(home_profile)

    print_team_summary(away)
    print_tactic_summary(away)
    print_starting_xi(away)
    print_player_details(away)
    print_strength_profile(away_profile)

    # Run match simulation
    match = Match(home, away)
    match.simulate_match(total_minutes=30, display_interval=5)


if __name__ == "__main__":
    main()
