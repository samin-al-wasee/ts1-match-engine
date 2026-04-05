from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommentaryLine:
    minute: int
    text: str
    importance: float = 0.5  # 0..1 for filtering
