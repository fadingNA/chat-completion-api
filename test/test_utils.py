from calendar import c
import traceback
import unittest
import os
import json
from unittest.mock import patch, MagicMock, mock_open
from app.utils import save_chat_history, extract_chunk_token_usage, get_file_content
from app.imports import HumanMessage, BaseChatMessageHistory


class MockChatHistory:
    """Mock chat history to simulate the expected interface with a messages attribute."""

    def __init__(self, messages):
        self.messages = messages


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_data = "This is a test data."
        self.test_session_id = "test_session_id"
        self.file_name = f"{self.test_session_id}.json"
        self.test_file = f"test/{self.file_name}"

    def text_extract_chunk_token_usage(self):
        chunk = MagicMock()
        chunk.usage_metadata = {"completion_tokens": 99, "prompt_tokens": 88}
        completion_tokens, prompt_tokens = extract_chunk_token_usage(
            chunk, "OpenAI API"
        )
        self.assertEqual(completion_tokens, 99)
        self.assertEqual(prompt_tokens, 88)

    def test_extract_chunk_token_usage_grok(self):
        chunk = MagicMock()
        chunk.usage_metadata = {
            "output_tokens": 80,
            "input_tokens": 40,
        }
        completion_tokens, prompt_tokens = extract_chunk_token_usage(chunk, "Grok API")
        self.assertEqual(completion_tokens, 80)
        self.assertEqual(prompt_tokens, 40)

    def test_save_chat_history(self):
        human_message = HumanMessage(content="Hello")
        ai_message = {
            "type": "ai",
            "content": "AI response",
            "metadata": {"info": "metadata"},
        }
        chat_history = MockChatHistory([human_message, ai_message])
        save_chat_history(self.test_session_id, chat_history)
        with open(self.test_file, "r") as file:
            written_data = json.load(file)
        expected_data = [
            {"type": "human", "content": "Hello"},
            {"type": "ai", "content": "AI response", "metadata": {"info": "metadata"}},
        ]
        self.assertEqual(written_data, expected_data)

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("app.utils.logger")
    def test_get_file_content_json_file(self, mock_logger, mock_file):
        # Test reading a JSON file
        file_path = "test_file.json"
        expected_content = json.dumps({"key": "value"}, indent=4)

        result = get_file_content(file_path)
        mock_file.assert_called_once_with(file_path, "r")
        self.assertEqual(result, expected_content)
        mock_logger.info.assert_called_with(
            f"Reading context from JSON file: {file_path}"
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="This is a text file content.",
    )
    @patch("app.utils.logger")
    def test_get_file_content_text_file(self, mock_logger, mock_file):
        # Test reading a text file
        file_path = "test_file.txt"
        expected_content = "This is a text file content."

        result = get_file_content(file_path)
        mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")
        self.assertEqual(result, expected_content)
        mock_logger.info.assert_called_with(
            f"Reading context from text file: {file_path}"
        )


if __name__ == "__main__":
    unittest.main()
