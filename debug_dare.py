import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.latin_logic import LatinMorphology
from database import Word

def debug_dare():
    # Simulate the Word object for 'dare'
    # dare: dō, dare, dedī, datum (1st conj)
    word = Word(
        latin="dare", # The user might have entered 'dare' as the main form, or 'dō'
        translation="dar",
        part_of_speech="verb",
        principal_parts="dō, dare, dedī, datum",
        conjugation="1"
    )
    
    print(f"Debugging verb: {word.latin}")
    print(f"Principal parts: {word.principal_parts}")
    
    forms = LatinMorphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts)
    
    print("\nGenerated Forms:")
    for key, value in forms.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    debug_dare()
