import random

from models.position import Position
from models.role import Role

# --- Attribute generation helpers (V1: 1..100) ------------------------------


def _clamp100(x: int) -> int:
    return max(1, min(100, int(x)))


def _jitter(val: int, spread: int = 6) -> int:
    return _clamp100(val + random.randint(-spread, spread))


def _mk_from_base(base: dict[str, int], spread: int = 6) -> dict[str, int]:
    return {k: _jitter(v, spread=spread) for k, v in base.items()}


def generate_player_attribute_groups(
    position: Position, role: Role
) -> tuple[
    dict[str, int], dict[str, int], dict[str, int], dict[str, int], dict[str, int]
]:
    """
    Returns: (technical, mental, physical, hidden, condition)
    All values 1..100.
    """

    # Core keys used by StrengthCalculator (keep these present)
    TECH_BASE = {
        "passing": 50,
        "first_touch": 50,
        "technique": 50,
        "dribbling": 50,
        "crossing": 50,
        "heading": 50,
        "marking": 50,
        "tackling": 50,
    }
    MENT_BASE = {
        "composure": 50,
        "decisions": 50,
        "vision": 50,
        "off_ball": 50,
        "positioning": 50,
        "teamwork": 50,
        "concentration": 50,
        "work_rate": 50,
        "aggression": 50,
    }
    PHYS_BASE = {
        "pace": 50,
        "acceleration": 50,
        "balance": 50,
        "agility": 50,
        "jumping": 50,
        "strength": 50,
        "stamina": 50,  # physical capacity (not the condition dict)
    }

    # GK keys (in doc)
    GK_TECH = {
        "gk_handling": 50,
        "gk_reflexes": 50,
        "gk_one_on_ones": 50,
        "gk_kicking": 50,
        "gk_command_of_area": 50,
    }

    # Hidden/personality keys (in doc)
    HIDDEN_BASE = {
        "consistency": 55,
        "big_matches": 50,
        "professionalism": 55,
        "ambition": 55,
        "temperament": 50,
        "loyalty": 50,
        "adaptability": 55,
        "injury_proneness": 45,  # lower is better, but we still keep it 1..100
    }

    # Condition/readiness keys (in doc)
    CONDITION_BASE = {
        "match_fitness": 80,
        "sharpness": 75,
        "morale": 75,
        "fatigue": 5,  # 0 is perfect; start slightly above 0
        "discipline": 75,
    }

    # --- Position archetypes ------------------------------------------------
    # Start from neutral 50s then bias by position group.
    tech = dict(TECH_BASE)
    ment = dict(MENT_BASE)
    phys = dict(PHYS_BASE)
    hidden = dict(HIDDEN_BASE)
    condition = dict(CONDITION_BASE)

    if position == Position.GK:
        # Goalkeepers: GK tech high, foot skills moderate, speed lower.
        tech.update(
            {
                "passing": 48,
                "first_touch": 46,
                "technique": 48,
                "dribbling": 35,
                "crossing": 25,
                "heading": 30,
                "marking": 30,
                "tackling": 28,
            }
        )
        tech.update(GK_TECH)
        ment.update(
            {
                "composure": 58,
                "decisions": 55,
                "vision": 48,
                "positioning": 58,
                "concentration": 60,
                "teamwork": 52,
                "work_rate": 48,
                "aggression": 40,
                "off_ball": 25,
            }
        )
        phys.update(
            {
                "pace": 35,
                "acceleration": 35,
                "agility": 55,
                "balance": 55,
                "jumping": 55,
                "strength": 52,
                "stamina": 45,
            }
        )
    elif position in (Position.CB,):
        tech.update(
            {
                "passing": 50,
                "first_touch": 46,
                "technique": 46,
                "dribbling": 38,
                "crossing": 25,
                "heading": 68,
                "marking": 68,
                "tackling": 67,
            }
        )
        ment.update(
            {
                "positioning": 66,
                "concentration": 62,
                "decisions": 56,
                "teamwork": 58,
                "aggression": 58,
                "composure": 54,
                "off_ball": 35,
                "vision": 40,
                "work_rate": 55,
            }
        )
        phys.update(
            {
                "pace": 52,
                "acceleration": 48,
                "strength": 68,
                "jumping": 66,
                "stamina": 56,
                "agility": 45,
                "balance": 55,
            }
        )
    elif position in (Position.RB, Position.LB):
        tech.update(
            {
                "passing": 54,
                "first_touch": 52,
                "technique": 52,
                "dribbling": 55,
                "crossing": 62,
                "heading": 45,
                "marking": 58,
                "tackling": 58,
            }
        )
        ment.update(
            {
                "positioning": 56,
                "concentration": 54,
                "decisions": 54,
                "teamwork": 58,
                "work_rate": 65,
                "off_ball": 55,
                "vision": 45,
                "aggression": 55,
                "composure": 50,
            }
        )
        phys.update(
            {
                "pace": 66,
                "acceleration": 66,
                "stamina": 66,
                "agility": 58,
                "balance": 55,
                "strength": 50,
                "jumping": 45,
            }
        )
    elif position in (Position.DM, Position.CM):
        tech.update(
            {
                "passing": 62,
                "first_touch": 58,
                "technique": 58,
                "dribbling": 52,
                "crossing": 40,
                "heading": 48,
                "marking": 55,
                "tackling": 58,
            }
        )
        ment.update(
            {
                "vision": 58,
                "decisions": 60,
                "composure": 58,
                "teamwork": 62,
                "work_rate": 62,
                "positioning": 58,
                "concentration": 56,
                "off_ball": 52,
                "aggression": 55,
            }
        )
        phys.update(
            {
                "stamina": 62,
                "pace": 55,
                "acceleration": 52,
                "agility": 52,
                "balance": 55,
                "strength": 55,
                "jumping": 50,
            }
        )
    elif position in (Position.AM, Position.RW, Position.LW):
        tech.update(
            {
                "passing": 62,
                "first_touch": 65,
                "technique": 66,
                "dribbling": 68,
                "crossing": 60 if position in (Position.RW, Position.LW) else 45,
                "heading": 40,
                "marking": 35,
                "tackling": 35,
            }
        )
        ment.update(
            {
                "vision": 65,
                "decisions": 60,
                "off_ball": 66,
                "composure": 58,
                "teamwork": 55,
                "work_rate": 55,
                "concentration": 52,
                "positioning": 40,
                "aggression": 45,
            }
        )
        phys.update(
            {
                "pace": 70 if position in (Position.RW, Position.LW) else 60,
                "acceleration": 72 if position in (Position.RW, Position.LW) else 62,
                "agility": 66,
                "balance": 55,
                "stamina": 58,
                "strength": 45,
                "jumping": 42,
            }
        )
    elif position == Position.ST:
        tech.update(
            {
                "passing": 48,
                "first_touch": 62,
                "technique": 60,
                "dribbling": 58,
                "crossing": 25,
                "heading": 66,
                "marking": 25,
                "tackling": 25,
            }
        )
        ment.update(
            {
                "off_ball": 68,
                "composure": 62,
                "decisions": 58,
                "vision": 45,
                "teamwork": 50,
                "work_rate": 52,
                "concentration": 55,
                "positioning": 30,
                "aggression": 55,
            }
        )
        phys.update(
            {
                "pace": 65,
                "acceleration": 63,
                "strength": 62,
                "jumping": 62,
                "stamina": 58,
                "agility": 52,
                "balance": 55,
            }
        )

    # --- Role tweaks (small, V1-friendly) -----------------------------------
    # (Only adjust a few key stats; keep it simple.)
    if role == Role.BALL_PLAYING_DEFENDER:
        tech["passing"] = _clamp100(tech["passing"] + 8)
        tech["first_touch"] = _clamp100(tech["first_touch"] + 6)
        ment["vision"] = _clamp100(ment["vision"] + 6)
        ment["composure"] = _clamp100(ment["composure"] + 4)

    if role == Role.WING_BACK:
        tech["crossing"] = _clamp100(tech["crossing"] + 6)
        phys["stamina"] = _clamp100(phys["stamina"] + 6)
        phys["pace"] = _clamp100(phys["pace"] + 4)
        ment["work_rate"] = _clamp100(ment["work_rate"] + 4)

    if role == Role.ANCHOR_HOLDING_MIDFIELDER or role == Role.HALF_BACK:
        ment["positioning"] = _clamp100(ment["positioning"] + 6)
        tech["tackling"] = _clamp100(tech["tackling"] + 4)
        tech["marking"] = _clamp100(tech["marking"] + 4)
        ment["decisions"] = _clamp100(ment["decisions"] + 2)

    if role == Role.TREQUARTISTA_PLAYMAKER_FREE_ATTACKING_MIDFIELDER:
        tech["passing"] = _clamp100(tech["passing"] + 6)
        ment["vision"] = _clamp100(ment["vision"] + 8)
        tech["dribbling"] = _clamp100(tech["dribbling"] + 4)
        ment["work_rate"] = _clamp100(ment["work_rate"] - 4)

    if role == Role.WINGER:
        tech["dribbling"] = _clamp100(tech["dribbling"] + 4)
        tech["crossing"] = _clamp100(tech["crossing"] + 4)
        phys["pace"] = _clamp100(phys["pace"] + 4)

    if role == Role.ADVANCED_FORWARD:
        ment["off_ball"] = _clamp100(ment["off_ball"] + 6)
        phys["pace"] = _clamp100(phys["pace"] + 4)
        ment["composure"] = _clamp100(ment["composure"] + 2)

    if role == Role.SHOT_STOPPER:
        # GK specialization
        tech["gk_reflexes"] = _clamp100(tech.get("gk_reflexes", 50) + 8)
        tech["gk_handling"] = _clamp100(tech.get("gk_handling", 50) + 6)
        ment["concentration"] = _clamp100(ment["concentration"] + 4)

    # Hidden tweaks: keep around 40-70 typically
    hidden = _mk_from_base(hidden, spread=5)
    hidden["professionalism"] = _clamp100(
        hidden["professionalism"] + random.randint(-3, 8)
    )
    hidden["consistency"] = _clamp100(hidden["consistency"] + random.randint(-3, 8))
    hidden["injury_proneness"] = _clamp100(
        hidden["injury_proneness"] + random.randint(-5, 5)
    )

    # Condition: should look "game-ready"
    condition = _mk_from_base(condition, spread=3)
    condition["fatigue"] = _clamp100(max(0, condition["fatigue"]))  # keep low

    # Apply jitter to the main groups last (so role tweaks still vary slightly)
    tech = _mk_from_base(tech, spread=6)
    ment = _mk_from_base(ment, spread=6)
    phys = _mk_from_base(phys, spread=6)

    return tech, ment, phys, hidden, condition
