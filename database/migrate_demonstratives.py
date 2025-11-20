import sys
import os
from sqlmodel import Session, select

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import engine
from database.models import Word

def migrate():
    print("Starting Demonstrative Pronouns Migration...")
    
    pronouns = [
        {
            "latin": "is",
            "translation": "ese, esa, eso; él, ella, ello",
            "part_of_speech": "pronoun",
            "level": 2,
            "category": "pronoun_demonstrative"
        },
        {
            "latin": "hic",
            "translation": "este, esta, esto",
            "part_of_speech": "pronoun",
            "level": 2,
            "category": "pronoun_demonstrative"
        },
        {
            "latin": "ille",
            "translation": "aquel, aquella, aquello",
            "part_of_speech": "pronoun",
            "level": 2,
            "category": "pronoun_demonstrative"
        },
        {
            "latin": "iste",
            "translation": "ese (de ustedes), esa, eso",
            "part_of_speech": "pronoun",
            "level": 3,
            "category": "pronoun_demonstrative"
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
        print(f"\n✅ Migration complete. Added {count} demonstrative pronouns.")

if __name__ == "__main__":
    migrate()
