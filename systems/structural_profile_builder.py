from __future__ import annotations

from typing import Dict, Iterable, List

from models.lineup import MatchLineup
from models.player import Player
from models.structural_profile import StructuralProfile
from models.player_attributes import get_player_attr


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _avg(values: Iterable[float], default: float = 0.5) -> float:
    vals = list(values)
    if not vals:
        return default
    return sum(vals) / len(vals)


class StructuralProfileBuilder:
    """Derives structure metrics from formation + lineup assignments + roles."""

    @staticmethod
    def _role_fit(player: Player, role_name: str) -> float:
        role = role_name.lower()
        tech = player.technical
        mental = player.mental
        physical = player.physical

        if "wing" in role:
            score = _avg(
                [
                    get_player_attr(tech, "dribbling") / 100.0,
                    get_player_attr(tech, "crossing") / 100.0,
                    get_player_attr(physical, "pace") / 100.0,
                    get_player_attr(mental, "off_ball") / 100.0,
                ]
            )
            return _clamp01(score)

        if (
            "forward" in role
            or "striker" in role
            or "poacher" in role
            or "target" in role
        ):
            score = _avg(
                [
                    get_player_attr(tech, "finishing") / 100.0,
                    get_player_attr(mental, "composure") / 100.0,
                    get_player_attr(mental, "off_ball") / 100.0,
                    get_player_attr(physical, "strength") / 100.0,
                ]
            )
            return _clamp01(score)

        if "defender" in role or "back" in role:
            score = _avg(
                [
                    get_player_attr(tech, "marking") / 100.0,
                    get_player_attr(tech, "tackling") / 100.0,
                    get_player_attr(mental, "positioning") / 100.0,
                    get_player_attr(mental, "concentration") / 100.0,
                ]
            )
            return _clamp01(score)

        if "keeper" in role:
            score = _avg(
                [
                    get_player_attr(tech, "gk_reflexes") / 100.0,
                    get_player_attr(tech, "gk_handling") / 100.0,
                    get_player_attr(tech, "gk_positioning") / 100.0,
                ]
            )
            return _clamp01(score)

        # Midfield/playmaker default profile
        score = _avg(
            [
                get_player_attr(tech, "short_passing") / 100.0,
                get_player_attr(tech, "technique") / 100.0,
                get_player_attr(mental, "vision") / 100.0,
                get_player_attr(mental, "decisions") / 100.0,
            ]
        )
        return _clamp01(score)

    @staticmethod
    def build(lineup: MatchLineup, players: List[Player]) -> StructuralProfile:
        by_id: Dict[int, Player] = {player.id: player for player in players}

        fits: List[float] = []
        role_fits: List[float] = []
        lateral_wide = 0
        lateral_center = 0
        high_line_count = 0
        deep_line_count = 0
        support_links = 0
        adjacency_links = 0

        for assignment in lineup.slot_assignments:
            slot = lineup.formation.slot_by_id(assignment.slot_id)
            player = by_id.get(assignment.player_id)
            if slot is None or player is None:
                continue

            pos_fit = (
                1.0
                if not slot.preferred_positions
                or player.position in slot.preferred_positions
                else 0.65
            )
            fits.append(pos_fit)
            role_fits.append(
                StructuralProfileBuilder._role_fit(
                    player,
                    assignment.role_assignment.role_name.value,
                )
            )

            if "wide" in slot.lateral_band:
                lateral_wide += 1
            if slot.lateral_band in {"center", "left_halfspace", "right_halfspace"}:
                lateral_center += 1
            if slot.vertical_band == "high":
                high_line_count += 1
            if slot.vertical_band == "deep":
                deep_line_count += 1

            support_links += len(slot.support_links)
            adjacency_links += len(slot.adjacency_slots)

        starter_count = max(1, len(lineup.slot_assignments))
        width_coverage = _clamp01(lateral_wide / starter_count)
        central_density = _clamp01(lateral_center / starter_count)

        support_network_quality = _clamp01(
            _avg(fits) * 0.45
            + _avg(role_fits) * 0.35
            + _clamp01(support_links / max(1, adjacency_links)) * 0.20
        )

        formation_tags = lineup.formation.structural_tags
        box_presence = _clamp01(
            (high_line_count / starter_count) * 0.60
            + formation_tags.get("natural_width", 0.5) * 0.20
            + _avg(role_fits) * 0.20
        )

        rest_defense_stability = _clamp01(
            (deep_line_count / starter_count) * 0.45
            + formation_tags.get("rest_defense_shape", 0.5) * 0.35
            + _avg(fits) * 0.20
        )

        press_shape_cohesion = _clamp01(
            formation_tags.get("press_front_line", 0.5) * 0.45
            + _avg(role_fits) * 0.25
            + _avg(
                get_player_attr(by_id[a.player_id].mental, "work_rate", 50) / 100.0
                for a in lineup.slot_assignments
                if a.player_id in by_id
            )
            * 0.30
        )

        transition_protection = _clamp01(
            rest_defense_stability * 0.55
            + _avg(
                get_player_attr(by_id[a.player_id].mental, "positioning", 50) / 100.0
                for a in lineup.slot_assignments
                if a.player_id in by_id
            )
            * 0.45
        )

        half_space_slot_hits = 0
        for assignment in lineup.slot_assignments:
            slot = lineup.formation.slot_by_id(assignment.slot_id)
            if slot is None:
                continue
            if slot.lateral_band in {"left_halfspace", "right_halfspace"}:
                half_space_slot_hits += 1
        half_space_access = _clamp01(
            _clamp01(half_space_slot_hits / max(1, starter_count)) * 0.60
            + _avg(role_fits) * 0.40
        )

        flank_isolation_risk = _clamp01(
            1.0
            - (
                width_coverage * 0.45
                + support_network_quality * 0.35
                + transition_protection * 0.20
            )
        )

        return StructuralProfile(
            width_coverage=width_coverage,
            central_density=central_density,
            support_network_quality=support_network_quality,
            box_presence=box_presence,
            rest_defense_stability=rest_defense_stability,
            press_shape_cohesion=press_shape_cohesion,
            transition_protection=transition_protection,
            half_space_access=half_space_access,
            flank_isolation_risk=flank_isolation_risk,
            slot_fit_score=_avg(fits),
            role_coherence=_avg(role_fits),
        )
