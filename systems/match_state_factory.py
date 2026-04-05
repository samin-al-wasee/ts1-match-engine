from __future__ import annotations


from models.match_state import MatchState, TeamMatchState
from models.team import Team


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _norm100(x: float) -> float:
    """Normalize 0..100-ish to 0..1 with clamping."""
    return _clamp01(x / 100.0)


class MatchStateFactory:
    """
    Creates initial Layer 4 state at kickoff.

    Option 2 seeding:
    - morale influences initial momentum (confidence/flow baseline)
    - chemistry influences initial discipline + a bit of coordination stability
    """

    @staticmethod
    def kickoff(home_team: Team, away_team: Team, max_minutes: int = 90) -> MatchState:
        def seed_team(t: Team) -> TeamMatchState:
            morale = _norm100(t.morale)  # 0..1
            chemistry = _norm100(t.chemistry)  # 0..1

            # Momentum baseline leans on morale.
            # Keep it close to 0.5 so in-match events still matter a lot.
            momentum = _clamp01(
                0.35 + 0.30 * morale
            )  # morale 0..1 -> momentum ~0.35..0.65

            # Discipline baseline leans on chemistry (cohesion reduces reckless actions).
            discipline = _clamp01(0.45 + 0.40 * chemistry)  # ~0.45..0.85

            # Start fresh; you can later seed fatigue from schedule congestion/injuries.
            fatigue = 0.0

            # Urgency will be computed by MatchStateUpdater.tick() from score+minute,
            # but set a reasonable kickoff baseline.
            urgency = 0.50

            return TeamMatchState(
                goals_for=0,
                goals_against=0,
                momentum=momentum,
                urgency=urgency,
                discipline=discipline,
                fatigue=fatigue,
            )

        return MatchState(
            minute=0,
            max_minutes=max_minutes,
            home=seed_team(home_team),
            away=seed_team(away_team),
        )
