import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.latin_logic import LatinMorphology

def test_passive():
    print("=== Testing Passive Voice ===\n")
    
    # Test 1st conjugation
    print("1. amō (1st conjugation)")
    forms = LatinMorphology.conjugate_verb("amō", "1", "amō, amāre, amāvī, amātum")
    print(f"   Present Passive: {forms.get('pres_pass_1sg')}, {forms.get('pres_pass_2sg')}, {forms.get('pres_pass_3sg')}")
    print(f"   Imperfect Passive: {forms.get('imp_pass_1sg')}, {forms.get('imp_pass_2sg')}, {forms.get('imp_pass_3sg')}")
    print(f"   Perfect Passive: {forms.get('perf_pass_1sg')}, {forms.get('perf_pass_3sg')}")
    print()
    
    # Test 2nd conjugation
    print("2. moneō (2nd conjugation)")
    forms = LatinMorphology.conjugate_verb("moneō", "2", "moneō, monēre, monuī, monitum")
    print(f"   Present Passive: {forms.get('pres_pass_1sg')}, {forms.get('pres_pass_2sg')}, {forms.get('pres_pass_3sg')}")
    print(f"   Perfect Passive: {forms.get('perf_pass_1sg')}")
    print()
    
    # Test 3rd conjugation
    print("3. regō (3rd conjugation)")
    forms = LatinMorphology.conjugate_verb("regō", "3", "regō, regere, rēxī, rēctum")
    print(f"   Present Passive: {forms.get('pres_pass_1sg')}, {forms.get('pres_pass_2sg')}, {forms.get('pres_pass_3sg')}")
    print(f"   Perfect Passive: {forms.get('perf_pass_1sg')}")
    print()
    
    # Test 4th conjugation
    print("4. audiō (4th conjugation)")
    forms = LatinMorphology.conjugate_verb("audiō", "4", "audiō, audīre, audīvī, audītum")
    print(f"   Present Passive: {forms.get('pres_pass_1sg')}, {forms.get('pres_pass_2sg')}, {forms.get('pres_pass_3sg')}")
    print(f"   Perfect Passive: {forms.get('perf_pass_1sg')}")
    print()
    
    print("✅ Passive voice forms generated successfully!")

if __name__ == "__main__":
    test_passive()
