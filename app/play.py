import sys
import os
import json

# NEED TO ADD THIS LINE TO IMPORT THE CONFIG FILE
# This is needed to import the config file from the parent directory
# THIS TELLS PYTHON TO LOOK FOR THE CONFIG FILE IN THE PARENT DIRECTORY
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from imports import *
from utils import *

# Setup logger
logger = setup_logging()

# Set the timezone
TIME_ZONE = pytz.timezone('America/Toronto')

## ADDITIONAL FUNCTIONS TO GET THE VERSION AND HELP
def get_version():
    """
    Get Version for cli tool by using -v or --version

    Returns:
    str: version number
    """
    try:
        if '--version' in sys.argv or '-v' in sys.argv:
            return VERSION
    except Exception as e:
        logger.error(f"Error in get_version at line {e.__traceback__.tb_lineno}: {e}")
        return None

def get_help():
    """
    Get Help for cli tool by using -h or --help
    Returns:
    str: help message
    """
    try:
        if '--help' in sys.argv or '-h' in sys.argv or '--howto' in sys.argv:
            return f"""
            {TOOL_NAME} - A simple CLI tool to do Chat Completion from OpenAI

            Usage:
            {TOOL_NAME} [options]

            Options:
            -h, --help, --howto     Show this help message
            -v, --version           Show the version of the tool
            --input                 Input text to generate completion
            --output                Output file to save the generated completion
            --temperature           Temperature for the completion
            --max_tokens            Maximum tokens for the completion
            --api_key               OpenAI API Key
            --model                 Model for the completion
            """
    
    except Exception as e:
        logger.error(f"Error in get_help at line {e.__traceback__.tb_lineno}: {e}")
        return None

def get_input():
    try:
        # Check if '--input_text' or '-i' is in the command-line arguments
        if '--input_text' in sys.argv:
            return sys.argv[sys.argv.index('--input_text') + 1]
        elif '-i' in sys.argv:
            return sys.argv[sys.argv.index('-i') + 1]
        else:
            raise ValueError("Input text is missing")
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None

def get_output():
    try:
        if '--output' in sys.argv or '-o' in sys.argv:
            return sys.argv[sys.argv.index('--output') + 1]
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None

def get_available_models():
    """
    Retrieve the list of available models from OpenAI.

    Returns:
    dict: JSON response from the API or None if an error occurs.
    """
    try:
        if '--models' in sys.argv:
            api_key = set_api_key()
            if api_key is None:
                raise Exception("API Key is missing")

            logger.info(f"Retrieving available models from OpenAI..")
            # Make a request to OpenAI API
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            response = requests.get(OPEN_AI_MODELS_URL, headers=headers)

            # Check for a successful request
            if response.status_code == 200:
                logger.info("Available models retrieved successfully.")
                return response.json()
            else:
                logger.error(f"Failed to retrieve models: {response.status_code} - {response.text}")
                return None

    except Exception as e:
        logger.error(f"Error in get_available_models at line {e.__traceback__.tb_lineno}: {e}")
        return None

## ADDITIONAL FUNCTIONS TO Set the temperature, max_tokens, api_key, and model
def set_temperature():
    """
    Retrieve temperature from command-line arguments.
    
    Returns:
    str: temperature if provided, None otherwise
    """
    try:
        if  '--temperature' in sys.argv or '-t' in sys.argv:
            logger.info(f"Temperature: {sys.argv[sys.argv.index('--temperature') + 1]}")
            return sys.argv[sys.argv.index('--temperature') + 1]
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None
    
def set_max_tokens():
    """
    Retrieve max tokens from command-line arguments.

    Returns:
    str: max tokens if provided, None using the default value.
    
    """
    try:
        if '--max_tokens' in sys.argv:
            logger.info(f"Max Tokens: {sys.argv[sys.argv.index('--max_tokens') + 1]}")
            return sys.argv[sys.argv.index('--max_tokens') + 1]
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None
    
def set_base_url():
    """
    Setting the base URL for the API request.

    Returns:
    str: base URL if provided, None otherwise.
    
    """
    try:
        if '--base-url' in sys.argv or '-u' in sys.argv:
            return sys.argv[sys.argv.index('--base-url') + 1]
    except Exception as e:
        logger.error(f"Error in set_base_url at line {e.__traceback__.tb_lineno}: {e}")
        return None

def set_api_key():
    """
    Retrieve API key from command-line arguments.

    Returns:
    str: API key if provided, None otherwise.
    """
    try:
        if '--api_key' in sys.argv:
            return sys.argv[sys.argv.index('--api_key') + 1]
        elif '-a' in sys.argv:
            return sys.argv[sys.argv.index('-a') + 1]
        else:
            raise ValueError("API Key is missing")
    except ValueError as e:
        logger.error(f"Error in set_api_key at line {e.__traceback__.tb_lineno}: {e}")
        return None
    except IndexError:
        logger.error("Error: '--api_key' or '-a' flag provided without a value.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in set_api_key at line {e.__traceback__.tb_lineno}: {e}")
        return None

def set_model():
    """
    Set the model for the completion.

    Returns:
    str: model if provided, gpt-4o otherwise.
    
    """
    try:
        if '--model' in sys.argv or '-m' in sys.argv:
            return sys.argv[sys.argv.index('--model') + 1]
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None

async def get_completion(input_text, output_file, temperature, max_tokens, api_key, model, context = None):
    """
    Call the Langchain ChatOpenAI Completion API to generate the completion.

    Parameters:
    input_text (str): The input text to generate the completion.
    output_file (str): The output file to save the generated completion.
    temperature (str): The temperature for the completion.
    max_tokens (str): The maximum tokens for the completion.
    api_key (str): The OpenAI API key.
    model (str): The model for the completion.
    context (str): The context for the completion.
    
    Returns:
    str: The generated completion or None if an error occurs.

    """
    
    
    try:
        if api_key is None:
            raise ValueError("API Key is missing")
        # LangchainOpenAI is a class that inherits from OpenAI

        if input_text is None:
            raise ValueError("Input text is missing")

        # Debugging the input parameters
        logger.info(f"Model: {model}")
        logger.info(f"Temperature: {temperature}")
        logger.info(f"Max Tokens: {max_tokens}")
        logger.info(f"Input Text: {input_text}")
        logger.info(f"Cotext: {context}")

        response = LangChainOpenAI(
            base_url = set_base_url(),
            api_key = api_key,
            model = model if model else "gpt-4o",
            temperature = temperature if temperature else 0.5,
            max_tokens = max_tokens if max_tokens else 100,
            max_retries=2,
        )

        message = [
            (
                "system",
                f"You are a professional analyst who is working on a different and you will use {context} as context and then provide answer based on user question.",
            ),
            (
                "human", f"{input_text}"
            )
        ]

        # async for chunk in response.astream(input_text):
        answer = []
        for chunk in response.stream(message):
            # AIMessageChunk is an object that contains the content of the message
            # using '.' to access the content of the message not ['content']
            logger.info(chunk.content, end="", flush=True)
            answer.append(chunk.content)
            

        """ 
        # This is the original code for OpenAI API
        response = client.chat.completions.create(
            model = model if model else "gpt-4o", # if user does not provide model, use gpt-4o
            messages=[
                {"role": "user", "content": input_text}
            ],
            stream = True,
            temperature = temperature if temperature else 0.5,
            max_tokens = max_tokens if max_tokens else 100,
        )
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                logger.info(chunk.choices[0].delta.content, end="")
        """
        
        logger.info("\n\nCompletion generated successfully.")
        completed_answer = "".join(answer)
        if output_file:
        # Write to the specified output file
            write_to_file(output_file, completed_answer)
        else:
            # Define the default file name
            default_file = f"completion_{datetime.now(TIME_ZONE).strftime('%Y-%m-%d')}.txt" # Set this as America/Toronto timezone
            write_to_file(default_file, completed_answer)

        return completed_answer
    
    except Exception as e:
        logger.error(f"Error in get_completion at line {e.__traceback__.tb_lineno}: {e}")
        return None

## Main function to run the tool
async def main():
    # Check for file arguments
    context = None

    # Check if argv[1] is provided and if it is a file we read the context from the file 
    # The context can be a JSON file or a text file
    # then using context with LLM Prompt to generate the completion
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            if file_path.endswith(".json"):
                logger.info(f"Reading context from JSON file: {file_path}")
                with open(file_path, "r") as f:
                    context = json.load(f)
                    context = json.dumps(context, indent=4) # using indent 4 for pretty logger.info
            else:
                logger.info(f"Reading context from text file: {file_path}")
                with open(file_path, "r") as f:
                    context = f.read()
        else:
            logger.error(f"File not found: {file_path}")
            context = None

    # Check if the version flag is present
    version = get_version()
    if version:
        logger.info(f"{TOOL_NAME} {version}")
        return  # Exit the script after logger.infoing the version
    
    # Check if the help flag is present
    help = get_help()
    if help:
        logger.info(help)
        return

    # Check if the models flag is present
    get_models_from_open_ai = get_available_models()
    if get_models_from_open_ai:
            logger.info("Available models from OpenAI:")
            pprint.pprint(get_models_from_open_ai)
            return

    # Get the API key from the command-line arguments  --api_key or -a
    api_key = set_api_key()
    if not api_key:
        logger.error("API Key is missing. Please provide it using '--api_key' or '-a'.")
        return
    

    # Get the input text from the command-line arguments --input_text or -i
    input_text = get_input()
    if not input_text:
        logger.error("Input text is missing. Please provide it using '--input_text' or '-i'.")
        return
    

    completion = await get_completion(
        input_text = input_text,
        output_file = get_output(),
        temperature = set_temperature(),
        max_tokens = set_max_tokens(),
        api_key = api_key,
        model = set_model(),
        context = context
        )
    
    if completion:
        logger.info(f"\n\nCompletion generated successfully:\n\n")
    

if __name__ == '__main__':
    # Need to using asyncio.run() to run the async function
    # We will using async for stream of Langchain for future development
    # with API request Response as streamingResponse.
    asyncio.run(main())