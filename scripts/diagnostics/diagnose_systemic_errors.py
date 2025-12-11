import sys
import os
import random
from typing import List, Tuple
from sqlmodel import Session, select, text
from database import engine, Word, InflectedForm, TextWordLink

# Ensure we can import from utils
sys.path.append(os.getcwd())

# Try to import Stanza
try:
    import stanza
    STANZA_AVAILABLE = True
except ImportError:
    STANZA_AVAILABLE = False
    print("⚠️ Stanza not found. Stanza checks will be skipped.")

def diagnose_systemic_errors():
    print("🔍 Starting Systemic Diagnosis...\n")
    
    with Session(engine) as session:
        # 1. Check for Orphaned InflectedForm records
        print("--- 1. Checking for Orphaned InflectedForms ---")
        query_orphaned_forms = text("""
            SELECT count(*) FROM inflectedform 
            WHERE word_id IS NOT NULL 
            AND word_id NOT IN (SELECT id FROM word)
        """)
        orphaned_forms_count = session.exec(query_orphaned_forms).one()
        print(f"Orphaned InflectedForm records: {orphaned_forms_count[0]}")
        if orphaned_forms_count[0] > 0:
             orphan_samples = session.exec(text("""
                SELECT form, word_id FROM inflectedform 
                WHERE word_id IS NOT NULL 
                AND word_id NOT IN (SELECT id FROM word)
                LIMIT 5
             """)).all()
             print(f"   Sample orphans: {orphan_samples}")

        # 2. Check for Orphaned TextWordLink records
        print("\n--- 2. Checking for Orphaned TextWordLinks ---")
        query_orphaned_links = text("""
            SELECT count(*) FROM textwordlink 
            WHERE word_id IS NOT NULL 
            AND word_id NOT IN (SELECT id FROM word)
        """)
        orphaned_links_count = session.exec(query_orphaned_links).one()
        print(f"Orphaned TextWordLink records: {orphaned_links_count[0]}")
        if orphaned_links_count[0] > 0:
            link_samples = session.exec(text("""
                SELECT form, word_id FROM textwordlink 
                WHERE word_id IS NOT NULL 
                AND word_id NOT IN (SELECT id FROM word)
                LIMIT 5
            """)).all()
            print(f"   Sample orphaned links: {link_samples}")

        # 3. Check for Suspicious Adjectives (Capitalized but linked to Adjective)
        print("\n--- 3. Checking for Suspicious Adjectives (Potential Missing Proper Nouns) ---")
        # We look for InflectedForms that start with Uppercase, linked to a Word that is 'adj'
        # And the distinct Word ID count
        
        # SQLite is case sensitive by default for glob/like usually, but let's be pythonic to be sure or use sql logic
        # GLOB '[A-Z]*' in SQLite checks for uppercase start
        query_suspicious = text("""
            SELECT DISTINCT w.id, w.latin, i.form 
            FROM word w
            JOIN inflectedform i ON w.id = i.word_id
            WHERE w.part_of_speech = 'adj'
            AND substr(i.form, 1, 1) GLOB '[A-Z]*'
            ORDER BY w.latin
            LIMIT 20
        """)
        
        suspicious_results = session.exec(query_suspicious).all()
        print(f"Found {len(suspicious_results)} sample suspicious adjectives (Capitalized forms linked to 'adj'):")
        for res in suspicious_results:
            print(f"   Word: {res[1]} (ID: {res[0]}) - Form: {res[2]}")

        # 4. Stanza Cross-Reference
        print("\n--- 4. Stanza Cross-Reference (Sample) ---")
        if STANZA_AVAILABLE:
            try:
                # Initialize Stanza for Latin
                nlp = stanza.Pipeline('la', processors='tokenize,mwt,pos,lemma', use_gpu=False, logging_level='ERROR')
                
                # Get random forms to check
                # Prefer forms that are NOT in the suspicious list to get a general baseline, 
                # but also check some suspicious ones?
                # Let's check generally "TextWordLinks" as that represents actual usage text
                
                links_to_check = session.exec(select(TextWordLink).where(TextWordLink.word_id != None).limit(20)).all()
                if not links_to_check:
                    print("No TextWordLinks found to check.")
                else:
                    mismatches = 0
                    for link in links_to_check:
                        word = session.get(Word, link.word_id)
                        if not word: continue
                        
                        doc = nlp(link.form)
                        # Assume single word
                        if not doc.sentences: continue
                        stanza_word = doc.sentences[0].words[0]
                        stanza_pos = stanza_word.upos
                        
                        # Map our POS types to UPOS roughly for comparison
                        # Our types: noun, proper_noun, adj, verb, adverb, preposition, conjunction, pronoun, numeral
                        # Stanza UPOS: NOUN, PROPN, ADJ, VERB, ADV, ADP, CCONJ/SCONJ, PRON, NUM
                        
                        db_pos_normalized = word.part_of_speech.lower() if word.part_of_speech else "unknown"
                        stanza_pos_normalized = stanza_pos.lower()
                        
                        # Basic mapping for mismatch detection
                        match = False
                        if db_pos_normalized == 'proper_noun' and stanza_pos_normalized == 'propn': match = True
                        elif db_pos_normalized == 'noun' and stanza_pos_normalized == 'noun': match = True
                        elif db_pos_normalized == 'adj' and stanza_pos_normalized == 'adj': match = True
                        elif db_pos_normalized == 'verb' and stanza_pos_normalized == 'verb': match = True
                        elif db_pos_normalized == 'adverb' and stanza_pos_normalized == 'adv': match = True
                        elif 'conj' in db_pos_normalized and 'conj' in stanza_pos_normalized: match = True
                        elif db_pos_normalized == 'preposition' and stanza_pos_normalized == 'adp': match = True
                         # Allow PROPN vs NOUN slack? Stanza is strict on PROPN.
                        elif db_pos_normalized == 'noun' and stanza_pos_normalized == 'propn': match = True # maybe ok
                        elif db_pos_normalized == 'proper_noun' and stanza_pos_normalized == 'noun': match = False # suspicious
                        
                        if not match:
                            mismatches += 1
                            print(f"   [MISMATCH] Form: '{link.form}' | DB: {db_pos_normalized} ({word.latin}) | Stanza: {stanza_pos} ({stanza_word.lemma})")
                    
                    print(f"   Checked {len(links_to_check)} samples. Found {mismatches} mismatches.")

            except Exception as e:
                print(f"   Error running Stanza: {e}")
        else:
            print("   Stanza check skipped.")

if __name__ == "__main__":
    diagnose_systemic_errors()
