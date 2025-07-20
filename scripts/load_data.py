import os
import csv
import sqlparse
from psycopg2.extensions import connection as _Connection
from pydantic import constr,EmailStr,TypeAdapter

from scripts.setup_db import server_connect, server_disconnect

text= TypeAdapter(str)
name= TypeAdapter(constr(min_length=3, max_length=32, pattern=r'^[A-Za-z0-9 ]*$'))
intiger= TypeAdapter(constr(min_length=1, max_length=10, pattern=r'^([1-9][0-9]*|0)$'))
price= TypeAdapter(constr(min_length=1, max_length=10, pattern=r'^(?:0|[1-9][0-9]*)(?:\.[0-9][0-9]?)?$'))
email= TypeAdapter(EmailStr)

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
        file_name="customers.csv"
        with open(f"data/{file_name}",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO customers(id,name,email,signup_date) 
                            VALUES(%s,%s,%s,%s)""",
                                (
                                intiger.validate_python(row['id']),
                                name.validate_python(row['name']),
                                email.validate_python(row['email']),
                                row['signup_date']
                                )
                            )
        connection.commit()
        os.system(f"cp data/{file_name} data/parsed_csvs/{file_name}")
        os.system(f"head -n 1 data/parsed_csvs/{file_name} > data/{file_name}")

#-------------------READING INTO TABLE categories----------------
        file_name="categories.csv"
        with open(f"data/{file_name}",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO categories(id,name) 
                                VALUES(%s,%s)""",
                                (
                                intiger.validate_python(row['id']),
                                text.validate_python(row['name'])
                                )
                            )
        connection.commit()
        os.system(f"cp data/{file_name} data/parsed_csvs/{file_name}")
        os.system(f"head -n 1 data/parsed_csvs/{file_name} > data/{file_name}")


#-------------------READING INTO TABLE products----------------
        file_name="products.csv"
        with open(f"data/{file_name}",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO products(id,name,category_id,price) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                intiger.validate_python(row['id']),
                                text.validate_python(row['name']),
                                intiger.validate_python(row['category_id']),
                                price.validate_python(row['price'])
                                )
                            )
        connection.commit()
        os.system(f"cp data/{file_name} data/parsed_csvs/{file_name}")
        os.system(f"head -n 1 data/parsed_csvs/{file_name} > data/{file_name}")

#-------------------READING INTO TABLE orders----------------
        file_name="orders.csv"
        with open(f"data/{file_name}",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO orders(id,customer_id,order_date,status) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                intiger.validate_python(row['id']),
                                intiger.validate_python(row['customer_id']),
                                row['order_date'],
                                row['status']
                                )
                            )
        connection.commit()  
        os.system(f"cp data/{file_name} data/parsed_csvs/{file_name}")
        os.system(f"head -n 1 data/parsed_csvs/{file_name} > data/{file_name}")

#-------------------READING INTO TABLE orderItems----------------
        file_name="order_items.csv"
        with open(f"data/{file_name}",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO orderItems(order_id,product_id,quantity,unit_price) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                intiger.validate_python(row['order_id']),
                                intiger.validate_python(row['product_id']),
                                intiger.validate_python(row['quantity']),
                                price.validate_python(row['unit_price'])
                                )
                            )
        connection.commit()
        os.system(f"cp data/{file_name} data/parsed_csvs/{file_name}")
        os.system(f"head -n 1 data/parsed_csvs/{file_name} > data/{file_name}")

#-------------------READING INTO TABLE returns----------------
        file_name="returns.csv"
        with open(f"data/{file_name}",newline="") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""INSERT INTO "returns"(order_id,product_id,return_date,reason) 
                                VALUES(%s,%s,%s,%s)""",
                                (
                                intiger.validate_python(row['order_id']),
                                intiger.validate_python(row['product_id']),
                                row['return_date'],
                                text.validate_python(row['reason'])
                                )
                            )
        connection.commit()
        os.system(f"cp data/{file_name} data/parsed_csvs/{file_name}")
        os.system(f"head -n 1 data/parsed_csvs/{file_name} > data/{file_name}")

        print("Everything was read successfully!")
    except Exception as _ex:
        connection.rollback()
        raise Exception(f"Exception occurred during reading from csv to DB.Exception:{_ex}")
    finally:
        cursor.close()
        server_disconnect(connection)

def load_functions():
    connection:_Connection=server_connect()#type:ignore
    cursor=connection.cursor()
    connection.autocommit=True
    try:
        with open("schema/functions.sql",encoding="UTF-8") as file:
            raw_sql=file.read()
            for itr in sqlparse.split(raw_sql,strip_semicolon=True):
                statement=itr.strip()
                if statement:
                    cursor.execute(statement)
    except Exception as _ex:
        raise Exception(f"An error occurred during loading function.Error:{_ex}")
    finally:
        cursor.close()
        server_disconnect(connection)

def load_triggers():
    connection:_Connection=server_connect()#type:ignore
    cursor=connection.cursor()
    try:
        with open("schema/triggers.sql",encoding="UTF-8") as file:
            raw_sql=file.read()
            for itr in sqlparse.split(raw_sql,strip_semicolon=True):
                statement=itr.strip()
                if statement:
                    cursor.execute(statement)
    except Exception as _ex:
        raise Exception(f"An error occurred during loading trigger function or a trigger.Error:{_ex}")
    finally:
        cursor.close()
        server_disconnect(connection)