import sys
import os
import json
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import engine
from database import Word

def fix_dare():
    print("Fixing 'dare' conjugation...")
    
    irregular_forms = {
        # Present (note short 'a' in damus, datis, dant)
        "pres_1sg": "dō",
        "pres_2sg": "dās",
        "pres_3sg": "dat",
        "pres_1pl": "damus",
        "pres_2pl": "datis",
        "pres_3pl": "dant",
        
        # Imperfect (regular)
        "imp_1sg": "dabam",
        "imp_2sg": "dabās",
        "imp_3sg": "dabat",
        "imp_1pl": "dabāmus",
        "imp_2pl": "dabātis",
        "imp_3pl": "dabant",
        
        # Perfect (regular-ish)
        "perf_1sg": "dedī",
        "perf_2sg": "dedistī",
        "perf_3sg": "dedit",
        "perf_1pl": "dedimus",
        "perf_2pl": "dedistis",
        "perf_3pl": "dedērunt"
    }
    
    with Session(engine) as session:
        # Find 'dare'
        word = session.exec(select(Word).where(Word.latin == "dare")).first()
        if word:
            print(f"Found word: {word.latin} (ID: {word.id})")
            word.irregular_forms = json.dumps(irregular_forms)
            word.conjugation = "irregular" # Mark as irregular to be safe
            session.add(word)
            session.commit()
            print("✅ Updated 'dare' with explicit irregular forms.")
        else:
            print("❌ Word 'dare' not found.")

if __name__ == "__main__":
    fix_dare()
