from __future__ import annotations

from typing import NamedTuple
from typing import Optional
from typing import Self

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

    @property
    def train_into_tier(self) -> Self:
        from src.heroes_training_calculator.consts import tiers

        if self.trained_into is None:
            return
        return next(
            tier for tier in tiers if tier.base_unit == self.trained_into
        )
