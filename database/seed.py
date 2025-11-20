"""
Seed script to populate the database with initial data.
Run this with: python -m database.seed
"""
import sys
import os
import csv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import create_db_and_tables, get_session, engine
from database.models import Word, UserProfile
from sqlmodel import select

def seed_vocabulary():
    """Import vocabulary from CSV file"""
    csv_path = os.path.join("data", "words.csv")
    
    if not os.path.exists(csv_path):
        print("Error: data/words.csv not found")
        return
    
    with get_session() as session:
        # Check if we already have words
        existing = session.exec(select(Word)).first()
        if existing:
            print("Database already contains words. Skipping seed.")
            return
        
        count = 0
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean latin word
                latin_clean = ''.join([c for c in row['latin'] if not c.isdigit() and c != '_'])
                
                word = Word(
                    latin=latin_clean,
                    translation=row['translation'],
                    part_of_speech=row['part_of_speech'],
                    level=int(row['level']),
                    genitive=row.get('genitive'),
                    gender=row.get('gender'),
                    declension=row.get('declension'),
                    principal_parts=row.get('principal_parts'),
                    conjugation=row.get('conjugation')
                )
                session.add(word)
                count += 1
        
        session.commit()
        print(f"✓ Successfully imported {count} words")

def seed_user():
    """Create default user profile"""
    with get_session() as session:
        user = session.exec(select(UserProfile)).first()
        if not user:
            new_user = UserProfile(
                username="Discipulus",
                level=1,
                xp=0,
                streak=0
            )
            session.add(new_user)
            session.commit()
            print("✓ Created default user profile")
        else:
            print("User profile already exists")

if __name__ == "__main__":
    print("Creating database tables...")
    create_db_and_tables()
    
    print("\nSeeding vocabulary...")
    seed_vocabulary()
    
    print("\nSeeding user profile...")
    seed_user()
    
    print("\n✨ Database seeding complete!")
