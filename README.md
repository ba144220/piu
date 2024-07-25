# piu
A collection of logit processors that enforces output format on large language models (LLM)

## Environment Setup
### Install Poetry
Follow the [instruction](https://python-poetry.org/docs/#installing-with-the-official-installer) based on your OS

> **_NOTE:_**  Remember to add `poetry` to `PATH`

### Config In-project Venv
```shell
poetry config virtualenvs.in-project true
``` 

### Creat Virtual Enviroment
```shell
poetry env use python
``` 

### Activate Shell
```shell
poetry shell
```

### Install All Dependency
```shell
poetry install
```

### Set Up Pre Commit Hooks
```shell
pre-commit install
```

## Add/Remove Package
> **_WARN:_**  Please **DONT** use `pip` to add/remove packages in this project

Please see poetry [add](https://python-poetry.org/docs/cli/#add) and [remove](https://python-poetry.org/docs/cli/#remove) for detail description

## Recreate Virtual Environment
Under Project Directory
```shell
rm -rf .venv
poetry env use python
```