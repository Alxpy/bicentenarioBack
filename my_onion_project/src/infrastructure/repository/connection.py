import os
from mysql.connector import pooling, Error

connection_pool = pooling.MySQLConnectionPool(
    pool_name=os.getenv("DB_POOL_NAME"),
    pool_size=int(os.getenv("DB_POOL_SIZE")),
    pool_reset_session=True,
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    connection_timeout=int(os.getenv("DB_TIMEOUT")),
    charset=os.getenv("DB_CHARSET"),
    collation=os.getenv("DB_COLLATION")
)


def get_connection():
    try:
        connection = connection_pool.get_connection()

        if not connection.is_connected():
            connection.reconnect(attempts=3, delay=2)

        return connection
    except Error as e:
        print(f"Error getting connection from pool: {e}")
        return None