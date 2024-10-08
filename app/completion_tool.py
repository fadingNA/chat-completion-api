# chat-completion-api/app/completion_tool.py
import sys
import os
import asyncio
from utils import *  # noqa F403
from imports import *  # noqa F403
from config import TOOL_NAME, VERSION, OPEN_AI_MODELS_URL, config

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logger
logger = setup_logging()

# Set the timezone
TIME_ZONE = pytz.timezone('America/Toronto')

print("Hello from completion_tool.py")
print("config: ", config)

class Minal:
    def __init__(self) -> None:
        self.input_text = None
        self.file_context = None
        self.output_file = None
        self.api_key = None
        self.temperature = 0.5
        self.max_tokens = 100
        self.model = "gpt-4"
        self.provider = "OpenAI API"
        self.streaming = False
        self.token_usage = False

    def parse_arguments(self):
        """Parse the command-line arguments, with fallback to config file."""
        if len(sys.argv) == 1:
            print(self.display_help())
            sys.exit(0)
        elif len(sys.argv) > 1:
            file_path = sys.argv[1]
            if os.path.exists(file_path):
                self.file_input = self._cleanup_text_on_file(file_path)
            else:
                logger.error(f"File not found: {file_path}")
                sys.exit(1)
        self.input_text = self.get_cli_argument(['--input_text', '-i'], config.get('input_text', "Default input text"))
        self.output_file = self.get_cli_argument(['--output', '-o'], config.get('output_file'))
        self.api_key = self.get_cli_argument(['--api_key', '-a'], config.get('api_key'))
        self.temperature = float(self.get_cli_argument(['--temperature', '-t'], config.get('temperature', 0.5)))
        self.max_tokens = int(self.get_cli_argument('--max_tokens', config.get('max_tokens', 100)))
        self.model = self.get_cli_argument(['--model', '-m'], config.get('model', "gpt-4"))
        self.provider = self.get_cli_argument('--provider', config.get('provider', "OpenAI API"))
        self.streaming = self.get_cli_argument(['--stream', '-s'], config.get('streaming', False))
        self.token_usage = self.get_cli_argument(['--token_usage'], config.get('token_usage', False))

        if '--version' in sys.argv or '-v' in sys.argv:
            print(f"{TOOL_NAME} version: {VERSION}")
            sys.exit(0)

        if '--help' in sys.argv or '-h' in sys.argv or '--howto' in sys.argv:
            print(self.display_help())
            sys.exit(0)

    @staticmethod
    def get_cli_argument(flags, default=None):
        """Helper function to retrieve CLI arguments, falling back to default."""
        if isinstance(flags, list):
            for flag in flags:
                if flag in sys.argv:
                    try:
                        return sys.argv[sys.argv.index(flag) + 1]
                    except IndexError:
                        logger.error(f"Expected argument after {flag}")
                        sys.exit(1)
        elif flags in sys.argv:
            try:
                return sys.argv[sys.argv.index(flags) + 1]
            except IndexError:
                logger.error(f"Expected argument after {flags}")
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
        
    def _cleanup_text_on_file(self, file_path):
        """
        Read the file and escape any curly braces in the content.
        Args:
        file_path (str): Path to the file to be processed.
        
        Returns:
        str: The cleaned-up content with escaped curly braces or None if the file could not be processed.
        """
        if file_path and os.path.exists(file_path):
            if file_path.endswith('.json') or file_path.endswith('.txt'):
                context = get_file_content(file_path)
                # Escape curly braces
                context = str(context).replace('{', '{{').replace('}', '}}')
            elif file_path.endswith('.pdf'):
                docs = load_pdf(file_path)
                context = format_docs(docs) if docs else None
            elif file_path.endswith('.docx'):
                docs = read_file_docx(file_path)
                context = format_docs(docs) if docs else None
            else:
                context = get_file_content(file_path)
                # Escape curly braces
                context = str(context).replace('{', '{{').replace('}', '}}')
            return context
        else:
            logger.error(f"File not found: {file_path}")
            return None
    
    def get_prompt_template(self):
        """Build the prompt template for LangChain."""
        # Log the inputs for debugging
        logger.info(f"file_input: {self.file_input}")
        logger.info(f"input_text: {self.input_text}")
        try:
            if not self.file_input or not isinstance(self.file_input, str):
                logger.error("file_input is invalid or empty.")
                return None

            if not self.input_text or not isinstance(self.input_text, str):
                logger.error("input_text is invalid or empty.")
                return None

            message = [
                ("system", 
                f"""
                You are a professional analyst working with different contexts.
                Use the provided context: {self.file_input} and respond based on the user's question.
                """),
                ("human", f"{self.input_text}")
            ]

            # Convert to the proper format for ChatPromptTemplate
            prompt = ChatPromptTemplate.from_messages(message)
            return prompt

        except Exception as e:
            logger.error(f"Error building prompt template: {e}")
            return None

    def generate_completion(self):
        """Generate completion using Langchain API (GROQ , OpenAI API)."""
        try:
            if not self.api_key:
                raise ValueError("API Key is required to generate completion.")
            logger.info("Generating completion using OpenAI API.")
            
            prompt = self.get_prompt_template()
            if not prompt:
                logger.error("Failed to generate prompt.")
                return
            response = self.get_response()

            if not response:
                logger.error("Failed to get response from the provider.")
                return
            
            try:
                chain_llm = prompt | response 
                
                if self.streaming:
                    _response = asyncio.run(self.handle_streaming(chain_llm))
                else:
                    _response = chain_llm.invoke({"input_text": self.input_text})
            except Exception as e:
                logger.error(f"Error generating completion: {e}")
                return

            print(response)
            if response:
                print(_response.content)
                logger.info("Completion generated successfully.")
                if self.output_file:
                    self._save_output(self.output_file, _response)
            else:
                logger.error("Failed to generate completion.")
        except KeyError as e:
            logger.error(f"Failed to generate completion: {e}")
            logger.error("Please check the input text and try again.")
    
    def get_response(self):
        """Get response from OpenAI API."""

        logger.info(f"Using provider: {self.provider}")
        logger.info(f"Using model: {self.model}")

        if self.provider == "OpenAI API":
            return LangChainOpenAI(
                base_url=self.get_cli_argument('--base_url'),
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                model=self.model
            )
        elif self.provider == "GROQ":
            return ChatGroq(
                base_url=self.get_cli_argument('--base_url'),
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                model=self.model
            )
        
        return None
    
    async def handle_streaming(self, response):
        """Handle streaming completion output."""
        try:
            async for chunk in response.stream({"input_text": self.input_text}):
                print(chunk.content, end="", flush=True)  # Stream the output in real-time
                if self.output_file:
                    # Save chunk to file incrementally
                    self.append_output_to_file(self.output_file, chunk.content)

                if self.token_usage:
                    completion_tokens, prompt_tokens = self.extract_chunk_token_usage(chunk, self.provider)
                    logger.info(f"Tokens used: completion={completion_tokens}, prompt={prompt_tokens}")
        except Exception as e:
            logger.error(f"Error during streaming: {e}")

    def extract_chunk_token_usage(self, chunk, provider):
        completion_tokens = prompt_tokens = 0

        if provider == "OpenAI API":
            usage = getattr(chunk, 'usage_metadata', None)
            if usage:
                completion_tokens = usage.get('completion_tokens', 0)
                prompt_tokens = usage.get('prompt_tokens', 0)
        else:
            usage_metadata = getattr(chunk, 'usage_metadata', None)
            if usage_metadata:
                completion_tokens = usage_metadata.get('output_tokens', 0)
        return completion_tokens, prompt_tokens
    
    @staticmethod
    def save_output_to_file(output_file, content):
        """Saves the full output to a file."""
        write_to_file(output_file, content)  
        logger.info(f"Output saved to {output_file}")

    @staticmethod
    def append_output_to_file(output_file, content):
        """Append the streamed output to a file."""
        write_to_file(output_file, content) 
    
    def run(self):
        """Main execution function."""
        self.parse_arguments()
        self.generate_completion()
            
        