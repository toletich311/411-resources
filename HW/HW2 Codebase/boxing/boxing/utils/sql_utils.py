from contextlib import contextmanager
import logging
import os
import sqlite3

from boxing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


# load the db path from the environment with a default value
DB_PATH = os.getenv("DB_PATH", "/app/sql/boxing.db")


def check_database_connection():

    """
    Check the database connection.

    Raises:
        Exception: If the database connection is not OK.

    """
    try:
        logger.info(f"Checking database connection to {DB_PATH}...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Execute a simple query to verify the connection is active
        cursor.execute("SELECT 1;")
        conn.close()
        logger.info("Database connection is healthy.")

    except sqlite3.Error as e:
        error_message = f"Database connection error: {e}"
        logger.error(error_message)
        raise Exception(error_message) from e

def check_table_exists(tablename: str):
    """
    Check if the table exists by querying the SQLite master table.

    Args:
        tablename (str): The name of the table to check.

    Raises:
        Exception: If the table does not exist.

    """
    try:
        logger.info(f"Checking if table '{tablename}' exists in {DB_PATH}...")


        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Use parameterized query to avoid SQL injection
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (tablen