from dataclasses import dataclass, field
from typing import Dict

from models.position import Position
from models.role import Role
from models.duty import Duty


@dataclass
class Player:
    id: int
    name: str
    position: Position
    role: Role
    duty: Duty

    technical: Dict[str, int] = field(default_factory=dict)
    mental: Dict[str, int] = field(default_factory=dict)
    physical: Dict[str, int] = field(default_factory=dict)
    hidden: Dict[str, int] = field(default_factory=dict)
    condition: Dict[str, int] = field(default_factory=dict)

    def overall_summary(self) -> str:
        return f"{self.name} ({self.position}) - {self.role} [{self.duty}]"
