#!/usr/bin/env python3
"""
Migration script: Add UserLessonProgressV2 table for organic progression system

Run with: python3 scripts/migrate_add_user_lesson_progress.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from database.models import UserLessonProgressV2  # Import to ensure table is registered
from database.connection import engine  # Import engine directly
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Create UserLessonProgressV2 table if it doesn't exist."""
    try:
        logger.info("Creating UserLessonProgressV2 table...")
        
        # Create only the UserLessonProgressV2 table
        SQLModel.metadata.create_all(engine, tables=[UserLessonProgressV2.__table__])
        
        logger.info("✅ Migration completed successfully!")
        logger.info("UserLessonProgressV2 table is ready for organic progression system")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()
