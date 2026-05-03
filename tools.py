import os
from crewai.tools import tool

@tool("List Directory")
def list_directory(directory_path: str) -> str:
    """Lists all files and directories in the given path."""
    try:
        items = os.listdir(directory_path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {e}"

@tool("Read File")
def read_file(file_path: str) -> str:
    """Reads the contents of a specific file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"
