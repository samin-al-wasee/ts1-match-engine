from dataclasses import dataclass, field
from datetime import date
from typing import Dict

from models.player_attributes import Footedness
from models.position import Position
from models.role import Role
from models.duty import Duty


@dataclass
class Player:
    id: int
    name: str
    date_of_birth: date
    height_cm: float
    weight_kg: float

    position: Position
    role: Role
    duty: Duty
    footedness: Footedness

    technical: Dict[str, int] = field(default_factory=dict)
    mental: Dict[str, int] = field(default_factory=dict)
    physical: Dict[str, int] = field(default_factory=dict)
    hidden: Dict[str, int] = field(default_factory=dict)
    condition: Dict[str, int] = field(default_factory=dict)

    def _calculate_age(self, on_date: date = date.today()) -> int:
        age = on_date.year - self.date_of_birth.year
        if (on_date.month, on_date.day) < (
            self.date_of_birth.month,
            self.date_of_birth.day,
        ):
            age -= 1
        return age

    @property
    def age(self, on_date: date = date.today()) -> int:
        return self._calculate_age(on_date)

    @property
    def height_m(self) -> float:
        return round(self.height_cm / 100, 2)

    @property
    def height_ft_inch(self) -> str:
        total_inches = self.height_cm / 2.54
        feet = int(total_inches // 12)
        inches = int(total_inches % 12)
        return f"{feet}'{inches}\""

    @property
    def weight_lb(self) -> float:
        return round(self.weight_kg * 2.20462, 1)

    def overall_summary(self) -> str:
        return f"{self.name} ({self.position}) - {self.role} [{self.duty}] - {self.footedness}"
