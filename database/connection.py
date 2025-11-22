from sqlmodel import create_engine, SQLModel, Session, select
from contextlib import contextmanager
from database.models import (
    Word, ReviewLog, UserProfile, Text, TextWordLink,
    Author, WordFrequency, SyntaxPattern  # Nuevos modelos Fase 1
)
import os
import csv

sqlite_file_name = "lingua_latina.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

# Flag to prevent multiple initializations
_db_initialized = False

def create_db_and_tables():
    """Create database tables only once"""
    global _db_initialized
    if not _db_initialized:
        SQLModel.metadata.create_all(engine)
        _db_initialized = True


def get_session():
    return Session(engine)

def init_db():
    create_db_and_tables()
    # Check if we have words, if not import seed
    with get_session() as session:
        statement = select(Word)
        results = session.exec(statement).first()
        if not results:
            import_seed_data(session)
        
        # Check for user profile
        user = session.exec(select(UserProfile)).first()
        if not user:
            new_user = UserProfile(username="Discipulus", level=1, xp=0, streak=0)
            session.add(new_user)
            session.commit()

def import_seed_data(session: Session):
    # This assumes running from project root
    # Check for seed_data.csv first (cleaned data)
    csv_path = os.path.join("data", "seed_data.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join("data", "vocabulary.csv")
    
    if not os.path.exists(csv_path):
        return

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = Word(
                latin=row['latin'],
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
    session.commit()
