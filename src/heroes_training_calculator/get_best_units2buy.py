from __future__ import annotations

import operator
from collections.abc import Sequence

from pulp import LpMaximize
from pulp import LpProblem
from pulp import LpVariable
from pulp import PULP_CBC_CMD

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.consts import tiers
from src.heroes_training_calculator.training_configuration import (
    TrainingConfiguration,
)


def get_best_units2buy(
    configuration: TrainingConfiguration,
    config: Config,
) -> tuple[float, Sequence[int]]:
    problem = LpProblem("Integer_Linear_Optimization", LpMaximize)

    n_units = tuple(
        LpVariable(
            tier.base_unit.value,
            lowBound=0,
            upBound=tier.n_units_to_recruit,
            cat="Integer",
        )
        for tier in tiers
    )

    problem += (
        sum(map(operator.mul, config.unit_weights, n_units)),
        "Objective",
    )

    problem += (
        sum(map(operator.mul, (tier.total_cost for tier in tiers), n_units))
        <= configuration.remaining_gold,
        "Money constraint",
    )

    assert problem.solve(PULP_CBC_CMD(msg=False)) > 0
    return problem.objective.value(), tuple(
        n_unit.value() for n_unit in n_units
    )
