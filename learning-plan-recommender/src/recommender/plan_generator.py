import json
from src.recommender.llm_client import LLMClient

class LearningPlanGenerator:
    def __init__(self, host, port, api_key):
        self.llm_client = LLMClient(host, port, api_key)
    
    def generate_plan(self, student, target_course, course_db):
        # Create a prompt for the LLM
        prompt = self._create_prompt(student, target_course, course_db)
        
        # Query the LLM
        response = self.llm_client.query_llm(prompt)
        
        # Return the learning plan content
        return response["content"]
    
    def _create_prompt(self, student, target_course, course_db):
            # Build a detailed prompt for the LLM
        courses_text = course_db.get_courses_as_text()
        
        prompt = f"""
        As a course advisor, create a personalized learning plan for a student with the following background:
        
        Academic Background:
        - Department: {student.department}
        - Degree Level: {student.degree_level}
        - Prior Courses: {', '.join(student.prior_courses)}
        
        The student wants to prepare for and succeed in: {target_course}
        
        Available courses in the catalog:
        {courses_text}
        
        Please provide:
        1. A recommended sequence of courses to take before the target course
        2. Justification for each recommendation based on the student's background
        3. Additional resources or self-study topics to complement formal coursework
        4. Expected timeline for completion
        
        Format your response as a clear, structured learning plan.
        
        Here are some example profiles and their corresponding learning plans:
        
        Example 1:
        Student Background:
        - Department: Computer Science
        - Degree Level: Graduate (non-CS undergrad)
        - Prior Courses: Programming in Python, Statistics
        - Goal: Deep Learning
        
        Recommended Plan:
        Take one of the following before Deep Learning:
        - CSci 543 Data Mining
        - Csci 632 Machine Learning
        
        Example 2:
        Student Background:
        - Department: Mechanical Engineering
        - Degree Level: Graduate
        - Prior Courses: MATLAB, Introduction to Python, Machine Learning Projects
        - Goal: Deep Learning
        
        Recommended Plan:
        May take Deep Learning directly, especially if comfortable completing Project 0.
        
        Example 3:
        Student Background:
        - Department: Psychology
        - Degree Level: Graduate
        - Prior Courses: Business Analytics, Introduction to Python
        - Goal: Deep Learning
        
        Recommended Plan:
        1. Take Csci 343 Fundamentals of Data Science
        2. Then take one of:
           - CSci 543 Data Mining
           - Csci 632 Machine Learning
        3. Then take Deep Learning
        
        Now, please provide a similarly structured learning plan for the current student.
        """
        
        return prompt