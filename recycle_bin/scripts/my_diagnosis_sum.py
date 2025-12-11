
import sys
import os
from sqlmodel import select, col

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Word, InflectedForm

def check_words():
    with get_session() as session:
        # Check sum
        sum_word = session.exec(select(Word).where(Word.latin == "sum")).first()
        print(f"Word 'sum': {sum_word}")
        if sum_word:
            est_forms = session.exec(select(InflectedForm).where(InflectedForm.word_id == sum_word.id)).all()
            print(f"Forms for 'sum' count: {len(est_forms)}")
            for f in est_forms:
                if f.form == "est":
                    print(f"FOUND 'est': {f}")
        
        # Check Rōma
        roma = session.exec(select(Word).where(Word.latin == "Rōma")).first()
        print(f"Word 'Rōma': {roma}")

if __name__ == "__main__":
    check_words()
