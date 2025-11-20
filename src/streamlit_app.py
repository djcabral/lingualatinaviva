import streamlit as st
from database import init_db
import os

# Page Config
st.set_page_config(
    page_title="Lingua Latina Viva",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "language" not in st.session_state:
    st.session_state.language = "es"

from i18n import get_text

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize DB
init_db()

# Sidebar Navigation
st.sidebar.markdown("<h1 style='text-align: center; color: #e0c097;'>🏛️ Lingua Latina Viva</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def navigate_to(page):
    st.session_state.page = page

# Navigation Buttons
nav_options = {
    "Dashboard": f"🏠 {get_text('dashboard', st.session_state.language)}",
    "Vocabularium": f"🎴 {get_text('vocabulary', st.session_state.language)}",
    "Declinatio": f"📜 {get_text('declension', st.session_state.language)}",
    "Conjugatio": f"⚔️ {get_text('conjugation', st.session_state.language)}",
    "Analysis": f"🔍 {get_text('analysis', st.session_state.language)}",
    "Lectio": f"📖 {get_text('reading', st.session_state.language)}"
}

for page, label in nav_options.items():
    if st.sidebar.button(label, use_container_width=True):
        navigate_to(page)

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align: center; color: #888;'><em>Discipulus: Diego</em></div>", unsafe_allow_html=True)

# Routing
if st.session_state.page == "Dashboard":
    from views.dashboard import show_dashboard
    show_dashboard()
elif st.session_state.page == "Vocabularium":
    from views.vocabulary import show_vocabulary
    show_vocabulary()
elif st.session_state.page == "Declinatio":
    from views.grammar import show_declension
    show_declension()
elif st.session_state.page == "Conjugatio":
    from views.grammar import show_conjugation
    show_conjugation()
elif st.session_state.page == "Analysis":
    from views.analysis import show_analysis
    show_analysis()
elif st.session_state.page == "Lectio":
    from views.reading import show_reading
    show_reading()
