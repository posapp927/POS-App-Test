import logging
import logging.config
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, SMTPHandler

# Logging configuration with default settings and ability to override
DEFAULT_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s - %(funcName)s: %(message)s',
        },
        'contextual': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(correlation_id)s]: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': os.path.join(os.path.dirname(__file__), 'app.log'),
            'mode': 'a',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': os.path.join(os.path.dirname(__file__), 'error.log'),
            'mode': 'a',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
        },
        'email': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'detailed',
            'mailhost': ('smtp.example.com', 587),
            'fromaddr': 'errors@example.com',
            'toaddrs': ['admin@example.com'],
            'subject': 'Critical Error in Application',
            'credentials': ('username', 'password'),
            'secure': (),
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'custom_discounts': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'astro_discounts': {
            'handlers': ['console', 'file', 'error_file', 'email'],
            'level': 'INFO',
            'propagate': False,
        },
        # Additional loggers for other modules can be defined here
    },
}

# Function to setup logging configuration
def setup_logging(logging_config=None):
    """
    Set up logging configuration. If logging_config is provided, it overrides the default configuration.
    """
    if logging_config is None:
        logging_config = DEFAULT_LOGGING_CONFIG
    logging.config.dictConfig(logging_config)
    logging.debug("Logging has been configured.")

# Function to get a logger for a specific module or class
def get_logger(name):
    """
    Retrieve a logger with the specified name.

    Args:
        name (str): Name of the logger to retrieve.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)

# Function to add context to logs, e.g., correlation IDs
def add_contextual_data(logger, **context):
    """
    Add contextual data (like correlation IDs) to log messages.

    Args:
        logger (logging.Logger): The logger to which context will be added.
        **context: Arbitrary context information to include in logs.
    """
    logger.addFilter(ContextualFilter(**context))

class ContextualFilter(logging.Filter):
    """
    A logging filter that adds contextual information (e.g., correlation_id) to log records.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.context = kwargs

    def filter(self, record):
        for key, value in self.context.items():
            setattr(record, key, value)
        return True

# Utility function for rotating logs manually
def rotate_logs(logger):
    """
    Rotate log files manually.

    Args:
        logger (logging.Logger): The logger whose handlers should rotate logs.
    """
    for handler in logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            handler.doRollover()
            logger.info("Log files rotated manually.")

# Utility function for logging critical errors and sending email notifications
def log_critical_error(logger, message):
    """
    Log a critical error and send an email notification if configured.

    Args:
        logger (logging.Logger): The logger to use for logging.
        message (str): The critical error message.
    """
    logger.critical(message)
    logger.debug("Critical error logged and email notification sent.")

# Error handling decorator for logging unhandled exceptions
def log_unhandled_exceptions(logger):
    """
    Decorator to log unhandled exceptions in a function.

    Args:
        logger (logging.Logger): The logger to use for logging exceptions.

    Returns:
        function: Wrapped function with exception logging.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Unhandled exception in {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator

# Setup logging when the module is imported
setup_logging()
