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
import json
from database import Word, UserProfile, Text
from sqlmodel import select
import csv

def seed_vocabulary():
    """Import vocabulary from CSV file"""
    csv_path = os.path.join("data", "seed_data.csv")
    
    if not os.path.exists(csv_path):
        print("Error: data/seed_data.csv not found")
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
                # Convert parisyllabic string to bool
                pari_value = None
                if row.get('parisyllabic') == 'TRUE':
                    pari_value = True
                elif row.get('parisyllabic') == 'FALSE':
                    pari_value = False
                
                word = Word(
                    latin=row['latin'],
                    translation=row['translation'],
                    part_of_speech=row['part_of_speech'],
                    level=int(row['level']),
                    genitive=row.get('genitive'),
                    gender=row.get('gender'),
                    declension=row.get('declension'),
                    principal_parts=row.get('principal_parts'),
                    conjugation=row.get('conjugation'),
                    parisyllabic=pari_value
                )
                session.add(word)
                count += 1
        
        session.commit()
        print(f"✓ Successfully imported {count} words")

def seed_texts():
    """Import texts from JSON file"""
    json_path = os.path.join("data", "texts.json")
    
    if not os.path.exists(json_path):
        print("Error: data/texts.json not found")
        return
    
    with get_session() as session:
        # Check if we already have texts
        existing = session.exec(select(Text)).first()
        if existing:
            print("Database already contains texts. Skipping seed.")
            return
        
        from database import Author
        
        with open(json_path, 'r', encoding='utf-8') as f:
            texts_data = json.load(f)
            
        count = 0
        for item in texts_data:
            # Handle Author
            author_name = item.get('author', 'Anónimo')
            author = session.exec(select(Author).where(Author.name == author_name)).first()
            
            if not author:
                author = Author(name=author_name, difficulty_level=1)
                session.add(author)
                session.commit()
                session.refresh(author)
            
            text = Text(
                title=item['title'],
                author_id=author.id,
                content=item['content'],
                difficulty=item['level'], # Map level to difficulty
                # level=item['level'], # Text model doesn't have 'level', it has 'difficulty'
            )
            session.add(text)
            count += 1
        
        session.commit()
        print(f"✓ Successfully imported {count} texts")

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
    
    print("\nSeeding texts...")
    seed_texts()
    
    print("\nSeeding user profile...")
    seed_user()
    
    print("\n✨ Database seeding complete!")
