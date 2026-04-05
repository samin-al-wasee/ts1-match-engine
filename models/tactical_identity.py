from dataclasses import dataclass


@dataclass(frozen=True)
class TacticalIdentity:
    """
    Full Tactical Identity modifier catalog (Concept Layer 1).

    This is the long-term bias layer that should eventually power:
    - route selection (left/central/right, wide vs narrow)
    - chance type selection (through balls, crosses, cutbacks, long shots, 1v1 isolations)
    - pressing triggers & defensive shape
    - transitions (counter vs hold; counter speed; counterpress)
    - set-piece tendencies

    This class also includes engine-facing fields used by the current minute-loop,
    so there is a single tactical identity model for both present and future layers.

    Conventions:
    - Most "bias" values use 0..1 (where 0 = low/left/zonal/etc, 1 = high/right/man/etc depending on the field).
    - Consumers should clamp/renormalize as appropriate.
    """

    # ---- Possession / risk profile ----
    # 0..1: 0 = very controlled, 1 = very chaotic/risky
    risk_taking: float = 0.50

    # ---- Build-up / progression ----
    # 0..1: 0 = short/passive, 1 = direct/vertical
    directness_bias: float = 0.50
    vertical_progression_bias: float = 0.50
    short_pass_bias: float = 0.50

    # ---- Width / attacking preference ----
    # 0..1: 0 = very narrow, 1 = very wide
    width_bias: float = 0.50

    # 0..1 each; consumers may renormalize to sum to 1
    attack_left_bias: float = 0.33
    attack_central_bias: float = 0.34
    attack_right_bias: float = 0.33

    # ---- Chance type / final third ----
    through_ball_bias: float = 0.35
    cross_bias: float = 0.30
    cutback_bias: float = 0.25
    dribble_creation_bias: float = 0.25
    long_shot_bias: float = 0.20

    # 0..1: 0 = shoot quickly, 1 = patient shot selection
    shot_patience: float = 0.50

    # ---- Defensive shape / pressing ----
    # 0..1: 0 = very deep, 1 = very high
    defensive_line_height: float = 0.50

    # 0..1: 0 = very low press, 1 = very high press
    press_intensity_bias: float = 0.50

    # 0..1: how often pressing triggers occur
    press_trigger_rate: float = 0.50

    # 0..1: 0 = very narrow, 1 = very wide
    defensive_width_bias: float = 0.50

    # 0..1: 0 = very loose, 1 = very compact
    compactness_bias: float = 0.50

    # 0..1: 0 = zonal, 1 = man
    marking_bias: float = 0.00

    # 0..1: 0 = cautious, 1 = aggressive
    tackling_aggression_bias: float = 0.50

    # ---- Transitions ----
    # 0..1: 0 = always hold/reset, 1 = counter immediately
    counter_trigger_bias: float = 0.50

    # 0..1: 0 = fall back, 1 = counterpress always
    counterpress_bias: float = 0.50

    # 0..1: 0 = slow, 1 = very fast
    counter_speed_bias: float = 0.50

    # ---- Set pieces ----
    # 0..1: 0 = short routines, 1 = delivery to box
    set_piece_attacking_bias: float = 0.50

    # 0..1: 0 = zonal, 1 = man
    set_piece_defensive_bias: float = 0.00

    # ---- Current minute-loop engine-facing knobs ----
    # -0.20 .. +0.20 (recommended)
    possession_tilt: float = 0.0

    # multipliers applied to base event weights (recommended ranges in docs)
    pass_weight_mult: float = 1.0
    turnover_weight_mult: float = 1.0
    shot_weight_mult: float = 1.0

    # delta applied to base goal probability (recommended -0.10 .. +0.10)
    shot_conversion_delta: float = 0.0
