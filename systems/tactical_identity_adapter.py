from __future__ import annotations

from models.tactical_identity import TacticalIdentity, TacticalIdentityV1


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _clamp01(x: float) -> float:
    return _clamp(x, 0.0, 1.0)


class TacticalIdentityAdapter:
    """
    Converts full TacticalIdentity (0..1 biases) into TacticalIdentityV1 knobs
    (minute-loop friendly multipliers/deltas).

    Goal: V1 is a stable projection of the full identity (no drift).
    """

    @staticmethod
    def to_v1(full: TacticalIdentity) -> TacticalIdentityV1:
        risk = _clamp01(full.risk_taking)
        short = _clamp01(full.short_pass_bias)
        direct = _clamp01(full.directness_bias)
        vertical = _clamp01(full.vertical_progression_bias)
        press = _clamp01(full.press_intensity_bias)
        patience = _clamp01(full.shot_patience)
        long_shots = _clamp01(full.long_shot_bias)

        # ---- possession tilt (-0.20..+0.20) ----
        # More short passing + more pressing -> more control.
        # More direct + more risky -> less control.
        tilt_raw = (
            +0.55 * (short - 0.5)
            + 0.25 * (press - 0.5)
            - 0.45 * (direct - 0.5)
            - 0.35 * (risk - 0.5)
        )
        possession_tilt = _clamp(tilt_raw * 0.40, -0.20, 0.20)

        # ---- pass weight multiplier (~0.85..1.15) ----
        # Short + patience -> more passing/recycling.
        pass_weight_mult = 1.0 + (
            0.12 * (short - 0.5) + 0.08 * (patience - 0.5) - 0.06 * (direct - 0.5)
        )
        pass_weight_mult = _clamp(pass_weight_mult, 0.85, 1.15)

        # ---- turnover weight multiplier (~0.85..1.20) ----
        # Risk + vertical/direct play -> more turnovers.
        turnover_weight_mult = 1.0 + (
            0.18 * (risk - 0.5)
            + 0.10 * (vertical - 0.5)
            + 0.08 * (direct - 0.5)
            - 0.08 * (short - 0.5)
        )
        turnover_weight_mult = _clamp(turnover_weight_mult, 0.85, 1.20)

        # ---- shot weight multiplier (~0.85..1.20) ----
        # Lower patience + higher risk + long_shot tendency -> more shots.
        shot_weight_mult = 1.0 + (
            0.16 * ((0.5 - patience)) + 0.10 * (risk - 0.5) + 0.08 * (long_shots - 0.5)
        )
        shot_weight_mult = _clamp(shot_weight_mult, 0.85, 1.20)

        # ---- conversion delta (-0.10..+0.10) ----
        # High patience -> better shot selection (slightly better conversion).
        # High risk -> more forced shots (slightly worse conversion).
        shot_conversion_delta = 0.06 * (patience - 0.5) - 0.04 * (risk - 0.5)
        shot_conversion_delta = _clamp(shot_conversion_delta, -0.10, 0.10)

        return TacticalIdentityV1(
            possession_tilt=float(possession_tilt),
            pass_weight_mult=float(pass_weight_mult),
            turnover_weight_mult=float(turnover_weight_mult),
            shot_weight_mult=float(shot_weight_mult),
            shot_conversion_delta=float(shot_conversion_delta),
        )
