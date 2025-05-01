import os
from dotenv import load_dotenv
from src.recommender.plan_generator import LearningPlanGenerator as BasicPlanGenerator
from src.recommender.plan_generator_rag import LearningPlanGenerator as RagPlanGenerator
from src.models.student import Student
from src.models.course_database import CourseDatabase

# Load environment variables
load_dotenv(dotenv_path='../backend/.env')

def main():
    print("\n===== Learning Plan Recommender System =====\n")
    
    # Get student information
    print("Please enter your academic background:")
    prior_courses = input("Prior courses taken (comma-separated): ").strip()
    department = input("Your department: ").strip()
    
    # Validate degree level input
    valid_degree_levels = ["undergraduate", "graduate"]
    while True:
        degree_level = input("Degree level (Undergraduate/Graduate): ").strip().lower()
        if degree_level in valid_degree_levels:
            # Convert first letter to uppercase for consistency
            degree_level = degree_level.capitalize()
            break
        else:
            print("Invalid input. Please enter either 'Undergraduate' or 'Graduate'.")
    
    # Create student object
    student = Student(
        prior_courses=prior_courses.split(",") if prior_courses else [],
        department=department,
        degree_level=degree_level
    )
    
    # Get target course
    target_course = input("\nTarget course you want to prepare for: ").strip()
    
    # Initialize course database with example courses
    course_db = CourseDatabase()
    
    # Initialize learning plan generator
    # plan_generator = BasicPlanGenerator(
    #     host=os.getenv("LLM_HOST"),
    #     port=os.getenv("LLM_PORT"),
    #     api_key=os.getenv("LLM_API_KEY")
    # )
    
    plan_generator = RagPlanGenerator(
        host=os.getenv("LLM_HOST"),
        port=os.getenv("LLM_PORT"),
        api_key=os.getenv("LLM_API_KEY")
    )
    
    # Generate learning plan
    print("\nGenerating your personalized learning plan...")
    learning_plan = plan_generator.generate_plan(student, target_course, course_db) # RAG
   
    # Display the learning plan
    print("\n===== Your Personalized Learning Plan =====\n")
    print(learning_plan)

if __name__ == "__main__":
    main()