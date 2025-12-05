from database import get_session, Word, Challenge
from sqlmodel import select

def check_content():
    with get_session() as session:
        word_count = len(session.exec(select(Word)).all())
        challenge_count = len(session.exec(select(Challenge)).all())
        
        print(f"Total Words: {word_count}")
        print(f"Total Challenges: {challenge_count}")
        
        if challenge_count == 0:
            print("WARNING: No challenges found in database!")
        
        if word_count == 0:
            print("WARNING: No words found in database!")

if __name__ == "__main__":
    check_content()
