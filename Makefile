PWD = $(shell pwd)
VENV = $(PWD)/.venv
ENV_D = $(PWD)/env.d
BIN_FLAKE8 = $(VENV)/bin/flake8
BIN_ISORT = $(VENV)/bin/isort
BIN_PIP = $(VENV)/bin/pip
BIN_PYTHON = $(VENV)/bin/python
BIN_PYTEST = $(VENV)/bin/pytest
BIN_UVIVORN = $(VENV)/bin/uvicorn

PYTEST_ARGS ?=


# .DEFAULT_GOAL = null
# .PHONY = null
NPROC ?= $(shell nproc)



clean:
	rm -rf $(VENV)


### System Installation ######################################

.PHONY: local-setup
local-setup: install git-hooks

install:
	poetry install --no-interaction --no-ansi --no-root
	poetry run python ./setup.py build

.PHONY: git-hooks
git-hooks:
	poetry run pre-commit install -t pre-commit \
	&& poetry run pre-commit install -t pre-push

### Static Analysis ##########################################

PYTHON_FILES = setup.py dominoes

flake8:
	poetry run flake8 $(PYTHON_FILES)

isort:
	poetry run isort .

mypy:
	poetry run mypy --install-types --non-interactive $(PYTHON_FILES)

.PHONY: lint
lint:
	poetry run flake8 $(PYTHON_FILES)
	poetry run isort .
	poetry run mypy --install-types --non-interactive $(PYTHON_FILES)

coverage:
	poetry run coverage run -m pytest tests \
	&& poetry run coverage report -m

start:
	$(BIN_UVIVORN) candid.main:app --reload

test_all:
	$(BIN_PYTEST) -n auto $(PYTEST_ARGS)
