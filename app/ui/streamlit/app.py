"""
Main Streamlit application.
"""
import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.database import init_db

# Page Config
st.set_page_config(
    page_title="Lingua Latina Viva",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "language" not in st.session_state:
    st.session_state.language = "es"

# Load CSS
def load_css():
    """Load custom CSS styles."""
    css_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize DB
init_db()

def main():
    """Main application function."""
    # Sidebar Navigation
    st.sidebar.markdown("<h1 style='text-align: center; color: #e0c097;'>🏛️ Lingua Latina Viva</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    def navigate_to(page):
        st.session_state.page = page

    # Navigation Buttons (these would be expanded in a full implementation)
    nav_options = {
        "Dashboard": "🏠 Dashboard",
        "Vocabulary": "🎴 Vocabularium",
        "Grammar": "📜 Grammatica",
        "Practice": "⚔️ Praxis",
        "Analysis": "🔍 Analysis",
        "Reading": "📖 Lectio"
    }

    for page, label in nav_options.items():
        if st.sidebar.button(label, key=f"nav_{page}"):
            navigate_to(page)

    st.sidebar.markdown("---")
    st.sidebar.markdown("<div style='text-align: center; color: #888;'><em>Discipulus: Diego</em></div>", unsafe_allow_html=True)

    # Page routing
    if st.session_state.page == "Dashboard":
        show_dashboard()
    elif st.session_state.page == "Vocabulary":
        show_vocabulary()
    # Other pages would be implemented similarly

def show_dashboard():
    """Show the dashboard page."""
    st.title("Dashboard")
    st.write("Welcome to Lingua Latina Viva!")

def show_vocabulary():
    """Show the vocabulary page."""
    st.title("Vocabulary")
    st.write("Vocabulary practice tools")

if __name__ == "__main__":
    main()