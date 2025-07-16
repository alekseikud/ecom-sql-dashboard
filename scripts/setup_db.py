import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _Connection

load_dotenv()


def server_connect()->_Connection | None:
    try:
        connection:_Connection=psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("Server was successfully connected")
        return connection
    except Exception as _ex:
        print(f"Exception: {_ex} occured during connection to server")
        raise _ex

def admin_server_connect()->_Connection | None:
    try:
        connection:_Connection=psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('ADMIN_DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("Server was successfully connected")
        return connection
    except Exception as _ex:
        print(f"Exception: {_ex} occured during connection to server")
        raise _ex


def server_disconnect(connection:_Connection)->None:
    try:
        connection.close()
        print("Server was successfully disconnected")
    except Exception as _ex:
        print(f"Cannot disconnect.Error ocurred: {_ex}")