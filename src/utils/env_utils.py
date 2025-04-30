"""
Utility functions for handling environment variables
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

def load_env_vars(env_file: Optional[str] = None) -> None:
    """
    Load environment variables from .env file

    Args:
        env_file: Path to the .env file. If None, uses default location.
    """
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to load from root directory first, then fall back to src/config/.env
        if os.path.exists(".env"):
            load_dotenv()
        elif os.path.exists(os.path.join("src", "config", ".env")):
            load_dotenv(os.path.join("src", "config", ".env"))

def get_env_var(var_name: str, default: Any = None) -> str:
    """
    Get an environment variable

    Args:
        var_name: Name of the environment variable
        default: Default value to return if the variable is not found

    Returns:
        The value of the environment variable, or the default value if not found
    """
    return os.environ.get(var_name, default)

def get_env_list(var_name: str, delimiter: str = ",") -> List[str]:
    """
    Get an environment variable as a list

    Args:
        var_name: Name of the environment variable
        delimiter: Delimiter to split the string by

    Returns:
        The value of the environment variable as a list
    """
    value = get_env_var(var_name)
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter)]

def set_env_var(var_name: str, value: str) -> None:
    """
    Set an environment variable

    Args:
        var_name: Name of the environment variable
        value: Value to set
    """
    os.environ[var_name] = value
