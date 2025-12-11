
import sys
import os
from sqlmodel import select, func

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Word, InflectedForm

def check_db():
    with get_session() as session:
        word_count = session.exec(select(func.count(Word.id))).one()
        inflected_count = session.exec(select(func.count(InflectedForm.id))).one()
        
        print(f"Total Words: {word_count}")
        print(f"Total Inflected Forms: {inflected_count}")
        
        # Check specific words
        roma = session.exec(select(Word).where(Word.latin == "Rōma")).first()
        print(f"Word 'Rōma' found: {roma is not None}")
        
        if roma:
            forms = session.exec(select(InflectedForm).where(InflectedForm.word_id == roma.id)).all()
            print(f"Inflected forms for Rōma: {len(forms)}")
            for f in forms:
                print(f" - {f.inflected_form} (norm: {f.normalized_form})")

if __name__ == "__main__":
    check_db()
