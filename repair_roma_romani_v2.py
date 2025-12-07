import sys
import json
from sqlmodel import Session, select
from database import engine, Word, InflectedForm
from utils.collatinus_analyzer import LatinMorphAnalyzer

def repair_database():
    with Session(engine) as session:
        analyzer = LatinMorphAnalyzer()
        
        # 1. Restore "Roma" (Proper Noun)
        print("\n--- Repairing 'Roma' ---")
        roma_word = session.exec(select(Word).where(Word.latin == "Roma")).first()
        
        if not roma_word:
            print("Creating Word entry for 'Roma'...")
            roma_word = Word(
                latin="Roma",
                translation="Roma",
                definition_es="Roma",
                part_of_speech="proper_noun",
                type="proper_noun",
                gender="fem",
                declension="1",
                is_singulare_tantum=True,
                status="active"
            )
            session.add(roma_word)
            session.commit()
            session.refresh(roma_word)
            print(f"Created Word 'Roma' (ID: {roma_word.id})")
        else:
            print(f"'Roma' already exists (ID: {roma_word.id})")

        # Link orphaned forms for Roma
        forms_to_fix = session.exec(select(InflectedForm).where(InflectedForm.form.in_(["Roma", "Romae", "Romam"]))).all()
        for form in forms_to_fix:
            if not form.word_id or not session.get(Word, form.word_id):
                print(f"Fixing orphaned form '{form.form}' (Old ID: {form.word_id}) -> New ID: {roma_word.id}")
                form.word_id = roma_word.id
                session.add(form)
        
        # 2. Add "Romani" (Noun) - The people
        print("\n--- Repairing 'Romani' (Noun) ---")
        romani_word = session.exec(select(Word).where(Word.latin == "Romani", Word.part_of_speech == "noun")).first()
        
        if not romani_word:
            print("Creating Word entry for 'Romani' (Noun)...")
            romani_word = Word(
                latin="Romani",
                translation="romans",
                definition_es="los romanos",
                part_of_speech="noun",
                type="noun", 
                gender="masc",
                declension="2",
                is_plurale_tantum=True,
                status="active"
            )
            session.add(romani_word)
            session.commit()
            session.refresh(romani_word)
            print(f"Created Word 'Romani' (ID: {romani_word.id})")
        else:
            print(f"'Romani' Word already exists (ID: {romani_word.id})")

        # Link ORPHANED "Romani" forms (like ID 564)
        orphaned_romani = session.exec(select(InflectedForm).where(InflectedForm.form == "Romani")).all()
        for form in orphaned_romani:
            if not form.word_id or not session.get(Word, form.word_id):
                 # Verify it matches our morphology roughly (Nominative Plural)
                 print(f"Fixing orphaned form '{form.form}' (Old ID: {form.word_id}) -> New ID: {romani_word.id}")
                 form.word_id = romani_word.id
                 session.add(form)

        # Check for missing forms on the new Romani word
        existing_forms_count = session.exec(select(InflectedForm).where(InflectedForm.word_id == romani_word.id)).all()
        if len(existing_forms_count) < 5:
            print("Populating missing forms for Romani...")
            forms_list = [
                ("Romani", {"case": "nom", "number": "plur", "gender": "masc"}),
                ("Romani", {"case": "voc", "number": "plur", "gender": "masc"}),
                ("Romanos", {"case": "acc", "number": "plur", "gender": "masc"}),
                ("Romanorum", {"case": "gen", "number": "plur", "gender": "masc"}),
                ("Romanis", {"case": "dat", "number": "plur", "gender": "masc"}),
                ("Romanis", {"case": "abl", "number": "plur", "gender": "masc"}),
            ]
            
            for form_text, morph in forms_list:
                # Check if this specific form/morph exists for this word
                # (Simple check)
                exists = False
                for existing in existing_forms_count:
                    if existing.form == form_text and existing.morphology == json.dumps(morph):
                        exists = True
                        break
                
                if not exists:
                    print(f"Adding form '{form_text}'...")
                    new_form = InflectedForm(
                        word_id=romani_word.id,
                        form=form_text,
                        normalized_form=form_text.lower(),
                        morphology=json.dumps(morph)
                    )
                    session.add(new_form)

        session.commit()
        print("\n✅ Repair complete.")

if __name__ == "__main__":
    repair_database()
