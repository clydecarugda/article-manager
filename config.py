import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  MONGO_URI = os.getenv('MONGO_URI')
  PORT = os.getenv('PORT')
  REDIS_URI = os.getenv('REDIS_URI')