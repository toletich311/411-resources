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
def sample_boxer_1():
    return Boxer(id=1, name="Ali", weight=150, height=70, reach=72.5, age=30)

@pytest.fixture
def sample_boxer_2():
    return Boxer(id=2, name="Tyson", weight=160, height=72, reach=73.0, age=32)


#testing enter_ring constructor 
def test_enter_ring_adds_boxer(ring_model, sample_boxer_1):
    ring_model.enter_ring(sample_boxer_1)
    assert len(ring_model.ring) == 1
    assert ring_model.ring[0].name == "Ali"