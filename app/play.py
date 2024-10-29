"""
Play file to run the CLI tool to generate the completion from Langchain Using GROQ
"""

from utils import *  # noqa F403
from imports import *  # noqa F403
from config import TOOL_NAME, VERSION, OPEN_AI_MODELS_URL
import sys
import os
from completion_tool import Minal


# NEED TO ADD THIS LINE TO IMPORT THE CONFIG FILE
# This is needed to import the config file from the parent directory
# THIS TELLS PYTHON TO LOOK FOR THE CONFIG FILE IN THE PARENT DIRECTORY
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Setup logger
logger = setup_logging()

# Set the timezone
TIME_ZONE = pytz.timezone("America/Toronto")


def get_version():
    """
    Get Version for cli tool by using -v or --version

    Returns:
    str: version number
    """
    try:
        if "--version" in sys.argv or "-v" in sys.argv:
            return VERSION
    except Exception as e:
        logger.error(f"Error in get_version at  {e}")
        return None


def display_help():
    """
    Get Help for cli tool by using -h or --help
    Returns:
    str: help message
    """
    return f"""
            {TOOL_NAME} - A simple CLI tool to do Chat Completion from OpenAI

            Usage:
            {TOOL_NAME} [options]

            Options:
            -h, --help, --howto              Show this help message
            -v, --version                    Show the version of the tool
            --input_text, -i                 Input text to generate completion
            --output, -o                     Output file to save the generated completion
            --temperature, -t                Temperature for the completion
            --max_tokens                     Maximum tokens for the completion
            --api_key, -a                    OpenAI API Key
            --model, -m                      Model for the completion
            --select_choice, -sc             Select the choice to perform the task
            --token-usage                    Show the token usage for the completion


            Examples:
            Set the input text to generate the completion:
            1. python3 app/play.py ../<YOUR_FILE> --input_text "Translate the provided text to Chinese" -a YOUR_API_KEY
            2. python3 app/play.py -i "Tell me about directional derivative" -a YOUR_API_KEY --output
            2. python3 app/play.py ../<YOUR_FILE> --select_choice translate -a YOUR_API_KEY
            3. python3 app/play.py ../<YOUR_FILE> --select_choice translate -a YOUR_API_KEY --output
            4. python3 app/play.py ../<YOUR_FILE> --select_choice translate -a YOUR_API_KEY --output --token-usage
            """


def get_input():
    """
    Get the input text from the command line arguments.
    Returns:
    str: The input text or None if not provided.
    """
    return (
        sys.argv[sys.argv.index("--input_text") + 1]
        if "--input_text" in sys.argv
        else None
    )


def get_output():
    """
    Get the output file from the command line arguments.
    Returns:
    str: The output file or None if not provided.
    """
    return sys.argv[sys.argv.index("--output") + 1] if "--output" in sys.argv else None


def get_available_models(api_key=None):
    """
    Retrieve the list of available models from OpenAI.

    Returns:
    dict: JSON response from the API or None if an error occurs.
    """
    try:
        if "--models" in sys.argv:
            api_key = (
                api_key or sys.argv[sys.argv.index("--api_key") + 1]
                if "--api_key" in sys.argv
                else sys.argv[sys.argv.index("-a") + 1]
            )
            if api_key is None:
                raise Exception("API Key is missing")

            # Make a request to OpenAI API
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(OPEN_AI_MODELS_URL, headers=headers)

            # Check for a successful request
            if response.status_code == 200:
                logger.info("Available models retrieved successfully.")
                return response.json()
            else:
                logger.error(
                    f"Failed to retrieve models: {response.status_code} - {response.text}"
                )
                return None

    except Exception as e:
        logger.error(f"Error in get_available_models at line  {e}")
        return None


# ADDITIONAL FUNCTIONS TO Set the temperature, max_tokens, api_key, and model


async def main():
    # Check for file arguments
    try:
        minal = Minal()
        minal.run()

    except Exception as e:
        logger.error(f"Error in main at line  {e.__traceback__.tb_lineno}")
        return False


if __name__ == "__main__":
    # Need to using asyncio.run() to run the async function
    # We will using async for stream of Langchain for future development
    # with API request Response as streamingResponse.
    asyncio.run(main())
