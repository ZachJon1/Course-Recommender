import json
import os
import fitz  # PyMuPDF for PDF parsing
from src.recommender.llm_client import LLMClient

class LearningPlanGenerator:
    def __init__(self, host, port, api_key, catalog_path=None):
        self.host = host
        self.port = port
        self.api_key = api_key
        self.catalog_path = catalog_path or "../engineering-course-catalog/engineering_catalog.pdf"
        self.catalog_text = self._load_catalog_text()
        
    def _load_catalog_text(self):
        """Load and extract text from the engineering course catalog PDF."""
        try:
            catalog_text = ""
            if not os.path.exists(self.catalog_path):
                print(f"Warning: Catalog file not found at {self.catalog_path}")
                return "Catalog data not available."
                
            pdf_document = fitz.open(self.catalog_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                catalog_text += page.get_text()
            return catalog_text
        except Exception as e:
            print(f"Error loading catalog: {e}")
            return "Error loading catalog data."
    
    def search_catalog(self, query, context_size=500):
        """
        Search the engineering catalog for relevant information.
        
        Args:
            query: The search query (course name, topic, etc.)
            context_size: Number of characters to include before and after match
            
        Returns:
            list: List of relevant text snippets from the catalog
        """
        query = query.lower()
        catalog_lower = self.catalog_text.lower()
        results = []
        
        # Find all occurrences of the query in the catalog
        start_pos = 0
        while True:
            pos = catalog_lower.find(query, start_pos)
            if pos == -1:
                break
                
            # Extract context around the match
            context_start = max(0, pos - context_size)
            context_end = min(len(self.catalog_text), pos + len(query) + context_size)
            context = self.catalog_text[context_start:context_end]
            
            # Add the snippet to results
            results.append(context)
            start_pos = pos + len(query)
            
        return results
    
    def generate_plan(self, student, target_course, course_db):
        """
        Generate a learning plan using a multi-turn interaction approach with RAG.
        
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
        
        # Step 3: Course selection with RAG - search catalog before recommending courses
        catalog_data = self._retrieve_catalog_information(gap_analysis, target_course)
        
        courses_prompt = self._create_rag_course_selection_prompt(
            student, target_course, knowledge_assessment, gap_analysis, 
            course_db, catalog_data
        )
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
    
    def _retrieve_catalog_information(self, gap_analysis, target_course):
        """
        Retrieve relevant information from the engineering catalog based on identified gaps.
        
        Args:
            gap_analysis: The identified knowledge gaps
            target_course: The target course
            
        Returns:
            str: Relevant catalog information
        """
        # Use a set for collecting key terms (eliminates duplicates automatically)
        key_terms = set()
        
        # Add the target course as a key term
        key_terms.add(target_course)
        
        # Extract potential course names and topics from gap analysis
        gap_lines = gap_analysis.split('\n')
        
        # List of common educational topics to look for
        educational_topics = {
            "calculus", "programming", "statistics", "algorithm", 
            "linear algebra", "probability", "machine learning", "data science",
            "neural networks", "deep learning", "computer vision", "nlp",
            "databases", "operating systems", "networks", "security"
        }
        
        for line in gap_lines:
            line_lower = line.lower()
            
            # Look for course indicators
            if "course" in line_lower or "prerequisite" in line_lower:
                words = line.split()
                for i in range(len(words) - 1):
                    if words[i].lower() in {"course", "courses", "class", "classes"}:
                        # Check for course codes (typically uppercase or containing numbers)
                        next_word = words[i+1] if i+1 < len(words) else ""
                        if next_word and (next_word[0].isupper() or any(c.isdigit() for c in next_word)):
                            key_terms.add(next_word)
                            
                            # capture course numbers that might follow
                            if i+2 < len(words) and any(c.isdigit() for c in words[i+2]):
                                key_terms.add(f"{next_word} {words[i+2]}")
            
            # Look for educational topics
            for topic in educational_topics:
                if topic in line_lower:
                    key_terms.add(topic)
                    
            # common course prefix patterns (CSCI 101, MATH-240)
            import re
            course_patterns = [
                r'\b([A-Z]{2,5})\s*[-]?\s*(\d{3,4}[A-Z]?)\b',  # CSCI 101
                r'\b([A-Z]{2,5})(\d{3,4}[A-Z]?)\b'             #  MATH240
            ]
            
            for pattern in course_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    course_code = f"{match[0]} {match[1]}"
                    key_terms.add(course_code)
        
        # Convert set to list for further processing
        key_terms_list = list(key_terms)
        
        # Search the catalog for each key term
        catalog_snippets = []
        for term in key_terms_list:
            snippets = self.search_catalog(term)
            catalog_snippets.extend(snippets[:2])  # Limit to top 2 snippets per term
            
        # Limit overall length
        max_catalog_text_length = 4000  # Prevent prompt from ~large
        catalog_text = "\n---\n".join(catalog_snippets[:8])  # Limit to 8 
        
        if len(catalog_text) > max_catalog_text_length:
            catalog_text = catalog_text[:max_catalog_text_length] + "...[truncated]"
            
        return catalog_text
    
    def _create_rag_course_selection_prompt(self, student, target_course, knowledge_assessment, gap_analysis, course_db, catalog_data):
        """Generate a RAG-enhanced prompt to select specific courses based on identified gaps."""
        
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
        
        Relevant Information from Engineering Catalog:
        {catalog_data}
        
        Based on the identified knowledge gaps AND the information from the actual engineering catalog, select specific courses that would best prepare this student for {target_course}.
        
        For each recommended course:
        1. Verify it exists in the catalog data
        2. Explain exactly which gap(s) it addresses
        3. Justify why this specific course is appropriate given the student's background
        4. Indicate if it's essential or optional
        5. Note any prerequisites for the recommended course
        
        If the student appears ready to take {target_course} directly, state this clearly with justification.
        
        Format your response as a structured list of course recommendations with clear explanations.
        """
        
        return prompt