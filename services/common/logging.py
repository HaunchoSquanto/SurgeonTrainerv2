"""
Centralized logging for all services
"""
import logging
import sys
from typing import Optional
from .config import get_config


_loggers = {}


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with standardized configuration.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    if name in _loggers:
        return _loggers[name]
    
    config = get_config()
    
    logger = logging.getLogger(name)
    logger.setLevel(config.log_level)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(config.log_level)
        
        formatter = logging.Formatter(config.log_format)
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    _loggers[name] = logger
    return logger


class StructuredLogger:
    """
    Structured logging helper for better log parsing/analysis.
    Usage:
        log = StructuredLogger(__name__)
        log.info("case_normalized", mrn="12345", procedure="rotator-cuff")
    """
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
    
    def _format_message(self, event: str, **kwargs) -> str:
        """Format message with event name and key-value pairs"""
        parts = [f"event={event}"]
        for key, value in kwargs.items():
            parts.append(f"{key}={value}")
        return " ".join(parts)
    
    def debug(self, event: str, **kwargs):
        self.logger.debug(self._format_message(event, **kwargs))
    
    def info(self, event: str, **kwargs):
        self.logger.info(self._format_message(event, **kwargs))
    
    def warning(self, event: str, **kwargs):
        self.logger.warning(self._format_message(event, **kwargs))
    
    def error(self, event: str, **kwargs):
        self.logger.error(self._format_message(event, **kwargs))
    
    def exception(self, event: str, **kwargs):
        self.logger.exception(self._format_message(event, **kwargs))
