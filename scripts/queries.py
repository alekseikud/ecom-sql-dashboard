from psycopg2.extensions import connection as _Connection
from tabulate import tabulate
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