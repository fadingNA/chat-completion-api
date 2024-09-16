"""
Module for importing all necessary modules and setting up logging.
"""

import sys
import logging
import asyncio
import os
import json
from datetime import datetime
import pprint
import requests
import pytz


from openai import OpenAI
from langchain_openai import ChatOpenAI as LangChainOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import (
    TextLoader,
    JSONLoader,
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader
)
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_groq import ChatGroq
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()


# You might add common utility functions here as well
def setup_logging():
    """
    Setup logging for the application.

    Returns:
        logging.Logger: The logger object.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(message)s')
    return logging.getLogger(__name__)
