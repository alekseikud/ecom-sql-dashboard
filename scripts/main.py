from setup_db import server_connect,server_disconnect
from psycopg2.extensions import connection as _Connection

connection:_Connection=server_connect() # type: ignore
with connection.cursor() as cursor:
    cursor.execute("SELECT VERSION()")
    print(cursor.fetchone())
server_disconnect(connection)