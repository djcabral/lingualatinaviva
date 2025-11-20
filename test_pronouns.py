import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.latin_logic import LatinMorphology

def test_pronouns():
    print("=== Testing Personal Pronouns ===\n")
    
    pronouns = ["ego", "tū", "nōs", "vōs"]
    
    for pron in pronouns:
        print(f"{pron}:")
        forms = LatinMorphology.decline_pronoun(pron)
        print(f"  Nom sg: {forms.get('nom_sg')}  | Nom pl: {forms.get('nom_pl')}")
        print(f"  Gen sg: {forms.get('gen_sg')}  | Gen pl: {forms.get('gen_pl')}")
        print(f"  Dat sg: {forms.get('dat_sg')}  | Dat pl: {forms.get('dat_pl')}")
        print(f"  Acc sg: {forms.get('acc_sg')}  | Acc pl: {forms.get('acc_pl')}")
        print(f"  Abl sg: {forms.get('abl_sg')}  | Abl pl: {forms.get('abl_pl')}")
        print()
    
    print("✅ All pronouns declined successfully!")

if __name__ == "__main__":
    test_pronouns()
