#!/usr/bin/env python3
"""
Comprehensive test to simulate Streamlit module execution
"""
import sys
import traceback

def test_dictionary_execution():
    """Simulate dictionary_view render_content execution"""
    print("\n" + "="*60)
    print("Testing Dictionary Execution")
    print("="*60)
    try:
        from pages.modules import dictionary_view
        
        # Try to execute the key parts without streamlit
        from database.connection import get_session, engine
        from utils.latin_logic import LatinMorphology
        from database import Word
        from sqlmodel import select
        
        morphology = LatinMorphology()
        print("✅ LatinMorphology initialized")
        
        # Test database query
        with get_session() as session:
            results = session.exec(select(Word).where(Word.latin == "amo")).all()
            print(f"✅ Database query executed: {len(results)} results")
        
        return True
    except Exception as e:
        print(f"❌ Dictionary execution FAILED")
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return False

def test_conjugations_execution():
    """Simulate conjugations_view render_content execution"""
    print("\n" + "="*60)
    print("Testing Conjugations Execution")
    print("="*60)
    try:
        from pages.modules import conjugations_view
        from database.connection import get_session
        from database import Word, UserProfile
        from sqlmodel import select
        from utils.latin_logic import LatinMorphology
        
        # Test getting user level (like conjugations_view does)
        with get_session() as session:
            user = session.exec(select(UserProfile).where(UserProfile.id == 1)).first()
            print(f"✅ User query executed: level {user.level if user else 'N/A'}")
            
            # Test getting verbs
            verbs = session.exec(
                select(Word).where(Word.part_of_speech == 'verb')
            ).all()
            print(f"✅ Verb query executed: {len(verbs)} verbs")
            
            # Test conjugation generation
            if verbs:
                verb = verbs[0]
                forms = LatinMorphology.conjugate_verb(
                    verb.latin,
                    verb.conjugation,
                    verb.principal_parts
                )
                print(f"✅ Conjugation generated: {len(forms)} forms")
        
        return True
    except Exception as e:
        print(f"❌ Conjugations execution FAILED")
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return False

def test_challenges_execution():
    """Simulate challenges_view render_content execution"""
    print("\n" + "="*60)
    print("Testing Challenges Execution")
    print("="*60)
    try:
        from pages.modules import challenges_view
        from database.connection import get_session
        from database import Challenge, UserChallengeProgress
        from sqlmodel import select
        from utils.challenge_engine import ChallengeEngine
        import json
        
        with get_session() as session:
            # Test getting challenges
            challenges = session.exec(select(Challenge)).all()
            print(f"✅ Challenge query executed: {len(challenges)} challenges")
            
            # Test challenge engine initialization
            engine = ChallengeEngine()
            print(f"✅ ChallengeEngine initialized")
            
            # Test parsing challenge config
            if challenges:
                challenge = challenges[0]
                try:
                    config = json.loads(challenge.config_json)
                    print(f"✅ Challenge config parsed: {challenge.challenge_type}")
                except json.JSONDecodeError as je:
                    print(f"⚠️ Challenge {challenge.id} has invalid JSON: {str(je)}")
        
        return True
    except Exception as e:
        print(f"❌ Challenges execution FAILED")
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return False

def test_adventure_execution():
    """Simulate adventure_view render_content execution"""
    print("\n" + "="*60)
    print("Testing Adventure Execution")
    print("="*60)
    try:
        from pages.modules import adventure_view
        from database.connection import get_session
        from database import Challenge, UserChallengeProgress
        from sqlmodel import select
        
        with get_session() as session:
            challenges = session.exec(select(Challenge)).all()
            print(f"✅ Challenge query executed: {len(challenges)} challenges")
            
            progress_list = session.exec(
                select(UserChallengeProgress).where(UserChallengeProgress.user_id == 1)
            ).all()
            print(f"✅ Progress query executed: {len(progress_list)} progress records")
        
        return True
    except Exception as e:
        print(f"❌ Adventure execution FAILED")
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    results = {
        "Dictionary": test_dictionary_execution(),
        "Conjugations": test_conjugations_execution(),
        "Challenges": test_challenges_execution(),
        "Adventure": test_adventure_execution(),
    }
    
    print("\n" + "="*60)
    print("EXECUTION TEST SUMMARY")
    print("="*60)
    for name, success in results.items():
        status = "✅ OK" if success else "❌ FAILED"
        print(f"{name:20} {status}")
    
    if not all(results.values()):
        print("\n⚠️ Some modules failed execution tests")
        sys.exit(1)
    else:
        print("\n✅ All modules passed execution tests")
