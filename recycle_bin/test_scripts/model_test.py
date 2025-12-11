#!/usr/bin/env python3
"""
Test to check UserProfile model specifically
"""

def test_user_profile():
    print("Testing UserProfile model...")
    
    try:
        # Import the UserProfile model
        from database import UserProfile
        print("✓ UserProfile model imported")
        
        # Try to create an instance
        user = UserProfile(
            username="testuser",
            level=1,
            xp=0,
            streak=0
        )
        print("✓ UserProfile instance created")
        print(f"  User ID: {user.id}")
        print(f"  Username: {user.username}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_db_session_with_user():
    print("Testing database session with UserProfile...")
    
    try:
        from database.connection import get_session
        from database import UserProfile
        
        with get_session() as session:
            # Try to query for a user
            from sqlmodel import select
            user = session.exec(select(UserProfile)).first()
            print("✓ Query executed")
            if user:
                print(f"  Found user: {user.username}")
            else:
                print("  No user found")
                
        print("✓ Session completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running model tests...")
    test1 = test_user_profile()
    print()
    test2 = test_db_session_with_user()
    
    if test1 and test2:
        print("\n🎉 All model tests passed!")
    else:
        print("\n❌ Some model tests failed!")