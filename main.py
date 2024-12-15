from __future__ import annotations

import numpy as np

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.config import create_config_with_args
from src.heroes_training_calculator.config import parse_arguments
from src.heroes_training_calculator.consts import tiers
from src.heroes_training_calculator.consts import units2buy
from src.heroes_training_calculator.get_best_configuration import (
    get_best_configuration,
)
from src.heroes_training_calculator.get_best_units2buy import (
    get_best_units2buy,
)
from src.heroes_training_calculator.get_valid_training_configurations import (
    get_valid_training_configurations,
)


def main():
    """
    The `main` function parses command-line arguments using a specified
    configuration, creates a configuration object based on those arguments, and
    then prints the resulting configuration.
    :return: A configuration object created from parsed command-line arguments.
    """
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    untrainable_cost = sum(
        tier.n_units * tier.update_cost
        for tier in tiers
        if tier.trained_into is None
    )
    remaining_gold = config.gold - untrainable_cost
    max_recruitment_value = np.sum(
        units2buy * np.array(config.unit_weights), axis=1
    ).max()
    valid_training_configurations = get_valid_training_configurations(
        remaining_gold, config
    )
    best_configuration = get_best_configuration(
        valid_training_configurations, config, max_recruitment_value
    )
    print(
        "Units to buy: "
        + ", ".join(
            map(
                " ".join,
                zip(
                    map(
                        str,
                        map(
                            int,
                            get_best_units2buy(best_configuration, config)[1],
                        ),
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
                    map(str, best_configuration.tuple()),
                    (
                        tier.base_unit.value
                        for tier in tiers
                        if tier.trained_into
                    ),
                ),
            )
        )
    )


if __name__ == "__main__":
    exit(main())
