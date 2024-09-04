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


# You might add common utility functions here as well
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    return logging.getLogger(__name__)