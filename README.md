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
your-repo/
├── schema/            
│   ├── tables.sql         # CREATE TABLE statements
│   ├── functions.sql      # CREATE FUNCTION … LANGUAGE plpgsql
│   └── triggers.sql       # CREATE TRIGGER … calls to your PL/pgSQL functions
│
├── scripts/        
|   ├── main.py            # Python file to test other functions
│   ├── setup_db.py        # Python “apply” script for tables, functions, triggers
│   ├── teardown_db.py     # (optional) Python script to DROP everything
│   └── queries.py         # Python file with reusable functions to run ad-hoc SQL
│
├── data/                 
│   └── load_data.sql      # INSERT / COPY statements for seed CSVs
│
├── .env                   # Your DB connection URL (git-ignored)
├── .gitignore
└── README.md              # (you already have one)
```
