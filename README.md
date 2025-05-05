# Learning Plan Recommender

This project is designed to help students generate personalized learning plans based on their academic background and target courses, specifically focusing on engineering courses. It can be utilized by all students beyond engineering, howevver, the current implemented RAG is for engineering courses.


## Project Structure

```

LLM-Local-Deployment
├── assets
│   ---

backend
├── node_modules            # Node.js dependencies

engineering-course-catalog
|── engineering_catalog.pdf
learning-plan-recommender
├── src
│   ├── app.py                # Main entry point of the application
│   ├── recommender           # Module for generating learning plans
│   │   ├── __init__.py
│   │   ├── llm_client.py     # Interacts with the local LLM API
│   │   └── plan_generator.py  # Logic for generating learning plans
│   ├── models                # Module for data models
│   │   ├── __init__.py
│   │   ├── student.py        # Defines the Student class
│   │   └── course.py         # Defines the Course class
│   ├── templates             # HTML templates for the web interface
│   │   ├── index.html        # Main input form
│   │   └── recommendation.html # Displays generated learning plans
│   └── static                # Static files (CSS, JS)
│       ├── css
│       │   └── style.css     # Styles for the web application
│       └── js
│           └── main.js       # Client-side interactivity
├── tests                     # Unit tests for the application
│   ├── __init__.py
│   ├── test_llm_client.py    # Tests for the llm_client module
│   └── test_plan_generator.py # Tests for the plan_generator module
├── config                    # Configuration settings
│   └── config.py             # API keys and constants
├── requirements.yml          # Python dependencies
├── .env                      # Example environment variables
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd learning-plan-recommender
   ```

2. **Install dependencies:**
   ```
   conda env create -f requirements.yml
   ```

3. **Set up environment variables:**
   Connect to llm using `.env` (talk to me for a test run).

4. **Run the application:**
   ```
   python app.py
   ```

5. **Sample run gif:**
   ![LLM Course Recommender](llm-course-recommender.gif)

## Usage

- ~~Open your web browser and navigate to `http://localhost:5000`.~~
- Input your academic background details and the target course (e.g., "Deep Learning").
- Submit the form to receive a personalized learning plan.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- [William Panlener](https://github.com/qwestduck) for the [web scapper](https://github.com/qwestduck/abet-catalog-generator) that scrapes the course information from the university website.
