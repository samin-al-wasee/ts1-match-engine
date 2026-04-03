from dataclasses import dataclass


@dataclass(frozen=True)
class TacticalIdentityV1:
    """
    V1 tactical identity biases for the current basic match engine loop.

    Values are intentionally small nudges applied to baseline weights/probabilities,
    then clamped by the consumer.
    """

    # -0.20 .. +0.20 (recommended)
    possession_tilt: float = 0.0

    # multipliers applied to base event weights (recommended ranges in docs)
    pass_weight_mult: float = 1.0
    turnover_weight_mult: float = 1.0
    shot_weight_mult: float = 1.0

    # delta applied to base goal probability (recommended -0.10 .. +0.10)
    shot_conversion_delta: float = 0.0
