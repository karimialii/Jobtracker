"""Logging configuration for Job Tracker application."""
import logging
import os
from datetime import datetime


def setup_logging():
    """
    Setup application-wide logging configuration.
    
    Logs to both console and file with detailed formatting.
    """
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with timestamp
    log_filename = os.path.join(log_dir, f"jobtracker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # File handler - logs everything
            logging.FileHandler(log_filename, mode='w'),
            # Console handler - logs INFO and above
            logging.StreamHandler()
        ]
    )
    
    # Set console handler to INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_filename}")
    
    return log_filename
