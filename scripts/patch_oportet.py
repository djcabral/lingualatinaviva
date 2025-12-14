import sys
import os
from sqlmodel import Session, select, create_engine

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Word

def fix_oportet():
    db_path = "sqlite:///lingua_latina.db"
    engine = create_engine(db_path)
    
    with Session(engine) as session:
        # Check for both forms just in case
        statement = select(Word).where(Word.latin.in_(["oportet", "oporteo"]))
        word = session.exec(statement).first()
        
        if word:
            print(f"Found existing entry: {word.latin}")
            word.latin = "oporteo"
            word.translation = "ser necesario/convenir"
            word.part_of_speech = "verb"
            word.level = 2
            word.conjugation = "2"
            word.principal_parts = "oporteo, oportere, oportui, -"
            word.irregular_forms = '{"impersonal": true}' 
            session.add(word)
            session.commit()
            print("✓ Updated entry to 'oporteo' (impersonal).")
        else:
            print("Entry not found. Creating 'oporteo'...")
            word = Word(
                latin="oporteo",
                translation="ser necesario/convenir",
                part_of_speech="verb",
                level=2,
                conjugation="2",
                principal_parts="oporteo, oportere, oportui, -",
                irregular_forms='{"impersonal": true}'
            )
            session.add(word)
            session.commit()
            print("✓ Created 'oporteo'.")

if __name__ == "__main__":
    fix_oportet()
