# chat-completion-api/app/completion_tool.py
import sys
import os
import asyncio
from utils import setup_logging
from imports import requests, pytz, LangChainOpenAI, ChatGroq
from config import TOOL_NAME, VERSION, OPEN_AI_MODELS_URL, ACCEPTED_FILE_EXTENSIONS

# Setup logger
logger = setup_logging()

# Set the timezone
TIME_ZONE = pytz.timezone('America/Toronto')

class Minal:
    def __init__(self) -> None:
        self.input_text = None
        self.output_file = None
        self.api_key = None
        self.temperature = 0.5
        self.max_tokens = 100
        self.model = "gpt-4"
        self.provider = "OpenAI API"

    def parse_arguments(self):
        """Parse the command-line arguments."""
        self.input_text = self.get_cli_argument('--input_text', default="Default input text")
        self.output_file = self.get_cli_argument('--output')
        self.api_key = self.get_cli_argument('--api_key')
        self.temperature = float(self.get_cli_argument('--temperature', default=0.5))
        self.max_tokens = int(self.get_cli_argument('--max_tokens', default=100))
        self.model = self.get_cli_argument('--model', default="gpt-4")
        self.provider = self.get_cli_argument('--provider', default="OpenAI API")

        if '--version' in sys.argv:
            print(f"{TOOL_NAME} version: {VERSION}")
            sys.exit(0)

        if '--help' in sys.argv or '-h' in sys.argv:
            print(self.display_help())
            sys.exit(0)
    
    @staticmethod
    def get_cli_argument(flag, default=None):
        """Helper function to retrieve CLI arguments."""
        if flag in sys.argv:
            try:
                return sys.argv[sys.argv.index(flag) + 1]
            except IndexError:
                logger.error(f"Expected argument after {flag}")
                sys.exit(1)
        return default
    
    @staticmethod
    def display_help():
        """Display help message."""
        return f"""
        {TOOL_NAME} - A simple CLI tool to do Chat Completion from OpenAI

        Usage:
        {TOOL_NAME} [options]

        Options:
        -h, --help, --howto      Show this help message
        -v, --version            Show the version of the tool
        --input_text, -i         Input text to generate completion
        --output, -o             Output file to save the generated completion
        --temperature, -t        Temperature for the completion
        --max_tokens             Maximum tokens for the completion
        --api_key, -a            OpenAI API Key
        --model, -m              Model for the completion
        --select_choice, -sc     Select the choice to perform the task
        --token-usage            Show the token usage for the completion

        Examples:
        1. python3 app/play.py ../<YOUR_FILE> --input_text "Translate the provided text to Chinese" -a YOUR_API_KEY
        2. python3 app/play.py -i "Tell me about directional derivative" -a YOUR_API_KEY --output
        """
    
    @staticmethod
    def get_available_models(api_key):
        """Retrieve available models from OpenAI."""
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(OPEN_AI_MODELS_URL, headers=headers)
            response.raise_for_status()  # Raise exception for bad responses
            logger.info("Available models retrieved successfully.")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve models: {e}")
            return None
        
    async def generate_completion(self):
        """Generate completion using Langchain API (GROQ , OpenAI API)."""
        try:
            if not self.api_key:
                raise ValueError("API Key is required to generate completion.")
            logger.info("Generating completion using OpenAI API.")

            response = await self.get_response()

            if response:
                logger.info("Completion generated successfully.")
                if self.output_file:
                    self._save_output(self.output_file, response)
            else:
                logger.error("Failed to generate completion.")
        except KeyError as e:
            logger.error(f"Failed to generate completion: {e}")
            logger.error("Please check the input text and try again.")
    
    async def get_response(self):
        """Get response from OpenAI API."""

        if self.provider == "OpenAI API":
            return LangChainOpenAI(
                base_url=self.get_cli_argument('--base_url'),
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                model=self.model
            ).invoke({"input_text": self.input_text})
        elif self.provider == "GROQ":
            return ChatGroq(
                base_url=self.get_cli_argument('--base_url'),
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                model=self.model
            ).invoke({"input_text": self.input_text})
        
        return None
    
    @staticmethod
    def save_output_to_file(output_file, content):
        """Saves the output to a file."""
        with open(output_file, "w") as file:
            file.write(content)
        logger.info(f"Output saved to {output_file}")

    def run(self):
        """Main execution function."""
        self.parse_arguments()
        asyncio.run(self.generate_completion())
            
        