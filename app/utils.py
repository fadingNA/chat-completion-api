from imports import *
from config import *

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

    file_path = os.path.join(EXAMPLE_FOlDER, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file does not exist, create it and write data
        with open(file_path, "w") as f:
            f.write(text_with_timestamp)
    else:
        # If the file exists, append the data
        with open(file_path, "a") as f:
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
            # Check if the next argument is not a flag and there is a next argument
            if len(sys.argv) > index + 1 and not sys.argv[index + 1].startswith("-"):
                parsed_args[key] = sys.argv[index + 1]
            # Check if it's a flag like -v or -h, set to True
            elif key in ACCEPTED_HELP_VERION:
                parsed_args[key] = True
            else:
                parsed_args[key] = ""
        except ValueError:
            # Argument not found
            parsed_args[key] = None
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
            with open(file_path, "r", encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path} at line {e.__traceback__.tb_lineno}: {e}")
        return None
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def load_pdf(pdf_path):
    try:
        loader = UnstructuredPDFLoader(pdf_path, mode="elements", strategy="fast")
        docs = loader.load()
        return docs
    except Exception as e:
        logger.error(f"Error reading file {pdf_path} at line {e.__traceback__.tb_lineno}: {e}")
        return None

def read_file_docx(docx):
    try:
        if docx.endswith(".docx"):
            logger.info(f"Reading context from DOCX file: {docx}")
            loader = UnstructuredWordDocumentLoader(docx, mode="elements",  strategy="fast" )
            docs = loader.load()
            return docs
        else:
            logger.warning(f"Unsupported file format: {docx}")
            return None
    except Exception as e:
        logger.error(f"Error reading file {docx} at line {e.__traceback__.tb_lineno}: {e}")
        return None
# later on implement credentials we will add user_id for each conversation

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")
    


def save_chat_history(session_id: str, chat_history: BaseChatMessageHistory):
    """
    Save chat history to a JSON file by appending new messages.

    Args:
    session_id (str): The session ID for which to save the chat history.
    chat_history (BaseChatMessageHistory): The chat history to save.
    """
    file_path = f"{session_id}_history.json"

    # Convert chat history messages to a serializable format
    new_messages = [
        {"type": "human", "content": message.content} if isinstance(message, HumanMessage) else
        {"type": "ai", "content": message.content, "metadata": message.response_metadata}
        for message in chat_history.messages
    ]

    # Initialize an empty list to hold existing messages
    combined_messages = []

    # Read existing messages if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                combined_messages = json.load(file)  # Load existing messages
            except json.JSONDecodeError:
                pass  # In case of an empty or invalid JSON file, ignore the error

    # Append new messages to the existing ones
    combined_messages.extend(new_messages)

    # Save the combined messages back to the JSON file
    with open(file_path, "w") as file:
        json.dump(combined_messages, file)

    logger.info(f"Chat history appended for session {session_id}.")  # Debug print


