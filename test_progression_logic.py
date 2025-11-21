def get_available_options(user_level):
    if user_level == 1:
        return ["1", "2"], ["noun"]
    elif user_level == 2:
        return ["1", "2"], ["noun", "adjective"]
    elif user_level == 3:
        return ["1", "2", "3"], ["noun", "adjective"]
    elif user_level == 4:
        return ["1", "2", "3"], ["noun", "adjective", "pronoun"]
    else:
        return ["1", "2", "3", "4", "5"], ["noun", "adjective", "pronoun"]

def verify():
    print("Verifying Progression Logic...")
    
    # Level 1
    decls, pos = get_available_options(1)
    assert "adjective" not in pos, "Level 1 should not have adjectives"
    assert "pronoun" not in pos, "Level 1 should not have pronouns"
    print("✅ Level 1: OK")
    
    # Level 2
    decls, pos = get_available_options(2)
    assert "adjective" in pos, "Level 2 MUST have adjectives"
    assert "pronoun" not in pos, "Level 2 should not have pronouns"
    print("✅ Level 2: OK")
    
    # Level 3
    decls, pos = get_available_options(3)
    assert "3" in decls, "Level 3 MUST have 3rd declension"
    assert "pronoun" not in pos, "Level 3 should not have pronouns"
    print("✅ Level 3: OK")
    
    # Level 4
    decls, pos = get_available_options(4)
    assert "pronoun" in pos, "Level 4 MUST have pronouns"
    print("✅ Level 4: OK")
    
    print("🎉 Logic verified!")

if __name__ == "__main__":
    verify()
