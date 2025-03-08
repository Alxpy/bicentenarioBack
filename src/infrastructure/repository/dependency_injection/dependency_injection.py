from src.infrastructure.repository.connection import get_connection


def get_db_connection():
    connection = get_connection()
    try:
        yield connection
    finally:
        if connection is not None:
            connection.close()
