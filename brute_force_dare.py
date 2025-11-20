import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.latin_logic import LatinMorphology

def brute_force():
    print("Searching for 'dare' in conjugation outputs...")
    
    # Test various conjugations and principal parts
    test_parts = [
        "dō, dare, dedī, datum",
        "do, dare, dedi, datum",
        "dare, dare, dedi, datum",
        "d, dare, dedi, datum"
    ]
    
    conjs = ["1", "2", "3", "4", "irregular"]
    
    found = False
    for pp in test_parts:
        for conj in conjs:
            forms = LatinMorphology.conjugate_verb("dare", conj, pp)
            for key, value in forms.items():
                if value == "dare" or value == "dāre":
                    print(f"FOUND! PP='{pp}', Conj='{conj}' -> {key}: {value}")
                    found = True
                    
    if not found:
        print("Not found in standard logic.")

if __name__ == "__main__":
    brute_force()
