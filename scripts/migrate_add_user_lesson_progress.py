#!/usr/bin/env python3
"""
Migration script: Add UserLessonProgress table for organic progression system

Run with: python3 scripts/migrate_add_user_lesson_progress.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from database.models import UserLessonProgress  # Import to ensure table is registered
from database.connection import engine  # Import engine directly
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Create UserLessonProgress table if it doesn't exist."""
    try:
        logger.info("Creating UserLessonProgress table...")
        
        # Create only the UserLessonProgress table
        SQLModel.metadata.create_all(engine, tables=[UserLessonProgress.__table__])
        
        logger.info("✅ Migration completed successfully!")
        logger.info("UserLessonProgress table is ready for organic progression system")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()
