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
        f"[bold]Build Up Style:[/bold] {t.build_up_style}\n"
        f"[bold]Tempo:[/bold] {t.tempo}\n"
        f"[bold]Width:[/bold] {t.width}\n"
        f"[bold]Final Third Focus:[/bold] {t.final_third_focus}\n"
        f"[bold]Passing Directness:[/bold] {t.passing_directness}\n"
        f"[bold]Chance Creation Style:[/bold] {t.chance_creation_style}\n"
        f"[bold]Crossing Style:[/bold] {t.crossing_style}\n"
        f"[bold]Shooting Tendency:[/bold] {t.shooting_tendency}\n"
        f"[bold]Dribbling Tendency:[/bold] {t.dribbling_tendency}\n"
        f"[bold]Defensive Line:[/bold] {t.defensive_line}\n"
        f"[bold]Pressing Intensity:[/bold] {t.pressing_intensity}\n"
        f"[bold]Press Trigger:[/bold] {t.press_trigger}\n"
        f"[bold]Defensive Width:[/bold] {t.defensive_width}\n"
        f"[bold]Line Compactness:[/bold] {t.line_compactness}\n"
        f"[bold]Marking Style:[/bold] {t.marking_style}\n"
        f"[bold]Tackling Style:[/bold] {t.tackling_style}\n"
        f"[bold]Transition On Win:[/bold] {t.transition_on_win}\n"
        f"[bold]Transition On Loss:[/bold] {t.transition_on_loss}\n"
        f"[bold]Counter Speed:[/bold] {t.counter_speed}\n"
        f"[bold]Set Piece Attacking Style:[/bold] {t.set_piece_attacking_style}\n"
        f"[bold]Set Piece Defensive Style:[/bold] {t.set_piece_defensive_style}"
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
    def _fmt_items(title: str, items: dict) -> str:
        if not items:
            return f"[bold]{title}:[/bold] (none)"
        lines = "\n".join(f"• {k}: {v}" for k, v in sorted(items.items()))
        return f"[bold]{title}:[/bold]\n{lines}"

    for p in team.starting_xi:
        tech_block = _fmt_items("Technical", getattr(p, "technical", {}))
        mental_block = _fmt_items("Mental", getattr(p, "mental", {}))
        phys_block = _fmt_items("Physical", getattr(p, "physical", {}))
        condition_block = _fmt_items("Condition", getattr(p, "condition", {}))
        hidden_block = _fmt_items("Hidden", getattr(p, "hidden", {}))

        content = (
            f"{tech_block}\n\n"
            f"{mental_block}\n\n"
            f"{phys_block}\n\n"
            f"{condition_block}\n\n"
            f"{hidden_block}"
        )

        print_panel(f"👤 {p.name} ({p.position}) - {p.role} [{p.duty}]", content)


# -------------------------
# Team Strength Profile
# -------------------------
def print_strength_profile(profile):
    table = Table(title="Team Strength Profile 💪", box=box.ROUNDED)
    table.add_column("Attribute")
    table.add_column("Value", justify="right")

    for attr, value in profile.to_dict().items():
        color = "green" if value >= 65 else "yellow" if value >= 50 else "red"
        table.add_row(attr, f"[{color}]{value:.1f}[/{color}]")

    console.print(table)


# -------------------------
# Match Printing Functions (Rich with Emojis)
# -------------------------
def print_match_kickoff(home_team: Team, away_team: Team):
    """Print match start information using Rich with emojis"""
    # Main match panel
    match_panel = Panel(
        f"[bold yellow]🏟️ {home_team.name} 🆚 {away_team.name}[/bold yellow]\n\n"
        f"[cyan]📋 Starting XI - {home_team.name}:[/cyan]\n"
        f"👕 {', '.join([p.name for p in home_team.starting_xi])}\n\n"
        f"[cyan]📋 Starting XI - {away_team.name}:[/cyan]\n"
        f"👕 {', '.join([p.name for p in away_team.starting_xi])}\n\n"
        f"[dim]⚙️ Formation: {home_team.formation} 🆚 {away_team.formation}[/dim]",
        title="[bold green]⚽ 🎬 MATCH START 🎬 ⚽[/bold green]",
        box=box.DOUBLE,
        style="bold",
    )
    console.print(match_panel)
    console.print("[bold green]🎯 Kickoff! ⏰⚽[/bold green]\n")
    console.print("[dim]🎶 Crowd cheering loudly! 📣[/dim]\n")


def print_match_event(minute: int, event: str):
    """Print a single match event with Rich formatting and emojis"""
    # Color-code and emoji-enhance different event types
    if "GOAL" in event:
        styled_event = f"[bold red]🎉⚽🔥 {event} 🔥⚽🎉[/bold red]"
    elif "🔴" in event:
        styled_event = f"[red]😤💔 {event} 💔😤[/red]"
    elif "🟢" in event:
        styled_event = f"[green]🎯✅ {event} ✅🎯[/green]"
    elif "shot" in event and "saved" in event:
        styled_event = f"[yellow]🧤💪 {event} 💪🧤[/yellow]"
    else:
        styled_event = f"[yellow]⚡ {event} ⚡[/yellow]"

    # Add minute with clock emoji
    clock_emoji = "⏱️" if minute % 15 == 0 else "⏲️"
    console.print(f"[dim]{clock_emoji} {minute}'[/dim] {styled_event}")


def print_match_summary(
    minute: int,
    home_score: int,
    away_score: int,
    home_team_name: str,
    away_team_name: str,
    home_possession: int,
    away_possession: int,
    recent_events: list,
):
    """Print match summary using Rich Table with emojis"""
    # Score table with trophy emojis
    score_table = Table(title=f"📊📈 Match Summary - {minute}' ⏰", box=box.ROUNDED)
    score_table.add_column("🏷️ Team", style="bold cyan")
    score_table.add_column("⚽ Score", style="bold", justify="center")
    score_table.add_column("🎯 Possession", justify="right")
    score_table.add_column("📊 Form", justify="center")

    # Add form indicators
    home_form = "📈" if home_possession > 50 else "📉" if home_possession < 50 else "➡️"
    away_form = "📈" if away_possession > 50 else "📉" if away_possession < 50 else "➡️"

    score_table.add_row(
        f"🏠 {home_team_name}",
        f"[bold green]{home_score}[/bold green]",
        f"{home_possession}%",
        home_form,
    )
    score_table.add_row(
        f"✈️ {away_team_name}",
        f"[bold green]{away_score}[/bold green]",
        f"{away_possession}%",
        away_form,
    )

    console.print(score_table)

    # Recent events panel with emojis
    events_text = "\n".join([f"• {e}" for e in recent_events[-5:]])
    events_panel = Panel(
        events_text,
        title="[bold]🔄 Recent Events 🔄[/bold]",
        box=box.MINIMAL,
        style="dim",
    )
    console.print(events_panel)

    # Add stat indicators
    console.print("[dim]🟢 Passes | 🔴 Turnovers | ⚽ Shots | 🎯 Goals[/dim]\n")


def print_full_time(
    home_team_name: str, away_team_name: str, home_score: int, away_score: int
):
    """Print full time result with Rich highlighting and emojis"""
    # Determine winner with emojis
    if home_score > away_score:
        result = f"🏆🎉👑 {home_team_name} wins the match! 👑🎉🏆"
        result_style = "bold green"
        celebration = "🎊🥳🎈"
    elif away_score > home_score:
        result = f"🏆🎉👑 {away_team_name} wins the match! 👑🎉🏆"
        result_style = "bold green"
        celebration = "🎊🥳🎈"
    else:
        result = "🤝 It's a draw! 🤝"
        result_style = "bold yellow"
        celebration = "😐🤷"

    # Calculate total goals
    total_goals = home_score + away_score
    goal_emoji = "⚽" * min(total_goals, 5) + ("⚽" if total_goals > 5 else "")

    full_time_panel = Panel(
        f"[bold]{home_team_name}[/bold] [bold cyan]{home_score}[/bold cyan] 🆚 "
        f"[bold cyan]{away_score}[/bold cyan] [bold]{away_team_name}[/bold]\n\n"
        f"[{result_style}]{result}[/{result_style}]\n\n"
        f"[dim]{goal_emoji} Total Goals: {total_goals} {goal_emoji}[/dim]\n"
        f"{celebration}",
        title="[bold red]🏁🔚 FULL TIME 🔚🏁[/bold red]",
        box=box.DOUBLE,
        style="bold",
    )
    console.print(full_time_panel)

    # Print match rating
    if total_goals >= 5:
        console.print("[bold green]🌟⭐ Match Rating: Exciting! ⭐🌟[/bold green]")
    elif total_goals >= 3:
        console.print("[bold yellow]👍 Match Rating: Entertaining! 👍[/bold yellow]")
    else:
        console.print("[dim]😴 Match Rating: Defensive battle... 😴[/dim]")


def print_minute_marker(minute: int):
    """Print a minute marker for key intervals"""
    if minute == 15:
        console.print("\n[dim]⏰ 🟢 15' - Quarter hour mark 🟢 ⏰[/dim]\n")
    elif minute == 30:
        console.print("\n[dim]⏰ 🟡 30' - Half hour mark 🟡 ⏰[/dim]\n")
    elif minute == 45:
        console.print("\n[bold yellow]⏰ 🟠 Half Time! 🟠 ⏰[/bold yellow]\n")
    elif minute == 60:
        console.print("\n[dim]⏰ 🔵 60' - Hour mark 🔵 ⏰[/dim]\n")
    elif minute == 75:
        console.print("\n[dim]⏰ 🟣 75' - Final quarter 🟣 ⏰[/dim]\n")
