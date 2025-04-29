class CourseDatabase:
    def __init__(self):
        self.courses = [
            {"code": "Csci 256", "name": "Programming in Python", "description": "Introduction to Python programming language", "prerequisites": []},
            {"code": "Csci 343", "name": "Fundamentals of Data Science", "description": "Basics of data science methodologies", "prerequisites": ["Csci 256"]},
            {"code": "CSci 356", "name": "Data Structures in Python", "description": "Implementation of data structures using Python", "prerequisites": ["Csci 256"]},
            {"code": "CSci 433", "name": "Algorithm and Data Structure Analysis", "description": "Analysis of algorithms and data structures", "prerequisites": ["CSci 356"]},
            {"code": "Csci 443", "name": "Advanced Data Science", "description": "Advanced topics in data science", "prerequisites": ["Csci 343", "CSci 356"]},
            {"code": "Csci 475", "name": "Introduction to Database Systems", "description": "Fundamentals of database design and management", "prerequisites": ["CSci 356"]},
            {"code": "CSci 345", "name": "Information Storage and Retrieval", "description": "Methods for storing and retrieving information", "prerequisites": ["Csci 256"]},
            {"code": "CSci 444", "name": "Information Visualization", "description": "Techniques for visualizing data and information", "prerequisites": ["Csci 343"]},
            {"code": "CSci 517", "name": "Natural Language Processing", "description": "Processing and analyzing natural language data", "prerequisites": ["Csci 632"]},
            {"code": "CSci 543", "name": "Data Mining", "description": "Techniques for extracting patterns from data", "prerequisites": ["Csci 443"]},
            {"code": "Csci 632", "name": "Machine Learning", "description": "Algorithms that learn from data", "prerequisites": ["Csci 443"]},
            {"code": "Csci 581", "name": "Special Topics in Computer Science (Computer Vision)", "description": "Computer vision algorithms and applications", "prerequisites": ["Csci 632"]},
            {"code": "CSci 492", "name": "Special Topics in Data Science (Deep Learning - Undergraduate)", "description": "Deep learning for undergraduates", "prerequisites": ["Csci 632"]},
            {"code": "Engr 691", "name": "Special Topics in Engineering Science (Deep Learning - Graduate)", "description": "Advanced deep learning for graduates", "prerequisites": ["Csci 632"]}
        ]
    
    def get_all_courses(self):
        return self.courses
    
    def get_course_by_code(self, code):
        for course in self.courses:
            if course["code"].lower() == code.lower():
                return course
        return None
    
    def get_courses_as_text(self):
        return "\n".join([f"{c['code']}: {c['name']}" for c in self.courses])