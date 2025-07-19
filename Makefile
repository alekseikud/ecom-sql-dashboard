PYTHON:= $(CURDIR)/.venv/bin/python

.PHONY: init set_up load_data

init: set_up load_data

set_up:
	$(PYTHON) -c "from scripts.restart_db import restart_db;restart_db()"

load_data:
	$(PYTHON) -c "from data.load_data import read_from_csv;read_from_csv()"