from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from models.player import Player
from models.tactic import TeamTactic
from models.team import Team
from systems.strength_calculator import StrengthCalculator

console = Console()


def make_player(player_id, name, position, role, duty):
    return Player(
        id=player_id,
        name=name,
        position=position,
        role=role,
        duty=duty,
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


def print_panel(title: str, content: str):
    console.print(Panel(content, title=title, box=box.DOUBLE, expand=False))


def print_team_summary(team: Team):
    content = (
        f"[bold]Team:[/bold] {team.name}\n"
        f"[bold]Formation:[/bold] {team.formation}\n"
        f"[bold]Chemistry:[/bold] {team.chemistry} | [bold]Morale:[/bold] {team.morale}"
    )
    print_panel("⚽ TEAM SUMMARY", content)


def print_tactic_summary(team: Team):
    t = team.tactic
    content = (
        f"[bold]Mentality:[/bold] {t.mentality}\n"
        f"[bold]Build-Up:[/bold] {t.build_up_style} | [bold]Tempo:[/bold] {t.tempo} | [bold]Width:[/bold] {t.width}\n"
        f"[bold]Attacking Focus:[/bold] {t.attacking_focus}\n"
        f"[bold]Defensive Line:[/bold] {t.defensive_line} | [bold]Pressing Intensity:[/bold] {t.pressing_intensity}\n"
        f"[bold]Transition (Win):[/bold] {t.transition_on_win} | [bold]Transition (Loss):[/bold] {t.transition_on_loss}"
    )
    print_panel("🛡️ TACTICAL SUMMARY", content)


def print_starting_xi(team: Team):
    table = Table(title="Starting XI ⚔️", box=box.SIMPLE)
    table.add_column("No", style="bold cyan", justify="right")
    table.add_column("Player", style="bold")
    table.add_column("Pos")
    table.add_column("Role")
    table.add_column("Duty")

    for idx, p in enumerate(team.starting_xi, start=1):
        table.add_row(str(idx), p.name, p.position, p.role, p.duty)

    console.print(table)


def print_player_details(team: Team):
    for p in team.starting_xi:
        tech = ", ".join(f"{k}:{v}" for k, v in p.technical.items())
        mental = ", ".join(f"{k}:{v}" for k, v in p.mental.items())
        phys = ", ".join(f"{k}:{v}" for k, v in p.physical.items())

        content = (
            f"[bold]Technical:[/bold] {tech}\n"
            f"[bold]Mental:[/bold] {mental}\n"
            f"[bold]Physical:[/bold] {phys}\n"
            f"[bold]Stamina:[/bold] {p.stamina} | [bold]Morale:[/bold] {p.morale} | [bold]Sharpness:[/bold] {p.sharpness}"
        )
        print_panel(f"👤 {p.name} ({p.position}) - {p.role} [{p.duty}]", content)


def print_strength_profile(profile):
    table = Table(title="Team Strength Profile 💪", box=box.ROUNDED)
    table.add_column("Attribute")
    table.add_column("Value", justify="right")

    for attr, value in profile.to_dict().items():
        color = "green" if value >= 65 else "yellow" if value >= 50 else "red"
        table.add_row(attr, f"[{color}]{value:.1f}[/{color}]")

    console.print(table)


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

    players = [
        make_player(1, "Alex Keeper", "GK", "Goalkeeper", "Defend"),
        make_player(2, "Leo Stone", "RB", "Fullback", "Support"),
        make_player(3, "Mason Reed", "CB", "Ball Playing Defender", "Defend"),
        make_player(4, "Ryan Cole", "CB", "Stopper", "Defend"),
        make_player(5, "Ethan Vale", "LB", "Wingback", "Attack"),
        make_player(6, "Noah Grant", "DM", "Anchor", "Defend"),
        make_player(7, "Luca Hayes", "CM", "Box-to-Box", "Support"),
        make_player(8, "Kai Mercer", "CM", "Advanced Playmaker", "Support"),
        make_player(9, "Jay Storm", "RW", "Inside Forward", "Attack"),
        make_player(10, "Owen Frost", "LW", "Winger", "Support"),
        make_player(11, "Zane Hunter", "ST", "Pressing Forward", "Attack"),
    ]

    team = Team(
        name="Redchester FC",
        formation="4-3-3",
        tactic=tactic,
        starting_xi=players,
        chemistry=82,
        morale=79,
    )

    profile = StrengthCalculator.calculate(team)

    console.rule("[bold magenta]FOOTBALL MANAGER ENGINE V1[/bold magenta]")
    print_team_summary(team)
    print_tactic_summary(team)
    print_starting_xi(team)
    print_player_details(team)
    print_strength_profile(profile)


if __name__ == "__main__":
    main()
