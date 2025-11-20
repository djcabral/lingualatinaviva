import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import UserProfile, Word, ReviewLog
from sqlmodel import select
from datetime import datetime, timedelta
from utils.i18n import get_text

st.set_page_config(page_title="Home - Lingua Latina Viva", page_icon="🏠", layout="wide")

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if 'language' not in st.session_state:
    st.session_state.language = 'es'

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif; color: #8b4513;'>
        🏠 Hodie - Hoy
    </h1>
    """,
    unsafe_allow_html=True
)

with get_session() as session:
    user = session.exec(select(UserProfile)).first()
    
    if user:
        # Stats Row
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
                    <div class="stat-label">Racha</div>
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
            all_words = session.exec(select(Word)).all()
            st.markdown(
                f"""
                <div class="stat-box">
                    <div class="stat-value">{len(all_words)}</div>
                    <div class="stat-label">Vocabula</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Today's objectives  
        st.markdown("## 📋 Hodie (Tareas de Hoy)")
        
        # Count words due for review
        today = datetime.now()
        reviews = session.exec(select(ReviewLog)).all()
        words_due = 0
        for review in reviews:
            next_review_date = review.review_date + timedelta(days=review.interval)
            if next_review_date <= today:
                words_due += 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"📚 **{words_due}** palabras para repasar")
            st.info("📜 Practicar declinaciones de 3ª")
            st.info("⚔️ Repasar tiempo perfecto")
        
        with col2:
            st.info("🔍 Análisis morfológico diario")
            st.info("📖 Continuar 'Capitulum Primum'")
        
        st.markdown("---")
        
        # Progress visualization
        st.markdown("## 🏛️ Progressus (Progreso)")
        
        progress = min(100, (user.xp / 1000) * 100)
        st.progress(progress / 100, text=f"Progreso hacia el siguiente nivel: {user.xp}/1000 PE")
        
        st.markdown("---")
        
        # Achievements preview
        st.markdown("## 🏆 Praemia (Logros)")
        
        achievements = []
        if user.xp >= 100:
            achievements.append("🎖️ Primus Gradus - ¡Primeros 100 PE!")
        if user.streak >= 7:
            achievements.append("🔥 Septimana Perfecta - 7 días seguidos")
        if len(all_words) >= 50:
            achievements.append("📚 Collector Verborum - 50+ palabras")
        
        if achievements:
            for achievement in achievements:
                st.success(achievement)
        else:
            st.info("Continúa aprendiendo para desbloquear logros...")
