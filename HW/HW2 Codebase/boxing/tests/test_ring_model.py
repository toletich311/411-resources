import pytest
import logging
import sqlite3

from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer
from boxing.models.boxers_model import update_boxer_stats
from boxing.utils.api_utils import get_random