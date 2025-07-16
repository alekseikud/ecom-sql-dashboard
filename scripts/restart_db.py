from psycopg2.extensions import connection as _Connection
from dotenv import load_dotenv
import os

from .setup_db import admin_server_connect,server_disconnect

load_dotenv()

def restart_db()->None:
    connection:_Connection=admin_server_connect() #type:ignore
    connection.autocommit=True
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {os.getenv('DB_NAME')}")
            cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
        print("DB was successfully resetted")
    except Exception as _ex:
        raise Exception(f"Error ocurred during restarting DB: {_ex}")
    finally:
        server_disconnect(connection)