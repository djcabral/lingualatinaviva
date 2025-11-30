import sys
import os
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import engine
from database import Word

def check_dare():
    with Session(engine) as session:
        # Search for 'dare' or 'dō' (since 'dare' is the infinitive, usually stored as 'dō' but maybe not)
        words = session.exec(select(Word).where(Word.translation == "dar")).all()
        for word in words:
            print(f"ID: {word.id}")
            print(f"Latin: {word.latin}")
            print(f"Translation: {word.translation}")
            print(f"Principal Parts: {word.principal_parts}")
            print(f"Conjugation: {word.conjugation}")
            print(f"Irregular Forms: {word.irregular_forms}")
            print("-" * 20)

if __name__ == "__main__":
    check_dare()
