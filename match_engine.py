import random
import time
from typing import List, Optional

from models.team import Team
from models.shot import ShotResult

from debug.printer import (
    print_match_kickoff,
    print_match_event,
    print_match_summary,
    print_full_time,
    print_minute_marker,
)

# Layer 1
from systems.tactical_identity_builder import TacticalIdentityBuilder

# Layer 2
from systems.strength_calculator import StrengthCalculator

# Layer 3
from systems.matchup_calculator import MatchupCalculator

# Layer 4
from systems.match_state_factory import MatchStateFactory

# Layer 5
from systems.phase_resolver_stepwise import PhaseResolverStepwiseV1

# Layer 6
from systems.narrator import NarratorV1


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _clamp01(x: float) -> float:
    return _clamp(x, 0.0, 1.0)


class Match:
    """
    Root match runner that wires together Concept Layers 1-6.

    Note: systems/match_state_updater.py does not exist yet.
    For now we do minimal Layer-4 updates inline:
      - increment minute
      - update score fields on goal
      - apply very small fatigue drift
      - compute a simple urgency drift from late-game + score state
    """

    def __init__(self, home_team: Team, away_team: Team, seed: Optional[int] = None):
        self.home_team = home_team
        self.away_team = away_team

        self.home_score = 0
        self.away_score = 0
        self.minute = 0

        # display-only estimate
        self.possession = {self.home_team.name: 50, self.away_team.name: 50}
        self.event_log: List[str] = []

        self.rng = random.Random(seed)

        # cached layer outputs
        self.home_id_full = None
        self.away_id_full = None
        self.home_strength = None
        self.away_strength = None
        self.matchup_home_vs_away = None
        self.state = None

    def start_match(self, total_minutes: int = 90):
        print_match_kickoff(self.home_team, self.away_team)

        # ---- Layer 1 (full identity) ----
        self.home_id_full = TacticalIdentityBuilder.build_full(self.home_team.tactic)  # type: ignore
        self.away_id_full = TacticalIdentityBuilder.build_full(self.away_team.tactic)  # type: ignore

        # ---- Layer 2 (strength) ----
        self.home_strength = StrengthCalculator.calculate(self.home_team)  # type: ignore
        self.away_strength = StrengthCalculator.calculate(self.away_team)  # type: ignore

        # ---- Layer 3 (matchup) ----
        self.matchup_home_vs_away = MatchupCalculator.calculate(  # type: ignore
            self.home_strength,  # type: ignore
            self.home_id_full,  # type: ignore
            self.away_strength,  # type: ignore
            self.away_id_full,  # type: ignore
        )

        # ---- Layer 4 (kickoff state) ----
        self.state = MatchStateFactory.kickoff(  # type: ignore
            self.home_team, self.away_team, max_minutes=total_minutes
        )

    def _tick_layer4(self) -> None:
        """
        Minimal Layer 4 tick:
        - advance minute
        - drift fatigue up
        - nudge urgency based on late game + score
        """
        self.state.minute = self.minute  # type: ignore

        # fatigue drift (tune later; keep tiny)
        self.state.home.fatigue = _clamp01(self.state.home.fatigue + 0.007)  # type: ignore
        self.state.away.fatigue = _clamp01(self.state.away.fatigue + 0.007)  # type: ignore

        # urgency: trailing teams push more, leading teams push less; stronger late-game effect
        late = 1.0 if self.state.is_late_game() else 0.0  # type: ignore

        # baseline 0.50 plus adjustments
        def compute_urgency(goals_for: int, goals_against: int) -> float:
            gd = goals_for - goals_against
            # trailing => +, leading => -
            score_push = _clamp(gd * -0.10, -0.20, 0.20)
            late_push = 0.10 * late
            return _clamp01(0.50 + score_push + late_push)

        self.state.home.urgency = compute_urgency(  # type: ignore
            self.state.home.goals_for, self.state.home.goals_against  # type: ignore
        )
        self.state.away.urgency = compute_urgency(  # type: ignore
            self.state.away.goals_for, self.state.away.goals_against  # type: ignore
        )

        # momentum: gentle mean reversion toward 0.5 (events will override later)
        self.state.home.momentum = _clamp01(  # type: ignore
            self.state.home.momentum + (0.50 - self.state.home.momentum) * 0.02  # type: ignore
        )
        self.state.away.momentum = _clamp01(  # type: ignore
            self.state.away.momentum + (0.50 - self.state.away.momentum) * 0.02  # type: ignore
        )

    def _apply_goal(self, scoring_side: str) -> None:
        """
        Apply goal effects to:
        - Match scoreboard (home_score/away_score)
        - Layer 4 score fields (goals_for/goals_against)
        - small momentum swing
        """
        if scoring_side == "home":
            self.home_score += 1
            self.state.home.goals_for += 1  # type: ignore
            self.state.away.goals_against += 1  # type: ignore
            self.state.home.momentum = _clamp01(self.state.home.momentum + 0.12)  # type: ignore
            self.state.away.momentum = _clamp01(self.state.away.momentum - 0.10)  # type: ignore
        else:
            self.away_score += 1
            self.state.away.goals_for += 1  # type: ignore
            self.state.home.goals_against += 1  # type: ignore
            self.state.away.momentum = _clamp01(self.state.away.momentum + 0.12)  # type: ignore
            self.state.home.momentum = _clamp01(self.state.home.momentum - 0.10)  # type: ignore

    def _update_possession_display(self, initiative_side: str) -> None:
        """
        Display-only possession estimate (not a real possession model yet).
        """
        if initiative_side == "home":
            self.possession[self.home_team.name] = min(
                100, self.possession[self.home_team.name] + 1
            )
            self.possession[self.away_team.name] = (
                100 - self.possession[self.home_team.name]
            )
        else:
            self.possession[self.away_team.name] = min(
                100, self.possession[self.away_team.name] + 1
            )
            self.possession[self.home_team.name] = (
                100 - self.possession[self.away_team.name]
            )

    def simulate_minute(self):
        self.minute += 1

        # ---- Layer 4 tick (inline) ----
        self._tick_layer4()

        # ---- Layer 5 resolve ----
        frame = PhaseResolverStepwiseV1.resolve_frame(
            minute=self.minute,
            state=self.state,
            home_strength=self.home_strength,
            away_strength=self.away_strength,
            home_id_full=self.home_id_full,
            away_id_full=self.away_id_full,
            matchup_home_vs_away=self.matchup_home_vs_away,
            rng=self.rng,
        )

        # Score + Layer 4 goal effects
        if frame.shot_result == ShotResult.GOAL:
            self._apply_goal(frame.initiative.value)

        # UI-only possession estimate
        self._update_possession_display(frame.initiative.value)

        # ---- Layer 6 narration ----
        line = NarratorV1.narrate(frame, rng=self.rng)
        self.event_log.append(line.text)
        print_match_event(self.minute, line.text)

    def simulate_match(self, total_minutes: int = 90, display_interval: int = 10):
        self.start_match(total_minutes=total_minutes)

        while self.minute < total_minutes:
            self.simulate_minute()

            if self.minute in [15, 30, 45, 60, 75]:
                print_minute_marker(self.minute)

            if self.minute % display_interval == 0 or self.minute == total_minutes:
                self.print_summary()
                time.sleep(0.1)

        print_full_time(
            self.home_team.name, self.away_team.name, self.home_score, self.away_score
        )
        self.print_summary()

    def print_summary(self):
        print_match_summary(
            self.minute,
            self.home_score,
            self.away_score,
            self.home_team.name,
            self.away_team.name,
            self.possession[self.home_team.name],
            self.possession[self.away_team.name],
            self.event_log[-5:],
        )
