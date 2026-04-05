from __future__ import annotations

import random
from typing import Sequence


def weighted_choice(
    items: Sequence[str], weights: Sequence[float], rng: random.Random | None = None
) -> str:
    rng = rng or random # type: ignore
    total = sum(max(0.0, w) for w in weights)
    if total <= 0:
        return items[0]
    r = rng.random() * total # type: ignore
    upto = 0.0
    for item, w in zip(items, weights):
        w = max(0.0, w)
        upto += w
        if upto >= r:
            return item
    return items[-1]
