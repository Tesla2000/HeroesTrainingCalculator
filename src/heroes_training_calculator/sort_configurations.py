from __future__ import annotations

import sys
from collections.abc import Iterable
from functools import partial

import numpy as np

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.training_configuration import (
    TrainingConfiguration,
)


def sort_configurations(
    configurations: Iterable[TrainingConfiguration],
    config: Config,
    units2buy_all: np.ndarray,
):
    max_recruitment_value = units2buy_all[:, -1].max()
    max_recruitment_cost = units2buy_all[:, -2].max()

    def _get_value_recruited(configuration: TrainingConfiguration) -> float:
        training_value = get_training_value(configuration, config)
        if configuration.remaining_gold >= max_recruitment_cost:
            return training_value + max_recruitment_value
        best_units2buy = get_best_units2buy(configuration, units2buy_all)
        return best_units2buy[-1] + training_value

    return sorted(
        configurations,
        key=_get_value_recruited,
        reverse=True,
    )


def get_best_configuration(
    configurations: Iterable[TrainingConfiguration],
    config: Config,
    units2buy_all: np.ndarray,
):
    best_value = -sys.maxsize
    max_recruitment_value = units2buy_all[:, -1].max()
    max_recruitment_cost = units2buy_all[:, -2].max()

    def _get_value_recruited(configuration: TrainingConfiguration) -> float:
        nonlocal best_value
        training_value = get_training_value(configuration, config)
        if configuration.remaining_gold >= max_recruitment_cost:
            return training_value + max_recruitment_value
        if training_value + max_recruitment_value < best_value:
            return training_value + max_recruitment_value
        best_units2buy = get_best_units2buy(configuration, units2buy_all)
        best_value = max(best_value, best_units2buy[-1] + training_value)
        return best_units2buy[-1] + training_value

    return max(
        sorted(
            configurations,
            key=partial(get_training_value, config=config),
            reverse=True,
        ),
        key=_get_value_recruited,
    )


def get_training_value(configuration: TrainingConfiguration, config: Config):
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


def get_best_units2buy(
    configuration: TrainingConfiguration,
    units2buy_all: np.ndarray,
) -> np.ndarray[float]:
    valid_units2buy = units2buy_all[
        np.where(units2buy_all[:, -2] < configuration.remaining_gold)[0]
    ]
    return valid_units2buy[np.argmax(valid_units2buy[:, -1])]
