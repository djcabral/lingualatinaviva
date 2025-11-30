from sqlmodel import Session, select, create_engine
from database import Word

sqlite_file_name = "lingua_latina.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

with Session(engine) as session:
    words = session.exec(select(Word)).all()
    print(f"Total words: {len(words)}")
    
    pos_counts = {}
    decl_counts = {}
    
    for w in words:
        pos_counts[w.part_of_speech] = pos_counts.get(w.part_of_speech, 0) + 1
        if w.part_of_speech == 'noun' or w.part_of_speech == 'adjective' or w.part_of_speech == 'adj':
            decl_counts[w.declension] = decl_counts.get(w.declension, 0) + 1
            
    print("Part of Speech counts:", pos_counts)
    print("Declension counts:", decl_counts)
    
    adjs = session.exec(select(Word).where(Word.part_of_speech.in_(['adj', 'adjective']))).all()
    print(f"Sample adjectives: {[w.latin for w in adjs[:5]]}")
    print(f"Sample adjective declensions: {[w.declension for w in adjs[:5]]}")

    # Fetch all verbs to check for homonyms in Python
    verbs = session.exec(select(Word).where(Word.part_of_speech == 'verb')).all()
    
    from collections import Counter
    import re
    
    def normalize(text):
        return re.sub(r'\d+', '', text)
        
    verb_counts = Counter(normalize(w.latin) for w in verbs)
    duplicates = {k: v for k, v in verb_counts.items() if v > 1}
    
    print(f"\nTotal unique verb forms (ignoring digits): {len(verb_counts)}")
    print(f"Total verb entries: {len(verbs)}")
    print(f"Potential homonyms found: {len(duplicates)}")
    
    if duplicates:
        print("Top 10 homonyms:")
        for k, v in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"- {k}: {v} entries")
            # Show examples
            examples = [w.latin for w in verbs if normalize(w.latin) == k]
            print(f"  Examples: {examples}")
