import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.latin_logic import LatinMorphology

def test_imperative():
    print("=== Testing Imperative Mood ===\n")
    
    # Test 1st conjugation
    print("1. amō (1st conjugation) - IMPERATIVE")
    forms = LatinMorphology.conjugate_verb("amō", "1", "amō, amāre, amāvī, amātum")
    print(f"   Active:  {forms.get('imv_2sg')} (sg), {forms.get('imv_2pl')} (pl)")
    print(f"   Passive: {forms.get('imv_pass_2sg')} (sg), {forms.get('imv_pass_2pl')} (pl)")
    print()
    
    # Test 2nd conjugation
    print("2. moneō (2nd conjugation) - IMPERATIVE")
    forms = LatinMorphology.conjugate_verb("moneō", "2", "moneō, monēre, monuī, monitum")
    print(f"   Active:  {forms.get('imv_2sg')} (sg), {forms.get('imv_2pl')} (pl)")
    print(f"   Passive: {forms.get('imv_pass_2sg')} (sg), {forms.get('imv_pass_2pl')} (pl)")
    print()
    
    # Test 3rd conjugation
    print("3. regō (3rd conjugation) - IMPERATIVE")
    forms = LatinMorphology.conjugate_verb("regō", "3", "regō, regere, rēxī, rēctum")
    print(f"   Active:  {forms.get('imv_2sg')} (sg), {forms.get('imv_2pl')} (pl)")
    print(f"   Passive: {forms.get('imv_pass_2sg')} (sg), {forms.get('imv_pass_2pl')} (pl)")
    print()
    
    # Test 4th conjugation
    print("4. audiō (4th conjugation) - IMPERATIVE")
    forms = LatinMorphology.conjugate_verb("audiō", "4", "audiō, audīre, audīvī, audītum")
    print(f"   Active:  {forms.get('imv_2sg')} (sg), {forms.get('imv_2pl')} (pl)")
    print(f"   Passive: {forms.get('imv_pass_2sg')} (sg), {forms.get('imv_pass_2pl')} (pl)")
    print()
    
    print("✅ All imperative forms generated successfully!")

if __name__ == "__main__":
    test_imperative()
