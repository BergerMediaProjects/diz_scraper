"""Utility functions for the DIZ scraper."""

import logging
import os
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists.
        
    Returns:
        Path object for the directory.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def clean_filename(filename: str) -> str:
    """Clean a filename by removing or replacing invalid characters.
    
    Args:
        filename: Filename to clean.
        
    Returns:
        Cleaned filename.
    """
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(". ")
    
    # Ensure the filename is not empty
    if not filename:
        filename = "unnamed"
        
    return filename


def get_file_size(path: Union[str, Path]) -> Optional[int]:
    """Get the size of a file in bytes.
    
    Args:
        path: Path to the file.
        
    Returns:
        Size of the file in bytes, or None if the file doesn't exist.
    """
    try:
        return os.path.getsize(path)
    except (OSError, IOError) as e:
        logger.warning(f"Failed to get size of {path}: {e}")
        return None


def format_file_size(size_bytes: int) -> str:
    """Format a file size in bytes to a human-readable string.
    
    Args:
        size_bytes: Size in bytes.
        
    Returns:
        Human-readable size string.
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB" 