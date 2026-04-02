# rich_printer.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from models.team import Team

console = Console()


# -------------------------
# General panel printer
# -------------------------
def print_panel(title: str, content: str):
    console.print(Panel(content, title=title, box=box.DOUBLE, expand=False))


# -------------------------
# Team Summary
# -------------------------
def print_team_summary(team: Team):
    content = (
        f"[bold]Team:[/bold] {team.name}\n"
        f"[bold]Formation:[/bold] {team.formation}\n"
        f"[bold]Chemistry:[/bold] {team.chemistry} | [bold]Morale:[/bold] {team.morale}"
    )
    print_panel(f"⚽ TEAM SUMMARY - {team.name}", content)


# -------------------------
# Tactical Summary
# -------------------------
def print_tactic_summary(team: Team):
    t = team.tactic
    content = (
        f"[bold]Mentality:[/bold] {t.mentality}\n"
        f"[bold]Build-Up:[/bold] {t.build_up_style} | [bold]Tempo:[/bold] {t.tempo} | [bold]Width:[/bold] {t.width}\n"
        f"[bold]Attacking Focus:[/bold] {t.attacking_focus}\n"
        f"[bold]Defensive Line:[/bold] {t.defensive_line} | [bold]Pressing Intensity:[/bold] {t.pressing_intensity}\n"
        f"[bold]Transition (Win):[/bold] {t.transition_on_win} | [bold]Transition (Loss):[/bold] {t.transition_on_loss}"
    )
    print_panel(f"🛡️ TACTICAL SUMMARY - {team.name}", content)


# -------------------------
# Starting XI Table
# -------------------------
def print_starting_xi(team: Team):
    table = Table(title=f"Starting XI ⚔️ - {team.name}", box=box.SIMPLE)
    table.add_column("No", style="bold cyan", justify="right")
    table.add_column("Player", style="bold")
    table.add_column("Pos")
    table.add_column("Role")
    table.add_column("Duty")

    for idx, p in enumerate(team.starting_xi, start=1):
        table.add_row(str(idx), p.name, p.position, p.role, p.duty)

    console.print(table)


# -------------------------
# Player Details
# -------------------------
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


# -------------------------
# Team Strength Profile
# -------------------------
def print_strength_profile(profile):
    table = Table(
        title="Team Strength Profile 💪", box=box.ROUNDED
    )
    table.add_column("Attribute")
    table.add_column("Value", justify="right")

    for attr, value in profile.to_dict().items():
        color = "green" if value >= 65 else "yellow" if value >= 50 else "red"
        table.add_row(attr, f"[{color}]{value:.1f}[/{color}]")

    console.print(table)
