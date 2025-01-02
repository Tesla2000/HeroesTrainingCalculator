from __future__ import annotations

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.consts import tiers
from src.heroes_training_calculator.consts import trainable_tiers
from src.heroes_training_calculator.consts import untrainable_cost
from src.heroes_training_calculator.get_best_units2buy import (
    get_best_units2buy_and_train,
)


def calculate(config: Config) -> str:
    remaining_gold = config.gold - untrainable_cost
    result = get_best_units2buy_and_train(remaining_gold, config)
    return (
        "Units to buy: "
        + ", ".join(
            map(
                " ".join,
                zip(
                    map(
                        str,
                        map(int, result.units2buy),
                    ),
                    (tier.base_unit.value for tier in tiers),
                ),
            )
        )
        + "\nUnits to train: "
        + ", ".join(
            map(
                " ".join,
                zip(
                    map(str, map(int, result.units2train)),
                    (tier.base_unit.value for tier in trainable_tiers),
                ),
            )
        )
    )
