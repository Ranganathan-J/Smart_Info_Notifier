"""
Centralized logging configuration for the application.

WHY THIS FILE EXISTS:
---------------------
This project continuously monitors external regulatory websites (RBI, SEBI, news).
Failures can occur at many stages:
- Web scraping (timeouts, HTML changes)
- Delta detection (hash mismatches)
- LLM analysis (timeouts, invalid responses)
- Notifications (email failures)

A centralized logger ensures:
1. Consistent log format across all modules
2. Easy debugging in production
3. Auditability for compliance workflows
4. Clear separation between business logic and observability
"""

from loguru import logger
import sys
from pathlib import Path

from config import settings  # loaded settings.yaml

# Ensure log directory exists
LOG_FILE_PATH = Path(settings.paths.logs)
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

def setup_logger():
    """
    Configure application-wide logging.

    PURPOSE:
    --------
    - Console logs help during development and debugging
    - File logs persist execution history for audits and post-mortems
    - Structured timestamps help correlate events across runs

    This function should be called ONCE at application startup.
    """

    # Remove default logger to avoid duplicate logs
    logger.remove()

    # Console logging (developer visibility)
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level}</level> | "
               "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "{message}"
    )

    # File logging (audit & troubleshooting)
    logger.add(
        LOG_FILE_PATH,
        level="INFO",
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    logger.info("Logger initialized successfully")


def get_logger(name: str | None = None):
    """
    Returns the configured logger instance.

    WHY NOT CREATE LOGGERS PER FILE?
    --------------------------------
    Using a single shared logger ensures:
    - Uniform log structure
    - Easier log aggregation
    - Simpler operational monitoring

    Usage:
    ------
    from utils.logger import get_logger
    log = get_logger()
    log.info("Scraping started for RBI Circulars")
    """
    return logger
