import sys
import os
from sqlmodel import Session, select

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import engine
from database import Word

def migrate():
    print("Starting Pronoun Migration...")
    
    pronouns = [
        {
            "latin": "ego",
            "translation": "yo",
            "part_of_speech": "pronoun",
            "level": 1,
            "category": "pronoun_personal"
        },
        {
            "latin": "tū",
            "translation": "tú",
            "part_of_speech": "pronoun",
            "level": 1,
            "category": "pronoun_personal"
        },
        {
            "latin": "nōs",
            "translation": "nosotros/as",
            "part_of_speech": "pronoun",
            "level": 1,
            "category": "pronoun_personal"
        },
        {
            "latin": "vōs",
            "translation": "vosotros/as, ustedes",
            "part_of_speech": "pronoun",
            "level": 1,
            "category": "pronoun_personal"
        }
    ]
    
    with Session(engine) as session:
        count = 0
        for p_data in pronouns:
            existing = session.exec(select(Word).where(Word.latin == p_data["latin"])).first()
            if not existing:
                pronoun = Word(**p_data)
                session.add(pronoun)
                count += 1
                print(f"  + Added: {p_data['latin']}")
            else:
                print(f"  . Skipped: {p_data['latin']} (already exists)")
        
        session.commit()
        print(f"\n✅ Migration complete. Added {count} pronouns.")

if __name__ == "__main__":
    migrate()
