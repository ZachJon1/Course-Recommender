"""Tests for the LLM client module."""

import unittest
from unittest.mock import MagicMock, patch
import os

from dotenv import load_dotenv
# Load environment variables
load_dotenv(dotenv_path='../../backend/.env')


from src.recommender.llm_client import LLMClient


class TestLLMClient(unittest.TestCase):
    """Test cases for LLM client functionality."""

    @patch('src.recommender.llm_client.openai.Client')
    def test_query_llm_success(self, mock_client):
        """Test successful LLM query with expected response."""
        # Arrange
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            'Recommended learning plan for Deep Learning.'
        )
        mock_client.return_value.chat.completions.create.return_value = (
            mock_response
        )
        

        host = os.getenv("LLM_HOST")
        port = os.getenv("LLM_PORT")
        api_key = os.getenv("LLM_API_KEY")
        message = 'What should I study to prepare for Deep Learning?'
        history_json = '[]'

        # Act
        client = LLMClient(host, port, api_key)
        result = client.query_llm(message, history_json)

        # Assert
        self.assertEqual(
            result['content'],
            'Recommended learning plan for Deep Learning.'
        )
        self.assertEqual(result['role'], 'assistant')

    @patch('src.recommender.llm_client.openai.Client')
    def test_query_llm_failure(self, mock_client):
        """Test LLM query failure with exception handling."""
        # Arrange
        mock_client.return_value.chat.completions.create.side_effect = (
            Exception('API error')
        )
        
        host = 'localhost'
        port = '5000'
        api_key = 'test_api_key'
        message = 'What should I study to prepare for Deep Learning?'
        history_json = '[]'

        # Act & Assert
        client = LLMClient(host, port, api_key)
        with self.assertRaises(Exception) as context:
            client.query_llm(message, history_json)
        self.assertTrue('API error' in str(context.exception))


if __name__ == '__main__':
    unittest.main()