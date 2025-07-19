# Retail Analytics SQL Pipeline

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Project Layout](#project-layout)
* [Quick‑start](#quick-start)
* [Usage](#usage)
* [Extending the project](#extending-the-project)
* [Contributing](#contributing)
* [License](#license)

## Overview

This repository contains an end‑to‑end mini data‑warehouse for an e‑commerce shop.
It demonstrates how to:

1. design a relational schema in PostgreSQL,
2. load raw CSV data,
3. encapsulate business logic in SQL functions and triggers,
4. expose Python utilities for automation and reporting, and
5. produce human‑readable CSV reports.

Everything is written in plain SQL and Python—no ORM or heavyweight ETL framework—so you can see every moving part.

---

## Features

| Layer         | Component               | Description                                                                                                                   |
| ------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Schema**    | `schema/tables.sql`     | DDL for 6 core tables (`customers`, `categories`, `products`, `orders`, `orderItems`, `returns`) plus an `order_status` enum. |
|               | `schema/functions.sql`  | Revenue, sales‑performance and customer‑retention functions, ready for BI tools.                                              |
|               | `schema/triggers.sql`   | Data‑quality triggers (name normalisation, 30‑day return window enforcement).                                                 |
| **Ingest**    | `data/load_data.py`     | Creates tables (if needed) and bulk‑inserts data from the `data/*.csv` dumps.                                                 |
| **DB ops**    | `scripts/setup_db.py`   | Thin wrapper around `psycopg2` that reads connection details from `.env`.                                                     |
|               | `scripts/restart_db.py` | Drops & recreates the target database in one command—handy for demos.                                                         |
| **Reporting** | `scripts/queries.py`    | Convenience functions that call the SQL API and write CSVs into `reports/`.                                                   |
| **CLI**       | `main.py`               | One‑step entry‑point that ties the above pieces together (see *Usage*).                                                       |

---

## Project layout

```text
.
├── data/                     # Raw source data (CSV)
├── reports/                  # Auto‑generated analytical CSVs
├── schema/                   # Pure SQL (DDL + business logic)
│   ├── tables.sql
│   ├── functions.sql
│   └── triggers.sql
├── scripts/                  # Python helpers
│   ├── setup_db.py
│   ├── restart_db.py
│   ├── load_data.py
│   └── queries.py
├── main.py                   # Example orchestration script
└── README.md
```

> **Note:** Runtime artefacts such as `__pycache__/` folders and the empty `scripts/teardown_db.py` are intentionally ignored.

---

## Quick start

### 1 – Prerequisites

* **PostgreSQL 15+**
* **Python 3.11** (any 3.9+ should work)
* `psycopg2‑binary`, `python‑dotenv`, `sqlparse`, `tabulate` (see `requirements.txt`).

### 2 – Install & configure

```bash
git clone https://github.com/<your‑git>/retail‑sql‑pipeline.git
cd retail‑sql‑pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail
ADMIN_DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=secret
```

### 3 – Bootstrap the database

```bash
# optional but handy
python scripts/restart_db.py

# create tables & ingest CSVs
python scripts/load_data.py read_from_csv

# load stored functions & triggers
python scripts/load_data.py load_functions
python scripts/load_data.py load_triggers
```

That's it—your database is ready!

---

## Usage

Generate the built‑in analytical reports:

```bash
# Monthly & total revenue
python scripts/queries.py get_revenue_csv

# Category sales performance
python scripts/queries.py get_sales_performance_csv

# New‑vs‑returning customers
python scripts/queries.py customer_retention_csv

# Customer lifetime value ranking
python scripts/queries.py customer_analisis_csv
```

The resulting CSVs land in the `reports/` directory, ready for further analysis or visualisation.

If you just want to peek at the tables:

```bash
python scripts/queries.py print_all_tables
```

---

## Extending the project

1. **New columns / tables** — add them to `schema/tables.sql`, then rerun `scripts/load_data.update_tables()` or recreate the database.
2. **Business metrics** — drop a new `CREATE FUNCTION` in `schema/functions.sql`; Python will pick it up automatically.
3. **Data‑quality rules** — write a trigger in `schema/triggers.sql` and call `load_triggers()`.

---

## Contributing

Pull requests and issue reports are welcome! Please open a discussion if you plan a larger change.

## License

MIT © Alex
