"""
Main Application Entry Point
This is the refactored main application with improved structure and performance.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.config.settings import settings
from app.services.user_service import UserService
from app.services.vocabulary_service import VocabularyService
from database.connection import init_db, get_session


def initialize_application():
    """
    Initialize the application components.
    """
    print(f"Initializing {settings.APP_NAME}...")
    print(f"Debug mode: {settings.DEBUG}")
    
    # Initialize database
    init_db()
    print("Database initialized successfully!")


def main():
    """
    Main application entry point.
    """
    initialize_application()
    
    # Initialize services with database session
    with get_session() as session:
        user_service = UserService(session)
        vocab_service = VocabularyService(session)
        
        # Get or create default user
        user = user_service.get_or_create_user(settings.DEFAULT_USER_NAME)
        
        print("Application initialized successfully!")
        print("Services ready:")
        print(f"  - User Service: {user_service}")
        print(f"  - Vocabulary Service: {vocab_service}")
        print(f"  - Current User: {user.username} (Level {user.level}, XP: {user.xp})")
        
        # Example usage
        words = vocab_service.get_words_by_level(1)
        print(f"  - Words at level 1: {len(words)} words found")


if __name__ == "__main__":
    main()