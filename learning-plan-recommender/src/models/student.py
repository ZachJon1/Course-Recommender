class Student:
    def __init__(self, prior_courses=None, department="", degree_level=""):
        self.prior_courses = prior_courses if prior_courses else []
        self.department = department
        self.degree_level = degree_level
    
    def to_dict(self):
        return {
            "prior_courses": self.prior_courses,
            "department": self.department,
            "degree_level": self.degree_level
        }
    
    def __str__(self):
        return (f"Student in {self.department} department, {self.degree_level} level, "
                f"with prior courses: {', '.join(self.prior_courses)}")