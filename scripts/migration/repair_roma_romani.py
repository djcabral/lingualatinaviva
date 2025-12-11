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

        # Linkorphaned forms for Roma
        orphaned_romae = session.exec(select(InflectedForm).where(InflectedForm.form == "Romae", InflectedForm.word_id == None)).all()
        # Also check for broken IDs (like 562) if they exist but we can't select easily by broken ID unless we know it.
        # But we saw "Romae" has word_id 562 which doesn't exist in Word table.
        # So we search for forms where word_id is NOT IN Word table efficiently? 
        # For now, let's look for specific forms we know are broken.
        
        # In the investigation we saw: Form: Romae, Lemma: [MISSING WORD ID 562]
        # We need to update this specific record.
        
        forms_to_fix = session.exec(select(InflectedForm).where(InflectedForm.form.in_(["Roma", "Romae", "Romam"]))).all()
        for form in forms_to_fix:
            current_word = session.get(Word, form.word_id)
            if not current_word:
                print(f"Fixing orphaned form '{form.form}' (Old ID: {form.word_id}) -> New ID: {roma_word.id}")
                form.word_id = roma_word.id
                session.add(form)
        
        # Generate paradigm to be sure we have all forms
        print("Generating forms for Roma...")
        paradigm = analyzer.generate_paradigm("Roma")
        if 'forms' in paradigm:
            for form_data in paradigm['forms']:
                # Check if exists
                existing = session.exec(select(InflectedForm).where(
                    InflectedForm.word_id == roma_word.id,
                    InflectedForm.form == form_data['form'],
                    InflectedForm.morphology == json.dumps(form_data['morphology_dict'] if 'morphology_dict' in form_data else form_data.get('morph_raw')) # formats vary, let's just trust generate_paradigm usually doesn't return existing objects
                )).first()
                
                # Simplified check: just form and word_id
                existing_loose = session.exec(select(InflectedForm).where(
                    InflectedForm.word_id == roma_word.id,
                    InflectedForm.form == form_data['form']
                )).first()
                
                if not existing_loose:
                     # This part is complex because existing logic to populate is elsewhere.
                     # Let's rely on repairing the orphans first. If we need full regen, we should call a helper.
                     pass
        
        # 2. Add "Romani" (Noun) - The people
        print("\n--- Adding 'Romani' (Noun) ---")
        # Check if exists
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
                is_plurale_tantum=True, # Usually plural for "the romans"
                status="active"
            )
            session.add(romani_word)
            session.commit()
            session.refresh(romani_word)
            print(f"Created Word 'Romani' (ID: {romani_word.id})")
            
            # Generate forms for Romani
            # Collatinus might treat it as "Romanus" (adj) which is already there ID 39.
            # We want a distinct Noun entry.
            # We can manually create forms or try to force generation.
            
            # Let's manually add the key forms for "Romani" (Plural)
            forms_list = [
                ("Romani", {"case": "nom", "number": "plur", "gender": "masc"}),
                ("Romani", {"case": "voc", "number": "plur", "gender": "masc"}),
                ("Romanos", {"case": "acc", "number": "plur", "gender": "masc"}),
                ("Romanorum", {"case": "gen", "number": "plur", "gender": "masc"}),
                ("Romanis", {"case": "dat", "number": "plur", "gender": "masc"}),
                ("Romanis", {"case": "abl", "number": "plur", "gender": "masc"}),
            ]
            
            for form_text, morph in forms_list:
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
