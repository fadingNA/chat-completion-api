import sys
import logging
import asyncio 
import os
import json
import requests
from datetime import datetime
import pytz

from openai import OpenAI
from langchain_openai import ChatOpenAI as LangChainOpenAI
import pprint
#from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import TextLoader, JSONLoader, UnstructuredPDFLoader, UnstructuredWordDocumentLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory





# You might add common utility functions here as well
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    return logging.getLogger(__name__)