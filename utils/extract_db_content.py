import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlmodel import select
from database.connection import get_session
from database.models import Word, Text

def extract_vocabulary(output_dir):
    print("Extracting vocabulary...")
    vocab_list = []
    
    with get_session() as session:
        words = session.exec(select(Word)).all()
        for word in words:
            vocab_list.append(word.model_dump())
            
    output_file = os.path.join(output_dir, "vocabulary.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(vocab_list, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"Exported {len(vocab_list)} words to {output_file}")

def extract_readings(output_dir):
    print("Extracting readings...")
    readings_list = []
    
    with get_session() as session:
        texts = session.exec(select(Text)).all()
        for text in texts:
            # Clean up SQLAlchemy state if needed, model_dump handles basic types
            readings_list.append(text.model_dump())
            
    output_file = os.path.join(output_dir, "readings.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(readings_list, f, indent=2, ensure_ascii=False, default=str)
        
    print(f"Exported {len(readings_list)} readings to {output_file}")

def main():
    output_dir = "portability"
    # Ensure subdir exists if we change structure, but root portability is fine for these
    # create specialized subdirs if preferred
    vocab_dir = os.path.join(output_dir, "vocabulary")
    readings_dir = os.path.join(output_dir, "readings")
    os.makedirs(vocab_dir, exist_ok=True)
    os.makedirs(readings_dir, exist_ok=True)

    extract_vocabulary(vocab_dir)
    extract_readings(readings_dir)
    
    print("Database extraction complete.")

if __name__ == "__main__":
    main()
