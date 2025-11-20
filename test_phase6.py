import sys
import os
from sqlmodel import Session, select, func

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import engine
from database.models import Word, Text, TextWordLink, Author

def verify():
    print("Verifying Phase 6...")
    with Session(engine) as session:
        # Check Author
        hyginus = session.exec(select(Author).where(Author.name == "Hyginus")).first()
        if hyginus:
            print(f"✅ Author found: {hyginus.name}")
        else:
            print("❌ Author Hyginus NOT found")

        # Check Texts
        texts = ["Schola Rōmāna", "Deīs et Deābus", "Promētheus", "Pandōra"]
        for t_title in texts:
            text = session.exec(select(Text).where(Text.title == t_title)).first()
            if text:
                link_count = session.exec(select(func.count()).where(TextWordLink.text_id == text.id)).one()
                print(f"✅ Text found: {text.title} (Level {text.difficulty}) - Linked Words: {link_count}")
            else:
                print(f"❌ Text NOT found: {t_title}")

        # Check specific vocab
        words = ["magister", "ignis", "creāre", "autem"]
        for w_latin in words:
            word = session.exec(select(Word).where(Word.latin == w_latin)).first()
            if word:
                print(f"✅ Word found: {word.latin} ({word.part_of_speech})")
            else:
                print(f"❌ Word NOT found: {w_latin}")

if __name__ == "__main__":
    verify()
