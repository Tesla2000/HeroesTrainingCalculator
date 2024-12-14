## Running

You can run script with docker or python

### Python
```shell
python main.py --config_file src/heroes_training_calculator/config_sample.toml
```

### Cmd
```shell
poetry install
poetry run heroes_training_calculator
```

### Docker
```shell
docker build -t HeroesTrainingCalculator .
docker run -it HeroesTrainingCalculator /bin/sh
python main.py
```
