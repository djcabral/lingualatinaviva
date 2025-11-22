import os
import sys
from sqlmodel import Session, select
from database.connection import engine
from database.models import Word
from utils.collatinus_importer import CollatinusImporter

def rescue_reservoir_words():
    """
    Attempts to rescue words from the reservoir by looking them up 
    in the local Collatinus dictionary files.
    """
    print("🔍 Starting Reservoir Rescue Operation...")
    
    # 1. Load Collatinus Data
    importer = CollatinusImporter("data/collatinus-repo/bin/data")
    print("📂 Loading Collatinus data (this may take a moment)...")
    
    lemmes_la_path = os.path.join(importer.data_dir, "lemmes.la")
    lemmes_es_path = os.path.join(importer.data_dir, "lemmes.es")
    
    if not os.path.exists(lemmes_la_path):
        print(f"❌ Error: {lemmes_la_path} not found.")
        return

    # Load Spanish definitions first
    es_definitions = {}
    if os.path.exists(lemmes_es_path):
        with open(lemmes_es_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('!') or ':' not in line:
                    continue
                lemma, translation = line.split(':', 1)
                norm_lemma = importer.normalize_lemma(lemma.strip())
                es_definitions[norm_lemma] = translation.strip()
    
    # Load Latin data into a lookup dict
    latin_lookup = {}
    with open(lemmes_la_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('!'):
                continue
            parts = line.strip().split('|')
            if not parts:
                continue
                
            # Format: lemma=normalized|model|gen/stem1|stem2|morph|freq
            raw_lemma_field = parts[0]
            if '=' in raw_lemma_field:
                lemma_key = raw_lemma_field.split('=')[0]
            else:
                lemma_key = raw_lemma_field
            
            norm_key = importer.normalize_lemma(lemma_key)
            
            if norm_key not in latin_lookup:
                latin_lookup[norm_key] = parts
            else:
                if parts[1] and not latin_lookup[norm_key][1]:
                    latin_lookup[norm_key] = parts

    print(f"📚 Loaded {len(latin_lookup)} Latin lemmas.")

    # 2. Fetch Reservoir Words
    with Session(engine) as session:
        reservoir_words = session.exec(select(Word).where(Word.status == "reservoir")).all()
        print(f"🌊 Found {len(reservoir_words)} words in the Reservoir.")
        
        rescued_count = 0
        
        for word in reservoir_words:
            print(f"  Checking '{word.latin}'...", end=" ")
            
            target_norm = importer.normalize_lemma(word.latin)
            
            if target_norm in latin_lookup:
                data = latin_lookup[target_norm]
                model = data[1]
                
                print(f"✅ FOUND! Model: {model}")
                
                word.collatinus_lemma = data[0].split('=')[1] if '=' in data[0] else data[0]
                word.collatinus_model = model
                
                if not word.definition_es and target_norm in es_definitions:
                    word.definition_es = es_definitions[target_norm]
                    if not word.translation or word.translation == "???":
                         word.translation = es_definitions[target_norm].split(',')[0]

                # Mark as active if we have a model
                if model:
                    word.status = "active"
                    rescued_count += 1
                    session.add(word)
            else:
                print("❌ Not found.")
        
        session.commit()
        print(f"\n🎉 Operation Complete. Rescued {rescued_count} words.")

if __name__ == "__main__":
    rescue_reservoir_words()
