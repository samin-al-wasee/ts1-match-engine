from __future__ import annotations

from enum import StrEnum


class Duty(StrEnum):
    """
    V1 duty/intention modifier.

    Balanced is included as a first-class value per docs:
    used when a role has no duty variants in V1.
    """

    DEFEND = "Defend"
    SUPPORT = "Support"
    ATTACK = "Attack"
    BALANCED = "Balanced"
