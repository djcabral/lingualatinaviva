"""
Script to reproduce conjugation issues and check for dirty vocabulary.
"""
import sys
import os
from sqlmodel import select

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Word
from utils.latin_logic import LatinMorphology

def check_conjugations():
    print("🔍 Checking Conjugations...")
    morphology = LatinMorphology()
    
    with get_session() as session:
        verbs = session.exec(select(Word).where(Word.part_of_speech == "verb")).all()
        print(f"Found {len(verbs)} verbs in database.")
        
        if not verbs:
            print("❌ No verbs found!")
            return

        success_count = 0
        fail_count = 0
        
        for verb in verbs:
            try:
                # Simulate what conjugations_view.py does
                if not verb.principal_parts or not verb.conjugation:
                    print(f"⚠️ Skipping {verb.latin}: Missing parts or conjugation")
                    continue
                    
                forms = morphology.conjugate_verb(verb.latin, verb.conjugation, verb.principal_parts, verb.irregular_forms)
                
                if forms:
                    success_count += 1
                else:
                    print(f"❌ Failed to generate forms for: {verb.latin} (Parts: {verb.principal_parts}, Conj: {verb.conjugation})")
                    fail_count += 1
            except Exception as e:
                print(f"🔥 CRASH on {verb.latin}: {e}")
                fail_count += 1

        print(f"\nResults: {success_count} succeeded, {fail_count} failed.")

def check_dirty_vocabulary():
    print("\n🔍 Checking for dirty vocabulary (e.g. syllaba_1242)...")
    with get_session() as session:
        # Check for words with underscores and digits
        dirty_words = session.exec(select(Word).where(Word.latin.like("%_%"))).all()
        
        count = 0
        for word in dirty_words:
            # Simple check for digit after underscore
            if any(char.isdigit() for char in word.latin):
                count += 1
                if count <= 5:
                    print(f"  Found dirty word: {word.latin} (ID: {word.id})")
        
        print(f"Total dirty words found: {count}")

if __name__ == "__main__":
    check_dirty_vocabulary()
    check_conjugations()
