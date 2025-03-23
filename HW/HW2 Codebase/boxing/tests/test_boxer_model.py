import sqlite3
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


