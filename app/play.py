import sys
import os

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

            print(f"Retrieving available models from OpenAI...")
            print(f"Your API Key: {api_key}")
            # Make a request to OpenAI API
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            response = requests.get(OPEN_AI_MODELS_URL, headers=headers)

            # Check for a successful request
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to retrieve models: {response.status_code} - {response.text}")
                return None

    except Exception as e:
        logger.error(f"Error in get_available_models at line {e.__traceback__.tb_lineno}: {e}")
        return None
    
## ADDITIONAL FUNCTIONS TO Set the temperature, max_tokens, api_key, and model
def set_temperature():
    try:
        if  '--temperature' in sys.argv or '-t' in sys.argv:
            return sys.argv[sys.argv.index('--temperature') + 1]
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None
    
def set_max_tokens():
    try:
        if '--max_tokens' in sys.argv:
            return sys.argv[sys.argv.index('--max_tokens') + 1]
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None
    
def set_base_url():
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
    try:
        if '--model' in sys.argv or '-m' in sys.argv:
            return sys.argv[sys.argv.index('--model') + 1]
    except Exception as e:
        logger.error(f"Error in get_input at line {e.__traceback__.tb_lineno}: {e}")
        return None


## Ollama API to get Completion

async def get_completion(input_text, output_file, temperature, max_tokens, api_key, model):
    try:
        if api_key is None:
            raise ValueError("API Key is missing")
        # LangchainOpenAI is a class that inherits from OpenAI

        # Debug
        print(f"API Key: {api_key}")
        print(f"Model: {model}")
        print(f"Temperature: {temperature}")
        print(f"Max Tokens: {max_tokens}")
        print(f"Input Text: {input_text}")

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
                "You are a helpful assistant with the general knowledge of a human mind. please provide at least 3 sentences of context to generate a completion.",
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
            print(chunk.content, end="", flush=True)
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
                print(chunk.choices[0].delta.content, end="")
        """
        
        print("\n\nCompletion generated successfully.")
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
    # Check if the version flag is present
    version = get_version()
    if version:
        print(f"{TOOL_NAME} {version}")
        return  # Exit the script after printing the version
    
    help = get_help()
    if help:
        print(help)
        return

    get_models_from_open_ai = get_available_models()
    if get_models_from_open_ai:
            print("Available models from OpenAI:")
            pprint.pprint(get_models_from_open_ai)
            return

    api_key = set_api_key()
    if not api_key:
        logger.error("API Key is missing. Please provide it using '--api_key' or '-a'.")
        return
    
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
        model = set_model()
        )

    if completion:
        print(f"Completion: {completion}")
    else:
        logger.error("Failed to generate completion.")
    

if __name__ == '__main__':
    # Need to using asyncio.run() to run the async function
    # We will using async for stream of Langchain for future development
    # with API request Response as streamingResponse.
    asyncio.run(main())