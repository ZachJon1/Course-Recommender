import unittest
from unittest.mock import patch, MagicMock
from src.recommender.plan_generator import LearningPlanGenerator
from src.models.student import Student
from src.models.course_database import CourseDatabase

class TestPlanGenerator(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        self.port = "8080"
        self.api_key = "test_key"
        
        # Create a sample student
        self.student = Student(
            department="Computer Science",
            degree_level="Bachelor's",
            prior_courses=["Introduction to Programming", "Data Structures"]
        )
        
        self.target_course = "Deep Learning"
        self.course_db = CourseDatabase()

    @patch('src.recommender.plan_generator.LLMClient')
    def test_generate_learning_plan_multi_turn(self, mock_llm_client_class):
        # Arrange - Set up the mock LLMClient
        mock_llm_client = MagicMock()
        mock_llm_client_class.return_value = mock_llm_client
        
        # Set up mock responses for each step
        mock_responses = [
            {"content": "Knowledge Assessment Content", "role": "assistant"},
            {"content": "Gap Analysis Content", "role": "assistant"},
            {"content": "Course Selection Content", "role": "assistant"},
            {"content": "Final Learning Plan Content", "role": "assistant"},
        ]
        
        # Configure the mock to return different responses in sequence
        mock_llm_client.query_llm.side_effect = mock_responses
        
        # Act
        plan_generator = LearningPlanGenerator(self.host, self.port, self.api_key)
        learning_plan = plan_generator.generate_plan(self.student, self.target_course, self.course_db)
        
        # Assert
        self.assertIsInstance(learning_plan, str)
        self.assertEqual(learning_plan, "Final Learning Plan Content")
        
        # Verify that the LLM client was called four times for the multi-turn interaction
        self.assertEqual(mock_llm_client.query_llm.call_count, 4)
        
        # Verify the content of the prompts
        calls = mock_llm_client.query_llm.call_args_list
        
        # First prompt should be about knowledge assessment
        self.assertIn("assessment", calls[0][0][0].lower())
        self.assertIn("Computer Science", calls[0][0][0])
        
        # Second prompt should be about gap analysis
        self.assertIn("gap", calls[1][0][0].lower())
        self.assertIn("Knowledge Assessment Content", calls[1][0][0])
        
        # Third prompt should be about course selection
        self.assertIn("course", calls[2][0][0].lower())
        self.assertIn("Gap Analysis Content", calls[2][0][0])
        
        # Fourth prompt should be about the final plan
        self.assertIn("learning plan", calls[3][0][0].lower())
        self.assertIn("Course Selection Content", calls[3][0][0])