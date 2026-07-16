ifeq ($(OS),Windows_NT)

PYTHON = python
PIP = pip
FLASK = flask --app app

else

PYTHON = python3
PIP = pip3
FLASK = flask --app app

endif

run:
	$(FLASK) run

install:
	$(PIP) install -r requirements.txt

data:
	$(FLASK) make-data

migrate:
	$(FLASK) db migrate -m "Migration"

upgrade:
	$(FLASK) db upgrade

downgrade:
	$(FLASK) db downgrade

init-db:
	$(FLASK) db init

format:
	ruff check . --fix
	ruff format .

format-check:
	ruff check .
	ruff format . --check

.PHONY: run install data migrate upgrade downgrade init-db format format-check