"""
Module for importing all necessary modules and setting up logging.
"""

import sys  # noqa: F401
import logging
import asyncio  # noqa: F401
import os  # noqa: F401
import json  # noqa: F401
from datetime import datetime  # noqa: F401
import pprint  # noqa: F401
import requests  # noqa: F401
import pytz  # noqa: F401

from openai import OpenAI  # noqa: F401
from langchain_openai import ChatOpenAI as LangChainOpenAI  # noqa: F401

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # noqa: F401

from langchain_community.chat_message_histories import (  # noqa: F401
    ChatMessageHistory,
)
from langchain_community.document_loaders import (  # noqa: F401
    TextLoader,
    JSONLoader,
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_core.chat_history import BaseChatMessageHistory  # noqa: F401
from langchain_core.runnables.history import RunnableWithMessageHistory  # noqa: F401
from langchain_core.messages import HumanMessage  # noqa: F401

from langchain_groq import ChatGroq  # noqa: F401

# import speech_recognition as sr  # noqa: F401
# import pyttsx3

# engine = pyttsx3.init()


def setup_logging():
    """
    Setup logging for the application.

    Returns:
        logging.Logger: The logger object.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
    )
    return logging.getLogger(__name__)
