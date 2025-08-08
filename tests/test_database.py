import sys
import os
import pytest

# Dynamically add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.influx_client import InfluxDBManager


@pytest.fixture
def influxdb_manager():
    db = InfluxDBManager()
    yield db
    db.close()


def test_influxdb_connection(influxdb_manager):
    """Test that InfluxDB client is initialized correctly"""
    assert influxdb_manager.client is not None
