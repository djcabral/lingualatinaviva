import sys
import os
from sqlmodel import select, func

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database.models import Challenge, UserChallengeProgress

def check_challenges():
    with get_session() as session:
        challenges_count = session.exec(select(func.count(Challenge.id))).one()
        progress_count = session.exec(select(func.count(UserChallengeProgress.id))).one()
        
        print(f"Challenges: {challenges_count}")
        print(f"UserProgress: {progress_count}")
        
        if challenges_count > 0:
            first_challenge = session.exec(select(Challenge).limit(1)).first()
            print(f"First Challenge: {first_challenge.title} (Type: {first_challenge.challenge_type})")

if __name__ == "__main__":
    check_challenges()
