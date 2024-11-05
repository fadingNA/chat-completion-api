"""
Utility module with common functions and configurations.
"""

import sys
import os
import json
import traceback
from datetime import datetime
import logging
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

# Define a directory for example usage
EXAMPLE_FOLDER = "/examples"


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
    file_path = os.path.join(EXAMPLE_FOLDER, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(text_with_timestamp)
    else:
        with open(file_path, "a") as f:
            f.write(text_with_timestamp)


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
                return json.dumps(json_content, indent=4)
        else:
            logger.info(f"Reading context from text file: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        logger.error(f"Error reading file {file_path} at line {tb[-1].lineno}: {e}")
        return None


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def load_pdf(pdf_path):
    try:
        loader = UnstructuredPDFLoader(pdf_path, mode="elements", strategy="fast")
        docs = loader.load()
        return docs
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        logger.error(f"Error reading file {pdf_path} at line {tb[-1].lineno}: {e}")
        return None


def read_file_docx(docx):
    try:
        if docx.endswith(".docx"):
            logger.info(f"Reading context from DOCX file: {docx}")
            loader = UnstructuredWordDocumentLoader(
                docx, mode="elements", strategy="fast"
            )
            docs = loader.load()
            return docs
        else:
            logger.warning(f"Unsupported file format: {docx}")
            return None
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        logger.error(f"Error reading file {docx} at line {tb[-1].lineno}: {e}")
        return None


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

    new_messages = [
        (
            {"type": "human", "content": message.content}
            if isinstance(message, HumanMessage)
            else {
                "type": "ai",
                "content": message.content,
                "metadata": message.response_metadata,
            }
        )
        for message in chat_history.messages
    ]

    combined_messages = []

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                combined_messages = json.load(file)
            except json.JSONDecodeError:
                pass

    combined_messages.extend(new_messages)

    with open(file_path, "w") as file:
        json.dump(combined_messages, file)

    logger.info(f"Chat history appended for session {session_id}.")


def select_provider():
    print("Please select Available Provider")
    print("1. Grok API")
    print("2. OpenAI API")

    choice = input("Enter the number of your choice: ")

    providers = {"1": "Grok API", "2": "OpenAI API"}

    provider = providers.get(choice)

    if provider:
        logger.info(f"You selected {provider}")
    else:
        logger.error("Invalid Choice, please retry.")
        sys.exit(0)
    return provider


def extract_chunk_token_usage(chunk, provider):
    completion_tokens = prompt_tokens = 0

    if provider == "OpenAI API":
        usage = getattr(chunk, "usage_metadata", None)
        if usage:
            completion_tokens = usage.get("completion_tokens", 0)
            prompt_tokens = usage.get("prompt_tokens", 0)
    else:
        usage_metadata = getattr(chunk, "usage_metadata", None)
        if usage_metadata:
            completion_tokens = usage_metadata.get("output_tokens", 0)
            prompt_tokens = usage_metadata.get("input_tokens", 0)

    return completion_tokens, prompt_tokens
