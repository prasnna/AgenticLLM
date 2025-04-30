"""
Utility functions for file operations
"""
import os
import json
from typing import Dict, List, Any, Union


def read_sql_file(file_path: str) -> str:
    """
    Read the contents of a SQL file
    
    Args:
        file_path: Path to the SQL file
        
    Returns:
        The contents of the SQL file as a string
    """
    with open(file_path, 'r') as f:
        return f.read()


def list_files_in_directory(directory_path: str, extension: str = None) -> List[str]:
    """
    List all files in a directory, optionally filtered by extension
    
    Args:
        directory_path: Path to the directory
        extension: Optional file extension to filter by (e.g., '.sql')
        
    Returns:
        A list of file paths
    """
    files = []
    for filename in os.listdir(directory_path):
        if extension is None or filename.endswith(extension):
            files.append(os.path.join(directory_path, filename))
    return files


def save_json(data: Union[Dict, List], file_path: str) -> None:
    """
    Save data to a JSON file
    
    Args:
        data: The data to save
        file_path: Path to the JSON file
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def load_json(file_path: str) -> Union[Dict, List]:
    """
    Load data from a JSON file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The data from the JSON file
    """
    with open(file_path, 'r') as f:
        return json.load(f)
