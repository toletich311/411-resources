
import pytest
import logging
import sqlite3

from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer
from boxing.models.boxers_model import update_boxer_stats
from boxing.utils.api_utils import get_random


# ------------------
# FIXTURES
# ------------------

@pytest.fixture
def ring_model():
    """Provides a new instance of RingModel."""
    return RingModel()


@pytest.fixture
def mock_update_boxer_stats(mocker):
    """Mock the update_boxer_stats function for testing purposes."""
    return mocker.patch("boxing.models.ring_model.update_boxer_stats")

"""Fixtures that provide a sample boxer"""
@pytest.fixture
def sample_boxer_1():
    return Boxer(id=1, name="Ali", weight=150, height=70, reach=72.5, age=30)

@pytest.fixture
def sample_boxer_2():
    return Boxer(id=2, name="Tyson", weight=160, height=72, reach=73.0, age=32)

@pytest.fixture
def sample_boxer_3():
    return Boxer(id=3, name="Samantha", weight=140, height=68, reach=71.0, age=23)


@pytest.fixture
def sample_boxer_4():
    return Boxer(id=4, name="Jake", weight=180, height=79, reach=74.5, age=37)

# ------------------
# TESTS FOR ENTERING THE RING 
# ------------------

def test_enter_ring_adds_first_boxer(ring_model, sample_boxer_1):
    """Test that adds a boxer into the ring"""
    ring_model.enter_ring(sample_boxer_1)
    assert len(ring_model.ring) == 1
    assert ring_model.ring[0].name == "Ali"

def test_enter_ring_adds_second_boxer(ring_model, sample_boxer_1, sample_boxer_2):
    """Test that adds two boxers into the ring"""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    assert len(ring_model.ring) == 2
    assert ring_model.ring[1].name == "Tyson"

def test_enter_ring_not_boxer(ring_model):
    """Test that an exception is raised when trying to add a non-Boxer object."""
    with pytest.raises(Exception):
        ring_model.enter_ring("not_a_boxer")

def test_enter_ring_raises_error_when_full(ring_model, sample_boxer_1, sample_boxer_2):
    """Test that a ValueError is raised when trying to add more than 2 boxers."""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    with pytest.raises(ValueError, match="Ring is full, cannot add more boxers."):
        ring_model.enter_ring(sample_boxer_1)


# ------------------
# TESTS FOR FIGHTING IN THE RING
# ------------------

def test_fight_return_winner(ring_model, sample_boxer_1, sample_boxer_2, mock_update_boxer_stats):
    """Test that calls the fight method and returns a valid winner."""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    winner = ring_model.fight()
    assert winner in [sample_boxer_1.name, sample_boxer_2.name]
    assert mock_update_boxer_stats.call_count == 2


def test_not_enough_boxers_raises_error(ring_model, sample_boxer_1):
    """Test that a ValueError is raised when trying to fight with less than 2 boxers."""
    ring_model.enter_ring(sample_boxer_1)
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()


def test_fight_return_winner_example(ring_model, sample_boxer_1, sample_boxer_2, mocker, mock_update_boxer_stats):
    """Test that confirms that the correct winner is returned after calling fight 
    with a mocked random number generator."""
    mocker.patch("boxing.models.ring_model.get_random", return_value=0.01)

    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)

    winner = ring_model.fight()

    assert winner == sample_boxer_1.name
    mock_update_boxer_stats.assert_any_call(sample_boxer_1.id, "win")
    mock_update_boxer_stats.assert_any_call(sample_boxer_2.id, "loss")
    assert mock_update_boxer_stats.call_count == 2

def test_two_consecutive_fights(ring_model, sample_boxer_1, sample_boxer_2, mock_update_boxer_stats):
    """Tests that two consecutive fights can occur back to back and that the ring
    resets properly"""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    winner1 = ring_model.fight()

    assert winner1 in [sample_boxer_1.name, sample_boxer_2.name]
    assert ring_model.get_boxers() == []
    assert mock_update_boxer_stats.call_count == 2

    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    winner2 = ring_model.fight()

    assert winner2 in [sample_boxer_1.name, sample_boxer_2.name]
    assert ring_model.get_boxers() == []
    assert mock_update_boxer_stats.call_count == 4
    
# ------------------
# TESTS FOR CLEARING THE RING  
# ------------------

def test_clear_ring(ring_model, sample_boxer_1, sample_boxer_2):
    """Test whether the ring can be cleared"""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    ring_model.clear_ring()
    assert ring_model.ring == []

def test_clear_rings_after_fight(ring_model , sample_boxer_1, sample_boxer_2, mock_update_boxer_stats):
    """Test that the ring is cleared after a fight"""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    ring_model.fight()
    assert ring_model.get_boxers() == []

def test_clear_ring_when_empty(ring_model):
    """Tests that clearing an empty ring does not raise an error"""
    ring_model.clear_ring()
    assert ring_model.get_boxers() == []

# ------------------
# TESTS FOR GETTING BOXERS 
# ------------------

def test_get_boxers(ring_model , sample_boxer_1, sample_boxer_2):
    """Test that get_boxers returns the boxers in the ring"""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    boxers = ring_model.get_boxers()
    assert boxers == [sample_boxer_1, sample_boxer_2]

# ------------------
# TESTS FOR RETURNING STATS
# ------------------

def test_get_fighter_skill(ring_model, sample_boxer_1):
    """Test that get_fighter_skill returns a float"""
    skill = ring_model.get_fighting_skill(sample_boxer_1)
    assert isinstance(skill, float)

def test_get_fighter_skill_expected(ring_model, sample_boxer_1):
    """Test that get_fighter_skill returns the expected value"""
    expected_skill = (150 * len("Ali")) + (72.5 / 10) + 0  # age_modifier is 0
    skill = ring_model.get_fighting_skill(sample_boxer_1)
    assert skill == expected_skill

def test_get_fighter_skill_young_modifier(ring_model, sample_boxer_3):
    """Test that get_fighter_skill returns the expected value for a young boxer"""
    expected_skill = (140 * len("Samantha")) + (71.0 / 10) - 1
    skill = ring_model.get_fighting_skill(sample_boxer_3)
    assert skill == expected_skill

def test_get_fighter_skill_old_modifier(ring_model, sample_boxer_4):
    """Test that get_fighter_skill returns the expected value for an old boxer"""
    expected_skill = (180 * len("Jake")) + (74.5 / 10) - 2
    skill = ring_model.get_fighting_skill(sample_boxer_4)
    assert skill == expected_skill



