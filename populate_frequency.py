import os
from sqlmodel import Session, select
from database.connection import engine
from database import Word
from utils.collatinus_importer import CollatinusImporter

def populate_frequency():
    print("📊 Starting Frequency Population...")
    
    # 1. Load Frequency Data from Collatinus
    importer = CollatinusImporter("data/collatinus-repo/bin/data")
    lemmes_la_path = os.path.join(importer.data_dir, "lemmes.la")
    
    # Dictionary to store max frequency for each normalized lemma
    # Some lemmas appear multiple times (different meanings), we'll take the max freq
    lemma_freqs = {}
    
    print("📂 Reading Collatinus data...")
    with open(lemmes_la_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('!'):
                continue
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
                
            # Format: lemma=normalized|model|gen/stem1|stem2|morph|freq
            raw_lemma = parts[0].split('=')[0]
            norm_lemma = importer.normalize_lemma(raw_lemma)
            
            try:
                freq = int(parts[5])
            except ValueError:
                freq = 0
                
            if norm_lemma in lemma_freqs:
                lemma_freqs[norm_lemma] = max(lemma_freqs[norm_lemma], freq)
            else:
                lemma_freqs[norm_lemma] = freq
                
    print(f"📚 Processed frequencies for {len(lemma_freqs)} lemmas.")
    
    # 2. Update Database
    with Session(engine) as session:
        words = session.exec(select(Word)).all()
        print(f"💾 Updating {len(words)} words in database...")
        
        updated_count = 0
        matched_count = 0
        
        # We need to rank them. 
        # Let's create a sorted list of (lemma, freq) to assign ranks
        # But wait, we need to assign ranks to OUR words.
        # So first, map our words to frequencies.
        
        word_freq_map = []
        
        for word in words:
            norm_latin = importer.normalize_lemma(word.latin)
            freq = lemma_freqs.get(norm_latin, 0)
            
            if freq > 0:
                matched_count += 1
            
            word_freq_map.append({
                'word': word,
                'freq': freq
            })
            
        # Sort by frequency descending
        word_freq_map.sort(key=lambda x: x['freq'], reverse=True)
        
        # Assign ranks
        # Rank 1 is highest frequency
        current_rank = 1
        for item in word_freq_map:
            word = item['word']
            freq = item['freq']
            
            # Only assign meaningful ranks to words with frequency > 0
            # Or assign them all? 
            # If freq is 0, they will be at the end.
            
            word.frequency_rank_global = current_rank
            session.add(word)
            current_rank += 1
            updated_count += 1
            
        session.commit()
        
        print(f"✅ Updated {updated_count} words.")
        print(f"🎯 Matched {matched_count} words with Collatinus frequency data.")
        print(f"📉 Top 5 most frequent words in your DB:")
        
        for i in range(5):
            item = word_freq_map[i]
            print(f"   {i+1}. {item['word'].latin} (Freq: {item['freq']})")

if __name__ == "__main__":
    populate_frequency()
