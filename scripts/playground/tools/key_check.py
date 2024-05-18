import os
import re

def find_api_keys(directory):
    """
    Find potential API keys in Python files within the specified directory.

    Args:
        directory (str): Path to the directory to search for API keys.

    Returns:
        list: List of potential API keys found.
    """
    api_keys = []
    # Regular expression to match potential API keys
    api_key_pattern = re.compile(r'(?:(?:[A-Za-z0-9+/]{4}){10,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    contents = f.read()
                    potential_keys = re.findall(api_key_pattern, contents)
                    if potential_keys:
                        api_keys.extend(potential_keys)

    return api_keys

if __name__ == "__main__":
    # Specify the directory to search for API keys
    search_directory = "scripts"

    # Find potential API keys
    found_keys = find_api_keys(search_directory)

    if found_keys:
        print("Potential API keys found:")
        for key in found_keys:
            print(key)
    else:
        print("No potential API keys found.")
