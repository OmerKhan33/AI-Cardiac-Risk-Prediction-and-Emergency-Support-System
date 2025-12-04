import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (for API keys later)
load_dotenv()

class Config:
    # 1. Project Info
    APP_NAME = "Cardiac Risk AI"
    VERSION = "1.0.0"
    
    # 2. Path Setup
    # This automatically finds your project ROOT folder, no matter where you move it
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Define specific paths
    DATA_PATH = os.path.join(BASE_DIR, "src", "data")
    MODEL_PATH = os.path.join(BASE_DIR, "src", "models")
    
    # 3. API Keys (For Day 3)
    # These will read from your .env file, or be empty strings if missing
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY", "")

# Create the instance we import elsewhere
settings = Config()