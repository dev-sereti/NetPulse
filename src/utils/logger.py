from loguru import logger
import sys
from src.utils.config_loader import config

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    level=config.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
logger.add(
    "logs/netpulse.log",
    rotation="10 MB",
    retention="7 days",
    level=config.log_level
)