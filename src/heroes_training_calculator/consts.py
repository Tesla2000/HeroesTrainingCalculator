from __future__ import annotations

import operator
from collections.abc import Mapping
from functools import reduce
from itertools import product
from operator import itemgetter

import numpy as np
from more_itertools import map_reduce

from src.heroes_training_calculator.counterstrike_level import (
    CounterstrikeLevel,
)
from src.heroes_training_calculator.tier import Tier
from src.heroes_training_calculator.unit import Unit

tiers = (
    Tier(Unit.PEASANT, 15, 10, 271, 22, 150, Unit.ARCHER),
    Tier(Unit.ARCHER, 50, 30, 123, 12, 255, Unit.FOOTMAN),
    Tier(Unit.FOOTMAN, 85, 45, 78, 10, 1800, Unit.PRIEST),
    Tier(Unit.GRIFFIN, 250, 120, 45, 5, None, None),
    Tier(Unit.PRIEST, 600, 250, 24, 3, 3900, Unit.CAVALIER),
    Tier(Unit.CAVALIER, 1300, 400, 14, 2, None, None),
    Tier(Unit.ANGEL, 2800, 700, 6, 1, None, None),
)
reduce(operator.mul, (tier.n_units_to_recruit for tier in tiers))
n_trainings = 20
n_cavalry_trainings = 4
unit2tier: Mapping[Unit, Tier] = map_reduce(
    tiers, lambda tier: tier.base_unit, reducefunc=itemgetter(0)
)
expert_trainer_bonus = 0.35
counterstrike_bonus = {
    CounterstrikeLevel.BASIC: 0,
    CounterstrikeLevel.ADVANCED: 0.15,
    CounterstrikeLevel.EXPERT: 0.3,
    CounterstrikeLevel.ULTIMATE: 0.45,
}
isabela_bonus_per_lvl = 0.02
units2buy = np.array(
    tuple(
        product(*tuple(range(tier.n_units_to_recruit + 1) for tier in tiers))
    )
)
units2buy_costs = np.sum(
    units2buy * np.array(tuple(tier.total_cost for tier in tiers)), axis=1
)
