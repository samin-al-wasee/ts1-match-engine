import random
import time
from models.team import Team


class Match:
    def __init__(self, home_team: Team, away_team: Team):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.possession = {self.home_team.name: 50, self.away_team.name: 50}
        self.minute = 0
        self.event_log = []

    def start_match(self):
        print(f"🏟️ Match: {self.home_team.name} vs {self.away_team.name}")
        print(
            f"Starting XI - {self.home_team.name}: {[p.name for p in self.home_team.starting_xi]}"
        )
        print(
            f"Starting XI - {self.away_team.name}: {[p.name for p in self.away_team.starting_xi]}"
        )
        print("Kickoff! ⚽\n")

    def simulate_minute(self):
        """Simulate a single minute of the match"""
        self.minute += 1

        # Randomly decide who has possession this minute
        poss_team = random.choices(
            [self.home_team, self.away_team],
            weights=[
                self.possession[self.home_team.name],
                self.possession[self.away_team.name],
            ],
        )[0]

        # Random event generation
        event_type = random.choices(["pass", "turnover", "shot"], weights=[60, 30, 10])[
            0
        ]

        if event_type == "pass":
            player = random.choice(poss_team.starting_xi)
            event = f"🟢 {player.name} completes a pass."
        elif event_type == "turnover":
            player = random.choice(poss_team.starting_xi)
            event = f"🔴 {player.name} loses the ball."
            # Optionally switch possession
            other_team = (
                self.away_team if poss_team == self.home_team else self.home_team
            )
            self.possession[poss_team.name] -= 5
            self.possession[other_team.name] += 5
        else:  # shot
            player = random.choice(poss_team.starting_xi)
            scored = random.choices([True, False], weights=[30, 70])[0]
            if scored:
                event = f"⚽ GOAL! {player.name} scores for {poss_team.name}!"
                if poss_team == self.home_team:
                    self.home_score += 1
                else:
                    self.away_score += 1
            else:
                event = f"🔹 {player.name} takes a shot, saved by the keeper."

        self.event_log.append(f"{self.minute}' {event}")

    def simulate_match(self, total_minutes=90, display_interval=10):
        """Run the full match simulation"""
        self.start_match()
        while self.minute < total_minutes:
            self.simulate_minute()
            if self.minute % display_interval == 0 or self.minute == total_minutes:
                self.print_summary()
                time.sleep(0.1)  # pause for readability

        print("\n🏁 Full Time!")
        self.print_summary()

    def print_summary(self):
        print("\n📝 Match Summary")
        print(f"Minute: {self.minute}")
        print(
            f"Score: {self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}"
        )
        print(
            f"Possession: {self.home_team.name} {self.possession[self.home_team.name]}% | "
            f"{self.away_team.name} {self.possession[self.away_team.name]}%"
        )
        print("Recent Events:")
        for event in self.event_log[-5:]:
            print(f" - {event}")
