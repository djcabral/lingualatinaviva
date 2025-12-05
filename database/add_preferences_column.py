"""
Migration: Add preferences_json to UserProfile

This migration adds the preferences_json column to the userprofile table
to store user UI preferences like font size.
"""

import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    # Get database path
    base_dir = os.getenv("USER_DATA_DIR", ".")
    db_path = os.path.join(base_dir, "lingua_latina.db")
    
    if not os.path.exists(db_path):
        logger.error(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(userprofile)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'preferences_json' in columns:
            logger.info("✓ preferences_json column already exists")
            return True
        
        # Add column
        logger.info("Adding preferences_json column to userprofile...")
        cursor.execute("""
            ALTER TABLE userprofile 
            ADD COLUMN preferences_json TEXT
        """)
        
        conn.commit()
        logger.info("✓ Migration completed successfully")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"✗ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed. Check logs above.")
