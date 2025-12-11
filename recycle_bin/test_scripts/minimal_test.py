#!/usr/bin/env python3
"""
Minimal test to reproduce the database session issue
"""

def test_minimal_db():
    print("Starting minimal database test...")
    
    try:
        # Import the database connection
        from database.connection import get_session
        print("✓ Database connection imported")
        
        # Try to create a session
        print("Creating session...")
        with get_session() as session:
            print("✓ Session created successfully")
            # Try a simple operation
            print("Session created, attempting simple operation...")
            
        print("✓ Session context completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_minimal_db()
    if success:
        print("\n🎉 Minimal test passed!")
    else:
        print("\n❌ Minimal test failed!")