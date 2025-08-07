# pyright: reportPrivateImportUsage=false

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import FluxTable
from typing import List, Dict, Any
from datetime import datetime
from src.utils.logger import logger
from src.utils.config_loader import config


class InfluxDBManager:
    def __init__(self):
        # Validate required config values
        assert config.influxdb_url is not None, "INFLUXDB_URL must be set"
        assert config.influxdb_token is not None, "INFLUXDB_TOKEN must be set"
        assert config.influxdb_org is not None, "INFLUXDB_ORG must be set"
        assert config.influxdb_bucket is not None, "INFLUXDB_BUCKET must be set"

        self.client = InfluxDBClient(
            url=config.influxdb_url,
            token=config.influxdb_token,
            org=config.influxdb_org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = config.influxdb_bucket
        logger.info(f"Connected to InfluxDB at {config.influxdb_url}")

    def write_metric(self, measurement: str, tags: Dict[str, str], fields: Dict[str, Any]):
        """Write a single metric to InfluxDB"""
        try:
            point = Point(measurement)
            for key, value in tags.items():
                point.tag(key, value)
            for key, value in fields.items():
                point.field(key, value)
            point.time(datetime.utcnow(), WritePrecision.NS)

            self.write_api.write(bucket=self.bucket, record=point)
            logger.debug(f"Written metric: {measurement} with tags {tags}")
        except Exception as e:
            logger.error(f"Error writing to InfluxDB: {e}")

    def query_metrics(self, query: str) -> List[Dict[str, Any]]:
        """Execute a Flux query and return results as a list of dictionaries"""
        try:
            tables: List[FluxTable] = self.query_api.query(query=query, org=config.influxdb_org)
            results: List[Dict[str, Any]] = []

            for table in tables:
                for record in table.records:
                    results.append(record.values)

            return results
        except Exception as e:
            logger.error(f"Error querying InfluxDB: {e}")
            return []

    def close(self):
        """Close the InfluxDB connection"""
        self.client.close()
