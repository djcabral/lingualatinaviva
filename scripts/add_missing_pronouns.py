import sys
import os
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import get_session, Word

def add_pronouns():
    pronouns = [
        {"latin": "ego", "translation": "yo", "part_of_speech": "pronoun", "category": "personal"},
        {"latin": "tu", "translation": "tú", "part_of_speech": "pronoun", "category": "personal"},
        {"latin": "nos", "translation": "nosotros", "part_of_speech": "pronoun", "category": "personal"},
        {"latin": "vos", "translation": "vosotros", "part_of_speech": "pronoun", "category": "personal"},
        {"latin": "is", "translation": "él / este", "part_of_speech": "pronoun", "category": "demonstrative"},
        {"latin": "ea", "translation": "ella / esta", "part_of_speech": "pronoun", "category": "demonstrative"},
        {"latin": "id", "translation": "ello / esto", "part_of_speech": "pronoun", "category": "demonstrative"},
    ]

    with get_session() as session:
        added_count = 0
        for p_data in pronouns:
            # Check if exists
            statement = select(Word).where(Word.latin == p_data["latin"])
            existing = session.exec(statement).first()
            
            if not existing:
                word = Word(
                    latin=p_data["latin"],
                    translation=p_data["translation"],
                    part_of_speech=p_data["part_of_speech"],
                    category=p_data["category"],
                    status="active"
                )
                session.add(word)
                added_count += 1
                print(f"✅ Added: {p_data['latin']}")
            else:
                print(f"ℹ️  Already exists: {p_data['latin']}")
        
        if added_count > 0:
            session.commit()
            print(f"\n🎉 Successfully added {added_count} pronouns.")
        else:
            print("\nNo new pronouns were added.")

if __name__ == "__main__":
    add_pronouns()
