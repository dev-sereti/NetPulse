import pytest

from src.database.influx_client import InfluxDBManager


@pytest.fixture
def influxdb_manager():
    db = InfluxDBManager()
    yield db
    db.close()


def test_influxdb_connection(influxdb_manager):
    """Test that InfluxDB client is initialized correctly"""
    assert influxdb_manager.client is not None
