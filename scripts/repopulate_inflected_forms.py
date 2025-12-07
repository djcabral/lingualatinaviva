
import sys
import os
import json
from sqlmodel import select, delete

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Word, InflectedForm
from utils.latin_logic import LatinMorphology

def populate_inflected_forms():
    print("🚀 Starting InflectedForm population...")
    
    with get_session() as session:
        # Clear existing forms to avoid duplicates
        print("Cleaning up old InflectedForm entries...")
        session.exec(delete(InflectedForm))
        session.commit()
        
        words = session.exec(select(Word)).all()
        print(f"Found {len(words)} words to process.")
        
        count = 0
        error_count = 0
        
        for word in words:
            forms_map = {}
            
            try:
                if word.part_of_speech == "noun" and word.declension:
                    forms_map = LatinMorphology.decline_noun(
                        word.latin, 
                        word.declension, 
                        word.gender, 
                        word.genitive,
                        irregular_forms=word.irregular_forms if hasattr(word, 'irregular_forms') else None,
                        parisyllabic=word.parisyllabic if hasattr(word, 'parisyllabic') else None
                    )
                elif word.part_of_speech == "verb" and word.conjugation:
                    forms_map = LatinMorphology.conjugate_verb(
                        word.latin,
                        word.conjugation,
                        word.principal_parts,
                        irregular_forms=word.irregular_forms if hasattr(word, 'irregular_forms') else None
                    )

                    
                    # Also add participles if we want them as separate entries or handle them?
                    # The analyzer logic looks for normalized_form in InflectedForm.
                    
                elif word.part_of_speech == "adjective" and word.declension:
                    forms_map = LatinMorphology.decline_adjective(
                        word.latin,
                        word.declension,
                        word.gender,
                        word.genitive
                    )
                elif word.part_of_speech == "pronoun":
                    forms_map = LatinMorphology.decline_pronoun(word.latin)

                # Save forms
                for form_key, form_val in forms_map.items():
                    # form_val could be comma separated if multiple variations? No, usually single string.
                    # normalize
                    if not form_val or form_val == "—":
                        continue
                        
                    norm = LatinMorphology.normalize_latin(form_val)
                    
                    # Create InflectedForm
                    # We store morphology as JSON. 
                    # Structure: {"case": "nom", "number": "sg"} etc derived from form_key
                    
                    morph_data = parse_morphology_key(form_key, word.part_of_speech)
                    
                    # Ensure database schema compliance
                    if not form_val:
                        print(f"Skipping empty form for {word.latin} ({form_key})")
                        continue

                    inf_form = InflectedForm(
                        word_id=word.id,
                        form=form_val,
                        normalized_form=norm,
                        morphology=json.dumps(morph_data)
                    )
                    session.add(inf_form)
                    count += 1
            
                session.commit() # Commit success for this word
            
            except Exception as e:
                print(f"Error processing {word.latin}: {e}")
                error_count += 1
                session.rollback() # Rollback the transaction on error to allow continuing

                
        session.commit()
        print(f"✅ Generated {count} inflected forms.")
        print(f"❌ Errors: {error_count}")

def parse_morphology_key(key: str, pos: str) -> dict:
    """Parses keys like 'nom_sg', 'pres_3sg' into dict"""
    data = {}
    parts = key.split('_')
    
    if pos == "noun" or pos == "pronoun" or pos == "adjective":
        # nom_sg, gen_pl
        if len(parts) >= 2:
            data["case"] = parts[0] # nom, gen, etc
            data["number"] = parts[1] # sg, pl
            
    elif pos == "verb":
        # pres_1sg, pres_subj_1sg, perf_pass_1sg
        # This is a bit complex parsing, let's do best effort
        if "pass" in key:
            data["voice"] = "pass"
        else:
            data["voice"] = "act"
            
        if "subj" in key:
            data["mood"] = "subj"
        elif "imv" in key:
            data["mood"] = "imv"
        else:
            data["mood"] = "ind"
            
        # Tense
        if key.startswith("pres"): data["tense"] = "pres"
        elif key.startswith("imp"): data["tense"] = "imp"
        elif key.startswith("futperf"): data["tense"] = "futperf" # Must check before fut
        elif key.startswith("fut"): data["tense"] = "fut"
        elif key.startswith("plup"): data["tense"] = "plup"
        elif key.startswith("perf"): data["tense"] = "perf"
        
        # Person/Number usually at the end: 1sg
        last = parts[-1]
        if '1' in last or '2' in last or '3' in last:
            data["person"] = last[0]
            data["number"] = last[1:]
            
    return data

if __name__ == "__main__":
    populate_inflected_forms()
