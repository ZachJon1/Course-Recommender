class Course:
    def __init__(self, name, description, prerequisites):
        self.name = name
        self.description = description
        self.prerequisites = prerequisites

    def get_course_info(self):
        return {
            "name": self.name,
            "description": self.description,
            "prerequisites": self.prerequisites
        }

    def has_prerequisites(self, completed_courses):
        return all(prereq in completed_courses for prereq in self.prerequisites)