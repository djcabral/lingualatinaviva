import csv
import os
import re

def count_syllables(word):
    """Count syllables in a Latin word (approximate)."""
    if not word:
        return 0
    # Remove macrons
    word = word.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u')
    # Simple vowel counting (approximate for Latin)
    vowels = 'aeiouyAEIOUY'
    syllables = 0
    prev_was_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllables += 1
        prev_was_vowel = is_vowel
    return max(1, syllables)  # At least 1 syllable

def detect_parisyllabic(nominative, genitive, declension):
    """Detect if a 3rd declension noun is parisyllabic."""
    if declension != '3' or not genitive:
        return None
    
    nom_syllables = count_syllables(nominative)
    gen_syllables = count_syllables(genitive)
    
    # Parisyllabic if nom and gen have same number of syllables
    return nom_syllables == gen_syllables

def clean_data():
    input_path = os.path.join("data", "vocabulary.csv")
    output_path = os.path.join("data", "seed_data.csv")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    print(f"Processing {input_path}...")
    
    seen_words = set()
    cleaned_rows = []
    
    with open(input_path, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = list(reader.fieldnames)
        
        # Add parisyllabic field if not present
        if 'parisyllabic' not in fieldnames:
            fieldnames.append('parisyllabic')
        
        for row in reader:
            # 1. Clean Latin: remove _\d+
            latin_clean = re.sub(r'_\d+$', '', row['latin'])
            row['latin'] = latin_clean
            
            # 2. Clean Translation: remove (var. \d+)
            trans_clean = re.sub(r'\s*\(var\. \d+\)', '', row['translation'])
            row['translation'] = trans_clean
            
            # 3. Normalize Part of Speech
            if row['part_of_speech'] == 'adj':
                row['part_of_speech'] = 'adjective'
            
            # 4. Normalize Adjective Declension
            if row['part_of_speech'] == 'adjective':
                if row['declension'] == '1/2':
                    row['declension'] = '1'
            
            # 5. Detect parisyllabic for 3rd declension nouns
            if row['part_of_speech'] == 'noun' and row.get('declension') == '3':
                is_pari = detect_parisyllabic(row['latin'], row.get('genitive', ''), row.get('declension', ''))
                row['parisyllabic'] = 'TRUE' if is_pari else 'FALSE'
            else:
                row['parisyllabic'] = ''
            
            # Deduplicate based on latin + part_of_speech
            key = (row['latin'], row['part_of_speech'])
            if key not in seen_words:
                seen_words.add(key)
                cleaned_rows.append(row)
            else:
                # print(f"Duplicate rejected: {key}")
                pass
                
    print(f"Total rows read: {reader.line_num}")
    print(f"Unique keys: {len(seen_words)}")
    
    # Inject missing 4th and 5th declension nouns
    missing_words = [
        # 4th Declension
        {"latin": "manus", "translation": "hand", "part_of_speech": "noun", "level": "1", "genitive": "manus", "gender": "f", "declension": "4", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "exercitus", "translation": "army", "part_of_speech": "noun", "level": "1", "genitive": "exercitus", "gender": "m", "declension": "4", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "cornu", "translation": "horn", "part_of_speech": "noun", "level": "1", "genitive": "cornus", "gender": "n", "declension": "4", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "domus", "translation": "house", "part_of_speech": "noun", "level": "1", "genitive": "domus", "gender": "f", "declension": "4", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "impetus", "translation": "attack", "part_of_speech": "noun", "level": "1", "genitive": "impetus", "gender": "m", "declension": "4", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        # 5th Declension
        {"latin": "dies", "translation": "day", "part_of_speech": "noun", "level": "1", "genitive": "diei", "gender": "m", "declension": "5", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "res", "translation": "thing", "part_of_speech": "noun", "level": "1", "genitive": "rei", "gender": "f", "declension": "5", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "spes", "translation": "hope", "part_of_speech": "noun", "level": "1", "genitive": "spei", "gender": "f", "declension": "5", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "fides", "translation": "faith", "part_of_speech": "noun", "level": "1", "genitive": "fidei", "gender": "f", "declension": "5", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "facies", "translation": "face", "part_of_speech": "noun", "level": "1", "genitive": "faciei", "gender": "f", "declension": "5", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        # Personal Pronouns
        {"latin": "ego", "translation": "I", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "tu", "translation": "you (singular)", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "nos", "translation": "we", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "vos", "translation": "you (plural)", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        # Demonstrative Pronouns
        {"latin": "hic", "translation": "this", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "ille", "translation": "that", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        {"latin": "is", "translation": "he/she/it", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""},
        # Relative Pronoun
        {"latin": "qui", "translation": "who/which", "part_of_speech": "pronoun", "level": "1", "genitive": "", "gender": "", "declension": "", "principal_parts": "", "conjugation": "", "parisyllabic": ""}
    ]
    
    for word in missing_words:
        key = (word['latin'], word['part_of_speech'])
        if key not in seen_words:
            cleaned_rows.append(word)
            seen_words.add(key)
            print(f"Injected: {word['latin']}")

    # Write to file
    with open(output_path, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
            
    print(f"Processed {len(cleaned_rows)} unique words.")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    clean_data()
