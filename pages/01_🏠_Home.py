import streamlit as st
import sys
import os
root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

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
    <h1 style='text-align: center; font-family: "Cinzel", serif;'>
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
        
        from utils.gamification import get_level_progress
        progress_data = get_level_progress(user.xp, user.level)
        
        st.progress(progress_data['percentage'], text=f"Nivel {user.level} → {user.level + 1}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"XP Actual: {user.xp} / {progress_data['next_level_xp']}")
        with c2:
            remaining = progress_data['next_level_xp'] - user.xp
            st.caption(f"Faltan {remaining} XP para el siguiente nivel")
        
        st.markdown("---")
        
        # Roadmap
        with st.expander("🗺️ Mapa de Progreso (Roadmap)"):
            st.markdown("""
            ### 🛤️ Tu Viaje
            
            **Nivel 1: Fundamentos**
            - 📜 Sustantivos: 1ª y 2ª declinación
            - ⚔️ Verbos: Presente de Indicativo
            
            **Nivel 2: Expansión**
            - 📜 **+ Adjetivos** (1ª y 2ª clase)
            
            **Nivel 3: Profundización**
            - 📜 **+ 3ª Declinación**
            - ⚔️ **+ Imperfecto**
            
            **Nivel 4: Complejidad**
            - 📜 **+ Pronombres**
            - ⚔️ **+ Subjuntivo e Imperativo**
            
            **Nivel 5: Maestría**
            - 📜 **+ 4ª y 5ª Declinación**
            - ⚔️ **+ Perfecto**
            
            **Nivel 6+: Perfeccionamiento**
            - Práctica avanzada de todas las formas.
            """)
        
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
