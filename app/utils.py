from imports import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime

logger = setup_logging()

# Import necessary modules



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

def generic_get_argv(keyword, argv):
    """
    Get the command line arguments passed to the script.
    
    Returns:
    list: The command line arguments passed to the script.
    """
    return sys.argv[1:]

def generic_set_argv(*args):
    """
    Set the command line arguments passed to the script.
    
    Args:
    argv (list): The command line arguments to set.
    """
    parsed_args = {}
    if args is None:
        return parsed_args
    
    for key in args:
        try:
            index = sys.argv.index(key)
            #print(f"Index: {index}")
            if len(sys.argv) > index + 1 and not sys.argv[index + 1].startswith("-"):
                parsed_args[key] = sys.argv[index + 1]
            else:
                parsed_args[key] = True
        except ValueError:
            #print(f"Error: {key} must be an integer.")
            parsed_args[key] = None
            #sys.exit(1)
    return parsed_args

def get_file_content(file_path):
    """
    Read the content of the provided file.

    Args:
    file_path (str): Path to the file.

    Returns:
    str: Content of the file as a string.
    """
    try:
        if file_path.endswith(".json"):
            logger.info(f"Reading context from JSON file: {file_path}")
            with open(file_path, "r") as f:
                json_content = json.load(f)
                return json.dumps(json_content, indent=4)  # Convert JSON to a formatted string
        else:
            logger.info(f"Reading context from text file: {file_path}")
            with open(file_path, "r") as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path} at line {e.__traceback__.tb_lineno}: {e}")
        return None