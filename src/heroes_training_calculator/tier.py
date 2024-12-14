from __future__ import annotations

from typing import NamedTuple
from typing import Optional

from src.heroes_training_calculator.unit import Unit


class Tier(NamedTuple):
    base_unit: Unit
    base_cost: int
    update_cost: int
    n_units: int
    n_units_to_recruit: int
    base_training_cost: Optional[int]
    trained_into: Optional[Unit]

    @property
    def total_cost(self) -> int:
        return self.base_cost + self.update_cost

    @property
    def n_units_total(self) -> int:
        return self.n_units + self.n_units_to_recruit
