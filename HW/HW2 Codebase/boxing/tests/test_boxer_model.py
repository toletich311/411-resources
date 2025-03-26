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


#Tests to check the create_boxer functionality
def test_create_boxer_valid(mocker):
    "tests that creating a boxer with valid input in facts creates a boxer"
    logger.info("Testing create_boxer with valid input")
    cursor = mock_cursor(mocker)
    create_boxer("Ali", 150, 70, 72.5, 30)
    assert cursor.execute.call_count == 2

def test_create_boxer_invalid_age():
    "tests that creating a boxer with invalid input throws an error"
    logger.info("Testing create_boxer with invalid age")
    with pytest.raises(ValueError):
        create_boxer("Ali", 150, 70, 72.5, 10)

def test_create_boxer_duplicate(mocker):
    "test that trying to create a duplicate boxer throws an error"
    logger.info("Testing create_boxer with duplicate name")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = (1,)
    with pytest.raises(ValueError):
        create_boxer("Ali", 150, 70, 72.5, 30)

#Tests to check delete_boxer functionality
def test_delete_existing_boxer(mocker):
    """Tests if an existing boxer can be deleted successfully."""
    logger.info("Testing delete_boxer for existing boxer")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = (1,)
    delete_boxer(1)
    assert cursor.execute.call_count == 2

def test_delete_nonexistent_boxer( mocker):
    """Tests that trying to delete a non-existent boxer throws a ValueError."""
    logger.info("Testing delete_boxer for non-existent boxer")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = None
    with pytest.raises(ValueError):
        delete_boxer(99)

#testing get_leaderbaord functionality 
def test_get_leaderboard_valid(mocker):
    """Tests leaderboard retrieval and proper calculation of win percentage."""
    logger.info("Testing get_leaderboard with valid data")
    cursor = mock_cursor(mocker)
    cursor.fetchall.return_value = [
        (1, "Ali", 150, 70, 72.5, 30, 5, 4, 0.8)
    ]
    board = get_leaderboard()
    assert board[0]["name"] == "Ali"
    logger.info("Testing get_leaderboard win percentage calculation")

    assert board[0]["win_pct"] == 80.0

def test_get_leaderboard_invalid_sort():
    """Tests that invalid sort_by parameter raises a ValueError."""
    logger.info("Testing get_leaderboard with invalid sort key")
    with pytest.raises(ValueError):
        get_leaderboard(sort_by="invalid") #if not win_pct or wins --> invalid

#testing get_boxer_by_id functionality 
def test_get_boxer_by_id_exists(mocker):
    """Tests retrieving a boxer by ID when the boxer exists."""
    logger.info("Testing get_boxer_by_id when boxer exists")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = (1, "Ali", 150, 70, 72.5, 30)
    boxer = get_boxer_by_id(1) #ali's id is 1
    assert isinstance(boxer, Boxer)
    assert boxer.name == "Ali"

def test_get_boxer_by_id_not_exists(mocker):
    """Tests that retrieving a boxer by ID that doesn't exist raises ValueError."""
    logger.info("Testing get_boxer_by_id when boxer does not exist")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = None
    with pytest.raises(ValueError):
        get_boxer_by_id(2)  #no boxer with id 2

#testing get_boxer_by_name functionality
def test_get_boxer_by_name_exists(mocker):
    """"Tests that retrieving a boxer by name that exitst in fact returns specified boxer"""
    logger.info("Testing get_boxer_by_name_exists when boxer name is found")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = (1, "Ali", 150, 70, 72.5, 30)
    boxer = get_boxer_by_name("Ali")
    assert isinstance(boxer, Boxer)
    assert boxer.name == "Ali"

def test_get_boxer_by_name_not_exists(mocker):
    """"Tests that retrieving a boxer by name that does not exists raises ValueError"""
    logger.info("tests the calling get_boxer_by_name for a nonexistent boxer raises ValueError")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = None
    with pytest.raises(ValueError):
        get_boxer_by_name("Bruce")  #there is no boxer named bruce 

#testing get_weight_class
def test_get_weight_class_featherweight():
    "Tests that a valid featherweight gets assigned to the correct weight class"
    logger.info("Testing get_weight_class with featherweight")
    assert get_weight_class(125) == "FEATHERWEIGHT"

def test_get_weight_class_lightweight():
    "Tests that a valid lightweight gets assigned to the correct weight class"
    logger.info("Testing get_weight_class with lightweight")
    assert get_weight_class(135) == "LIGHTWEIGHT"

def test_get_weight_class_middleweight():
    "Tests that a valid middleweight gets assigned to the correct weight class"
    logger.info("Testing get_weight_class with middleweight")
    assert get_weight_class(182) == "MIDDLEWEIGHT"

def test_get_weight_class_heavyweight():
    "Tests that a valid heavyweight gets assigned to the correct weight class"
    logger.info("Testing get_weight_class with heavyweight")
    assert get_weight_class(225) == "HEAVYWEIGHT"

def test_get_weight_class_invalid():
    "Tests that an invalid weight input throws an error"
    logger.info("Testing get_weight_class with invalid weight")
    with pytest.raises(ValueError, match="Invalid weight: 100."):
        get_weight_class(100)

#testing update_boxer_stats

def test_update_boxer_stats_win(mocker):
    """Tests updating stats after a win for an existing boxer."""
    logger.info("Testing update_boxer_stats with win result")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = (1,)
    update_boxer_stats(1, "win")
    assert "wins = wins + 1" in cursor.execute.call_args_list[1][0][0]

def test_update_boxer_stats_loss(mocker):
    """Tests updating stats after a loss for an existing boxer."""
    logger.info("Testing update_boxer_stats with loss result")
    cursor = mock_cursor(mocker)
    cursor.fetchone.return_value = (1,)
    update_boxer_stats(1, "loss")
    assert "fights = fights + 1 WHERE id = ?" in cursor.execute.call_args_list[1][0][0]

def test_update_boxer_stats_invalid():
    """Tests updating stats with invalid result raises ValueError"""
    logger.info("Testing update_boxer_stats with invlaid input")
    with pytest.raises(ValueError):
        update_boxer_stats(1, "tie")



    










