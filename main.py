from psycopg2.extensions import connection as _Connection

from scripts.setup_db import server_connect,server_disconnect
from scripts.restart_db import restart_db
from data.load_data import read_from_csv
from scripts.queries import print_all_tables
if __name__ == "__main__":
    connection:_Connection=server_connect() # type: ignore
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        print(cursor.fetchone())
    server_disconnect(connection)

    restart_db()
    read_from_csv()
    print_all_tables()