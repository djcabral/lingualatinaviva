"""
Streamlit Application Entry Point
Refactored Streamlit UI with improved structure and performance.
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.config.settings import settings
from app.services.user_service import UserService
from app.services.vocabulary_service import VocabularyService
from database.connection import get_session


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=settings.APP_NAME,
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def load_custom_css():
    """Load custom CSS styles."""
    st.markdown(
        """
        <style>
        .main-header {
            text-align: center;
            font-family: 'Cinzel', serif;
            color: #8B4513;
        }
        .stat-box {
            border: 1px solid #e0c097;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            background-color: #f9f5f0;
            margin: 10px 0;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #8B4513;
        }
        .stat-label {
            font-size: 1em;
            color: #666;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        st.markdown(
            f"<h1 class='main-header'>🏛️ {settings.APP_NAME}</h1>",
            unsafe_allow_html=True
        )
        st.markdown("---")
        
        # Navigation
        pages = {
            "🏠 Dashboard": "dashboard",
            "📘 Lessons": "lessons",
            "🧠 Vocabulary": "vocabulary",
            "⚔️ Practice": "practice",
            "🔍 Analysis": "analysis"
        }
        
        selected_page = st.radio("Navigation", list(pages.keys()))
        st.session_state.current_page = pages[selected_page]
        
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #888; font-size: 0.9em;'>"
            "<p>Lingua Latina Viva</p>"
            "<p>A Latin learning application</p>"
            "</div>",
            unsafe_allow_html=True
        )


def render_dashboard(user, user_service):
    """Render the dashboard page."""
    st.markdown(
        "<h1 class='main-header'>🏠 Welcome to Lingua Latina Viva!</h1>",
        unsafe_allow_html=True
    )
    
    # Get user stats
    stats = user_service.get_user_stats(user.id)
    
    # User stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-value">{stats['level']}</div>
                <div class="stat-label">Level</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-value">{stats['xp']}</div>
                <div class="stat-label">Experience</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-value">{stats['streak']}</div>
                <div class="stat-label">Streak</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Introduction
    st.markdown("---")
    st.markdown(
        f"""
        ## 🎯 About This Application
        
        Welcome, **{user.username}**! **Lingua Latina Viva** is a comprehensive Latin learning 
        platform designed to help you master the ancient language through modern techniques.
        
        ### Four Pillars of Learning:
        
        1. **📘 Lessons** - Structured curriculum with progressive difficulty
        2. **🧠 Vocabulary** - Spaced repetition system for memorization
        3. **⚔️ Practice** - Interactive exercises for grammar and morphology
        4. **🔍 Analysis** - Deep syntactic analysis of Latin texts
        
        ---
        
        Select a section from the sidebar to begin your journey into the world of Latin!
        """
    )


def main():
    """Main Streamlit application."""
    configure_page()
    load_custom_css()
    render_sidebar()
    
    try:
        # Initialize services with database session
        with get_session() as session:
            user_service = UserService(session)
            vocab_service = VocabularyService(session)
            
            # Get or create default user
            user = user_service.get_or_create_user(settings.DEFAULT_USER_NAME)
            
            # Route to appropriate page
            current_page = st.session_state.get("current_page", "dashboard")
            
            if current_page == "dashboard":
                render_dashboard(user, user_service)
            elif current_page == "lessons":
                st.markdown("# 📘 Lessons")
                st.info("Lessons module - coming soon")
            elif current_page == "vocabulary":
                st.markdown("# 🧠 Vocabulary")
                # Show some vocabulary stats
                words = vocab_service.get_words_by_level(1)
                st.info(f"Vocabulary module - {len(words)} words at level 1")
            elif current_page == "practice":
                st.markdown("# ⚔️ Practice")
                st.info("Practice module - coming soon")
            elif current_page == "analysis":
                st.markdown("# 🔍 Analysis")
                st.info("Analysis module - coming soon")
    except Exception as e:
        st.error(f"Database connection error: {e}")
        st.info("Please check the database configuration or try restarting the application.")
        logger = logging.getLogger(__name__)
        logger.error(f"Database error in Streamlit app: {e}", exc_info=True)


if __name__ == "__main__":
    main()