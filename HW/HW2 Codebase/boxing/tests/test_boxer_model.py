import sqlite3
import logging
import pytest
import re
from contextlib import contextmanager

from boxing.models.boxers_model import (
    create_boxer,
    delete_boxer,
    get_leaderboard,
    get_boxer_by_id,
    get_boxer_by_name,
    get_weight_class,
    update_boxer_stats,
    Boxer
)

# ------------------
# FIXTURES
# ------------------

def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_cursor.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("boxing.models.boxers_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

# Configure test logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#Tests to check the weight class constuctor in Boxer class
def test_get_weight_class_featherweight():
    logger.info("Testing get_weight_class with featherweight")
    assert get_weight_class(125) == "FEATHERWEIGHT"

def test_get_weight_class_invalid():
    logger.info("Testing get_weight_class with invalid weight")
    with pytest.raises(ValueError, match="Invalid weight: 100."):
        get_weight_class(100)

#Tests to check the create_boxer functionality
def test_create_boxer_valid(mocker):
    logger.info("Testing create_boxer with valid input")
    cursor = mock_cursor(mocker)
    create_boxer("Ali", 150, 70, 72.5, 30)
    assert cursor.execute.call_count == 2

def test_create_boxer_invalid_age():
    logger.info("Testing create_boxer with invalid age")
    with pytest.raises(ValueError):
        create_boxer("Ali", 150, 70, 72.5, 10)

def test_create_boxer_duplicate(mocker):
    logger.info("Testing create_boxer with duplicate name")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = (1,)
    with pytest.raises(ValueError):
        create_boxer("Ali", 150, 70, 72.5, 30)





