import os
import sys
import tomli
from pprint import pprint

"""
Configuration module for the chatminal application.
Contains constants and default settings.
"""

# App Configurations
TOOL_NAME = "chatminal"
VERSION = "0.1.0"
OPEN_AI_MODELS_URL = "https://api.openai.com/v1/models"
STORE = {}
ACCEPTED_FILE_EXTENSIONS = ['.txt', '.pdf', '.docx', '.json']
ACCEPTED_HELP_VERION = ['-v', '--version', '-h', '--help']
EXAMPLE_FOLDER = 'examples'

# Default configuration dictionary
config = {
    "TOOL_NAME": TOOL_NAME,
    "VERSION": VERSION,
    "OPEN_AI_MODELS_URL": OPEN_AI_MODELS_URL,
    "STORE": STORE,
    "ACCEPTED_FILE_EXTENSIONS": ACCEPTED_FILE_EXTENSIONS,
    "ACCEPTED_HELP_VERION": ACCEPTED_HELP_VERION,
    "EXAMPLE_FOLDER": EXAMPLE_FOLDER
}


def setup_logging():
    """
    Setup the logger for this module.
    Returns:
    Logger object.
    """
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


# Initialize logger
logger = setup_logging()


def load_config():
    """
    Load configuration from the user's home directory TOML file.

    Returns:
    dict: Configuration values from the TOML file if it exists, otherwise an empty dictionary.
    """
    home_dir = os.path.expanduser("~")  # Get the home directory path
    config_file = os.path.join(home_dir, ".chatminal-config.toml")  # Specify the TOML file name

    if os.path.isfile(config_file):  # Check if the file exists
        try:
            with open(config_file, "rb") as f:
                user_config = tomli.load(f)  # Parse the TOML file into a dictionary
                logger.info(f"Successfully loaded configuration file: {config_file}")
                return user_config
        except tomli.TOMLDecodeError as e:  # Handle parsing errors
            logger.error(f"Error: Unable to parse {config_file}. Please check the file format: {e}")
            sys.exit(1)  # Exit the program if the file format is invalid
    else:
        logger.warning(f"No configuration file found at {config_file}. Using default settings.")
        return {}  # Return an empty dictionary if no config file is found


def print_config():
    """
    Print the final configuration settings for debugging.
    """
    logger.info("Final Configuration Settings:")
    pprint(config)


# Load user configurations and update the default settings
user_settings = load_config()
config.update(user_settings)

# Print out the final configuration values
print_config()
