import sys
import os
from datetime import datetime

# Import necessary modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def create_file_name_with_timestamp():
    """
    Create a unique file name with the current timestamp.
    Returns:
    str: The generated file name with a timestamp.
    """
    return datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"

def write_to_file(file_name, data):
    """
    Write data to a file. Creates or overwrites the file if it exists.
    
    Args:
    file_name (str): The name of the file to write to.
    data (str): The data to write into the file.
    """

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text_with_timestamp = f"{current_time}:\n{data}\n"


    # Check if the file exists
    if not os.path.exists(file_name):
        # If the file does not exist, create it and write data
        with open(file_name, "w") as f:
            f.write(text_with_timestamp)
    else:
        # If the file exists, append the data
        with open(file_name, "a") as f:
            f.write(text_with_timestamp)