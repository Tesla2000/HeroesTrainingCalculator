from __future__ import annotations

import numpy as np

from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.config import create_config_with_args
from src.heroes_training_calculator.config import parse_arguments
from src.heroes_training_calculator.consts import tiers
from src.heroes_training_calculator.consts import units2buy
from src.heroes_training_calculator.consts import units2buy_costs
from src.heroes_training_calculator.get_valid_training_configurations import (
    get_valid_training_configurations,
)
from src.heroes_training_calculator.sort_configurations import (
    get_best_configuration,
)  # noqa: E501
from src.heroes_training_calculator.sort_configurations import (
    get_best_units2buy,
)  # noqa: E501


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
    units2buy_values = np.sum(
        units2buy * np.array(config.unit_weights), axis=1
    )
    units2buy_all = np.concat(
        (
            units2buy,
            units2buy_costs.reshape(-1, 1),
            units2buy_values.reshape(-1, 1),
        ),
        axis=1,
    )
    valid_training_configurations = get_valid_training_configurations(
        remaining_gold, config
    )
    # sorted_configurations = sort_configurations(
    #     valid_training_configurations, config, units2buy_all
    # )
    sorted_configurations = [
        get_best_configuration(
            valid_training_configurations, config, units2buy_all
        )
    ]
    print(
        "\n".join(
            f"Units to buy: {', '.join(map(' '.join, zip(map(str, map(int, get_best_units2buy(configuration, units2buy_all)[:7])), ('peasants', 'archers', 'footman', 'griffin', 'priests', 'cavalier', 'angel'))))}\nUnits to train: {', '.join(map(' '.join, zip(map(str, configuration.tuple()), ('peasants', 'archers', 'footman', 'priests'))))}"  # noqa: E501
            for configuration in sorted_configurations
        )
    )


if __name__ == "__main__":
    exit(main())
