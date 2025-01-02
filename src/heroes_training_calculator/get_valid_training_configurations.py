from __future__ import annotations

from collections.abc import Sequence
from functools import partial
from itertools import product
from itertools import starmap
from math import ceil

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.consts import counterstrike_bonus
from src.heroes_training_calculator.consts import expert_trainer_bonus
from src.heroes_training_calculator.consts import isabela_bonus_per_lvl
from src.heroes_training_calculator.consts import n_cavalry_trainings
from src.heroes_training_calculator.consts import n_trainings
from src.heroes_training_calculator.consts import unit2tier
from src.heroes_training_calculator.training_configuration import (
    TrainingConfiguration,
)
from src.heroes_training_calculator.unit import Unit


def get_valid_training_configurations(
    gold: int, config: Config
) -> Sequence[TrainingConfiguration]:
    all_configurations = starmap(
        TrainingConfiguration,
        filter(
            lambda items: sum(items) <= n_trainings,
            product(
                range(n_trainings + 1),
                range(n_trainings + 1),
                range(n_trainings + 1),
                range(n_cavalry_trainings + (config.isabela_level != 1) + 1),
            ),
        ),
    )
    training_cost_modifier = get_training_cost_modifier(config)
    return tuple(
        filter(
            partial(
                _is_gold_sufficient,
                gold=gold,
                training_cost_modifier=training_cost_modifier,
            ),
            all_configurations,
        )
    )


def get_training_cost_modifier(config: Config) -> float:
    return 1 - (
        counterstrike_bonus[config.counterstrike_level]
        + config.is_expert_trainer * expert_trainer_bonus
        + (config.isabela_level - 1) * isabela_bonus_per_lvl
    )


def _is_gold_sufficient(
    configuration: TrainingConfiguration,
    gold: int,
    training_cost_modifier: float,
) -> bool:
    total = 0
    for unit, n_units in zip(
        (Unit.PEASANT, Unit.ARCHER, Unit.FOOTMAN, Unit.PRIEST),
        configuration.tuple(),
    ):
        tier = unit2tier[unit]
        trained_tier = unit2tier[tier.trained_into]
        total += max(
            0,
            ceil(
                n_units
                * (
                    tier.base_training_cost * training_cost_modifier
                    + trained_tier.update_cost
                )
            )
            - 1,
        )
        total += (tier.n_units_total - n_units) * tier.update_cost
    configuration.remaining_gold = gold - total
    return total < gold
