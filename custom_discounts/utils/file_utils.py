import os
import csv
import json
import shutil
import logging
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

# Initialize the logger for file utilities
logger = logging.getLogger('custom_discounts.utils.file_utils')


# File existence check
def file_exists(file_path: str) -> bool:
    """Check if the specified file exists."""
    exists = os.path.isfile(file_path)
    if exists:
        logger.debug(f"File exists: {file_path}")
    else:
        logger.warning(f"File not found: {file_path}")
    return exists


# Directory existence check and creation
def ensure_directory_exists(dir_path: str) -> None:
    """Ensure that the directory exists; create it if it doesn't."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.info(f"Created directory: {dir_path}")
    else:
        logger.debug(f"Directory already exists: {dir_path}")


# Read CSV file
def read_csv(file_path: str, delimiter: str = ',', encoding: str = 'utf-8') -> List[Dict[str, Any]]:
    """Read a CSV file and return a list of dictionaries."""
    if not file_exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with open(file_path, mode='r', encoding=encoding) as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        data = [row for row in reader]
    
    logger.info(f"Read {len(data)} rows from CSV file: {file_path}")
    return data


# Write to CSV file
def write_csv(file_path: str, data: List[Dict[str, Any]], delimiter: str = ',', encoding: str = 'utf-8', include_header: bool = True) -> None:
    """Write a list of dictionaries to a CSV file."""
    ensure_directory_exists(os.path.dirname(file_path))

    with open(file_path, mode='w', encoding=encoding, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=delimiter)
        if include_header:
            writer.writeheader()
        writer.writerows(data)
    
    logger.info(f"Wrote {len(data)} rows to CSV file: {file_path}")


# Read JSON file
def read_json(file_path: str, encoding: str = 'utf-8') -> Any:
    """Read a JSON file and return the data."""
    if not file_exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    with open(file_path, mode='r', encoding=encoding) as file:
        data = json.load(file)
    
    logger.info(f"Read JSON file: {file_path}")
    return data


# Write to JSON file
def write_json(file_path: str, data: Any, encoding: str = 'utf-8', pretty_print: bool = False) -> None:
    """Write data to a JSON file."""
    ensure_directory_exists(os.path.dirname(file_path))

    with open(file_path, mode='w', encoding=encoding) as file:
        if pretty_print:
            json.dump(data, file, indent=4)
        else:
            json.dump(data, file)
    
    logger.info(f"Wrote JSON file: {file_path}")


# File deletion
def delete_file(file_path: str) -> None:
    """Delete the specified file."""
    if file_exists(file_path):
        os.remove(file_path)
        logger.info(f"Deleted file: {file_path}")
    else:
        logger.warning(f"Attempted to delete non-existent file: {file_path}")


# File backup and restore
def backup_file(file_path: str, backup_dir: Optional[str] = None) -> str:
    """Create a backup of the specified file."""
    if not file_exists(file_path):
        raise FileNotFoundError(f"File to backup not found: {file_path}")

    if backup_dir is None:
        backup_dir = os.path.join(os.path.dirname(file_path), 'backups')
    
    ensure_directory_exists(backup_dir)

    backup_path = os.path.join(backup_dir, f"{os.path.basename(file_path)}.bak")
    shutil.copy2(file_path, backup_path)
    
    logger.info(f"Created backup of {file_path} at {backup_path}")
    return backup_path


# File locking mechanism
@contextmanager
def file_lock(file_path: str):
    """Context manager for file locking."""
    lock_file_path = f"{file_path}.lock"
    try:
        if os.path.exists(lock_file_path):
            raise RuntimeError(f"File is locked: {file_path}")
        
        with open(lock_file_path, 'w') as lock_file:
            lock_file.write("LOCKED")
        logger.debug(f"Locked file: {file_path}")

        yield

    finally:
        if os.path.exists(lock_file_path):
            os.remove(lock_file_path)
            logger.debug(f"Unlocked file: {file_path}")


# File path normalization
def normalize_file_path(path: str) -> str:
    """Normalize a file path to ensure it is valid and consistent."""
    normalized_path = os.path.normpath(path)
    logger.debug(f"Normalized file path: {normalized_path}")
    return normalized_path


# List files in a directory
def list_files_in_directory(directory: str, extension: Optional[str] = None) -> List[str]:
    """List all files in a directory, optionally filtering by extension."""
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Not a directory: {directory}")

    files = []
    for file in os.listdir(directory):
        if extension is None or file.endswith(extension):
            files.append(os.path.join(directory, file))
    
    logger.info(f"Found {len(files)} files in directory: {directory}")
    return files
