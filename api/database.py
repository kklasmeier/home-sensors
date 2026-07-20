from contextlib import contextmanager
from typing import Generator

import mysql.connector
from mysql.connector import MySQLConnection

from api.config import settings


def check_database_connection() -> bool:
    try:
        conn = mysql.connector.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
        )
        conn.close()
        return True
    except mysql.connector.Error:
        return False


@contextmanager
def get_connection() -> Generator[MySQLConnection, None, None]:
    conn = mysql.connector.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )
    try:
        yield conn
    finally:
        conn.close()
