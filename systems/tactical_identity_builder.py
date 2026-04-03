from models.tactic import TeamTactic
from models.tactical_identity import TacticalIdentityV1


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


class TacticalIdentityBuilder:
    """
    Builds TacticalIdentityV1 from a TeamTactic.

    V1 intentionally maps only fields that the current basic engine can consume:
    - build_up_style
    - tempo
    - pressing_intensity
    - mentality

    Other TeamTactic fields are intentionally ignored in V1.
    """

    @staticmethod
    def build_v1(tactic: TeamTactic) -> TacticalIdentityV1:
        possession_tilt = 0.0
        pass_mult = 1.0
        turnover_mult = 1.0
        shot_mult = 1.0
        shot_conv_delta = 0.0

        # build_up_style
        if tactic.build_up_style == "Build From Back":
            possession_tilt += 0.08
            pass_mult += 0.08
            turnover_mult -= 0.03
            shot_mult -= 0.02
        elif tactic.build_up_style == "Long Ball":
            possession_tilt -= 0.10
            pass_mult -= 0.06
            turnover_mult += 0.05
            shot_mult += 0.06

        # tempo
        if tactic.tempo == "High":
            possession_tilt -= 0.03
            turnover_mult += 0.06
            shot_mult += 0.04
            shot_conv_delta -= 0.02
        elif tactic.tempo == "Low":
            possession_tilt += 0.03
            turnover_mult -= 0.05
            pass_mult += 0.05
            shot_mult -= 0.02
            shot_conv_delta += 0.01

        # pressing_intensity
        if tactic.pressing_intensity == "High":
            possession_tilt += 0.04
            turnover_mult += 0.03
        elif tactic.pressing_intensity == "Extreme":
            possession_tilt += 0.06
            turnover_mult += 0.06
            shot_mult += 0.02
            shot_conv_delta -= 0.01
        elif tactic.pressing_intensity == "Low":
            possession_tilt -= 0.04

        # mentality
        if tactic.mentality == "Positive":
            shot_mult += 0.06
            shot_conv_delta += 0.02
        elif tactic.mentality == "Defensive":
            shot_mult -= 0.05
            shot_conv_delta -= 0.01
            # pick one; for V1 we bias slightly toward control (not ceding)
            possession_tilt += 0.02

        # Clamp values to keep them sane for V1
        possession_tilt = _clamp(possession_tilt, -0.20, 0.20)
        pass_mult = _clamp(pass_mult, 0.80, 1.20)
        turnover_mult = _clamp(turnover_mult, 0.80, 1.20)
        shot_mult = _clamp(shot_mult, 0.80, 1.25)
        shot_conv_delta = _clamp(shot_conv_delta, -0.10, 0.10)

        return TacticalIdentityV1(
            possession_tilt=possession_tilt,
            pass_weight_mult=pass_mult,
            turnover_weight_mult=turnover_mult,
            shot_weight_mult=shot_mult,
            shot_conversion_delta=shot_conv_delta,
        )
