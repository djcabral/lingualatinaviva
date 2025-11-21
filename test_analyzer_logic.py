def construct_tag(tense, person, number, mood, voice):
    tense_map = {"Presente": "pres", "Imperfecto": "imp", "Perfecto": "perf"}
    number_map = {"Singular": "sg", "Plural": "pl"}
    person_map = {"1ª": "1", "2ª": "2", "3ª": "3"}
    
    if mood == "Imperativo":
        prefix = "imv"
        if voice == "Pasiva":
            prefix += "_pass"
        # Imperative uses fixed person/tense logic in the app, but let's test the construction
        return f"{prefix}_{person_map[person]}{number_map[number]}"
    else:
        prefix = tense_map[tense]
        if mood == "Subjuntivo":
            prefix += "_subj"
        if voice == "Pasiva":
            prefix += "_pass"
        return f"{prefix}_{person_map[person]}{number_map[number]}"

def verify():
    print("Verifying Tag Construction...")
    
    # Test 1: Present Active Indicative
    tag = construct_tag("Presente", "1ª", "Singular", "Indicativo", "Activa")
    assert tag == "pres_1sg", f"Expected pres_1sg, got {tag}"
    print("✅ Present Active Indicative: OK")
    
    # Test 2: Imperfect Subjunctive Passive
    tag = construct_tag("Imperfecto", "3ª", "Plural", "Subjuntivo", "Pasiva")
    assert tag == "imp_subj_pass_3pl", f"Expected imp_subj_pass_3pl, got {tag}"
    print("✅ Imperfect Subjunctive Passive: OK")
    
    # Test 3: Imperative Active
    tag = construct_tag("Presente", "2ª", "Singular", "Imperativo", "Activa")
    assert tag == "imv_2sg", f"Expected imv_2sg, got {tag}"
    print("✅ Imperative Active: OK")
    
    # Test 4: Imperative Passive
    tag = construct_tag("Presente", "2ª", "Plural", "Imperativo", "Pasiva")
    assert tag == "imv_pass_2pl", f"Expected imv_pass_2pl, got {tag}"
    print("✅ Imperative Passive: OK")
    
    print("🎉 All tags constructed correctly!")

if __name__ == "__main__":
    verify()
