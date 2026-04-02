from dataclasses import dataclass


@dataclass
class TeamTactic:
    mentality: str
    build_up_style: str
    tempo: str
    width: str
    attacking_focus: str
    defensive_line: str
    pressing_intensity: str
    transition_on_win: str
    transition_on_loss: str

    def summary(self) -> str:
        return (
            f"Mentality: {self.mentality}, "
            f"Build-Up: {self.build_up_style}, "
            f"Tempo: {self.tempo}, "
            f"Width: {self.width}"
        )
