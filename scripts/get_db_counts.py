import sys
import os
from sqlmodel import select, func

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database.models import Word

def check_counts():
    with get_session() as session:
        total_words = session.exec(select(func.count(Word.id))).one()
        nouns = session.exec(select(func.count(Word.id)).where(Word.part_of_speech == "noun")).one()
        verbs = session.exec(select(func.count(Word.id)).where(Word.part_of_speech == "verb")).one()
        adjectives = session.exec(select(func.count(Word.id)).where(Word.part_of_speech == "adjective")).one()
        others = total_words - nouns - verbs - adjectives
        
        print(f"Total Words: {total_words}")
        print(f"Nouns: {nouns}")
        print(f"Verbs: {verbs}")
        print(f"Adjectives: {adjectives}")
        print(f"Others: {others}")

if __name__ == "__main__":
    check_counts()
