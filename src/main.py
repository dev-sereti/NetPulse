import asyncio
from src.utils.logger import logger
from src.database.influx_client import InfluxDBManager
from src.utils.config_loader import config

async def main():
    logger.info("Starting Network Monitor Application")
    
    # Initialize database connection
    db_manager = InfluxDBManager()
    
    try:
        # Main monitoring loop will be implemented here
        logger.info("Network Monitor is running...")
        while True:
            await asyncio.sleep(config.monitoring_interval)
    except KeyboardInterrupt:
        logger.info("Shutting down Network Monitor")
    finally:
        db_manager.close()

if __name__ == "__main__":
    asyncio.run(main())