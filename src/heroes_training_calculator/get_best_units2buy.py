from __future__ import annotations

import operator
from collections.abc import Sequence
from math import ceil

from pulp import LpMaximize
from pulp import LpProblem
from pulp import LpVariable
from pulp import PULP_CBC_CMD
from typing_extensions import NamedTuple

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.consts import n_cavalry_trainings
from src.heroes_training_calculator.consts import n_trainings
from src.heroes_training_calculator.consts import tiers
from src.heroes_training_calculator.consts import trainable_indexes
from src.heroes_training_calculator.consts import trainable_tiers
from src.heroes_training_calculator.get_valid_training_configurations import (
    get_training_cost_modifier,
)


def get_best_units2buy_and_train(
    remaining_gold: int,
    config: Config,
) -> Result:
    problem = LpProblem("Integer_Linear_Optimization", LpMaximize)

    n_units_2buy = tuple(
        LpVariable(
            tier.base_unit.value,
            lowBound=0,
            upBound=tier.n_units_to_recruit,
            cat="Integer",
        )
        for tier in tiers
    )
    n_units_2train = tuple(
        LpVariable(
            tier.base_unit.value + "_to_train",
            lowBound=0,
            upBound=n_trainings,
            cat="Integer",
        )
        for tier in trainable_tiers
    )
    n_units_2train[-1].upBound = n_cavalry_trainings + (
        config.isabela_level != 1
    )

    problem += (
        sum(map(operator.mul, config.unit_weights, n_units_2buy))
        + sum(
            to_train
            * (
                config.unit_weights[trainable_index + 1]
                - config.unit_weights[trainable_index]
            )
            for to_train, trainable_index in zip(
                n_units_2train, trainable_indexes
            )
        ),
        "Objective",
    )
    training_cost_modifier = get_training_cost_modifier(config)
    problem += (
        sum(
            map(
                operator.mul, (tier.total_cost for tier in tiers), n_units_2buy
            )
        )
        + sum(
            n_units
            * (
                ceil(tier.base_training_cost * training_cost_modifier)
                - 1
                + tier.train_into_tier.update_cost
            )
            + (tier.n_units - n_units) * tier.update_cost
            for tier, n_units in zip(trainable_tiers, n_units_2train)
        )
        <= remaining_gold,
        "Money_constraint",
    )
    problem += (
        sum(n_units_2train) <= n_trainings,
        "Training_constraint",
    )

    assert problem.solve(PULP_CBC_CMD(msg=False)) > 0
    return Result(
        tuple(n_unit.value() for n_unit in n_units_2buy),
        tuple(n_unit.value() for n_unit in n_units_2train),
        tuple(problem.constraints["Money_constraint"].values()),
    )


class Result(NamedTuple):
    units2buy: Sequence[int]
    units2train: Sequence[int]
    coefficients: Sequence[int]

    @property
    def gold_spent(self):
        return sum(
            map(
                operator.mul,
                self.coefficients,
                (*self.units2buy, *self.units2train),
            )
        )
