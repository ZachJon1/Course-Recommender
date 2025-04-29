# filepath: /learning-plan-recommender/learning-plan-recommender/config/config.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../../backend/.env')

class Config:
    LLM_HOST = os.getenv("LLM_HOST")
    LLM_PORT = os.getenv("LLM_PORT")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    DEFAULT_COURSE = "Deep Learning"
    MAX_HISTORY_LENGTH = 10  # Maximum number of messages to keep in history for LLM queries
    TEMPERATURE = 0.6  # Controls randomness in LLM responses
    TOP_P = 0.95  # Controls diversity via nucleus sampling