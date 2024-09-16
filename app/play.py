from zmq import has
from utils import *  # noqa F403
from imports import *  # noqa F403
from config import TOOL_NAME, VERSION, OPEN_AI_MODELS_URL, ACCEPTED_FILE_EXTENSIONS
import sys
import os
from typing import Optional
from pprint import pprint


# NEED TO ADD THIS LINE TO IMPORT THE CONFIG FILE
# This is needed to import the config file from the parent directory
# THIS TELLS PYTHON TO LOOK FOR THE CONFIG FILE IN THE PARENT DIRECTORY
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Setup logger
logger = setup_logging()

# Set the timezone
TIME_ZONE = pytz.timezone('America/Toronto')


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
        logger.error(
            f"Error in get_version at  {e}")
        return None


def get_help():
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
    return sys.argv[sys.argv.index('--input_text') + 1] if '--input_text' in sys.argv else None


def get_output():
    """
    Get the output file from the command line arguments.
    Returns:
    str: The output file or None if not provided.
    """
    return sys.argv[sys.argv.index('--output') + 1] if '--output' in sys.argv else None


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
                logger.error(
                    f"Failed to retrieve models: {response.status_code} - {response.text}")
                return None

    except Exception as e:
        logger.error(
            f"Error in get_available_models at line  {e}")
        return None

# ADDITIONAL FUNCTIONS TO Set the temperature, max_tokens, api_key, and model


async def get_completion(input_text, output_file, base_url, temperature, max_tokens, api_key, model,
                         context=None, output=None, selected_choice=None, target_language="Chinese", token_usage=False):
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
    output (str): The output for the completion.
    selected_choice (str): The selected choice to perform the task.
    target_language (str): The target language for the translation.

    Returns:
    str: The generated completion or None if an error occurs.

    """

    try:
        if api_key is None:
            raise ValueError("API Key is missing")

        if input_text is None:
            print("We will set the input text to the default prompt as translation")

        logger.info("""Model: %s",
                    model if model is not None else
                        "The model without provide on the command line we will use gpt 3.5 turbo instead.
                    """)
        logger.info("Temperature: %s", temperature if temperature else "0.5 (default)")
        logger.info("Max Tokens: %s", max_tokens if max_tokens else "100 (default)")
        logger.info("Input Text: %s", input_text if input_text else "No input text provided")
        # Display the first 30 characters of the context
        logger.info(f"Cotext: {context}")
        logger.info(
            f"Output File: {output_file if output_file else 'No output file provided'}")
        logger.info(
            f"Target Language: {target_language if target_language else 'No target language provided'}"
        )
        logger.info(f"selected_choice: {selected_choice}")
        logger.info(f"Token Usage: {token_usage}")
        response = ChatGroq(
            base_url=base_url,
            api_key=api_key,
            model=model if model else "llama-3.1-8b-instant",  # model=model if model else "gpt-3.5-turbo",
            temperature=temperature if temperature else 0.5,
            max_tokens=max_tokens if max_tokens else 100,
            max_retries=2,
            stop_sequences=["\n"],
        )

        # Get the session history
        if isinstance(input_text, str):
            input_text = input_text
        else:
            input_text = input_text.decode("utf-8")

        # Create the message template with placeholders based on the selected task
        if selected_choice == 'translate':
            message = [
                ("system",
                 f"You are a helpful assistant that translates {context}. to {target_language}"),
                # MessagesPlaceholder(variable_name="history"),
                ("human", f"{input_text}")
            ]
        else:
            message = [
                ("system",
                 f"""
                 You are a professional analyst working with different contexts.
                 Use the provided context: {context} and respond based on the user question.
                 """),
                # MessagesPlaceholder(variable_name="history"),
                ("human", f"{input_text}")
            ]

        prompt = ChatPromptTemplate.from_messages(message)

        # Create Runnable with message LLM | Prompt we can use "|" to combine the two objects
        runnable = prompt | response

        answer = []
        completion_token = None
        output_token = None
        total_token = None
        print("\n" + "*" * 100)
        for chunk in runnable.stream({"input_text": input_text}):
            print(chunk.content, end="", flush=True)
            answer.append(chunk.content)
            if token_usage and chunk.usage_metadata: # type: ignore
                completion_token = chunk.usage_metadata.get("input_tokens") # type: ignore
                output_token = chunk.usage_metadata.get("output_tokens") # type: ignore
                total_token = chunk.usage_metadata.get("total_tokens") # type: ignore


        # Check for the token_usage flag if it is present or not.
        # If present, retrieve the output and input tokens used for the completion.
        # Making two identical loops helps us prevent the IF checks in the loop if the token_usage flag is not used.
        if token_usage:
            for chunk in runnable.stream({"input_text": input_text}):
                print(chunk.content, end="", flush=True)
                answer.append(chunk.content)

                # Check for the attribute usage_metadata in the chunk.
                # Retrieve the output and input tokens if available.
                if chunk.usage_metadata: # type: ignore
                    # usage_metadata = {'output_tokens': number, 'input_tokens': number, 'total_tokens': number}
                    completion_tokens = chunk.usage_metadata.get('output_tokens') # type: ignore
                    prompt_tokens = chunk.usage_metadata.get('input_tokens') # type: ignore
        else:
            for chunk in runnable.stream({"input_text": input_text}):
                print(chunk.content, end="", flush=True)
                answer.append(chunk.content)
        print("\n" + "*" * 100)
        logger.error(f"Completion Token: {completion_token}")
        logger.error(f"Output Token: {output_token}")
        logger.error(f"Total Token: {total_token}")

        logger.info("\n\nCompletion generated successfully.")
        completed_answer = "".join(answer)
        chat_history = get_session_history("test1") # type: ignore

        save_chat_history(session_id="test2", chat_history=chat_history) # type: ignore
        logger.info(
            f"The answer is saved to the chat history. with session_id: {chat_history.session_id}")

        # Handle file output if specified
        if output_file:
            # Check if the user provided an extension, if not, append a timestamp and .txt extension
            if not any(output_file.endswith(ext) for ext in ACCEPTED_FILE_EXTENSIONS):
                file_to_write = f"{output_file}_{datetime.now(TIME_ZONE).strftime('%Y-%m-%d')}.txt"
            else:
                file_to_write = output_file

            write_to_file(file_to_write, completed_answer)
            logger.info(f"Completion saved to {file_to_write}")
        else:
            logger.info("Completion done without saving to file")

        if token_usage:
            logger.error(f"Tokens used for completion: {completion_tokens}")
            logger.error(f"Tokens used for prompt: {prompt_tokens}")

        return True

    except Exception as e:
        logger.error(
            f"Error in get_completion at line  {e}")
        return False


async def main():
    # Check for file arguments

    arguments = generic_set_argv(
        '--version', '-v', '--help', '-h', '--howto',
        '--input_text', '-i', '--output', '-o',
        '--temperature', '-t', '--max_tokens',
        '--api_key', '-a', '--model', '-m',
        '--base-url', '-u',
        '--models', '--select_choice', '-sc',
        '--target_language', '-tl','--token-usage'
        # '--voice', '-vc'
    )
    # Check if the version flag is present
    if arguments.get('--version') or arguments.get('-v'): # type: ignore
        print(f"{TOOL_NAME} version: {VERSION}")
        logger.info(f"{TOOL_NAME} version: {VERSION}")
        return

    # Check if the help flag is present
    if arguments.get('--help') or arguments.get('-h') or arguments.get('--howto'): # type: ignore
        help_message = get_help()
        logger.info(help_message)
        return

    if len(sys.argv) == 1:
        logger.info("""
              Please provide a file as the first argument. follwing by the command line arguments
              you can use -h or --help to see the help message \n
              or you can use the command line arguments directly without providing a file
              but with arguments --input_text or -i to provide the input text
              """)
        return

    context = None
    file_path: Optional[str] = None
    target_language: str = "Chinese"

    for arg in sys.argv[1:]:
        if os.path.exists(arg):  # Check if any argument is a valid file path
            file_path = arg
            break

    if file_path:
        # Determine the file type and load the content accordingly
        if file_path and not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        if file_path.endswith('.json') or file_path.endswith('.txt'):
            context = get_file_content(file_path)
            context = str(context).replace('{', '{{').replace('}', '}}')
        elif file_path.endswith('.pdf'):
            docs = load_pdf(file_path)
            context = format_docs(docs) if docs else None
        elif file_path.endswith('.docx'):
            docs = read_file_docx(file_path)
            context = format_docs(docs) if docs else None
        else:
            context = get_file_content(file_path)
            context = str(context).replace('{', '{{').replace('}', '}}')

    input_text = generic_set_argv('--input_text', '-i').get(
        '--input_text') or generic_set_argv('--input_text', '-i').get('-i')

    # Handling different scenarios based on input presence
    if not input_text and not context:
        logger.info("""
                    If no file is provided,
                    please provide the input text using --input_text or -i.
                    """)
    elif not context and input_text:
        logger.info("""
                    Generate anaswer based on the input text provided.
                    """)
    elif not input_text and context:
        logger.info("""
                    We will use a pre-prompt that you will select to perform the task for your file.
                    """)

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
        else:
            logger.error("Failed to retrieve models from OpenAI")
            return

    select_choices = arguments.get('--select_choice') or arguments.get('-sc')

    if not input_text and not select_choices:
        print("Please provide the choice to perform tasks of the tool")
        print("1. Translate English to Chinese")
        print("2. Translate Chinese to English")
        print("3. Translate English to French")
        select_choices_language_select = input(
            "Please see the above choices and provide the choice with just (1,2,3)").strip().lower()
        if not file_path:
            print("Please provide a file as the second argument after run script.")
            return

        if select_choices_language_select == '1':
            target_language = "Chinese"
            input_text = "Translate the provided text to Chinese"
        elif select_choices_language_select == '2':
            target_language = "English"
            input_text = "Translate the provided text to English"
        elif select_choices_language_select == '3':
            target_language = "French"
            input_text = "Translate the provided text to French"
        else:
            logger.warning(
                "Invalid choice. Please provide the choice with just (1 , 2 ,3 ,4)")
            return

        select_choices = "translate"

    try:
        completion = await get_completion(
            input_text=input_text if input_text else None,
            output_file=arguments.get('--output') or arguments.get('-o'),
            base_url=arguments.get('--base-url') or arguments.get('-u'),
            temperature=arguments.get('--temperature') or arguments.get('-t'),
            max_tokens=arguments.get('--max_tokens'),
            api_key=arguments.get('--api_key') or arguments.get('-a'),
            model=arguments.get('--model') or arguments.get('-m'),
            context=context,
            token_usage=arguments.get('--token-usage'), # type: ignore
            selected_choice=select_choices,
            target_language=target_language if not input_text else "Prompt defined",
        )

        if completion:
            logger.info("Completion generated successfully.")
        else:
            logger.error("Failed to generate completion.")

    except Exception as e:
        logger.error(f"Error in generating completion: {e}")
        print(f"Error in generating completion: {e}")


if __name__ == '__main__':
    # Need to using asyncio.run() to run the async function
    # We will using async for stream of Langchain for future development
    # with API request Response as streamingResponse.
    asyncio.run(main())
