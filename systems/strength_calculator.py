from models.team import Team
from models.team_strength import TeamStrengthProfile


class StrengthCalculator:
    @staticmethod
    def calculate(team: Team) -> TeamStrengthProfile:
        players = team.starting_xi

        if not players:
            return TeamStrengthProfile(
                build_up_quality=0.0,
                press_resistance=0.0,
                wide_attack=0.0,
                central_creativity=0.0,
                aerial_threat=0.0,
                defensive_compactness=0.0,
                transition_threat=0.0,
                pressing_force=0.0,
            )

        build_up_quality = StrengthCalculator._average(
            players,
            [
                ("technical", "passing"),
                ("technical", "first_touch"),
                ("mental", "composure"),
                ("mental", "decisions"),
                ("mental", "vision"),
            ],
        )

        press_resistance = StrengthCalculator._average(
            players,
            [
                ("technical", "first_touch"),
                ("mental", "composure"),
                ("mental", "decisions"),
                ("physical", "balance"),
                ("physical", "agility"),
            ],
        )

        wide_attack = StrengthCalculator._average(
            players,
            [
                ("technical", "dribbling"),
                ("technical", "crossing"),
                ("physical", "pace"),
                ("mental", "off_ball"),
            ],
        )

        central_creativity = StrengthCalculator._average(
            players,
            [
                ("technical", "passing"),
                ("mental", "vision"),
                ("technical", "technique"),
                ("mental", "decisions"),
                ("mental", "off_ball"),
            ],
        )

        aerial_threat = StrengthCalculator._average(
            players,
            [
                ("technical", "heading"),
                ("physical", "jumping"),
                ("physical", "strength"),
            ],
        )

        defensive_compactness = StrengthCalculator._average(
            players,
            [
                ("mental", "positioning"),
                ("mental", "teamwork"),
                ("mental", "concentration"),
                ("technical", "marking"),
                ("technical", "tackling"),
            ],
        )

        transition_threat = StrengthCalculator._average(
            players,
            [
                ("physical", "pace"),
                ("physical", "acceleration"),
                ("mental", "off_ball"),
                ("technical", "dribbling"),
                ("mental", "decisions"),
            ],
        )

        pressing_force = StrengthCalculator._average(
            players,
            [
                ("mental", "work_rate"),
                ("mental", "aggression"),
                ("physical", "stamina"),
                ("mental", "positioning"),
                ("mental", "teamwork"),
            ],
        )

        # Apply tactical modifiers
        build_up_quality += StrengthCalculator._build_up_modifier(team)
        wide_attack += StrengthCalculator._width_modifier(team)
        transition_threat += StrengthCalculator._transition_modifier(team)
        pressing_force += StrengthCalculator._pressing_modifier(team)

        # Apply chemistry and morale scaling
        chemistry_factor = team.chemistry / 100
        morale_factor = team.morale / 100
        scaling = (chemistry_factor + morale_factor) / 2

        return TeamStrengthProfile(
            build_up_quality=round(build_up_quality * scaling, 1),
            press_resistance=round(press_resistance * scaling, 1),
            wide_attack=round(wide_attack * scaling, 1),
            central_creativity=round(central_creativity * scaling, 1),
            aerial_threat=round(aerial_threat * scaling, 1),
            defensive_compactness=round(defensive_compactness * scaling, 1),
            transition_threat=round(transition_threat * scaling, 1),
            pressing_force=round(pressing_force * scaling, 1),
        )

    @staticmethod
    def _average(players, attribute_map):
        values = []

        for player in players:
            for category, attr in attribute_map:
                category_data = getattr(player, category, {})
                values.append(category_data.get(attr, 50))

        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _build_up_modifier(team: Team) -> float:
        if team.tactic.build_up_style == "Build From Back":
            return 5.0
        if team.tactic.build_up_style == "Long Ball":
            return -3.0
        return 0.0

    @staticmethod
    def _width_modifier(team: Team) -> float:
        if team.tactic.width == "Wide":
            return 4.0
        if team.tactic.width == "Very Wide":
            return 6.0
        if team.tactic.width == "Narrow":
            return -2.0
        return 0.0

    @staticmethod
    def _transition_modifier(team: Team) -> float:
        if team.tactic.transition_on_win == "Counter Immediately":
            return 5.0
        if team.tactic.transition_on_win == "Hold Shape":
            return -2.0
        return 0.0

    @staticmethod
    def _pressing_modifier(team: Team) -> float:
        if team.tactic.pressing_intensity == "High":
            return 5.0
        if team.tactic.pressing_intensity == "Extreme":
            return 8.0
        if team.tactic.pressing_intensity == "Low":
            return -3.0
        return 0.0
