import unittest
import io
from unittest.mock import patch, MagicMock
from app.completion_tool import Minal
from app.config import TOOL_NAME, VERSION


"""
`patch` acts as a function decorator, class decorator or a context
manager. Inside the body of the function or with statement, the `target`
is patched with a `new` object. When the function/with statement exits
the patch is undone.
"""


@patch("sys.exit")
@patch("app.completion_tool.logger")
class TestMinal(unittest.TestCase):
    def setUp(self):
        self.minal = Minal()
        self.minal.api_key = "test-api-key"
        self.minal.input_text = "Teach me what is directional derivative."
        self.minal.file_input = None
        self.minal.streaming = False
        self.minal.token_usage = False
        self.minal.model = "gpt-4"

        # Create a mock response object
        self.mock_response = MagicMock()
        self.mock_prompt = MagicMock()
        self.mock_chain_llm = MagicMock()
        self.mock_invoke_return = MagicMock()
        self.mock_response.content = (
            "The directional derivative is a concept in calculus..."
        )
        self.mock_response.response_metadata = {
            "token_usage": {
                "completion_tokens": 86,
                "prompt_tokens": 48,
                "total_tokens": 134,
            },
            "model_name": "gpt-4-0613",
            "finish_reason": "stop",
        }
        self.mock_response.id = "mocked-id-12345"
        self.mock_response.usage_metadata = {
            "input_tokens": 48,
            "output_tokens": 86,
            "total_tokens": 134,
        }

    def test_only_file_argument(self, mock_logger, mock_exit):
        with patch("sys.argv", ["completion_tool.py", "test_file.txt"]):
            with patch("os.path.exists", return_value=True):
                self.minal.parse_arguments()
                self.assertEqual(self.minal.input_text, "Default input text")
                self.assertEqual(self.minal.temperature, 0.5)
                self.assertEqual(self.minal.max_tokens, 100)
                self.assertEqual(self.minal.model, "gpt-4")
                mock_exit.assert_not_called()

    def test_parse_arguments_with_valid_string_and_flag(self, mock_logger, mock_exit):
        with patch(
            "sys.argv",
            [
                "completion_tool.py",
                "test_file.txt",
                "--input_text",
                "Hello",
                "--stream",
            ],
        ):
            with patch("os.path.exists", return_value=True):
                self.minal.parse_arguments()
                self.assertEqual(self.minal.input_text, "Hello")
                self.assertTrue(self.minal.streaming)
                mock_exit.assert_not_called()

    def test_parse_arguments_with_missing_config(self, mock_logger, mock_exit):
        with patch.dict(
            "app.completion_tool.config", {"input_text": None, "temperature": None}
        ):
            with patch("sys.argv", ["completion_tool.py", "test_file.txt"]):
                # second patch is needed to avoid the error
                # mock object has no attribute 'info'
                with patch("os.path.exists", return_value=True):
                    self.minal.parse_arguments()
                    self.assertEqual(self.minal.input_text, None)
                    self.assertEqual(self.minal.temperature, 0.5)

    def test_parse_arguments_with_invalid_file(self, mock_logger, mock_exit):
        with patch("sys.argv", ["completion_tool.py", "test_file.txt"]):
            with patch("os.path.exists", return_value=False):
                self.minal.parse_arguments()
                mock_exit.assert_called_once()

    def test_valid_temperature_argument(self, mock_logger, mock_exit):
        with patch(
            "sys.argv", ["completion_tool.py", "test_file.txt", "--temperature", "0.7"]
        ):
            with patch("os.path.exists", return_value=True):
                self.minal.parse_arguments()
                self.assertEqual(self.minal.temperature, 0.7)

    def test_invalid_temperature_argument(self, mock_logger, mock_exit):
        with patch(
            "sys.argv",
            ["completion_tool.py", "test_file.txt", "--temperature", "invalid"],
        ):
            with patch("os.path.exists", return_value=True):
                self.minal.parse_arguments()
                self.assertEqual(self.minal.temperature, 0.5)
                mock_logger.error.assert_any_call(
                    "Invalid temperature value: invalid, using default value."
                )

    def test_valid_max_tokens_argument(self, mock_logger, mock_exit):
        with patch(
            "sys.argv", ["completion_tool.py", "test_file.txt", "--max_tokens", "150"]
        ):
            with patch("os.path.exists", return_value=True):
                self.minal.parse_arguments()
                self.assertEqual(self.minal.max_tokens, 150)

    def test_invalid_max_tokens_argument(self, mock_logger, mock_exit):
        with patch(
            "sys.argv",
            ["completion_tool.py", "test_file.txt", "--max_tokens", "invalid"],
        ):
            with patch("os.path.exists", return_value=True):
                self.minal.parse_arguments()
                self.assertEqual(self.minal.max_tokens, 100)
                mock_logger.error.assert_any_call(
                    "Invalid max tokens value: invalid, using default value."
                )

    def test_version_flag_exits_with_version(self, mock_logger, mock_exit):
        with patch("sys.argv", ["completion_tool.py", "--version"]):
            with patch("builtins.print") as mock_print:
                self.minal.parse_arguments()
                mock_print.assert_any_call(f"{TOOL_NAME} version: {VERSION}")
                mock_exit.assert_called_once()

    def test_help_flag_exits_with_help_message(self, mock_logger, mock_exit):
        with patch("sys.argv", ["completion_tool.py", "--help"]):
            with patch("builtins.print") as mock_print:
                self.minal.parse_arguments()
                mock_print.assert_called_with(self.minal.display_help())
                mock_exit.assert_called_once()

    def test_streaming_and_token_usage_flags(self, mock_logger, mock_exit):
        with patch(
            "sys.argv",
            ["completion_tool.py", "test_file.txt", "--stream", "--token_usage"],
        ):
            with patch("os.path.exists", return_value=True):
                self.minal.parse_arguments()
                self.assertTrue(self.minal.streaming)
                self.assertTrue(self.minal.token_usage)

    def test_get_prompt_template_with_valid_input(self, mock_logger, mock_exit):
        # Arrange
        self.minal.file_input = "Test context"
        self.minal.input_text = "Provide details on the topic"

        # Act
        prompt = self.minal.get_prompt_template()

        # Debug: Print out each message as a string to inspect structure
        for message in prompt.messages:
            print(str(message))

        # Adjusted assertion: Convert messages to strings for the search
        self.assertTrue(
            any("Provide details" in str(message) for message in prompt.messages),
            "Expected 'Provide details' to be in one of the messages",
        )

    def test_generate_completion_without_api_key(self, mock_logger, mock_exit):
        self.minal.api_key = None
        with self.assertRaises(ValueError) as context:
            self.minal.generate_completion()
        self.assertEqual(
            str(context.exception), "API Key is required to generate completion."
        )

    def test_get_response_with_valid_provider(self, mock_logger, mock_exit):
        self.minal.provider = "OpenAI API"
        self.minal.api_key = "test-key"
        response = self.minal.get_response()
        self.assertIsNotNone(response)
        mock_logger.info.assert_any_call(f"Using provider: {self.minal.provider}")

    def test_get_response_with_unknown_provider(self, mock_logger, mock_exit):
        self.minal.provider = "Unknown API"
        response = self.minal.get_response()
        self.assertIsNone(response)
        mock_logger.info.assert_any_call(f"Using provider: {self.minal.provider}")

    def test_generate_completion_successful(self, mock_logger, mock_exit):
        expected_output = (
            "The directional derivative of a function is the rate at which the function "
            "changes at a point in a particular direction."
        )

        self.mock_invoke_return.content = expected_output
        self.mock_chain_llm.invoke.return_value = self.mock_invoke_return
        self.mock_prompt.__or__.return_value = self.mock_chain_llm

        with patch.object(
            self.minal, "get_prompt_template", return_value=self.mock_prompt
        ):
            with patch.object(
                self.minal, "get_response", return_value=self.mock_response
            ):
                with patch("sys.stdout", new=io.StringIO()) as fake_out:
                    self.minal.generate_completion()
                    printed_output = fake_out.getvalue()
                    self.assertEqual(printed_output, expected_output + "\n")
                    mock_logger.info.assert_any_call(
                        "Completion generated successfully."
                    )

    def test_generate_completion(self, mock_logger, mock_exit):
        with patch("app.completion_tool.LangChainOpenAI") as MockLangChainOpenAI:
            mock_llm_instance = MockLangChainOpenAI.return_value
            mock_chain_llm = self.mock_response.__or__.return_value
            mock_chain_llm.invoke.return_value = self.mock_response

            # Patch get_prompt_template and get_response to return mocks
            with patch.object(
                self.minal, "get_prompt_template", return_value=self.mock_response
            ):
                with patch.object(
                    self.minal, "get_response", return_value=mock_llm_instance
                ):
                    # using patch to mock the standard output
                    # and capture the printed output
                    # because our project print _reponse.content + '\n'
                    # to the standard output and we have to capture and mock it
                    with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                        self.minal.generate_completion()
                        printed_output = fake_out.getvalue()

                    expected_output = self.mock_response.content + "\n"
                    self.assertEqual(printed_output, expected_output)


if __name__ == "__main__":
    unittest.main()
