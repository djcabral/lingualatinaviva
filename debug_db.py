from sqlmodel import Session, select, create_engine
from database.models import Word

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
