from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI