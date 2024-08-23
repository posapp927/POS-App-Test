# custom_discounts/utils/__init__.py

"""
Utilities for the custom_discounts module.

This package contains utility modules that provide common functionalities used across the custom_discounts module.
"""

from .common import *
from .logging_utils import setup_custom_logger
from .validation_utils import validate_discount_data
from .scraping_utils import Scraper
from .date_utils import parse_date_range, is_date_within_range
from .file_utils import load_csv_data, save_to_file

# Initialize default logging setup
setup_custom_logger()

__all__ = [
    'setup_custom_logger',
    'validate_discount_data',
    'Scraper',
    'parse_date_range',
    'is_date_within_range',
    'load_csv_data',
    'save_to_file',
]
