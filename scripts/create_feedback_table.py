import sys
import os
from sqlmodel import SQLModel

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import engine
from database import Feedback

def create_feedback_table():
    print("Creating Feedback table...")
    SQLModel.metadata.create_all(engine)
    print("Feedback table created successfully.")

if __name__ == "__main__":
    create_feedback_table()
