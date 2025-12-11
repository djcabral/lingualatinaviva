import sys
import json
from sqlmodel import Session, select
from database import engine, Word, InflectedForm, Text, TextWordLink
from utils.collatinus_analyzer import LatinMorphAnalyzer

def repair_names():
    with Session(engine) as session:
        analyzer = LatinMorphAnalyzer()
        
        # 1. Repair Aemilia (ID 567)
        # It exists but is 'adjective'. Convert to Proper Noun.
        print("\n--- Repairing 'Aemilia' ---")
        aemilia_word = session.exec(select(Word).where(Word.latin == 'Aemilia')).first()
        if aemilia_word:
            print(f"Updating Aemilia (ID: {aemilia_word.id}) from {aemilia_word.part_of_speech} to proper_noun")
            aemilia_word.part_of_speech = 'proper_noun'
            aemilia_word.translation = 'Aemilia'
            aemilia_word.definition_es = 'Aemilia'
            session.add(aemilia_word)
        else:
            print("Aemilia not found! Creating...")
            aemilia_word = Word(
                latin="Aemilia",
                translation="Aemilia",
                definition_es="Aemilia",
                part_of_speech="proper_noun",
                gender="fem",
                declension="1",
                is_singulare_tantum=True,
                status="active"
            )
            session.add(aemilia_word)
            session.commit()
            session.refresh(aemilia_word)

        # 2. Repair Iulia
        # 'Iulia' often links to 'iulius' (adj) ID 570 or 'Iulius' (noun) ID 566
        # We want a dedicated Proper Noun 'Iulia'
        print("\n--- Repairing 'Iulia' ---")
        iulia_word = session.exec(select(Word).where(Word.latin == 'Iulia', Word.part_of_speech == 'proper_noun')).first()
        
        if not iulia_word:
            print("Creating Word entry for 'Iulia'...")
            iulia_word = Word(
                latin="Iulia",
                translation="Julia",
                definition_es="Julia",
                part_of_speech="proper_noun",
                gender="fem",
                declension="1",
                is_singulare_tantum=True,
                status="active"
            )
            session.add(iulia_word)
            session.commit()
            session.refresh(iulia_word)
            print(f"Created Word 'Iulia' (ID: {iulia_word.id})")
        else:
            print(f"'Iulia' already exists (ID: {iulia_word.id})")

        # Relink forms for Iulia
        # Find forms 'Iulia', 'Iuliae', 'Iuliam' associated with other words (like 570)
        forms_to_fix = session.exec(select(InflectedForm).where(InflectedForm.form.in_(["Iulia", "Iuliae", "Iuliam"]))).all()
        for form in forms_to_fix:
            if form.word_id != iulia_word.id:
                print(f"Relinking form '{form.form}' (Old ID: {form.word_id}) -> New ID: {iulia_word.id}")
                form.word_id = iulia_word.id
                session.add(form)
                
        # Generate paradigm for Iulia to ensure all forms exist
        paradigm = analyzer.generate_paradigm("Iulia")
        if 'forms' in paradigm:
             # Basic check to ensure we have the forms
             pass

        session.commit()
        print("\n✅ Name repair complete.")
        
        # 3. Find relevant texts for re-analysis
        print("\n--- Re-analyzing Texts ---")
        # Look for texts containing these names
        target_texts = session.exec(select(Text).where(
            (Text.content.like("%Aemilia%")) | 
            (Text.content.like("%Iulia%"))
        )).all()
        
        print(f"Found {len(target_texts)} texts containing Aemilia/Iulia.")
        
        from utils.stanza_analyzer import analyze_and_save_text
        for text_obj in target_texts:
            print(f"Re-analyzing Text ID {text_obj.id}: {text_obj.title}...")
            try:
                analyze_and_save_text(text_obj.id, text_obj.content, session)
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    repair_names()
