from __future__ import annotations

import random

from models.commentary import CommentaryLine
from models.phase_v2 import InitiativeResult, ProgressionResult, Route, PhaseFrame
from models.chance import ChanceType
from models.shot import ShotResult


def _side_name(side: InitiativeResult) -> str:
    return "Home" if side == InitiativeResult.HOME else "Away"


def _route_text(route: Route) -> str:
    if route == Route.LEFT:
        return "down the left"
    if route == Route.RIGHT:
        return "down the right"
    return "through the middle"


def _chance_text(ct: ChanceType) -> str:
    mapping = {
        ChanceType.THROUGH_BALL: "a through ball",
        ChanceType.CROSS: "a cross",
        ChanceType.CUTBACK: "a cutback",
        ChanceType.DRIBBLE: "a dribble",
        ChanceType.LONG_SHOT: "a long-range hit",
    }
    return mapping.get(ct, "a chance")


class NarratorV1:
    """
    Layer 6: narration only.
    Takes PhaseFrame (Layer 5 output) and returns a CommentaryLine.
    Does not mutate state or affect probabilities.
    """

    @staticmethod
    def narrate(frame: PhaseFrame, rng: random.Random | None = None) -> CommentaryLine:
        rng = rng or random  # type: ignore

        m = frame.minute
        side = _side_name(frame.initiative)
        route = _route_text(frame.route)

        # Step 5: goal/shot commentary
        if frame.shot_result == ShotResult.GOAL:
            xg_txt = f"{frame.xg:.2f}" if frame.xg is not None else "?"
            ct_txt = (
                _chance_text(frame.chance_type) if frame.chance_type else "the move"
            )
            templates = [
                f"{m}' Goal {side}! {ct_txt.capitalize()} opens them up {route}. (xG {xg_txt})",
                f"{m}' {side} score! They break through {route} and finish. (xG {xg_txt})",
                f"{m}' It’s in! {side} strike after attacking {route}. (xG {xg_txt})",
            ]
            return CommentaryLine(minute=m, text=rng.choice(templates), importance=1.0)  # type: ignore

        if frame.shot_result == ShotResult.SHOT:
            xg_txt = f"{frame.xg:.2f}" if frame.xg is not None else "?"
            ct_txt = (
                _chance_text(frame.chance_type) if frame.chance_type else "a chance"
            )
            templates = [
                f"{m}' Shot {side}! {ct_txt.capitalize()} creates an opening {route}. (xG {xg_txt})",
                f"{m}' {side} threaten {route}—they get a shot away. (xG {xg_txt})",
                f"{m}' {side} go close {route}, but it stays out. (xG {xg_txt})",
            ]
            return CommentaryLine(minute=m, text=rng.choice(templates), importance=0.75)  # type: ignore

        # No shot: progression narratives
        if frame.progression == ProgressionResult.TURNOVER:
            templates = [
                f"{m}' {side} lose possession {route}.",
                f"{m}' Turnover—{side} can’t progress {route} and give it away.",
                f"{m}' {side} try to force it {route}, but the ball is lost.",
            ]
            return CommentaryLine(minute=m, text=rng.choice(templates), importance=0.35)  # type: ignore

        if frame.progression == ProgressionResult.ADVANCE:
            # (If later you decouple ADVANCE -> shot, this remains useful)
            ct_txt = (
                _chance_text(frame.chance_type) if frame.chance_type else "the attack"
            )
            templates = [
                f"{m}' {side} move forward {route}.",
                f"{m}' Good progression by {side} {route}—{ct_txt} looks on.",
            ]
            return CommentaryLine(minute=m, text=rng.choice(templates), importance=0.40)  # type: ignore

        # STALLED
        templates = [
            f"{m}' {side} recycle the ball {route}, no opening yet.",
            f"{m}' Patient possession from {side} {route}.",
            f"{m}' {side} slow it down {route} and keep control.",
        ]
        return CommentaryLine(minute=m, text=rng.choice(templates), importance=0.20)  # type: ignore
