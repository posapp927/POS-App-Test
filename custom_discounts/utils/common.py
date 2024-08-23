# custom_discounts/utils/common.py

import os
import json
import logging
from typing import Any, Dict, Optional, Union

# Set up a logger specifically for common utilities
logger = logging.getLogger('custom_discounts.utils.common')

def create_directory(directory_path: str) -> None:
    """
    Create a directory if it doesn't already exist.

    Args:
        directory_path (str): The path of the directory to create.

    Raises:
        OSError: If the directory cannot be created.
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info(f"Directory created at: {directory_path}")
        else:
            logger.debug(f"Directory already exists: {directory_path}")
    except OSError as e:
        logger.error(f"Failed to create directory {directory_path}: {e}")
        raise

def load_json(file_path: str) -> Optional[Dict[Any, Any]]:
    """
    Load a JSON file and return its content.

    Args:
        file_path (str): The path of the JSON file to load.

    Returns:
        Optional[Dict[Any, Any]]: The content of the JSON file as a dictionary, or None if loading fails.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        OSError: If there is an error reading the file.
    """
    if not os.path.exists(file_path):
        logger.error(f"JSON file not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logger.info(f"JSON file loaded successfully: {file_path}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding failed for file {file_path}: {e}")
        raise
    except OSError as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        raise

def save_json(file_path: str, data: Dict[Any, Any]) -> None:
    """
    Save a dictionary as a JSON file.

    Args:
        file_path (str): The path of the JSON file to save.
        data (Dict[Any, Any]): The data to save in the JSON file.

    Raises:
        OSError: If there is an error writing to the file.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logger.info(f"JSON file saved successfully: {file_path}")
    except OSError as e:
        logger.error(f"Failed to save JSON file {file_path}: {e}")
        raise

def file_exists(file_path: str) -> bool:
    """
    Check if a file exists at the given path.

    Args:
        file_path (str): The path of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    exists = os.path.exists(file_path)
    logger.debug(f"File exists check for {file_path}: {exists}")
    return exists

def read_file(file_path: str) -> Optional[str]:
    """
    Read the contents of a file.

    Args:
        file_path (str): The path of the file to read.

    Returns:
        Optional[str]: The contents of the file as a string, or None if reading fails.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If there is an error reading the file.
    """
    if not file_exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            logger.info(f"File read successfully: {file_path}")
            return content
    except OSError as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise

def write_file(file_path: str, content: str) -> None:
    """
    Write content to a file.

    Args:
        file_path (str): The path of the file to write.
        content (str): The content to write to the file.

    Raises:
        OSError: If there is an error writing to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
            logger.info(f"File written successfully: {file_path}")
    except OSError as e:
        logger.error(f"Failed to write file {file_path}: {e}")
        raise

def validate_file_extension(file_path: str, valid_extensions: Union[str, tuple]) -> bool:
    """
    Validate that the file has a specific extension.

    Args:
        file_path (str): The path of the file to validate.
        valid_extensions (str or tuple): A string or tuple of valid file extensions.

    Returns:
        bool: True if the file has a valid extension, False otherwise.
    """
    if not isinstance(valid_extensions, (str, tuple)):
        logger.error("Valid extensions must be a string or a tuple of strings.")
        raise ValueError("Valid extensions must be a string or a tuple of strings.")

    is_valid = file_path.lower().endswith(valid_extensions)
    logger.debug(f"File extension validation for {file_path}: {is_valid}")
    return is_valid

def find_files_with_extension(directory_path: str, extension: str) -> List[str]:
    """
    Find all files in a directory with a specific extension.

    Args:
        directory_path (str): The path of the directory to search.
        extension (str): The file extension to search for.

    Returns:
        List[str]: A list of file paths that match the extension.

    Raises:
        OSError: If there is an error accessing the directory.
    """
    try:
        files_with_extension = [
            os.path.join(directory_path, file)
            for file in os.listdir(directory_path)
            if file.endswith(extension)
        ]
        logger.info(f"Found {len(files_with_extension)} files with extension {extension} in {directory_path}")
        return files_with_extension
    except OSError as e:
        logger.error(f"Failed to access directory {directory_path}: {e}")
        raise
