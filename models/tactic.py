from dataclasses import dataclass

from models.tactic_attributes import (
    AttackingFocus,
    BuildUpStyle,
    Compactness,
    DefensiveLine,
    DefensiveWidth,
    DribblingRisk,
    FinalThirdFocus,
    FreeKickStrategy,
    LineOfEngagement,
    MarkingStyle,
    OverloadFocus,
    PassingRisk,
    PressingIntensity,
    SetPieceAttack,
    SetPieceDefense,
    ShootingPolicy,
    TacklingAggression,
    TeamMentality,
    Tempo,
    TransitionOnLoss,
    TransitionOnWin,
    VerticalStretch,
    Width,
)


@dataclass
class TeamTactic:
    # Team Tactics: Attacking Tactics (SPEC Part 2.A)
    build_up_style: BuildUpStyle
    tempo: Tempo
    width: Width
    final_third_focus: FinalThirdFocus
    attacking_focus: AttackingFocus

    # Team Tactics: Defensive Tactics (SPEC Part 2.B)
    defensive_line: DefensiveLine
    line_of_engagement: LineOfEngagement
    pressing_intensity: PressingIntensity
    defensive_width: DefensiveWidth
    marking_style: MarkingStyle
    tackling_aggression: TacklingAggression

    # Team Tactics: Transition Tactics (SPEC Part 2.C)
    transition_on_win: TransitionOnWin
    transition_on_loss: TransitionOnLoss

    # Team Tactics: Mentality / Match Approach (SPEC Part 2.D)
    team_mentality: TeamMentality

    # Team Tactics: Risk Management (SPEC Part 2.E)
    passing_risk: PassingRisk
    dribbling_risk: DribblingRisk
    shooting_policy: ShootingPolicy

    # Team Tactics: Space Control (SPEC Part 2.F)
    compactness: Compactness
    vertical_stretch: VerticalStretch
    overload_focus: OverloadFocus

    # Set Piece Control System (SPEC Part 5)
    set_piece_attack: SetPieceAttack
    set_piece_defense: SetPieceDefense
    free_kick_strategy: FreeKickStrategy

    def summary(self) -> str:
        return (
            f"Build-Up Style: {self.build_up_style}\n"
            f"Tempo: {self.tempo}\n"
            f"Width: {self.width}\n"
            f"Final Third Focus: {self.final_third_focus}\n"
            f"Attacking Focus: {self.attacking_focus}\n"
            f"Defensive Line: {self.defensive_line}\n"
            f"Line of Engagement: {self.line_of_engagement}\n"
            f"Pressing Intensity: {self.pressing_intensity}\n"
            f"Defensive Width: {self.defensive_width}\n"
            f"Marking Style: {self.marking_style}\n"
            f"Tackling Aggression: {self.tackling_aggression}\n"
            f"Transition on Win: {self.transition_on_win}\n"
            f"Transition on Loss: {self.transition_on_loss}\n"
            f"Team Mentality: {self.team_mentality}\n"
            f"Passing Risk: {self.passing_risk}\n"
            f"Dribbling Risk: {self.dribbling_risk}\n"
            f"Shooting Policy: {self.shooting_policy}\n"
            f"Compactness: {self.compactness}\n"
            f"Vertical Stretch: {self.vertical_stretch}\n"
            f"Overload Focus: {self.overload_focus}\n"
            f"Set Piece Attack: {self.set_piece_attack}\n"
            f"Set Piece Defense: {self.set_piece_defense}\n"
            f"Free Kick Strategy: {self.free_kick_strategy}"
        )
