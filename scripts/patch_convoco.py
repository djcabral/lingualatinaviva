import sys
import os
from sqlmodel import Session, select, create_engine

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Word

def fix_convoco():
    db_path = "sqlite:///lingua_latina.db"
    engine = create_engine(db_path)
    
    with Session(engine) as session:
        statement = select(Word).where(Word.latin == "convoco")
        word = session.exec(statement).first()
        
        if word:
            print(f"Found convoco: {word.latin}")
            word.conjugation = "1"
            word.principal_parts = "convoco, convocare, convocavi, convocatum"
            word.translation = "convocar"
            word.level = 1
            session.add(word)
            session.commit()
            print("✓ Fixed convoco data.")
        else:
            print("convoco not found in DB. Creating...")
            word = Word(
                latin="convoco",
                translation="convocar",
                part_of_speech="verb",
                level=1,
                conjugation="1",
                principal_parts="convoco, convocare, convocavi, convocatum"
            )
            session.add(word)
            session.commit()
            print("✓ Created convoco.")

if __name__ == "__main__":
    fix_convoco()
