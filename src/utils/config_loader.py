import os
from typing import Dict, Any
from dotenv import load_dotenv
import yaml

load_dotenv()

class Config:
    def __init__(self):
        self.influxdb_url = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
        self.influxdb_token = os.getenv('INFLUXDB_TOKEN')
        self.influxdb_org = os.getenv('INFLUXDB_ORG', 'netpulse')
        self.influxdb_bucket = os.getenv('INFLUXDB_BUCKET', 'network-metrics')
        
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.monitoring_interval = int(os.getenv('MONITORING_INTERVAL', '60'))
        self.alert_check_interval = int(os.getenv('ALERT_CHECK_INTERVAL', '30'))
        
        self.snmp_community = os.getenv('SNMP_COMMUNITY', 'public')
        self.snmp_version = os.getenv('SNMP_VERSION', '2c')
    
    def load_devices(self, config_file: str = 'config/devices.yaml') -> Dict[str, Any]:
        """Load device configuration from YAML file"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

config = Config()