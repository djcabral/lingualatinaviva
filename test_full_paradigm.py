from utils.latin_logic import LatinMorphology

def verify():
    print("Verifying Full Verb Paradigm...")
    morph = LatinMorphology()
    
    # Test 1: 1st Conjugation (amo)
    # amo, amāre, amāvi, amātum
    forms_1 = morph.conjugate_verb("amo", "1", "amo, amāre, amāvi, amātum")
    
    # Future Active
    assert forms_1["fut_1sg"] == "amābō", f"Expected amābō, got {forms_1.get('fut_1sg')}"
    # Pluperfect Active
    assert forms_1["plup_1sg"] == "amāveram", f"Expected amāveram, got {forms_1.get('plup_1sg')}"
    # Future Perfect Active
    assert forms_1["futperf_1sg"] == "amāverō", f"Expected amāverō, got {forms_1.get('futperf_1sg')}"
    
    # Future Passive
    assert forms_1["fut_pass_1sg"] == "amābor", f"Expected amābor, got {forms_1.get('fut_pass_1sg')}"
    
    # Perfect Subjunctive Active
    assert forms_1["perf_subj_1sg"] == "amāverim", f"Expected amāverim, got {forms_1.get('perf_subj_1sg')}"
    # Pluperfect Subjunctive Active
    assert forms_1["plup_subj_1sg"] == "amāvissem", f"Expected amāvissem, got {forms_1.get('plup_subj_1sg')}"
    
    # Perfect Subjunctive Passive
    assert forms_1["perf_subj_pass_1sg"] == "amātum sim", f"Expected amātum sim, got {forms_1.get('perf_subj_pass_1sg')}"
    # Pluperfect Subjunctive Passive
    assert forms_1["plup_subj_pass_1sg"] == "amātum essem", f"Expected amātum essem, got {forms_1.get('plup_subj_pass_1sg')}"
    
    print("✅ 1st Conjugation: OK")
    
    # Test 2: 3rd Conjugation (rego)
    # regō, regere, rēxī, rēctum
    forms_3 = morph.conjugate_verb("rego", "3", "regō, regere, rēxī, rēctum")
    
    # Future Active (3rd conj uses -am, -es...)
    assert forms_3["fut_1sg"] == "regam", f"Expected regam, got {forms_3.get('fut_1sg')}"
    assert forms_3["fut_2sg"] == "regēs", f"Expected regēs, got {forms_3.get('fut_2sg')}"
    
    # Future Passive
    assert forms_3["fut_pass_1sg"] == "regar", f"Expected regar, got {forms_3.get('fut_pass_1sg')}"
    assert forms_3["fut_pass_2sg"] == "regēris", f"Expected regēris, got {forms_3.get('fut_pass_2sg')}"
    
    print("✅ 3rd Conjugation: OK")
    
    print("🎉 Full Paradigm Verified!")

if __name__ == "__main__":
    verify()
