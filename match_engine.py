import random
import time
from typing import List
from models.team import Team
from debug.printer import (
    print_match_kickoff,
    print_match_event,
    print_match_summary,
    print_full_time,
    print_minute_marker,
)

from systems.tactical_identity_builder import TacticalIdentityBuilder


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


class Match:
    def __init__(self, home_team: Team, away_team: Team):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.possession = {self.home_team.name: 50, self.away_team.name: 50}
        self.minute = 0
        self.event_log: List[str] = []

    def start_match(self):
        """Print match start using Rich printer"""
        print_match_kickoff(self.home_team, self.away_team)

    def simulate_minute(self):
        """Simulate a single minute of the match"""
        self.minute += 1

        # --- Tactical Identity (V1) ---
        # Convert tactics into small probability nudges for the current basic engine.
        home_id = TacticalIdentityBuilder.build_v1(self.home_team.tactic)
        away_id = TacticalIdentityBuilder.build_v1(self.away_team.tactic)

        # --- Possession selection (tactically-shaped) ---
        # Base weights come from current possession values, but we apply a small tilt.
        # tilt is relative: home tilt up + away tilt down (and vice versa).
        # Map possession_tilt (-0.20..+0.20) to at most about +/-10 possession points.
        tilt_points = 50.0 * (home_id.possession_tilt - away_id.possession_tilt)
        tilt_points = _clamp(tilt_points, -10.0, 10.0)

        home_poss_w = max(
            1.0, float(self.possession[self.home_team.name]) + tilt_points
        )
        away_poss_w = max(
            1.0, float(self.possession[self.away_team.name]) - tilt_points
        )

        poss_team = random.choices(
            [self.home_team, self.away_team],
            weights=[home_poss_w, away_poss_w],
        )[0]

        # Determine which identity applies for event resolution
        tid = home_id if poss_team == self.home_team else away_id

        # --- Event generation (tactically-shaped) ---
        # Base event weights reflect current engine defaults.
        base_pass_w, base_turnover_w, base_shot_w = 60.0, 30.0, 10.0

        pass_w = max(0.1, base_pass_w * tid.pass_weight_mult)
        turnover_w = max(0.1, base_turnover_w * tid.turnover_weight_mult)
        shot_w = max(0.1, base_shot_w * tid.shot_weight_mult)

        event_type = random.choices(
            ["pass", "turnover", "shot"],
            weights=[pass_w, turnover_w, shot_w],
        )[0]

        if event_type == "pass":
            player = random.choice(poss_team.starting_xi)
            event = f"🟢 {player.name} completes a pass."

        elif event_type == "turnover":
            player = random.choice(poss_team.starting_xi)
            event = f"🔴 {player.name} loses the ball."
            # Switch possession
            other_team = (
                self.away_team if poss_team == self.home_team else self.home_team
            )
            self.possession[poss_team.name] -= 5
            self.possession[other_team.name] += 5

        else:  # shot
            player = random.choice(poss_team.starting_xi)

            # Base goal probability is 0.30 in current engine; apply tactical delta and clamp.
            goal_prob = _clamp(0.30 + tid.shot_conversion_delta, 0.05, 0.60)
            scored = random.random() < goal_prob

            if scored:
                event = f"⚽ GOAL! {player.name} scores for {poss_team.name}!"
                if poss_team == self.home_team:
                    self.home_score += 1
                else:
                    self.away_score += 1
            else:
                event = f"🔹 {player.name} takes a shot, saved by the keeper."

        self.event_log.append(f"{self.minute}' {event}")
        # Use Rich printer for event
        print_match_event(self.minute, event)

    def simulate_match(self, total_minutes=90, display_interval=10):
        """Run the full match simulation"""

        self.start_match()
        while self.minute < total_minutes:
            self.simulate_minute()

            # Print minute markers for key intervals
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
        """Print match summary using Rich printer"""
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
