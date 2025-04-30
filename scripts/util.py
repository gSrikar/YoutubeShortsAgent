import os

def load_instructions_from_file(file_path):
    """
    Reads instructions from a file and returns them as a string.

    Args:
        file_path (str): The path to the file containing instructions.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"An error occurred while reading the file {file_path}: {e}")