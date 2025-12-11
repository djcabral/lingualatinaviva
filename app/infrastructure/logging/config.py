"""
Logging Configuration

Centralized logging setup for the application.
"""

import logging
import os
from typing import Optional

def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Configure application logging
    
    Args:
        log_level: Log level as string (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    # Get log level from environment or parameter
    level_str = log_level or os.getenv('LOG_LEVEL', 'INFO')
    level = getattr(logging, level_str.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create and configure application logger
    logger = logging.getLogger('lingua_latina')
    logger.setLevel(level)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f'lingua_latina.{name}')