from dataclasses import dataclass

from models.tactic_attributes import (
    BuildUpStyle,
    ChanceCreationStyle,
    CounterSpeed,
    CrossingStyle,
    DefensiveLine,
    DefensiveWidth,
    DribblingTendency,
    FinalThirdFocus,
    LineCompactness,
    MarkingStyle,
    Mentality,
    PassingDirectness,
    PressingIntensity,
    PressTrigger,
    SetPieceAttackingStyle,
    SetPieceDefensiveStyle,
    ShootingTendency,
    TacklingStyle,
    Tempo,
    TransitionOnLoss,
    TransitionOnWin,
    Width,
)


@dataclass
class TeamTactic:
    # Core identity
    mentality: Mentality
    build_up_style: BuildUpStyle
    tempo: Tempo
    width: Width
    final_third_focus: FinalThirdFocus
    passing_directness: PassingDirectness
    chance_creation_style: ChanceCreationStyle
    crossing_style: CrossingStyle
    shooting_tendency: ShootingTendency
    dribbling_tendency: DribblingTendency

    # Out of possession
    defensive_line: DefensiveLine
    pressing_intensity: PressingIntensity
    press_trigger: PressTrigger
    defensive_width: DefensiveWidth
    line_compactness: LineCompactness
    marking_style: MarkingStyle
    tackling_style: TacklingStyle

    # Transitions
    transition_on_win: TransitionOnWin
    transition_on_loss: TransitionOnLoss
    counter_speed: CounterSpeed

    # Set pieces
    set_piece_attacking_style: SetPieceAttackingStyle
    set_piece_defensive_style: SetPieceDefensiveStyle

    def summary(self) -> str:
        return (
            f"Mentality: {self.mentality}\n"
            f"Build-Up Style: {self.build_up_style}\n"
            f"Tempo: {self.tempo}\n"
            f"Width: {self.width}\n"
            f"Final Third Focus: {self.final_third_focus}\n"
            f"Passing Directness: {self.passing_directness}\n"
            f"Chance Creation Style: {self.chance_creation_style}\n"
            f"Crossing Style: {self.crossing_style}\n"
            f"Shooting Tendency: {self.shooting_tendency}\n"
            f"Dribbling Tendency: {self.dribbling_tendency}\n"
            f"Defensive Line: {self.defensive_line}\n"
            f"Pressing Intensity: {self.pressing_intensity}\n"
            f"Press Trigger: {self.press_trigger}\n"
            f"Defensive Width: {self.defensive_width}\n"
            f"Line Compactness: {self.line_compactness}\n"
            f"Marking Style: {self.marking_style}\n"
            f"Tackling Style: {self.tackling_style}\n"
            f"Transition on Win: {self.transition_on_win}\n"
            f"Transition on Loss: {self.transition_on_loss}\n"
            f"Counter Speed: {self.counter_speed}\n"
            f"Set Piece Attacking Style: {self.set_piece_attacking_style}\n"
            f"Set Piece Defensive Style: {self.set_piece_defensive_style}"
        )
