from utils.latin_logic import LatinMorphology
import json
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_irregular_verbs():
    print("Verificando verbos irregulares...\n")
    
    # Test Case 1: Sum (Irregular)
    print("1. Testing 'sum'...")
    sum_json = json.dumps({
        "pres_1sg": "sum", "pres_2sg": "es", "pres_3sg": "est",
        "pres_1pl": "sumus", "pres_2pl": "estis", "pres_3pl": "sunt",
        "imp_1sg": "eram", "imp_2sg": "erās", "imp_3sg": "erat",
        "imp_1pl": "erāmus", "imp_2pl": "erātis", "imp_3pl": "erant"
    })
    forms = LatinMorphology.conjugate_verb("sum", "irregular", "sum, esse, fuī, futūrus", sum_json)
    
    assert forms["pres_1sg"] == "sum", f"Expected sum, got {forms.get('pres_1sg')}"
    assert forms["pres_3pl"] == "sunt", f"Expected sunt, got {forms.get('pres_3pl')}"
    assert forms["imp_1sg"] == "eram", f"Expected eram, got {forms.get('imp_1sg')}"
    assert forms["perf_1sg"] == "fuī", f"Expected fuī, got {forms.get('perf_1sg')}" # Regular perfect
    print("   ✅ Sum passed")

    # Test Case 2: Fero (Irregular)
    print("\n2. Testing 'ferō'...")
    fero_json = json.dumps({
        "pres_1sg": "ferō", "pres_2sg": "fers", "pres_3sg": "fert",
        "pres_1pl": "ferimus", "pres_2pl": "fertis", "pres_3pl": "ferunt"
    })
    forms = LatinMorphology.conjugate_verb("ferō", "irregular", "ferō, ferre, tulī, lātum", fero_json)
    
    assert forms["pres_2sg"] == "fers", f"Expected fers, got {forms.get('pres_2sg')}"
    assert forms["pres_3sg"] == "fert", f"Expected fert, got {forms.get('pres_3sg')}"
    assert forms["perf_1sg"] == "tulī", f"Expected tulī, got {forms.get('perf_1sg')}"
    print("   ✅ Fero passed")

    print("\n🎉 All Phase 3 verification tests passed!")

if __name__ == "__main__":
    verify_irregular_verbs()
