# E-Commerce SQL Dashboard

A complete SQL-based project to design, build, and analyze an e-commerce sales database. This repository contains schema definitions, data loading scripts, analytical views, reporting queries, and Python utilities—ready to run locally with PostgreSQL.

---

## 🔍 Project Overview

The goal of this project is to:

* **Design** a normalized relational schema for customers, products, orders, and returns.
* **Load** sample data via staged CSV imports and ETL scripts.
* **Build** views and analytical queries to track revenue, returns, and customer lifetime value.
* **Optimize** performance using indexes and materialized views.
* **Automate** schema setup and queries through Python scripts without running on every import (guarded execution).

This walkthrough takes you from initial DDL all the way to a functioning analytics dashboard.

---

## 📁 Repository Structure

```
.
├── data/                            # CSV data + loader script 
│   ├── categories.csv
│   ├── customers.csv
│   ├── load_data.py                 # Reads CSVs & INSERTs/COPYs into the DB
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   └── returns.csv
│
├── scripts/                         # Database management & query utilities
│   ├── queries.py                   # Reusable functions to run ad-hoc SQL
│   ├── restart_db.py                # DROP + CREATE database for a fresh start
│   ├── setup_db.py                  # APPLY schema: types, tables, functions, triggers
│   └── teardown_db.py               # DROP everything (schema + data)
│
├── schema/                          # DDL scripts
│   ├── functions.sql                # PL/pgSQL helper functions
│   ├── tables.sql                   # CREATE TYPE / TABLE statements
│   └── triggers.sql                 # TRIGGER definitions
│
├── reports/                         # Analytics & visualization dashboards 
│   └── …                            
│
├── main.py                          # Quick end-to-end runner for setup, load, queries
└──  README.md                        # This file
```
