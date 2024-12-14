from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TrainingConfiguration:
    n_peasants: int
    n_archers: int
    n_footman: int
    n_priests: int
    remaining_gold: Optional[int] = None

    def tuple(self):
        return self.n_peasants, self.n_archers, self.n_footman, self.n_priests
