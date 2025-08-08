import pytest  # type: ignore[unused-import]

from src.database.influx_client import InfluxDBManager

def test_influxdb_connection():
    """Test InfluxDB connection"""
    db = InfluxDBManager()
    assert db.client is not None
    db.close()