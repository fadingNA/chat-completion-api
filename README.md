# chat-minal

The chat-minal is a command-line tool work on terminal that makes it easy to interact with the OpenAI Chat Completion API using Langchain. This tool allows you to send text prompts and receive AI-generated responses directly from the command line. You can customize the model, set parameters like temperature and token limits, and save the output to a file. 

References [Langchain Document](https://api.python.langchain.com/en/latest/llms/langchain_openai.llms.base.OpenAI.html)

## Demo walkthrough the chatminal

Demo Link [chat-minal tutorial](https://github.com/fadingNA/chat-completion-api)

## Example of Usage

<img src="assets/code_reviews.png" alt="Chat Completion Tool Screenshot" width="500" height="300">
<img src="assets/convert_json_tocsv.png" alt="Chat Completion Tool Screenshot" width="500" height="300">
<img src="assets/generate_markdown.png" alt="Chat Completion Tool Screenshot" width="500" height="300">
<img src="assets/summarize_text.png" alt="Chat Completion Tool Screenshot" width="500" height="300">



## Table of Contributors

| Name          | Blog Post (URL)                  | GitHub Repo (URL)                       | Language    |
|---------------|---------------------------------|-----------------------------------------|-------------|
| Nonthachai Plodthong    | [Blog Post](https://dev.to/fadingna/open-source-development-187j) | [GitHub Repo](https://github.com/fadingNA/chat-completion-api) | Python + SSH |

## Overview

This tool allows you to interact with the ChatOpenAPI from Langchain via a command-line interface (CLI). You can provide input text, specify a model, and configure other parameters to generate chat completions.

Langchain is a Python or Javascript library that provide a flexibility to interact with OpenAI API. It allows you to generate completions for various tasks, such as chat, code, and text generation. You can use Langchain to build AI-powered applications, automate tasks, and enhance your projects with AI capabilities.

- Embedding: Embedding is a process of converting text into a numerical representation. It is a crucial step in natural language processing (NLP) tasks, such as text classification, sentiment analysis, and named entity recognition. Embeddings capture the semantic meaning of words and sentences, enabling machine learning models to understand and process text data.

- Vectorization: Vectorization is a process of converting text data into a numerical representation. It is a fundamental step in natural language processing (NLP) tasks, such as text classification, sentiment analysis, and named entity recognition. Vectorization transforms text data into a format that machine learning models can process and analyze.

- RAG: Retrieval-Augmented Generation (RAG) is a model architecture that combines retrieval and generation to improve the quality of text generation tasks. RAG leverages a retriever to retrieve relevant information from a large corpus of text and a generator to generate responses based on the retrieved information. This approach enables the model to generate more accurate and contextually relevant responses.


## Features

- Easy-to-use CLI for the ChatOpenAI Completion API from Langchain
- Supports various models, temperature settings, and maximum token limits
- Outputs to a specified file or a default file
- Includes error handling and logging
- Streaming Response
- Selecting Models

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/fadingNA/chat-completion-api.git
   cd chat-completion-api
   pip install -r requirements.txt # if you are using pip3 change pip to pip3 instead.
   ```

## Usage
  ```bash
  python3 play.py ../examples/sample2.json --api_key sk_xxx \
  # using 2 argv[0] and argv[1] for run file and source file
   -i "Tell me about directional derivatives" \ # input text
   --temperature 0.7 \
   --max_tokens 150 \
   --model gpt-4 \ # gpt-4o or gpt-4 
   --output_file output.txt \
   
  ```


## Options

- `-h, --help, --howto`: Show the help message.
- `-v, --version`: Show the version of the tool.
- `--input_text, -i`: Input text to generate completion.
- `--output, -o`: Output file to save the generated completion.
- `--temperature, -t`: Temperature for the completion.
- `--max_tokens`: Maximum tokens for the completion.
- `--api_key, -a`: OpenAI API Key.
- `--model, -m`: Model for the completion.

## Functions

- `get_version()`: Get the version of the tool.
- `get_help()`: Get the help message.
- `get_input()`: Get the input text from command line argument.
- `get_output()`: Get the output file path from command line argument.
- `get_available_models()`: Retrieve the list of available models from OpenAI.
- `set_temperature()`: Set the temperature for the completion.
- `set_max_tokens()`: Set the maximum tokens for the completion.
- `set_api_key()`: Retrieve the API key from command line argument.
- `set_model()`: Retrieve the model from command line argument.
- `get_source()`: Get the source file path from command line argument.
- `get_completion()`: Get the chat completion from OpenAI API.

## Requirements

- Python 3.7+
- An OpenAI API key


# License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/fadingNA/chat-completion-api/blob/main/LICENSE) file for details.
