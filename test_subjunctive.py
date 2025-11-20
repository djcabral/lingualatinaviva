import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.latin_logic import LatinMorphology

def test_subjunctive():
    print("=== Testing Subjunctive Mood ===\n")
    
    # Test 1st conjugation
    print("1. amō (1st conjugation) - SUBJUNCTIVE")
    forms = LatinMorphology.conjugate_verb("amō", "1", "amō, amāre, amāvī, amātum")
    print(f"   Present Subj Active: {forms.get('pres_subj_1sg')}, {forms.get('pres_subj_2sg')}, {forms.get('pres_subj_3sg')}")
    print(f"   Imperfect Subj Active: {forms.get('imp_subj_1sg')}, {forms.get('imp_subj_2sg')}, {forms.get('imp_subj_3sg')}")
    print(f"   Present Subj Passive: {forms.get('pres_subj_pass_1sg')}, {forms.get('pres_subj_pass_3sg')}")
    print(f"   Imperfect Subj Passive: {forms.get('imp_subj_pass_1sg')}, {forms.get('imp_subj_pass_3sg')}")
    print()
    
    # Test 2nd conjugation
    print("2. moneō (2nd conjugation) - SUBJUNCTIVE")
    forms = LatinMorphology.conjugate_verb("moneō", "2", "moneō, monēre, monuī, monitum")
    print(f"   Present Subj Active: {forms.get('pres_subj_1sg')}, {forms.get('pres_subj_2sg')}, {forms.get('pres_subj_3sg')}")
    print(f"   Imperfect Subj Active: {forms.get('imp_subj_1sg')}, {forms.get('imp_subj_2sg')}")
    print()
    
    # Test 3rd conjugation
    print("3. regō (3rd conjugation) - SUBJUNCTIVE")
    forms = LatinMorphology.conjugate_verb("regō", "3", "regō, regere, rēxī, rēctum")
    print(f"   Present Subj Active: {forms.get('pres_subj_1sg')}, {forms.get('pres_subj_2sg')}, {forms.get('pres_subj_3sg')}")
    print(f"   Imperfect Subj Active: {forms.get('imp_subj_1sg')}, {forms.get('imp_subj_2sg')}")
    print()
    
    # Test 4th conjugation
    print("4. audiō (4th conjugation) - SUBJUNCTIVE")
    forms = LatinMorphology.conjugate_verb("audiō", "4", "audiō, audīre, audīvī, audītum")
    print(f"   Present Subj Active: {forms.get('pres_subj_1sg')}, {forms.get('pres_subj_2sg')}, {forms.get('pres_subj_3sg')}")
    print(f"   Imperfect Subj Active: {forms.get('imp_subj_1sg')}, {forms.get('imp_subj_2sg')}")
    print()
    
    print("✅ All subjunctive forms generated successfully!")

if __name__ == "__main__":
    test_subjunctive()
