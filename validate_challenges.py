"""
Script to validate challenge content integrity and correctness.
"""
import sys
import os
import json
import re
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import Challenge, Word
from utils.latin_logic import LatinMorphology
from sqlmodel import select

def normalize_text(text: str) -> str:
    return text.lower().strip()

def extract_case_from_option(option_text: str) -> str:
    """Maps Spanish option text to internal case code."""
    text = normalize_text(option_text)
    if 'nominativo' in text: return 'nom'
    if 'genitivo' in text: return 'gen'
    if 'dativo' in text: return 'dat'
    if 'acusativo' in text: return 'acc'
    if 'ablativo' in text: return 'abl'
    if 'vocativo' in text: return 'voc'
    return None

def validate_challenges():
    session = get_session()
    challenges = session.exec(select(Challenge)).all()
    
    print(f"🔍 Validating {len(challenges)} challenges...\n")
    
    issues_found = 0
    
    for challenge in challenges:
        try:
            config_list = json.loads(challenge.config_json)
            if not isinstance(config_list, list):
                config_list = [config_list]
                
            for stage_idx, config in enumerate(config_list):
                context = f"Challenge #{challenge.id} ({challenge.title}) - Stage {stage_idx+1}"
                
                # 1. Validate Declension/Conjugation Words Exist
                if challenge.challenge_type == 'declension':
                    word_latin = config.get('word')
                    word = session.exec(select(Word).where(Word.latin == word_latin)).first()
                    if not word:
                        print(f"❌ {context}: Word '{word_latin}' not found in database.")
                        issues_found += 1
                    else:
                        # Verify generation doesn't crash
                        try:
                            forms = LatinMorphology.decline_noun(
                                word.latin, word.declension, word.gender, word.genitive,
                                word.irregular_forms, word.parisyllabic, 
                                word.is_plurale_tantum, word.is_singulare_tantum
                            )
                            if not forms:
                                print(f"⚠️ {context}: LatinMorphology returned empty forms for '{word_latin}'.")
                                issues_found += 1
                        except Exception as e:
                            print(f"❌ {context}: Error generating forms for '{word_latin}': {e}")
                            issues_found += 1

                elif challenge.challenge_type == 'conjugation':
                    verb_latin = config.get('verb')
                    verb = session.exec(select(Word).where(Word.latin == verb_latin)).first()
                    if not verb:
                        print(f"❌ {context}: Verb '{verb_latin}' not found in database.")
                        issues_found += 1
                    else:
                        try:
                            forms = LatinMorphology.conjugate_verb(
                                verb.latin, verb.conjugation, verb.principal_parts, verb.irregular_forms
                            )
                            if not forms:
                                print(f"⚠️ {context}: LatinMorphology returned empty forms for '{verb_latin}'.")
                                issues_found += 1
                        except Exception as e:
                            print(f"❌ {context}: Error generating forms for '{verb_latin}': {e}")
                            issues_found += 1

                # 2. Validate Multiple Choice Logic
                elif challenge.challenge_type == 'multiple_choice':
                    questions = config.get('questions', [])
                    for q_idx, q in enumerate(questions):
                        q_text = q.get('text', '')
                        options = q.get('options', [])
                        correct_idx = q.get('correct')
                        
                        # Check index bounds
                        if not isinstance(correct_idx, int) or correct_idx < 0 or correct_idx >= len(options):
                            print(f"❌ {context}: Question {q_idx+1} has invalid correct index {correct_idx} (Options: {len(options)}).")
                            issues_found += 1
                            continue
                            
                        # Heuristic: Check for "What case is 'word'?" pattern
                        # Regex to find quoted word: 'word' or "word"
                        match = re.search(r"['\"](\w+)['\"]", q_text)
                        if match:
                            target_form = match.group(1)
                            
                            # Try to find this form in the DB (reverse lookup would be ideal, but let's try strict match on known words for now)
                            # This is hard without context. Let's assume the question implies a specific word if we can guess it.
                            # For now, let's just check if the "correct" option makes sense if it's a case question.
                            
                            correct_option = options[correct_idx]
                            claimed_case = extract_case_from_option(correct_option)
                            
                            if claimed_case:
                                # The question claims 'target_form' is 'claimed_case'.
                                # Let's see if we can verify that.
                                # We need to know the LEMMA to verify. 
                                # If we can't find the lemma, we skip deep validation but warn.
                                pass 
                                # (Deep validation requires knowing the lemma, which isn't in the config for MC questions usually)
                        
                        # Check for "Todas las anteriores" logic errors (like the rosae one)
                        # If "Todas las anteriores" is correct, verify if other options are mutually exclusive?
                        # Hard to automate without deep semantic understanding.
                        
                        # Specific check for the "rosae" error pattern (Singular + Nominative)
                        if "rosae" in q_text and "singular" in q_text.lower():
                            # Rosae is Gen/Dat Sg, Nom/Voc Pl.
                            # If option says "Nominativo" and is marked correct -> ERROR
                            if "Nominativo" in options[correct_idx]:
                                print(f"❌ {context}: Question '{q_text}' marks 'Nominativo' as correct for 'rosae' (singular). This is incorrect.")
                                issues_found += 1

        except json.JSONDecodeError:
            print(f"❌ Challenge #{challenge.id}: Invalid JSON config.")
            issues_found += 1
        except Exception as e:
            print(f"❌ Challenge #{challenge.id}: Unexpected error: {e}")
            issues_found += 1
            
    if issues_found == 0:
        print("✅ No issues found in challenges!")
    else:
        print(f"\nFound {issues_found} potential issues.")

if __name__ == "__main__":
    validate_challenges()
