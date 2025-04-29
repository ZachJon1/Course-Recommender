# Learning Plan Recommender

This project is designed to help students generate personalized learning plans based on their academic background and target courses, specifically focusing on "Deep Learning."

## Project Structure

```
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
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables
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
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in the required values.

4. **Run the application:**
   ```
   python src/app.py
   ```

## Usage

- Open your web browser and navigate to `http://localhost:5000`.
- Input your academic background and the target course (e.g., "Deep Learning").
- Submit the form to receive a personalized learning plan.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.