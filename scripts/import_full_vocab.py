import sys
import os
import csv
from sqlmodel import select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database.models import Word

def import_vocabulary():
    csv_path = os.path.join("data", "vocabulary.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return
    
    print(f"Reading from {csv_path}...")
    
    with get_session() as session:
        # Get existing words to avoid duplicates
        existing_words = session.exec(select(Word.latin)).all()
        existing_set = set(existing_words)
        
        count = 0
        skipped = 0
        
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                latin = row['latin'].strip()
                
                if latin in existing_set:
                    skipped += 1
                    continue
                
                # Handle optional fields
                pari_value = None
                if row.get('parisyllabic') == 'TRUE':
                    pari_value = True
                elif row.get('parisyllabic') == 'FALSE':
                    pari_value = False
                
                # Clean up empty strings to None
                def clean(val):
                    return val.strip() if val and val.strip() else None

                word = Word(
                    latin=latin,
                    translation=clean(row['translation']),
                    part_of_speech=clean(row['part_of_speech']),
                    level=int(row['level']) if row['level'] else 1,
                    genitive=clean(row.get('genitive')),
                    gender=clean(row.get('gender')),
                    declension=clean(row.get('declension')),
                    principal_parts=clean(row.get('principal_parts')),
                    conjugation=clean(row.get('conjugation')),
                    parisyllabic=pari_value
                )
                session.add(word)
                existing_set.add(latin) # Add to set to prevent duplicates within the file itself
                count += 1
                
                if count % 100 == 0:
                    print(f"Processed {count} words...")
        
        session.commit()
        print(f"✓ Import complete.")
        print(f"  Added: {count}")
        print(f"  Skipped (duplicates): {skipped}")

if __name__ == "__main__":
    import_vocabulary()
