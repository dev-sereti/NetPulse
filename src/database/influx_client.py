# pyright: reportPrivateImportUsage=false

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List, Dict, Any
from datetime import datetime
from src.utils.logger import logger
from src.utils.config_loader import config

class InfluxDBManager:
    def __init__(self):
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
    
    def query_metrics(self, query: str) -> List[Dict]:
        """Execute a Flux query and return results"""
        try:
            result = self.query_api.query(query=query, org=config.influxdb_org)
            return result
        except Exception as e:
            logger.error(f"Error querying InfluxDB: {e}")
            return []
    
    def close(self):
        """Close the InfluxDB connection"""
        self.client.close()
