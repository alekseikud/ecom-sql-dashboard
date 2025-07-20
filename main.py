# main.py

from scripts.setup_db import server_disconnect
from scripts.restart_db import restart_db
from scripts.load_data import (
    read_from_csv,
    load_functions,
    load_triggers,
)
from scripts.queries import (
    print_all_tables,
    get_revenue_csv,
    get_sales_performance_csv,
    customer_analisis_csv,
    customer_retention_csv,
)


def main():
    tasks = [
        ("Restart database (drop & recreate)", restart_db),
        ("Load CSV data into tables", read_from_csv),
        ("Load SQL functions", load_functions),
        ("Load SQL triggers", load_triggers),
        ("Print all tables to console", print_all_tables),
        ("Generate revenue reports", get_revenue_csv),
        ("Generate category sales performance report", get_sales_performance_csv),
        ("Generate customer analysis report", customer_analisis_csv),
        ("Generate customer retention report", customer_retention_csv),
    ]

    for description, func in tasks:
        print(f"\n=== {description} ===")
        try:
            # All your functions take no args (they use defaults/env)
            func()
        except Exception as e:
            print(f"Error during '{description}': {e}")
            break




if __name__ == "__main__":
    main()
