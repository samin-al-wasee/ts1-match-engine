from dataclasses import dataclass


@dataclass
class TeamStrengthProfile:
    # -------------------------
    # Build-up and core play
    # -------------------------
    build_up_quality: float
    press_resistance: float
    wide_attack: float
    central_creativity: float
    aerial_threat: float
    defensive_compactness: float
    transition_threat: float
    pressing_force: float

    # -------------------------
    # Possession control
    # -------------------------
    possession_security: float
    turnover_liability: float

    # -------------------------
    # Attacking output
    # -------------------------
    finishing_quality: float
    shot_volume_tendency: float
    chance_conversion: float

    # -------------------------
    # Defensive structure
    # -------------------------
    transition_defense: float
    wide_defense: float
    central_defense: float

    # -------------------------
    # Set pieces
    # -------------------------
    set_piece_attack_strength: float
    set_piece_defense_strength: float

    # -------------------------
    # Discipline and goalkeeper
    # -------------------------
    discipline_control: float
    gk_distribution_quality: float
    gk_shot_stopping: float

    # -------------------------
    # Intangibles
    # -------------------------
    chemistry: float
    morale: float

    def summary(self) -> str:
        return (
            f"Build-Up: {self.build_up_quality:.1f}\n"
            f"Press Resistance: {self.press_resistance:.1f}\n"
            f"Wide Attack: {self.wide_attack:.1f}\n"
            f"Central Creativity: {self.central_creativity:.1f}\n"
            f"Aerial Threat: {self.aerial_threat:.1f}\n"
            f"Defensive Compactness: {self.defensive_compactness:.1f}\n"
            f"Transition Threat: {self.transition_threat:.1f}\n"
            f"Pressing Force: {self.pressing_force:.1f}\n"
            f"Finishing Quality: {self.finishing_quality:.1f}\n"
            f"Shot Volume Tendency: {self.shot_volume_tendency:.1f}\n"
            f"Chance Conversion: {self.chance_conversion:.1f}\n"
            f"Transition Defense: {self.transition_defense:.1f}\n"
            f"Wide Defense: {self.wide_defense:.1f}\n"
            f"Central Defense: {self.central_defense:.1f}\n"
            f"Set Piece Attack: {self.set_piece_attack_strength:.1f}\n"
            f"Set Piece Defense: {self.set_piece_defense_strength:.1f}\n"
            f"Possession Security: {self.possession_security:.1f}\n"
            f"Turnover Liability: {self.turnover_liability:.1f}\n"
            f"Discipline Control: {self.discipline_control:.1f}\n"
            f"GK Distribution: {self.gk_distribution_quality:.1f}\n"
            f"GK Shot Stopping: {self.gk_shot_stopping:.1f}\n"
            f"Chemistry: {self.chemistry:.1f}\n"
            f"Morale: {self.morale:.1f}\n"
        )

    def to_dict(self) -> dict:
        return {
            # Build-up and control
            "Build-Up Quality": self.build_up_quality,
            "Press Resistance": self.press_resistance,
            "Possession Security": self.possession_security,
            "Turnover Liability": self.turnover_liability,
            # Attacking output
            "Wide Attack": self.wide_attack,
            "Central Creativity": self.central_creativity,
            "Aerial Threat": self.aerial_threat,
            "Finishing Quality": self.finishing_quality,
            "Shot Volume Tendency": self.shot_volume_tendency,
            "Chance Conversion": self.chance_conversion,
            # Defensive structure
            "Defensive Compactness": self.defensive_compactness,
            "Pressing Force": self.pressing_force,
            "Transition Defense": self.transition_defense,
            "Wide Defense": self.wide_defense,
            "Central Defense": self.central_defense,
            # Transition and set pieces
            "Transition Threat": self.transition_threat,
            "Set Piece Attack": self.set_piece_attack_strength,
            "Set Piece Defense": self.set_piece_defense_strength,
            # Discipline and goalkeeper
            "Discipline Control": self.discipline_control,
            "GK Distribution": self.gk_distribution_quality,
            "GK Shot Stopping": self.gk_shot_stopping,
            # Intangibles
            "Chemistry": self.chemistry,
            "Morale": self.morale,
        }
