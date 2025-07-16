import os
import csv
import sqlparse
from psycopg2.extensions import connection as _Connection

from scripts.setup_db import server_connect, server_disconnect

def update_tables()->None:
    connection:_Connection=server_connect()#type:ignore
    connection.autocommit = True
    cursor=connection.cursor()
    try:
        with open("schema/tables.sql",encoding="UTF-8") as file:
            raw_sql=file.read()
        for itr in sqlparse.split(raw_sql):
            stmnt=itr.strip()
            if stmnt:
                cursor.execute(stmnt)
    except Exception as _ex:
        raise Exception(f"Exception occurred during updating tables: {_ex}")
    finally:
        cursor.close()
        server_disconnect(connection)

def read_from_csv()->None:  # READING DATA FROM CSVS TO DATABASE
    connection:_Connection=server_connect()#type:ignore
    connection.autocommit = False
    cursor=connection.cursor()
    update_tables()
    try:
#-------------------READING INTO TABLE Customers----------------
        with open("data/customers.csv",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO customers(id,name,email,signup_date) 
                            VALUES(%s,%s,%s,%s)""",
                                (
                                int(row['id']),
                                row['name'],
                                row['email'],
                                row['signup_date']
                                )
                            )
        connection.commit()

#-------------------READING INTO TABLE categories----------------
        with open("data/categories.csv",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO categories(id,name) 
                                VALUES(%s,%s)""",
                                (
                                int(row['id']),
                                row['name']
                                )
                            )
        connection.commit()

#-------------------READING INTO TABLE products----------------
        with open("data/products.csv",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO products(id,name,category_id,price) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                int(row['id']),
                                row['name'],
                                int(row['category_id']),
                                float(row['price'])
                                )
                            )
        connection.commit()

#-------------------READING INTO TABLE orders----------------
        with open("data/orders.csv",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO orders(id,customer_id,order_date,status) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                int(row['id']),
                                int(row['customer_id']),
                                row['order_date'],
                                row['status']
                                )
                            )
        connection.commit()  

#-------------------READING INTO TABLE orderItems----------------
        with open("data/order_items.csv",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO orderItems(order_id,product_id,quantity,unit_price) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                int(row['order_id']),
                                int(row['product_id']),
                                int(row['quantity']),
                                float(row['unit_price'])
                                )
                            )
        connection.commit()

#-------------------READING INTO TABLE returns----------------
        with open("data/returns.csv",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO "returns"(order_id,product_id,return_date,reason) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                int(row['order_id']),
                                int(row['product_id']),
                                row['return_date'],
                                row['reason']
                                )
                            )
        connection.commit()
        print("Everything was read successfully!")
    except Exception as _ex:
        connection.rollback()
        raise Exception(f"Exception occurred during reading from csv to DB.Exception:{_ex}")
    finally:
        cursor.close()
        server_disconnect(connection)