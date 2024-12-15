from __future__ import annotations

import sys
from collections.abc import Iterable
from functools import partial

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.consts import max_units2buy_cost
from src.heroes_training_calculator.get_best_units2buy import (
    get_best_units2buy,
)
from src.heroes_training_calculator.training_configuration import (
    TrainingConfiguration,
)


def get_best_configuration(
    configurations: Iterable[TrainingConfiguration],
    config: Config,
    max_recruitment_value: float,
):
    best_value = -sys.maxsize

    def _get_value_recruited(configuration: TrainingConfiguration) -> float:
        nonlocal best_value
        training_value = _get_training_value(configuration, config)
        if configuration.remaining_gold >= max_units2buy_cost:
            return training_value + max_recruitment_value
        if training_value + max_recruitment_value < best_value:
            return training_value + max_recruitment_value
        best_units2buy_value = get_best_units2buy(configuration, config)[0]
        best_value = max(best_value, best_units2buy_value + training_value)
        return best_units2buy_value + training_value

    return max(
        sorted(
            configurations,
            key=partial(_get_training_value, config=config),
            reverse=True,
        ),
        key=_get_value_recruited,
    )


def _get_training_value(configuration: TrainingConfiguration, config: Config):
    return (
        -configuration.n_peasants * config.unit_weights[0]
        + (configuration.n_peasants - configuration.n_archers)
        * config.unit_weights[1]
        + (configuration.n_archers - configuration.n_footman)
        * config.unit_weights[2]
        + (configuration.n_footman - configuration.n_priests)
        * config.unit_weights[4]
        + configuration.n_priests * config.unit_weights[5]
    )
