# config/logging_config.py

import logging
import logging.config
import os

# Define a basic logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s - %(funcName)s: %(message)s',
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
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename': os.path.join(os.path.dirname(__file__), 'app.log'),
            'mode': 'a',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'custom_discounts': {  # Logger for the custom_discounts module
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'cart': {  # Logger for the cart module
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'product': {  # Logger for the product module
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Add other loggers here as needed for different modules
    },
}

def setup_logging():
    """Set up logging configuration."""
    logging.config.dictConfig(LOGGING_CONFIG)
