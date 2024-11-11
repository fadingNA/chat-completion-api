from calendar import c
import unittest
import os
import json
from unittest.mock import patch, MagicMock, mock_open
from app.utils import (
    save_chat_history,
    extract_chunk_token_usage,
)
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


if __name__ == "__main__":
    unittest.main()
