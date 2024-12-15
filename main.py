from __future__ import annotations

from src.heroes_training_calculator.calculate import calculate
from src.heroes_training_calculator.config import Config
from src.heroes_training_calculator.config import create_config_with_args
from src.heroes_training_calculator.config import parse_arguments


def main():
    """
    The `main` function parses command-line arguments using a specified
    configuration, creates a configuration object based on those arguments, and
    then prints the resulting configuration.
    :return: A configuration object created from parsed command-line arguments.
    """
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    print(calculate(config))


if __name__ == "__main__":
    exit(main())
