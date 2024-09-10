from utils import *
from imports import *
from config import *
import sys
import os
import json

# NEED TO ADD THIS LINE TO IMPORT THE CONFIG FILE
# This is needed to import the config file from the parent directory
# THIS TELLS PYTHON TO LOOK FOR THE CONFIG FILE IN THE PARENT DIRECTORY
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Setup logger
logger = setup_logging()

# Set the timezone
TIME_ZONE = pytz.timezone('America/Toronto')

# ADDITIONAL FUNCTIONS TO GET THE VERSION AND HELP


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
        return f"""
            {TOOL_NAME} - A simple CLI tool to do Chat Completion from OpenAI

            Usage:
            {TOOL_NAME} [options]

            Options:
            -h, --help, --howto     Show this help message
            -v, --version           Show the version of the tool
            --input_text, -i                 Input text to generate completion
            --output, -o                Output file to save the generated completion
            --temperature, -t           Temperature for the completion
            --max_tokens            Maximum tokens for the completion
            --api_key, -a               OpenAI API Key
            --model, -m                 Model for the completion
            """

    except Exception as e:
        logger.error(f"Error in get_help at line {e.__traceback__.tb_lineno}: {e}")
        return None


def get_input():
    try:
        # Check if '--input_text' or '-i' is in the command-line arguments
        return sys.argv[sys.argv.index('--input_text') + 1] if '--input_text' in sys.argv else sys.argv[sys.argv.index('-i') + 1]
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


def get_available_models(api_key=None):
    """
    Retrieve the list of available models from OpenAI.

    Returns:
    dict: JSON response from the API or None if an error occurs.
    """
    try:
        if '--models' in sys.argv:
            api_key = api_key or sys.argv[sys.argv.index(
                '--api_key') + 1] if '--api_key' in sys.argv else sys.argv[sys.argv.index('-a') + 1]
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

# ADDITIONAL FUNCTIONS TO Set the temperature, max_tokens, api_key, and model


async def get_completion(input_text, output_file, base_url, temperature, max_tokens, api_key, model, context=None , output=None):
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
        logger.info(f"Model: {model if model is not None else 'The model without provide on the command line we will use gpt-4o'}")
        logger.info(f"Temperature: {temperature if temperature else f'{0.5} (default)'}")
        logger.info(f"Max Tokens: {max_tokens if max_tokens else f'{100} (default)'}")
        logger.info(f"Input Text: {input_text if input_text else 'No input text provided'}")
        logger.info(f"Cotext: {context}")

        response = LangChainOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model if model else "gpt-4o",
            temperature=temperature if temperature else 0.5,
            max_tokens=max_tokens if max_tokens else 100,
            max_retries=2,
        )

        # Get the session history
        #chat_history.add_user_mesaage(input_text)

        # Create the message template with placeholders
        message = [
            ("system", f"You are a professional analyst working with different contexts. Use the provided context: {context} and respond based on the user question."),
            MessagesPlaceholder(variable_name="history"),
            ("human", f"{input_text}")
        ]
        
        prompt = ChatPromptTemplate.from_messages(
            message
        )
        chat_history = get_session_history("1")
        

        runnable = prompt | response

        # Manage message history with RunnableWithMessageHistory
        with_message_history = RunnableWithMessageHistory(
            runnable,
            get_session_history,
        )

        # async for chunk in response.astream(input_text):
        # Execute the runnable and stream the response
        answer = []
        print("*" * 100)
        for chunk in with_message_history.stream([HumanMessage(content=input_text)], config={"configurable": {"session_id": "1"}}):
            print(chunk.content, end="", flush=True)
            answer.append(chunk.content)
        print("\n" + "*" * 100)

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
        chat_history = get_session_history("1")

        print("Chat History: ", chat_history.messages)

        save_chat_history(session_id="test1", chat_history=chat_history)

        if output is True:
            if output_file:
                # Write to the specified output file
                write_to_file(output_file, completed_answer)
            else:
                # Define the default file name
                default_file = f"completion_{datetime.now(TIME_ZONE).strftime('%Y-%m-%d')}.txt"  # Set this as America/Toronto timezone
                write_to_file(default_file, completed_answer)
        else:
            logger.info(f"Completion: Done without saving to file")

        return True

    except Exception as e:
        logger.error(f"Error in get_completion at line {e.__traceback__.tb_lineno}: {e}")
        return False

# Main function to run the tool


async def main():
    # Check for file arguments

    if len(sys.argv) == 1:
        print(f"Please provide a file as the first argument. follwing by the command line arguments you can use -h or --help to see the help message")
        return
    context = None

    
    # Check if argv[1] is provided and if it is a file we read the context from the file
    # The context can be a JSON file or a text file
    # then using context with LLM Prompt to generate the completion

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        context = get_file_content(sys.argv[1])
        # logger.info(f"Context: {context}")

    arguments = generic_set_argv(
        '--version', '-v', '--help', '-h', '--howto',
        '--input_text', '-i', '--output', '-o',
        '--temperature', '-t', '--max_tokens',
        '--api_key', '-a', '--model', '-m',
        '--base-url', '-u'
    )

    # put', '-o', '--temperature', '-t', '--max_tokens', '--api_key', '-a', '--model', '-m', '--base-url', '-u'
    # Check if the version flag is present
    # Parse command-line arguments

    if arguments.get('--models'):
        api_key = arguments.get('--api_key') or arguments.get('-a')
        if api_key is None or api_key == "":
            logger.error("API Key is missing")
            return
        get_models_from_open_ai = get_available_models(api_key=api_key)
        if get_models_from_open_ai:
            logger.info("Available models from OpenAI:")
            pprint.pprint(get_models_from_open_ai)
            return

    # Check if the version flag is present
    if arguments.get('--version') or arguments.get('-v'):
        print(f"{TOOL_NAME} version: {VERSION}")
        logger.info(f"{TOOL_NAME} version: {VERSION}")
        return

    # Check if the help flag is present
    if arguments.get('--help') or arguments.get('-h') or arguments.get('--howto'):
        help_message = get_help()
        print(help_message)
        # logger.info(help_message)
        return

    # Check for input text
    input_text = arguments.get('--input_text') or arguments.get('-i')
    if not input_text:
        input_text = get_input()

    is_output = arguments.get('--output') or arguments.get('-o')
    if not is_output:
        logger.info("No output file specified. The result will be displayed on the console.")

    # Call get_completion asynchronously
    completion = await get_completion(
        input_text=input_text,
        output_file=arguments.get('--output') or arguments.get('-o'),
        base_url=arguments.get('--base-url') or arguments.get('-u'),
        temperature=arguments.get('--temperature') or arguments.get('-t'),
        max_tokens=arguments.get('--max_tokens'),
        api_key=arguments.get('--api_key') or arguments.get('-a'),
        # if model is not provided, use gpt-4o
        model=arguments.get('--model') or arguments.get('-m'),
        context=context,
        output=True
    )

    if completion:
        logger.info("Completion generated successfully.")
        return


if __name__ == '__main__':
    # Need to using asyncio.run() to run the async function
    # We will using async for stream of Langchain for future development
    # with API request Response as streamingResponse.
    asyncio.run(main())
