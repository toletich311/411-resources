
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

"""Fixtures that provide a sample boxer"""
@pytest.fixture
def sample_boxer_1():
    return Boxer(id=1, name="Ali", weight=150, height=70, reach=72.5, age=30)

@pytest.fixture
def sample_boxer_2():
    return Boxer(id=2, name="Tyson", weight=160, height=72, reach=73.0, age=32)



# ------------------
# TESTS FOR ENTERING THE RING 
# ------------------

def test_enter_ring_adds_first_boxer(ring_model, sample_boxer_1):
    ring_model.enter_ring(sample_boxer_1)
    assert len(ring_model.ring) == 1
    assert ring_model.ring[0].name == "Ali"

def test_enter_ring_adds_second_boxer(ring_model, sample_boxer_1, sample_boxer_2):
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    assert len(ring_model.ring) == 2
    assert ring_model.ring[1].name == "Tyson"

def test_enter_ring_not_boxer(ring_model):
    with pytest.raises(TypeError, match="Invalid input, Expected 'Boxer'"):
        ring_model.enter_ring("not_a_boxer")

def test_enter_ring_raises_error_when_full(ring_model, sample_boxer_1, sample_boxer_2):
    """Test that a ValueError is raised when trying to add more than 2 boxers."""
    ring_model.enter_ring(sample_boxer_1)
    ring_model.enter_ring(sample_boxer_2)
    with pytest.raises(ValueError, match="The ring is at max capacity."):
        ring_model.enter_ring(sample_boxer_1)


# ------------------
# TESTS FOR FIGHTING IN THE RING
# ------------------

def test_fight_return_winner():
    pass

def test_not_enough_boxers_raises_error():
    pass

# ------------------
# TESTS FOR CLEARING THE RING  
# ------------------

def test_clear_ring(ring_model):
    pass 

def test_clear_rings_after_fight():
    pass

def test_clear_ring_when_empty():
    pass

# ------------------
# TESTS FOR GETTING BOXERS 
# ------------------

def test_get_boxers():
    pass

# ------------------
# TESTS FOR RETURNING STATS
# ------------------

def test_get_fighter_stats():
    pass

def test_get_fighter_stats_no_fighters():
    pass