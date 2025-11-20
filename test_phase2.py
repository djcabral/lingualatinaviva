from utils.latin_logic import LatinMorphology
import json
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_irregular_forms():
    print("Verificando formas irregulares...\n")
    
    # Test Case 1: Filia (dat/abl pl: filiabus)
    print("1. Testing 'filia' (1st decl, irregular dat/abl pl)...")
    irregular_json = json.dumps({"dat_pl": "filiābus", "abl_pl": "filiābus"})
    forms = LatinMorphology.decline_noun("filia", "1", "f", "filiae", irregular_json)
    
    assert forms["dat_pl"] == "filiābus", f"Expected filiābus, got {forms['dat_pl']}"
    assert forms["abl_pl"] == "filiābus", f"Expected filiābus, got {forms['abl_pl']}"
    assert forms["nom_sg"] == "filia", f"Expected filia, got {forms['nom_sg']}"
    print("   ✅ Filia passed (filiābus correctly generated)")

    # Test Case 2: Domus (4th/2nd mixed)
    print("\n2. Testing 'domus' (Mixed 4th/2nd)...")
    domus_json = json.dumps({
        "abl_sg": "domō",
        "acc_pl": "domōs",
        "gen_pl": "domuum",
        "loc_sg": "domī"
    })
    forms = LatinMorphology.decline_noun("domus", "4", "f", "domūs", domus_json)
    
    assert forms["abl_sg"] == "domō", f"Expected domō, got {forms['abl_sg']}"
    assert forms["acc_pl"] == "domōs", f"Expected domōs, got {forms['acc_pl']}"
    assert forms["gen_sg"] == "domūs", f"Expected domūs (regular 4th), got {forms['gen_sg']}"
    print("   ✅ Domus passed (mixed forms correctly generated)")

    # Test Case 3: Vis (Irregular)
    print("\n3. Testing 'vis' (Irregular)...")
    vis_json = json.dumps({
        "nom_sg": "vīs", "acc_sg": "vim", "abl_sg": "vī",
        "nom_pl": "vīrēs", "gen_pl": "vīrium", "dat_pl": "vīribus",
        "acc_pl": "vīrēs", "abl_pl": "vīribus"
    })
    forms = LatinMorphology.decline_noun("vis", "3", "f", "—", vis_json)
    
    assert forms["acc_sg"] == "vim", f"Expected vim, got {forms['acc_sg']}"
    assert forms["gen_pl"] == "vīrium", f"Expected vīrium, got {forms['gen_pl']}"
    print("   ✅ Vis passed (fully irregular forms generated)")

    print("\n🎉 All Phase 2 verification tests passed!")

if __name__ == "__main__":
    verify_irregular_forms()
