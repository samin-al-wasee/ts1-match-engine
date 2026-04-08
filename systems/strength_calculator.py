from models.team import Team
from models.player_attributes import get_player_attr
from models.team_strength import TeamStrengthProfile
from models.tactic_attributes import (
    BuildUpStyle,
    DefensiveWidth,
    PassingRisk,
    PressingIntensity,
    SetPieceAttack,
    SetPieceDefense,
    ShootingPolicy,
    TacklingAggression,
    TransitionOnLoss,
    TransitionOnWin,
    Width,
)


class StrengthCalculator:
    @staticmethod
    def calculate(team: Team) -> TeamStrengthProfile:
        players = team.starting_xi
        structural = team.structural_profile

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
                finishing_quality=0.0,
                shot_volume_tendency=0.0,
                chance_conversion=0.0,
                transition_defense=0.0,
                wide_defense=0.0,
                central_defense=0.0,
                set_piece_attack_strength=0.0,
                set_piece_defense_strength=0.0,
                possession_security=0.0,
                turnover_liability=0.0,
                discipline_control=0.0,
                gk_distribution_quality=0.0,
                gk_shot_stopping=0.0,
                chemistry=0.0,
                morale=0.0,
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

        # V1.5 expanded dimensions
        finishing_quality = StrengthCalculator._average(
            players,
            [
                ("technical", "finishing"),
                ("technical", "technique"),
                ("mental", "composure"),
                ("mental", "decisions"),
            ],
        )

        shot_volume_tendency = StrengthCalculator._average(
            players,
            [
                ("mental", "off_ball"),
                ("mental", "aggression"),
                ("technical", "long_shots"),
                ("physical", "pace"),
            ],
        )

        chance_conversion = StrengthCalculator._average(
            players,
            [
                ("technical", "finishing"),
                ("mental", "composure"),
                ("technical", "heading"),
                ("technical", "weak_foot_accuracy"),
            ],
        )

        transition_defense = StrengthCalculator._average(
            players,
            [
                ("mental", "positioning"),
                ("mental", "teamwork"),
                ("physical", "pace"),
                ("physical", "acceleration"),
                ("physical", "stamina"),
            ],
        )

        wide_defense = StrengthCalculator._average(
            players,
            [
                ("technical", "marking"),
                ("technical", "tackling"),
                ("mental", "positioning"),
                ("physical", "pace"),
            ],
        )

        central_defense = StrengthCalculator._average(
            players,
            [
                ("technical", "marking"),
                ("technical", "tackling"),
                ("mental", "positioning"),
                ("mental", "concentration"),
                ("physical", "strength"),
            ],
        )

        set_piece_attack_strength = StrengthCalculator._average(
            players,
            [
                ("technical", "heading"),
                ("physical", "jumping"),
                ("physical", "strength"),
                ("technical", "set_piece_delivery"),
                ("technical", "crossing"),
            ],
        )

        set_piece_defense_strength = StrengthCalculator._average(
            players,
            [
                ("technical", "marking"),
                ("technical", "heading"),
                ("physical", "jumping"),
                ("mental", "positioning"),
                ("technical", "gk_command_of_area"),
            ],
        )

        possession_security = StrengthCalculator._average(
            players,
            [
                ("technical", "first_touch"),
                ("technical", "short_passing"),
                ("mental", "composure"),
                ("mental", "decisions"),
                ("physical", "balance"),
            ],
        )

        discipline_control = StrengthCalculator._average(
            players,
            [
                ("mental", "discipline"),
                ("condition", "discipline"),
                ("mental", "composure"),
                ("hidden", "temperament"),
            ],
        )

        gk_distribution_quality = StrengthCalculator._average(
            players,
            [
                ("technical", "gk_kicking"),
                ("technical", "gk_throwing"),
                ("technical", "short_passing"),
                ("mental", "vision"),
            ],
        )

        gk_shot_stopping = StrengthCalculator._average(
            players,
            [
                ("technical", "gk_reflexes"),
                ("technical", "gk_handling"),
                ("technical", "gk_one_on_ones"),
                ("technical", "gk_positioning"),
            ],
        )

        chemistry = StrengthCalculator._calculate_team_chemistry(players)
        morale = StrengthCalculator._calculate_team_morale(players)

        turnover_liability = 100.0 - possession_security

        # Apply tactical modifiers
        build_up_quality += StrengthCalculator._build_up_modifier(team)
        wide_attack += StrengthCalculator._width_modifier(team)
        transition_threat += StrengthCalculator._transition_modifier(team)
        pressing_force += StrengthCalculator._pressing_modifier(team)

        possession_security += StrengthCalculator._passing_risk_security_modifier(team)
        turnover_liability += StrengthCalculator._passing_risk_turnover_modifier(team)
        shot_volume_tendency += StrengthCalculator._shooting_policy_volume_modifier(
            team
        )
        chance_conversion += StrengthCalculator._shooting_policy_conversion_modifier(
            team
        )

        transition_defense += StrengthCalculator._transition_defense_modifier(team)
        set_piece_attack_strength += StrengthCalculator._set_piece_attack_modifier(team)
        set_piece_defense_strength += StrengthCalculator._set_piece_defense_modifier(
            team
        )

        wide_defense += StrengthCalculator._defensive_width_wide_modifier(team)
        central_defense += StrengthCalculator._defensive_width_central_modifier(team)

        pressing_force += StrengthCalculator._tackling_press_modifier(team)
        discipline_control += StrengthCalculator._tackling_discipline_modifier(team)

        # Apply lineup/formation structural expression multipliers.
        wide_attack *= 1.0 + (structural.width_coverage - 0.5) * 0.18
        central_creativity *= 1.0 + (structural.central_density - 0.5) * 0.18
        chance_conversion *= 1.0 + (structural.box_presence - 0.5) * 0.14
        pressing_force *= 1.0 + (structural.press_shape_cohesion - 0.5) * 0.18
        transition_defense *= 1.0 + (structural.transition_protection - 0.5) * 0.20
        defensive_compactness *= 1.0 + (structural.rest_defense_stability - 0.5) * 0.16
        set_piece_attack_strength *= 1.0 + (structural.box_presence - 0.5) * 0.12
        set_piece_defense_strength *= (
            1.0 + (structural.rest_defense_stability - 0.5) * 0.12
        )

        # Keep all profile dimensions in a stable 0..100 style scale.
        possession_security = max(0.0, min(100.0, possession_security))
        turnover_liability = max(0.0, min(100.0, turnover_liability))
        discipline_control = max(0.0, min(100.0, discipline_control))
        chemistry = max(0.0, min(100.0, chemistry))
        morale = max(0.0, min(100.0, morale))

        # Apply chemistry and morale scaling
        chemistry_factor = chemistry / 100
        morale_factor = morale / 100
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
            finishing_quality=round(finishing_quality * scaling, 1),
            shot_volume_tendency=round(shot_volume_tendency * scaling, 1),
            chance_conversion=round(chance_conversion * scaling, 1),
            transition_defense=round(transition_defense * scaling, 1),
            wide_defense=round(wide_defense * scaling, 1),
            central_defense=round(central_defense * scaling, 1),
            set_piece_attack_strength=round(set_piece_attack_strength * scaling, 1),
            set_piece_defense_strength=round(set_piece_defense_strength * scaling, 1),
            possession_security=round(possession_security * scaling, 1),
            turnover_liability=round(turnover_liability * scaling, 1),
            discipline_control=round(discipline_control * scaling, 1),
            gk_distribution_quality=round(gk_distribution_quality * scaling, 1),
            gk_shot_stopping=round(gk_shot_stopping * scaling, 1),
            chemistry=round(chemistry, 1),
            morale=round(morale, 1),
        )

    @staticmethod
    def _average(players, attribute_map):
        values = []

        for player in players:
            for category, attr in attribute_map:
                category_data = getattr(player, category, {})
                values.append(get_player_attr(category_data, attr, default=50))

        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _calculate_team_chemistry(players) -> float:
        # Chemistry reflects cohesion and collective tactical fit.
        return StrengthCalculator._average(
            players,
            [
                ("mental", "teamwork"),
                ("mental", "leadership"),
                ("mental", "discipline"),
                ("hidden", "professionalism"),
                ("hidden", "adaptability"),
                ("condition", "morale"),
            ],
        )

    @staticmethod
    def _calculate_team_morale(players) -> float:
        # Morale reflects current emotional state and confidence.
        return StrengthCalculator._average(
            players,
            [
                ("condition", "morale"),
                ("condition", "sharpness"),
                ("condition", "match_fitness"),
                ("mental", "composure"),
                ("hidden", "consistency"),
                ("hidden", "big_matches"),
            ],
        )

    @staticmethod
    def _build_up_modifier(team: Team) -> float:
        if team.tactic.build_up_style == BuildUpStyle.BUILD_FROM_BACK:
            return 5.0
        if team.tactic.build_up_style == BuildUpStyle.LONG_BALL:
            return -3.0
        return 0.0

    @staticmethod
    def _width_modifier(team: Team) -> float:
        if team.tactic.width == Width.WIDE:
            return 4.0
        if team.tactic.width == Width.VERY_WIDE:
            return 6.0
        if team.tactic.width == Width.NARROW:
            return -2.0
        return 0.0

    @staticmethod
    def _transition_modifier(team: Team) -> float:
        if team.tactic.transition_on_win == TransitionOnWin.COUNTER_IMMEDIATELY:
            return 5.0
        if team.tactic.transition_on_win == TransitionOnWin.HOLD_SHAPE:
            return -2.0
        return 0.0

    @staticmethod
    def _pressing_modifier(team: Team) -> float:
        if team.tactic.pressing_intensity == PressingIntensity.HIGH:
            return 5.0
        if team.tactic.pressing_intensity == PressingIntensity.EXTREME:
            return 8.0
        if team.tactic.pressing_intensity == PressingIntensity.LOW:
            return -3.0
        return 0.0

    @staticmethod
    def _passing_risk_security_modifier(team: Team) -> float:
        if team.tactic.passing_risk == PassingRisk.VERY_SAFE:
            return 6.0
        if team.tactic.passing_risk == PassingRisk.SAFE:
            return 3.0
        if team.tactic.passing_risk == PassingRisk.RISKY:
            return -3.0
        if team.tactic.passing_risk == PassingRisk.VERY_RISKY:
            return -6.0
        return 0.0

    @staticmethod
    def _passing_risk_turnover_modifier(team: Team) -> float:
        if team.tactic.passing_risk == PassingRisk.VERY_SAFE:
            return -6.0
        if team.tactic.passing_risk == PassingRisk.SAFE:
            return -3.0
        if team.tactic.passing_risk == PassingRisk.RISKY:
            return 3.0
        if team.tactic.passing_risk == PassingRisk.VERY_RISKY:
            return 6.0
        return 0.0

    @staticmethod
    def _shooting_policy_volume_modifier(team: Team) -> float:
        if team.tactic.shooting_policy == ShootingPolicy.SHOOT_MORE:
            return 4.0
        if team.tactic.shooting_policy == ShootingPolicy.SHOOT_AGGRESSIVELY:
            return 7.0
        if team.tactic.shooting_policy == ShootingPolicy.SHOOT_LESS:
            return -4.0
        return 0.0

    @staticmethod
    def _shooting_policy_conversion_modifier(team: Team) -> float:
        if team.tactic.shooting_policy == ShootingPolicy.SHOOT_LESS:
            return 3.0
        if team.tactic.shooting_policy == ShootingPolicy.SHOOT_AGGRESSIVELY:
            return -4.0
        return 0.0

    @staticmethod
    def _transition_defense_modifier(team: Team) -> float:
        if team.tactic.transition_on_loss == TransitionOnLoss.REGROUP:
            return 6.0
        if team.tactic.transition_on_loss == TransitionOnLoss.DROP_DEEP_IMMEDIATELY:
            return 4.0
        if team.tactic.transition_on_loss == TransitionOnLoss.COUNTERPRESS:
            return -2.0
        return 0.0

    @staticmethod
    def _set_piece_attack_modifier(team: Team) -> float:
        if team.tactic.set_piece_attack == SetPieceAttack.TALL_PLAYER_TARGETING:
            return 7.0
        if team.tactic.set_piece_attack == SetPieceAttack.NEAR_POST_CORNERS:
            return 3.0
        if team.tactic.set_piece_attack == SetPieceAttack.FAR_POST_CORNERS:
            return 3.0
        if team.tactic.set_piece_attack == SetPieceAttack.SHORT_CORNERS:
            return -1.0
        return 0.0

    @staticmethod
    def _set_piece_defense_modifier(team: Team) -> float:
        if team.tactic.set_piece_defense == SetPieceDefense.ZONAL_MARKING:
            return 4.0
        if team.tactic.set_piece_defense == SetPieceDefense.MAN_MARKING:
            return 4.0
        if team.tactic.set_piece_defense == SetPieceDefense.NEAR_POST_GUARD:
            return 2.0
        if team.tactic.set_piece_defense == SetPieceDefense.LEAVE_PLAYERS_UP:
            return -3.0
        return 0.0

    @staticmethod
    def _defensive_width_wide_modifier(team: Team) -> float:
        if team.tactic.defensive_width == DefensiveWidth.WIDE:
            return 4.0
        if team.tactic.defensive_width == DefensiveWidth.VERY_WIDE:
            return 6.0
        if team.tactic.defensive_width == DefensiveWidth.NARROW:
            return -3.0
        if team.tactic.defensive_width == DefensiveWidth.VERY_NARROW:
            return -5.0
        return 0.0

    @staticmethod
    def _defensive_width_central_modifier(team: Team) -> float:
        if team.tactic.defensive_width == DefensiveWidth.NARROW:
            return 4.0
        if team.tactic.defensive_width == DefensiveWidth.VERY_NARROW:
            return 6.0
        if team.tactic.defensive_width == DefensiveWidth.WIDE:
            return -3.0
        if team.tactic.defensive_width == DefensiveWidth.VERY_WIDE:
            return -5.0
        return 0.0

    @staticmethod
    def _tackling_press_modifier(team: Team) -> float:
        if team.tactic.tackling_aggression == TacklingAggression.AGGRESSIVE:
            return 2.0
        if team.tactic.tackling_aggression == TacklingAggression.VERY_AGGRESSIVE:
            return 4.0
        if team.tactic.tackling_aggression == TacklingAggression.STAY_ON_FEET:
            return -1.0
        return 0.0

    @staticmethod
    def _tackling_discipline_modifier(team: Team) -> float:
        if team.tactic.tackling_aggression == TacklingAggression.STAY_ON_FEET:
            return 4.0
        if team.tactic.tackling_aggression == TacklingAggression.AGGRESSIVE:
            return -3.0
        if team.tactic.tackling_aggression == TacklingAggression.VERY_AGGRESSIVE:
            return -6.0
        return 0.0
