from psycopg2.extensions import connection as _Connection
from psycopg2._psycopg import Column
from tabulate import tabulate
from typing import Any
from datetime import datetime
import csv

from scripts.setup_db import server_connect,server_disconnect

def print_all_tables()->None:
    connection:_Connection=server_connect()#type:ignore
    cursor=connection.cursor()
    try:
        tables=["categories","customers","orderItems","orders","products",'"returns"']
        for itr in tables:
            cursor.execute(f"SELECT * FROM {itr}")
            print(f"------Table {itr}:------")
            colnames=[i[0] for i in cursor.description]#type:ignore
            rows=cursor.fetchall()
            if rows:
                print(tabulate(rows,colnames,"psql"))
            else:
                print("No rows in this table")

    except Exception as _ex:
        raise Exception(f"Something happend during printing.Error:{_ex}")
    finally:
        cursor.close()
        server_disconnect(connection)

#----------FUNCTION FOR  WRITING REPORTS TO CSVs ------------
def select_to_csv(csv_name:str,rows:list[tuple[Any,...]],header:tuple[Column,...])->None:
    try:
        # os.system(f"touch reports/{csv_name}.csv") Do not need since opening automatically create a file
        with open(f"reports/{csv_name}.csv",mode ="w",encoding="UTF-8") as file:
            writer=csv.writer(file)
            writer.writerow([itr[0] for itr in header])
            writer.writerows(rows)
    except Exception as _er:
        raise RuntimeError(f"""Failed writing reports/{csv_name}.csv:\nError:{_er}""")

#----------FUNCTIONS FOR REVENUE DISPLAYMENT------------
def get_revenue_csv()->None:
    connection:_Connection=server_connect()#type:ignore
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_monthly_revenue()")
            rows=cursor.fetchall()
            if rows and cursor.description:
                select_to_csv("monthly_revenue_report",rows,cursor.description)
            cursor.execute("SELECT * FROM get_total_revenue()")
            rows=cursor.fetchall()
            if rows and cursor.description:
                select_to_csv("total_revenue_report",rows,cursor.description)
    except Exception as _ex :
        raise RuntimeError(f"Failed making report. Error:{_ex}")
    finally:
        server_disconnect(connection)

#----------FUNCTION FOR Monthly Category Sales Performance------------
def get_sales_performance_csv()->None:
    connection:_Connection=server_connect()#type:ignore
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sales_performance()")
            rows=cursor.fetchall()
            if rows and cursor.description:
                select_to_csv("monthly_category_sales_performance_report",rows,cursor.description)
    except Exception as _ex :
        raise RuntimeError(f"Failed making report. Error:{_ex}")
    finally:
        server_disconnect(connection)
#----------Helper function to find day of the first purchase----------
def get_first_date()->datetime|None:
    connection:_Connection=server_connect()#type:ignore
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM first_sale_date()")
            return (cursor.fetchall())[0][0]
    except Exception as _ex:
        raise RuntimeError(f"Error ocurred during finding first date.\nError:{_ex}")

#------------FUNCTION New vs. Returning Customer Analysis------------
def customer_retention_csv(start_date:datetime|None=None,end_date:datetime=datetime.now())->None:
    connection:_Connection=server_connect()#type:ignore
    try:
        with connection.cursor() as cursor:
            if start_date==None:
                start:datetime|None=get_first_date()
                if start:
                    start_date=datetime(start.year,start.month,start.day)
            sql="SELECT * FROM customer_retention(%s,%s)"
            parameters=(str(start_date.date()),str(end_date.date()))#type:ignore
            cursor.execute(sql,parameters)
            rows=cursor.fetchall()
            if rows and cursor.description:
                select_to_csv("customer_retention",rows,cursor.description)
    except Exception as _ex :
        raise RuntimeError(f"Failed making report. Error:{_ex}")
    finally:
        server_disconnect(connection)

#----------------Function Rating customers----------------
def customer_analisis_csv(start_date:datetime|None=None,end_date:datetime=datetime.now())->None:
    connection:_Connection=server_connect()#type:ignore
    try:
        with connection.cursor() as cursor:
            if start_date==None:
                start:datetime|None=get_first_date()
                if start:
                    start_date=datetime(start.year,start.month,start.day)
            sql="SELECT * FROM customer_analisis(%s,%s)"
            parameters=(str(start_date.date()),str(end_date.date()))#type:ignore
            cursor.execute(sql,parameters)
            rows=cursor.fetchall()
            if rows and cursor.description:
                select_to_csv("customer_analisis",rows,cursor.description)
    except Exception as _ex :
        raise RuntimeError(f"Failed making report. Error:{_ex}")
    finally:
        server_disconnect(connection)