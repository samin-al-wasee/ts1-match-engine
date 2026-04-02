from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Player:
    id: int
    name: str
    position: str
    role: str
    duty: str

    technical: Dict[str, int] = field(default_factory=dict)
    mental: Dict[str, int] = field(default_factory=dict)
    physical: Dict[str, int] = field(default_factory=dict)

    stamina: float = 100.0
    morale: float = 75.0
    sharpness: float = 75.0
    discipline: float = 75.0

    def overall_summary(self) -> str:
        return f"{self.name} ({self.position}) - {self.role} [{self.duty}]"
