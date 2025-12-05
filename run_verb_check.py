
import sys
import os
from sqlmodel import select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from database.connection import get_session
from database.models import Word

def check_verbs():
    with get_session() as session:
        verbs = session.exec(select(Word).where(Word.part_of_speech == "verb")).all()
        print(f"Total verbs found: {len(verbs)}")
        if verbs:
            print(f"Sample verb: {verbs[0].latin} ({verbs[0].translation})")
        else:
            print("No verbs found! This will cause st.stop() in conjugations_view.py")

        # Also check for 'verbo' in case of language mismatch
        verbs_es = session.exec(select(Word).where(Word.part_of_speech == "verbo")).all()
        print(f"Total verbs with pos='verbo': {len(verbs_es)}")

if __name__ == "__main__":
    check_verbs()
