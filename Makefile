.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: help
help:			## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: install
install:		## Install dependencies
	@echo "Installing dependencies"
	poetry install
	@echo "Installing pre-commit hooks"
	pre-commit install

.PHONY: update
update:		## Update dependencies
	@echo "Updating dependencies"
	poetry update
	@echo "Updating pre-commit hooks"
	pre-commit autoupdate

.PHONY: test
test:			## Run the tests
	@echo "Running the tests"
	poetry run pytest