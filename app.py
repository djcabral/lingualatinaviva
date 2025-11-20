import streamlit as st
import sys
import os

# Add paths for imports
sys.path.append(os.path.dirname(__file__))

from database.connection import init_db
from utils.i18n import get_text

# Page configuration
st.set_page_config(
    page_title="Lingua Latina Viva",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize database
init_db()

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'es'
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

# Splash screen for first visit
if st.session_state.first_visit:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 80vh; flex-direction: column;">
            <div style="background: linear-gradient(135deg, rgba(139,69,19,0.1), rgba(160,82,45,0.1));
                        padding: 60px;
                        border-radius: 20px;
                        border: 3px solid rgba(139,69,19,0.3);
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                        text-align: center;
                        max-width: 700px;">
                <h1 style="font-family: 'Cinzel', serif; 
                           font-size: 3.5em; 
                           color: #8b4513;
                           margin-bottom: 30px;
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                    📜 Lingua Latina Viva 📜
                </h1>
                <p style="font-family: 'Cardo', serif; 
                          font-size: 2em; 
                          color: #654321;
                          font-style: italic;
                          margin-bottom: 40px;
                          line-height: 1.6;">
                    "Ave, discipule.<br>Incipiamus iter per linguam aeternam."
                </p>
                <p style="font-family: 'Lato', sans-serif; 
                          color: #777;
                          font-size: 1.1em;">
                    Bienvenido/a • Welcome • Willkommen
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("✨ Ingredere (Entrar)", use_container_width=True):
            st.session_state.first_visit = False
            st.rerun()
else:
    # Main navigation
    st.sidebar.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif; color: #8b4513;'>
            📜 Lingua Latina Viva
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    st.sidebar.info(
        """
        **Navigatio**: Usa el menú de la izquierda para explorar los módulos.
        
        **Módulos Disponibles:**
        - 🏠 Home (Hodie)
        - 🎴 Vocabularium
        - 📜 Declinatio
        - ⚔️ Conjugatio
        - 🔍 Analysis
        - 📖 Lectio
        - ⚙️ Admin
        """
    )
    
    # Main content
    st.markdown(
        """
        <div style='text-align: center; padding: 50px 0;'>
            <h1 style='font-family: "Cinzel", serif; font-size: 3em; color: #8b4513;'>
                Ave, Discipule!
            </h1>
            <p style='font-family: "Cardo", serif; font-size: 1.5em; color: #654321; font-style: italic;'>
                Elige un módulo del menú lateral para comenzar tu práctica diaria.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Quick stats overview
    from database.connection import get_session
    from database.models import UserProfile, Word
    from sqlmodel import select
    
    with get_session() as session:
        user = session.exec(select(UserProfile)).first()
        if user:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{user.level}</div>
                        <div class="stat-label">Nivel</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{user.streak}</div>
                        <div class="stat-label">Racha (días)</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{user.xp}</div>
                        <div class="stat-label">PE</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col4:
                total_words = session.exec(select(Word)).all()
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{len(total_words)}</div>
                        <div class="stat-label">Vocabula</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
