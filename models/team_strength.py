from dataclasses import dataclass


@dataclass
class TeamStrengthProfile:
    build_up_quality: float
    press_resistance: float
    wide_attack: float
    central_creativity: float
    aerial_threat: float
    defensive_compactness: float
    transition_threat: float
    pressing_force: float

    def summary(self) -> str:
        return (
            f"Build-Up: {self.build_up_quality:.1f}\n"
            f"Press Resistance: {self.press_resistance:.1f}\n"
            f"Wide Attack: {self.wide_attack:.1f}\n"
            f"Central Creativity: {self.central_creativity:.1f}\n"
            f"Aerial Threat: {self.aerial_threat:.1f}\n"
            f"Defensive Compactness: {self.defensive_compactness:.1f}\n"
            f"Transition Threat: {self.transition_threat:.1f}\n"
            f"Pressing Force: {self.pressing_force:.1f}"
        )
        
    def to_dict(self) -> dict:
        return {
            "Build-Up Quality": self.build_up_quality,
            "Press Resistance": self.press_resistance,
            "Wide Attack": self.wide_attack,
            "Central Creativity": self.central_creativity,
            "Aerial Threat": self.aerial_threat,
            "Defensive Compactness": self.defensive_compactness,
            "Transition Threat": self.transition_threat,
            "Pressing Force": self.pressing_force,
        }
