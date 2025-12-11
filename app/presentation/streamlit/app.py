"""
Main Streamlit Application

Entry point for the Streamlit interface.
"""

import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.infrastructure.logging.config import setup_logging
from app.core.services.user_service import UserService
from app.core.services.vocabulary_service import VocabularyService

# Setup logging
logger = setup_logging()

# Page configuration
st.set_page_config(
    page_title="Lingua Latina Viva",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "language" not in st.session_state:
    st.session_state.language = "es"

# Initialize services
user_service = UserService()
vocab_service = VocabularyService()

def main():
    """Main application entry point"""
    st.title("Lingua Latina Viva")
    
    # Get or create user
    user = user_service.get_or_create_user()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["Dashboard", "Vocabulary", "Grammar", "Practice", "Reading"]
    )
    
    if page == "Dashboard":
        show_dashboard(user)
    elif page == "Vocabulary":
        show_vocabulary(user)
    # Other pages would be implemented similarly

def show_dashboard(user):
    """Show dashboard page"""
    st.header("Dashboard")
    st.write(f"Welcome, {user.username}!")
    st.write(f"Level: {user.level}")
    st.write(f"XP: {user.xp}")
    st.write(f"Streak: {user.streak}")

def show_vocabulary(user):
    """Show vocabulary page"""
    st.header("Vocabulary Practice")
    
    # Get words for review
    words = vocab_service.get_words_for_review(user)
    
    if not words:
        st.info("No words are due for review right now. Great job!")
        return
    
    # Display words for review
    for i, word in enumerate(words):
        st.subheader(f"{word.latin} - {word.translation}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Again", key=f"again_{i}"):
                vocab_service.record_review(word.id, user.id, 0)
                st.experimental_rerun()
                
        with col2:
            if st.button("Hard", key=f"hard_{i}"):
                vocab_service.record_review(word.id, user.id, 2)
                st.experimental_rerun()
                
        with col3:
            if st.button("Easy", key=f"easy_{i}"):
                vocab_service.record_review(word.id, user.id, 4)
                st.experimental_rerun()

if __name__ == "__main__":
    main()