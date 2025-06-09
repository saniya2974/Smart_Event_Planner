import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load values from .env file
load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["event_planner"]
events_collection = db["events"]

# Weather API
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
