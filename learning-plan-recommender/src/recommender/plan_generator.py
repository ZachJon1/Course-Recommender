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
        You are an academic advisor helping students choose the right path to take advanced courses.
        
        Given the student's background and their goal, think step by step and explain the reasoning behind the recommended learning plan.
        Make sure to explain any prerequisite knowledge that might be missing.
        
        Student Background:
        - Department: {student.department}
        - Degree Level: {student.degree_level}
        - Prior Courses: {', '.join(student.prior_courses)}
        - Goal: {target_course}
        
        Available courses in the catalog:
        {courses_text}
        
        Step-by-step reasoning and recommendation:
        1. First, assess the student's current knowledge based on their background and prior courses
        2. Identify specific knowledge gaps needed for {target_course}
        3. Determine which courses would fill these gaps
        4. Consider the most efficient pathway based on prerequisites
        5. Provide a final recommendation with justification for each course
        
        Please structure your response as follows:
        
        ## Current Knowledge Assessment
        [Detailed assessment of what the student already knows]
        
        ## Knowledge Gaps for {target_course}
        [Specific topics or skills needed for {target_course} that the student may lack]
        
        ## Recommended Learning Path
        [Step-by-step course recommendations with clear reasoning for each]
        
        ## Additional Resources
        [Supplementary materials or self-study topics]
        
        ## Timeline
        [Estimated timeline for completion]
        
        Here is an example of thoughtful reasoning:
        
        Student Background: A graduate student in Mechanical Engineering. Familiar with MATLAB, took Intro to Python, and has done ML projects.
        Goal: Take Deep Learning.
        
        ## Current Knowledge Assessment
        This student has an engineering background which typically includes strong mathematics fundamentals. They already know MATLAB and some Python, suggesting comfort with programming. Most importantly, they have experience with ML projects, indicating familiarity with core machine learning concepts.
        
        ## Knowledge Gaps for Deep Learning
        While the student has ML experience, deep learning requires specific knowledge of neural network architectures, backpropagation, gradient descent optimization, and frameworks like PyTorch or TensorFlow. The extent of their ML projects will determine how much preparation they need.
        
        ## Recommended Learning Path
        Given their existing ML experience, this student could likely take Deep Learning directly, especially if they feel comfortable with the prerequisite assessment (Project 0) that tests fundamental ML concepts.
        
        If they want additional preparation:
        - Taking "CSci 632 Machine Learning" would formalize their ML knowledge and ensure they have the theoretical foundation
        
        ## Additional Resources
        - Review linear algebra concepts critical for deep learning
        - Familiarize with either PyTorch or TensorFlow through online tutorials
        - Practice implementing basic neural networks
        
        ## Timeline
        The student can likely begin Deep Learning in the upcoming term if they feel confident in their ML background. If taking CSci 632 first, they would need one additional term before starting Deep Learning.
        
        Now, please provide a similar thoughtful, step-by-step analysis for the current student.
        """
        
        return prompt