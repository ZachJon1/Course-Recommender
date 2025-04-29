import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recommender.plan_generator import LearningPlanGenerator
from src.models.student import Student
from src.models.course_database import CourseDatabase

class TestPlanGenerator(unittest.TestCase):

    def setUp(self):
        # Create a student object
        self.student = Student(
            prior_courses=["Introduction to Machine Learning", "Linear Algebra"],
            department="Computer Science",
            degree_level="Bachelor's"
        )
        self.target_course = "Deep Learning"
        self.course_db = CourseDatabase()
        
        # Mock configuration for the LLM
        self.host = "localhost"
        self.port = "1234"
        self.api_key = "test-key"

    @patch('src.recommender.plan_generator.LLMClient')
    def test_generate_learning_plan(self, mock_llm_client_class):
        # Arrange - Set up the mock LLMClient
        mock_llm_client = MagicMock()
        mock_llm_client_class.return_value = mock_llm_client
        
        # Set up the mock response from LLM
        mock_response = {
            "content": "This is a learning plan for Deep Learning",
            "role": "assistant"
        }
        mock_llm_client.query_llm.return_value = mock_response
        
        # Act
        plan_generator = LearningPlanGenerator(self.host, self.port, self.api_key)
        learning_plan = plan_generator.generate_plan(self.student, self.target_course, self.course_db)
        
        # Assert
        self.assertIsInstance(learning_plan, str)
        self.assertEqual(learning_plan, "This is a learning plan for Deep Learning")
        
        # Verify that the LLM client was called correctly
        mock_llm_client.query_llm.assert_called_once()
        # The prompt should contain student info and target course
        prompt = mock_llm_client.query_llm.call_args[0][0]
        self.assertIn("Bachelor's", prompt)
        self.assertIn("Computer Science", prompt)
        self.assertIn("Deep Learning", prompt)

if __name__ == '__main__':
    unittest.main()