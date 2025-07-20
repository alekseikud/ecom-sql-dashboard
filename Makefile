PYTHON:= $(CURDIR)/.venv/bin/python

.PHONY: init set_up load_data clean reports

# Default goal: clean, schema reset, and data load
init: clean set_up load_data

# Drop & recreate database
set_up:
	@$(PYTHON) -c "from scripts.restart_db import restart_db;restart_db()"

# Bulk-insert CSVs into tables
load_data:
	@$(PYTHON) -c "from scripts.load_data import read_from_csv;read_from_csv()"

# Cleanup reports output and parsed CSVs
clean:
	@rm -rf reports/*
	@rm -rf data/parsed_csvs/*
	@clear

# Generate all analytical reports
reports:
	@$(PYTHON) -c "import scripts.queries as q; \
q.get_revenue_csv(); \
q.get_sales_performance_csv(); \
q.customer_retention_csv(); \
q.customer_analisis_csv()"
	@clear
	@echo "Reports were succesfully generated and send to `pwd`/reports"
