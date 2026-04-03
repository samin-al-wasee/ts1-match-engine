from models.duty import Duty
from models.player import Player
from models.position import Position
from models.role import Role
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
from utils.attr_generator import generate_player_attribute_groups


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
        Player(
            0, "Vancouver Derwin Server", Position.GK, Role.SHOT_STOPPER, Duty.DEFEND
        ),
        Player(1, "Kyle Walkerstone", Position.RB, Role.FULL_BACK, Duty.SUPPORT),
        Player(2, "Michael Stoneman", Position.CB, Role.CENTRAL_DEFENDER, Duty.DEFEND),
        Player(3, "David Ironwood", Position.CB, Role.CENTRAL_DEFENDER, Duty.DEFEND),
        Player(4, "Lucas Greenfield", Position.LB, Role.FULL_BACK, Duty.SUPPORT),
        Player(
            5,
            "James Steelheart",
            Position.DM,
            Role.ANCHOR_HOLDING_MIDFIELDER,
            Duty.DEFEND,
        ),
        Player(
            6,
            "Ryan Thunderstrike",
            Position.DM,
            Role.DEEP_LYING_PLAYMAKER_REGISTA,
            Duty.SUPPORT,
        ),
        Player(7, "Ethan Swiftblade", Position.AM, Role.SHADOW_STRIKER, Duty.ATTACK),
        Player(8, "Oliver Stormrider", Position.RW, Role.WINGER, Duty.ATTACK),
        Player(9, "Benjamin Fireforge", Position.LW, Role.WINGER, Duty.ATTACK),
        Player(
            10, "Alexander Ironfist", Position.ST, Role.ADVANCED_FORWARD, Duty.ATTACK
        ),
    ]

    # Generate random attributes for each player
    for player in home_players:
        (technical, mental, physical, hidden, condition) = (
            generate_player_attribute_groups(player.position, player.role)
        )
        player.technical = technical
        player.mental = mental
        player.physical = physical
        player.hidden = hidden
        player.condition = condition

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
        Player(11, "Liam Thunderstone", Position.GK, Role.SHOT_STOPPER, Duty.DEFEND),
        Player(12, "Noah Stormblade", Position.RB, Role.FULL_BACK, Duty.SUPPORT),
        Player(13, "Mason Ironwood", Position.CB, Role.CENTRAL_DEFENDER, Duty.DEFEND),
        Player(14, "Logan Steelheart", Position.CB, Role.CENTRAL_DEFENDER, Duty.DEFEND),
        Player(15, "Ethan Greenfield", Position.LB, Role.FULL_BACK, Duty.SUPPORT),
        Player(
            16,
            "Jacob Fireforge",
            Position.DM,
            Role.DEEP_LYING_PLAYMAKER_REGISTA,
            Duty.DEFEND,
        ),
        Player(
            17,
            "William Swiftblade",
            Position.DM,
            Role.DEEP_LYING_PLAYMAKER_REGISTA,
            Duty.SUPPORT,
        ),
        Player(18, "Michael Stormrider", Position.AM, Role.SHADOW_STRIKER, Duty.ATTACK),
        Player(19, "Alexander Ironfist", Position.RW, Role.WINGER, Duty.ATTACK),
        Player(20, "Daniel Thunderstrike", Position.LW, Role.WINGER, Duty.ATTACK),
        Player(
            21, "Matthew Steelheart", Position.ST, Role.ADVANCED_FORWARD, Duty.ATTACK
        ),
    ]

    for player in away_players:
        (technical, mental, physical, hidden, condition) = (
            generate_player_attribute_groups(player.position, player.role)
        )
        player.technical = technical
        player.mental = mental
        player.physical = physical
        player.hidden = hidden
        player.condition = condition

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
