from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MatchupProfile:
    """
    Layer 3 — Matchup Layer output.

    Captures detailed tactical matchup between two teams.
    Edges are expressed from Team A perspective:
      -1.0 = strong advantage Team B
       0.0 = neutral
      +1.0 = strong advantage Team A

    Based on SPEC tactical dimensions:
    - Build-up Style & Pressing
    - Space Control & Compactness
    - Tempo & Rhythm
    - Final Third Actions & Risk
    - Transitions & Counter-Actions
    - Set Pieces & Aerial
    - Wing vs Central Routes
    - Fullback vs Winger Duel
    """

    # ==================== POSSESSION & BUILD-UP ====================
    # How A's build-up style matches against B's press resistance
    buildup_edge: float = 0.0

    # How effective A's pressing is vs B's build-up structure
    pressing_edge: float = 0.0

    # Counterpressing (when possession lost)
    counterpressing_edge: float = 0.0

    # ==================== SPACE CONTROL ====================
    # Compactness matchup: A's compactness vs B's ability to penetrate
    compactness_edge: float = 0.0

    # Defensive line height matchup: A's line vs B's offside trap vulnerability
    defensive_line_edge: float = 0.0

    # ==================== ROUTE & CHANCE CREATION ====================
    # Flank/wing progression: A's width strategy vs B's flank coverage
    wide_edge: float = 0.0

    # Central control & through-ball effectiveness
    central_edge: float = 0.0

    # Fullback vs Winger duel (wing battleground)
    fullback_edge: float = 0.0

    # ==================== FINAL THIRD & SHOOTING ====================
    # How teams finish: A's final third approach vs B's defensive positioning
    final_third_edge: float = 0.0

    # Shot quality influenced by risk tolerance
    shooting_risk_edge: float = 0.0

    # ==================== TRANSITIONS ====================
    # Transition speed when possession won
    transition_out_edge: float = 0.0

    # Transition vulnerability when possession lost
    transition_in_edge: float = 0.0

    # ==================== SET PIECES & AERIAL ====================
    # Aerial duels & set-piece effectiveness
    aerial_edge: float = 0.0

    # Defensive set-piece vulnerability
    setpiece_defense_edge: float = 0.0

    # ==================== TEMPO & FATIGUE ====================
    # Tempo compatibility: high pace vs controlled play
    tempo_edge: float = 0.0

    # ==================== KEY PLAYER INFLUENCE ====================
    # Playmaker presence & impact zones
    playmaker_edge: float = 0.0

    # Striker effectiveness & support quality
    striker_support_edge: float = 0.0

    def summary(self) -> str:
        """Generate human-readable matchup summary."""
        return (
            "=== POSSESSION & BUILD-UP ===\n"
            f"Buildup Edge: {self.buildup_edge:+.2f}\n"
            f"Pressing Edge: {self.pressing_edge:+.2f}\n"
            f"Counterpressing Edge: {self.counterpressing_edge:+.2f}\n"
            "\n=== SPACE CONTROL ===\n"
            f"Compactness Edge: {self.compactness_edge:+.2f}\n"
            f"Defensive Line Edge: {self.defensive_line_edge:+.2f}\n"
            "\n=== ROUTE & CREATION ===\n"
            f"Wide Edge: {self.wide_edge:+.2f}\n"
            f"Central Edge: {self.central_edge:+.2f}\n"
            f"Fullback Edge: {self.fullback_edge:+.2f}\n"
            "\n=== FINAL THIRD & SHOOTING ===\n"
            f"Final Third Edge: {self.final_third_edge:+.2f}\n"
            f"Shooting Risk Edge: {self.shooting_risk_edge:+.2f}\n"
            "\n=== TRANSITIONS ===\n"
            f"Transition Out Edge: {self.transition_out_edge:+.2f}\n"
            f"Transition In Edge: {self.transition_in_edge:+.2f}\n"
            "\n=== SET PIECES & AERIAL ===\n"
            f"Aerial Edge: {self.aerial_edge:+.2f}\n"
            f"Set-Piece Defense Edge: {self.setpiece_defense_edge:+.2f}\n"
            "\n=== TEMPO & FATIGUE ===\n"
            f"Tempo Edge: {self.tempo_edge:+.2f}\n"
            "\n=== KEY PLAYERS ===\n"
            f"Playmaker Edge: {self.playmaker_edge:+.2f}\n"
            f"Striker Support Edge: {self.striker_support_edge:+.2f}"
        )
