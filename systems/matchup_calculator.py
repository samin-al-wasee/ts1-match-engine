from __future__ import annotations

from dataclasses import replace

from models.matchup import MatchupProfile
from models.team_strength import TeamStrengthProfile
from models.tactical_identity import TacticalIdentity


def _clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _safe_div(n: float, d: float, default: float = 0.0) -> float:
    return n / d if abs(d) > 1e-9 else default


def _edge_from_strength_diff(
    a: float,
    b: float,
    scale: float = 20.0,
) -> float:
    """
    Convert a raw strength diff (often around 0..100-ish) to an edge [-1, +1].

    scale=20 means:
      diff=+20 -> +1.0 (strong)
      diff=+10 -> +0.5 (moderate)
    """
    return _clamp(_safe_div(a - b, scale))


def _shot_aggression_bias(identity: TacticalIdentity) -> float:
    """Approximate shot aggression from available tactical fields (0..1)."""
    return _clamp(
        0.65 * identity.risk_taking + 0.35 * identity.long_shot_bias, 0.0, 1.0
    )


def _defensive_caution_bias(identity: TacticalIdentity) -> float:
    """Approximate defensive caution from available tactical fields (0..1)."""
    return _clamp(
        0.50 * (1.0 - identity.risk_taking)
        + 0.30 * identity.compactness_bias
        + 0.20 * (1.0 - identity.press_intensity_bias),
        0.0,
        1.0,
    )


def _tempo_bias(identity: TacticalIdentity) -> float:
    """Approximate attacking tempo intent from available tactical fields (0..1)."""
    return _clamp(
        0.35 * identity.vertical_progression_bias
        + 0.25 * identity.directness_bias
        + 0.20 * identity.counter_speed_bias
        + 0.20 * identity.risk_taking,
        0.0,
        1.0,
    )


class MatchupCalculator:
    """
    Layer 3 — Matchup Layer.

    Produces per-domain matchup edges by combining:
    - Layer 2: TeamStrengthProfile (players/chemistry/morale derived capability)
    - Layer 1: TacticalIdentity (intent/biases that nudge probabilities)

    This is V1: it intentionally uses only currently available strength fields.
    As you expand TeamStrengthProfile (finishing, set pieces, etc.), you can
    upgrade the formulas here without changing the consumer interface.
    """

    @staticmethod
    def calculate(
        strength_a: TeamStrengthProfile,
        identity_a: TacticalIdentity,
        strength_b: TeamStrengthProfile,
        identity_b: TacticalIdentity,
    ) -> MatchupProfile:
        shot_aggr_a = _shot_aggression_bias(identity_a)
        shot_aggr_b = _shot_aggression_bias(identity_b)
        def_caution_a = _defensive_caution_bias(identity_a)
        def_caution_b = _defensive_caution_bias(identity_b)
        tempo_a = _tempo_bias(identity_a)
        tempo_b = _tempo_bias(identity_b)

        # ====================================================================
        # POSSESSION & BUILD-UP
        # ====================================================================
        # Buildup vs pressure: A buildup quality vs B pressing force
        buildup_edge = _edge_from_strength_diff(
            strength_a.build_up_quality,
            strength_b.pressing_force,
            scale=18.0,
        )

        # Pressing edge: A pressing force vs B press resistance
        pressing_edge = _edge_from_strength_diff(
            strength_a.pressing_force,
            strength_b.press_resistance,
            scale=18.0,
        )

        # Counterpressing: A's ability to press immediately after losing ball
        # vs B's transition threat (how quickly B escapes after winning ball)
        counterpressing_edge = _edge_from_strength_diff(
            strength_a.pressing_force * 0.8,  # Counterpressing requires quick reaction
            strength_b.transition_threat,
            scale=18.0,
        )

        # ====================================================================
        # SPACE CONTROL
        # ====================================================================
        # Compactness: A's defensive_compactness vs B's ability to find space/penetrate
        # (inverse: higher A compactness = better containment)
        compactness_edge = _edge_from_strength_diff(
            strength_a.defensive_compactness,
            strength_b.central_creativity,  # B's ability to unlock tight spaces
            scale=18.0,
        )

        # Defensive line edge: A's defensive line positioning vs B's ability to exploit it
        # (depends on B's counter/transition speed and A's line height via tactics)
        defensive_line_edge = _edge_from_strength_diff(
            strength_a.transition_defense,
            strength_b.transition_threat,
            scale=18.0,
        )

        # ====================================================================
        # ROUTE & CHANCE CREATION
        # ====================================================================
        # Wide edge: A's wide attack capability vs B's ability to defend flanks
        wide_edge = _edge_from_strength_diff(
            strength_a.wide_attack,
            strength_b.defensive_compactness,
            scale=20.0,
        )

        # Central edge: A's central creativity vs B's central defensive solidity
        central_edge = _edge_from_strength_diff(
            strength_a.central_creativity,
            strength_b.defensive_compactness,
            scale=20.0,
        )

        # Fullback edge: A's fullback/wing dominance in 1v1 scenarios
        # Use wide attack and press resistance as proxies for fullback quality
        fullback_edge = _edge_from_strength_diff(
            strength_a.wide_attack * 0.6 + strength_a.press_resistance * 0.4,
            strength_b.wide_attack * 0.6 + strength_b.press_resistance * 0.4,
            scale=18.0,
        )

        # ====================================================================
        # FINAL THIRD & SHOOTING
        # ====================================================================
        # Final third edge: A's ability to create and finish chances
        # Combine creativity with finishing/conversion for a fuller final-third signal.
        final_third_edge = _edge_from_strength_diff(
            (
                strength_a.central_creativity * 0.45
                + strength_a.finishing_quality * 0.35
                + strength_a.chance_conversion * 0.20
            ),
            (
                strength_b.central_defense * 0.60
                + strength_b.defensive_compactness * 0.40
            ),
            scale=18.0,
        )

        # Shooting risk edge: influenced by A's risk appetite vs B's defensive positioning
        # Higher risk should correlate with more shots (good or bad quality)
        shooting_risk_edge = _edge_from_strength_diff(
            shot_aggr_a * 50,
            def_caution_b * 50,
            scale=30.0,
        )

        # ====================================================================
        # TRANSITIONS
        # ====================================================================
        # Transition out edge: A's ability to quickly transition when winning possession
        # Driven by transition threat and counter speed bias
        transition_out_edge = _edge_from_strength_diff(
            strength_a.transition_threat,
            strength_b.defensive_compactness,
            scale=20.0,
        )

        # Transition in edge: A's defensive vulnerability when losing possession
        # (higher = better at defending transitions; opposite direction of transition_out)
        transition_in_edge = _edge_from_strength_diff(
            strength_a.defensive_compactness,
            strength_b.transition_threat,
            scale=20.0,
        )

        # ====================================================================
        # SET PIECES & AERIAL
        # ====================================================================
        # Aerial edge: A's set-piece attacking threat vs B's set-piece defense
        aerial_edge = _edge_from_strength_diff(
            (
                strength_a.aerial_threat * 0.70
                + strength_a.set_piece_attack_strength * 0.30
            ),
            (
                strength_b.aerial_threat * 0.40
                + strength_b.set_piece_defense_strength * 0.60
            ),
            scale=22.0,
        )

        # Set-piece defense edge: A's ability to defend set pieces
        setpiece_defense_edge = _edge_from_strength_diff(
            strength_a.set_piece_defense_strength,
            strength_b.set_piece_attack_strength,
            scale=22.0,
        )

        # ====================================================================
        # TEMPO & FATIGUE
        # ====================================================================
        # Tempo edge: A's comfort with pace and high activity vs B's preference
        # (this is mostly tactical; will be nudged significantly below)
        tempo_edge = _edge_from_strength_diff(
            tempo_a * 40,
            tempo_b * 40,
            scale=30.0,
        )

        # ====================================================================
        # KEY PLAYER INFLUENCE
        # ====================================================================
        # Playmaker edge: A's creative influence vs B's ability to suppress playmakers
        playmaker_edge = _edge_from_strength_diff(
            strength_a.central_creativity,
            strength_b.pressing_force,
            scale=18.0,
        )

        # Striker support edge: A's striker involvement / support lines
        # vs B's ability to isolate the striker
        striker_support_edge = _edge_from_strength_diff(
            strength_a.central_creativity * 0.9,
            strength_b.defensive_compactness * 0.8,
            scale=18.0,
        )

        profile = MatchupProfile(
            buildup_edge=buildup_edge,
            pressing_edge=pressing_edge,
            counterpressing_edge=counterpressing_edge,
            compactness_edge=compactness_edge,
            defensive_line_edge=defensive_line_edge,
            wide_edge=wide_edge,
            central_edge=central_edge,
            fullback_edge=fullback_edge,
            final_third_edge=final_third_edge,
            shooting_risk_edge=shooting_risk_edge,
            transition_out_edge=transition_out_edge,
            transition_in_edge=transition_in_edge,
            aerial_edge=aerial_edge,
            setpiece_defense_edge=setpiece_defense_edge,
            tempo_edge=tempo_edge,
            playmaker_edge=playmaker_edge,
            striker_support_edge=striker_support_edge,
        )

        # --- Tactical identity nudges (small, clamped) ---
        # Pressing: if A is more intense than B, increase pressing edge slightly.
        press_nudge = _clamp(
            (identity_a.press_intensity_bias - identity_b.press_intensity_bias) * 0.30
        )
        trigger_nudge = _clamp(
            (identity_a.press_trigger_rate - identity_b.press_trigger_rate) * 0.20
        )
        profile = replace(
            profile,
            pressing_edge=_clamp(profile.pressing_edge + press_nudge + trigger_nudge),
        )

        # Buildup: directness and short-pass bias interplay with opponent press.
        # If A is very short-pass vs a strong press profile, reduce buildup edge slightly.
        short_vs_press_penalty = (
            identity_a.short_pass_bias * identity_b.press_intensity_bias
        ) * 0.15
        profile = replace(
            profile,
            buildup_edge=_clamp(profile.buildup_edge - short_vs_press_penalty),
        )

        # Wide/Central: route bias should amplify the team’s advantage in that lane a bit.
        # (This does not create advantage; it only helps you express it.)
        wide_route_amp = (identity_a.width_bias - 0.5) * 0.20
        central_route_amp = (
            identity_a.attack_central_bias - identity_b.attack_central_bias
        ) * 0.20
        profile = replace(
            profile,
            wide_edge=_clamp(profile.wide_edge + wide_route_amp),
            central_edge=_clamp(profile.central_edge + central_route_amp),
        )

        # Fullback edge: influenced by width and fullback usage
        fullback_tactical_amp = (identity_a.width_bias - 0.5) * 0.15
        profile = replace(
            profile,
            fullback_edge=_clamp(profile.fullback_edge + fullback_tactical_amp),
        )

        # Final third & shooting: directness and shot risk bias
        shoot_amp = (shot_aggr_a - def_caution_b) * 0.20
        profile = replace(
            profile,
            final_third_edge=_clamp(profile.final_third_edge + shoot_amp * 0.7),
            shooting_risk_edge=_clamp(profile.shooting_risk_edge + shoot_amp),
        )

        # Compactness: affected by defensive mentality
        defensive_tightness = _clamp(def_caution_a - shot_aggr_b) * 0.20
        profile = replace(
            profile,
            compactness_edge=_clamp(profile.compactness_edge + defensive_tightness),
        )

        # Defensive line: if A plays high line vs B's counter threat, small penalty
        high_line_risk = (
            identity_a.defensive_line_height * identity_b.counter_trigger_bias
        ) * 0.15
        profile = replace(
            profile,
            defensive_line_edge=_clamp(profile.defensive_line_edge - high_line_risk),
        )

        # Counterpressing: high counterpress bias vs low counter-speed of opponent
        counterpress_nudge = _clamp(
            (identity_a.counterpress_bias - identity_b.counter_speed_bias) * 0.25
        )
        profile = replace(
            profile,
            counterpressing_edge=_clamp(
                profile.counterpressing_edge + counterpress_nudge
            ),
        )

        # Tempo: highly influenced by tactical tempo preference
        tempo_amp = (tempo_a - tempo_b) * 0.30
        profile = replace(
            profile,
            tempo_edge=_clamp(profile.tempo_edge + tempo_amp),
        )

        # Playmaker: affected by pressing intensity (can suppress playmakers)
        playmaker_suppress = identity_b.press_intensity_bias * 0.15
        profile = replace(
            profile,
            playmaker_edge=_clamp(profile.playmaker_edge - playmaker_suppress),
        )

        # Striker support: influenced by attacking mentality and directness
        striker_support_amp = (identity_a.attack_central_bias - def_caution_b) * 0.15
        profile = replace(
            profile,
            striker_support_edge=_clamp(
                profile.striker_support_edge + striker_support_amp
            ),
        )

        # Transition: counter bias boosts the ability to exploit transition edge.
        counter_amp = (
            identity_a.counter_trigger_bias - identity_b.counterpress_bias
        ) * 0.25
        speed_amp = (
            identity_a.counter_speed_bias - identity_b.counter_speed_bias
        ) * 0.10
        profile = replace(
            profile,
            transition_out_edge=_clamp(
                profile.transition_out_edge + counter_amp + speed_amp
            ),
        )

        # Transition defense: if B is exposed (low counterpress), A is safer
        recover_amp = (
            identity_a.counterpress_bias - identity_b.counter_speed_bias
        ) * 0.15
        profile = replace(
            profile,
            transition_in_edge=_clamp(profile.transition_in_edge + recover_amp),
        )

        # Aerial/Set piece: amplify with set-piece intent biases
        sp_amp = (
            identity_a.set_piece_attacking_bias - identity_b.set_piece_defensive_bias
        ) * 0.20
        profile = replace(
            profile,
            aerial_edge=_clamp(profile.aerial_edge + sp_amp),
            setpiece_defense_edge=_clamp(profile.setpiece_defense_edge - sp_amp),
        )

        return profile
