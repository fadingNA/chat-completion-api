# Chat Completion API

The Chat Completion API is a command-line tool that makes it easy to interact with the OpenAI Chat Completion API using Langchain. This tool allows you to send text prompts and receive AI-generated responses directly from the command line. You can customize the model, set parameters like temperature and token limits, and save the output to a file. 

References [Langchain Document](https://api.python.langchain.com/en/latest/llms/langchain_openai.llms.base.OpenAI.html)


## Table of Contributors

| Name          | Blog Post (URL)                  | GitHub Repo (URL)                       | Language    |
|---------------|---------------------------------|-----------------------------------------|-------------|
| Nonthachai Plodthong    | [Blog Post](https://dev.to/fadingna/open-source-development-187j) | [GitHub Repo](https://github.com/fadingNA/chat-completion-api/examples) | Python + SSH |

## Overview

This tool allows you to interact with the OpenAI Chat Completion API via a command-line interface (CLI). You can provide input text, specify a model, and configure other parameters to generate chat completions.

## Features

- Easy-to-use CLI for the OpenAI Chat Completion API
- Supports various models, temperature settings, and maximum token limits
- Outputs to a specified file or a default file
- Includes error handling and logging

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/fadingNA/chat-completion-api.git
   cd chat-completion-api
   pip install -r requirements.txt # if you are using pip3 change pip to pip3 instead.
   ```

## Usage
  ```bash
  python3 play.py --api_key sk_xxx \
   -i "Tell me about directional derivatives" \
   --temperature 0.7 \
   --max_tokens 150 \
   --model gpt-4 \ # gpt-4o or gpt-4
   --output_file output.txt 
  ```

# License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/fadingNA/chat-completion-api/blob/main/LICENSE) file for details.
