import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.latin_logic import LatinMorphology

def test_demonstratives():
    print("=== Testing Demonstrative Pronouns ===\n")
    
    pronouns = ["is", "hic", "ille", "iste"]
    
    for pron in pronouns:
        print(f"{pron}:")
        forms = LatinMorphology.decline_pronoun(pron)
        print(f"  Nom sg (m/f/n): {forms.get('nom_sg_m')} / {forms.get('nom_sg_f')} / {forms.get('nom_sg_n')}")
        print(f"  Gen sg (all):   {forms.get('gen_sg_m')}")
        print(f"  Acc sg (m/f/n): {forms.get('acc_sg_m')} / {forms.get('acc_sg_f')} / {forms.get('acc_sg_n')}")
        print(f"  Nom pl (m/f/n): {forms.get('nom_pl_m')} / {forms.get('nom_pl_f')} / {forms.get('nom_pl_n')}")
        print()
    
    print("✅ All demonstratives declined successfully!")

if __name__ == "__main__":
    test_demonstratives()
