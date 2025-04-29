import json
from src.recommender.llm_client import LLMClient

class LearningPlanGenerator:
    def __init__(self, host, port, api_key):
        self.host = host
        self.port = port
        self.api_key = api_key

    def generate_plan(self, student, target_course, course_db):
        """
        Generate a learning plan using a multi-turn interaction approach.
        
        Args:
            student: Student object with background information
            target_course: The target course the student wants to take
            course_db: CourseDatabase object with course information
            
        Returns:
            str: A personalized learning plan
        """
        # Initialize LLM client
        llm_client = LLMClient(self.host, self.port, self.api_key)
        
        # Step 1: Knowledge assessment - understand what the student already knows
        knowledge_prompt = self._create_knowledge_assessment_prompt(student, target_course)
        knowledge_response = llm_client.query_llm(knowledge_prompt)
        knowledge_assessment = knowledge_response.get("content", "")
        
        # Step 2: Gap analysis - identify what knowledge/skills are missing
        gap_prompt = self._create_gap_analysis_prompt(student, target_course, knowledge_assessment, course_db)
        gap_response = llm_client.query_llm(gap_prompt)
        gap_analysis = gap_response.get("content", "")
        
        # Step 3: Course selection - determine specific courses to take
        courses_prompt = self._create_course_selection_prompt(student, target_course, knowledge_assessment, gap_analysis, course_db)
        courses_response = llm_client.query_llm(courses_prompt)
        course_selection = courses_response.get("content", "")
        
        # Step 4: Final plan generation - combine all insights into a complete plan
        final_prompt = self._create_final_plan_prompt(student, target_course, knowledge_assessment, gap_analysis, course_selection)
        final_response = llm_client.query_llm(final_prompt)
        
        # Return the final learning plan
        return final_response.get("content", "Error generating learning plan.")

    def _create_knowledge_assessment_prompt(self, student, target_course):
        """Generate a prompt focused solely on assessing the student's current knowledge."""
        
        prompt = f"""
        You are an academic advisor assessing a student's current knowledge.
        
        Student Background:
        - Department: {student.department}
        - Degree Level: {student.degree_level}
        - Prior Courses: {', '.join(student.prior_courses)}
        
        Based solely on this information, provide a detailed assessment of what this student likely knows that is relevant to {target_course}.
        
        Focus on:
        - Mathematical foundations they likely have
        - Programming skills they've developed
        - Domain-specific knowledge from their field
        - Relevant concepts they've been exposed to through their prior courses
        
        Format your response as a structured assessment with clear sections. Be specific and comprehensive.
        """
        
        return prompt
        
    def _create_gap_analysis_prompt(self, student, target_course, knowledge_assessment, course_db):
        """Generate a prompt to identify knowledge gaps based on previous assessment."""
        
        courses_text = course_db.get_courses_as_text()
        
        prompt = f"""
        You are an academic advisor identifying knowledge gaps for a student.
        
        Student Background:
        - Department: {student.department}
        - Degree Level: {student.degree_level}
        - Prior Courses: {', '.join(student.prior_courses)}
        
        Target Course: {target_course}
        
        Previous Knowledge Assessment:
        {knowledge_assessment}
        
        Available courses in the catalog:
        {courses_text}
        
        Based on the knowledge assessment and the requirements for {target_course}, identify specific knowledge and skill gaps this student needs to address. Consider:
        - Mathematical prerequisites
        - Programming skills and frameworks
        - Theoretical foundations
        - Practical experience needed
        
        Format your response as a clear list of specific gaps that need to be addressed.
        """
        
        return prompt
        
    def _create_course_selection_prompt(self, student, target_course, knowledge_assessment, gap_analysis, course_db):
        """Generate a prompt to select specific courses based on identified gaps."""
        
        courses_text = course_db.get_courses_as_text()
        
        prompt = f"""
        You are an academic advisor selecting courses to fill specific knowledge gaps.
        
        Student Background:
        - Department: {student.department}
        - Degree Level: {student.degree_level}
        - Prior Courses: {', '.join(student.prior_courses)}
        
        Target Course: {target_course}
        
        Knowledge Assessment:
        {knowledge_assessment}
        
        Identified Gaps:
        {gap_analysis}
        
        Available courses in the catalog:
        {courses_text}
        
        Based on the identified knowledge gaps, select specific courses from the catalog that would best prepare this student for {target_course}. For each recommended course:
        1. Explain exactly which gap(s) it addresses
        2. Justify why this specific course is appropriate given the student's background
        3. Indicate if it's essential or optional
        
        If the student appears ready to take {target_course} directly, state this clearly with justification.
        
        Format your response as a structured list of course recommendations with clear explanations.
        """
        
        return prompt
        
    def _create_final_plan_prompt(self, student, target_course, knowledge_assessment, gap_analysis, course_selection):
        """Generate a prompt to create the final learning plan that integrates all previous insights."""
        
        prompt = f"""
        You are an academic advisor creating a complete learning plan for a student.
        
        Student Background:
        - Department: {student.department}
        - Degree Level: {student.degree_level}
        - Prior Courses: {', '.join(student.prior_courses)}
        
        Target Course: {target_course}
        
        Knowledge Assessment:
        {knowledge_assessment}
        
        Identified Gaps:
        {gap_analysis}
        
        Course Recommendations:
        {course_selection}
        
        Using all of this information, create a comprehensive learning plan for this student to successfully prepare for and complete {target_course}. Your plan should include:
        
        ## Current Knowledge Assessment
        [Summarize the student's current relevant knowledge]
        
        ## Knowledge Gaps for {target_course}
        [Summarize the key gaps that need to be addressed]
        
        ## Recommended Learning Path
        [Provide a sequential path of courses and learning activities]
        
        ## Additional Resources
        [Suggest supplementary materials, online resources, or self-study topics]
        
        ## Timeline
        [Recommend a realistic timeline for completing the preparation and target course]
        
        Make your plan specific, actionable, and tailored to this student's unique background and needs.
        """
        
        return prompt