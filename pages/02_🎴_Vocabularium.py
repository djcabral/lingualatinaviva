import streamlit as st
import sys
import os
import random
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word, ReviewLog, UserProfile, Text, TextWordLink
from sqlmodel import select
from utils.i18n import get_text
from utils.srs import calculate_next_review

st.set_page_config(page_title="Vocabularium", page_icon="🎴", layout="wide")

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if 'language' not in st.session_state:
    st.session_state.language = 'es'

if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'current_word_id' not in st.session_state:
    st.session_state.current_word_id = None
if 'study_mode' not in st.session_state:
    st.session_state.study_mode = 'general'
if 'selected_text_id' not in st.session_state:
    st.session_state.selected_text_id = None

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif; color: #8b4513;'>
        🎴 Vocabularium - Flashcards SRS
    </h1>
    """,
    unsafe_allow_html=True
)

# Study Mode Selector
with get_session() as session:
    texts = session.exec(select(Text)).all()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        mode = st.radio(
            "Modo de Estudio:",
            ["general", "text_prep"],
            format_func=lambda x: "📚 General (SRS)" if x == "general" else "📖 Preparación de Texto",
            horizontal=True,
            key="mode_selector"
        )
        st.session_state.study_mode = mode
    
    with col2:
        if mode == "text_prep":
            if texts:
                text_options = {t.id: f"{t.title} ({t.author or 'Anónimo'})" for t in texts}
                selected = st.selectbox(
                    "Selecciona un texto:",
                    options=list(text_options.keys()),
                    format_func=lambda x: text_options[x]
                )
                st.session_state.selected_text_id = selected
            else:
                st.warning("No hay textos disponibles. Añade textos en el panel de Admin.")
                st.stop()

st.markdown("---")

with get_session() as session:
    # Get words based on study mode
    if st.session_state.study_mode == "general":
        all_words = session.exec(select(Word)).all()
    else:  # text_prep
        if st.session_state.selected_text_id:
            # Get words linked to the selected text
            links = session.exec(
                select(TextWordLink).where(TextWordLink.text_id == st.session_state.selected_text_id)
            ).all()
            word_ids = [link.word_id for link in links]
            all_words = [session.get(Word, wid) for wid in word_ids]
            
            if not all_words:
                st.info("Este texto no tiene palabras vinculadas aún.")
                st.stop()
        else:
            st.warning("Selecciona un texto para estudiar.")
            st.stop()
    
    # Get current word or select a new one
    if st.session_state.current_word_id is None:
        word = random.choice(all_words)
        st.session_state.current_word_id = word.id
    else:
        word = session.get(Word, st.session_state.current_word_id)
    
    if word is None:
        st.error("Error cargando palabra")
        st.stop()
    
    # Display word card
    st.markdown(
        f"""
        <div class="vocab-card">
            <div class="vocab-latin">{word.latin}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Show answer button
    if not st.session_state.show_answer:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📖 " + get_text('show_answer', st.session_state.language), use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()
    else:
        # Show translation and details
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <div class="vocab-translation">{word.translation}</div>
                <div class="vocab-pos">{get_text(word.part_of_speech, st.session_state.language)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Show additional info
        if word.genitive:
            st.info(f"**Genitivo:** {word.genitive}")
        if word.principal_parts:
            st.info(f"**Partes principales:** {word.principal_parts}")
        
        st.markdown("---")
        st.markdown(f"**{get_text('how_well', st.session_state.language)}**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("❌ " + get_text('again', st.session_state.language), use_container_width=True):
                # Record review with quality 0
                handle_review(session, word, 0)
        
        with col2:
            if st.button("😓 " + get_text('hard', st.session_state.language), use_container_width=True):
                handle_review(session, word, 2)
        
        with col3:
            if st.button("✅ " + get_text('good', st.session_state.language), use_container_width=True):
                handle_review(session, word, 4)
        
        with col4:
            if st.button("⭐ " + get_text('easy', st.session_state.language), use_container_width=True):
                handle_review(session, word, 5)

def handle_review(session, word, quality):
    """Handle SRS review logic"""
    # Get previous review for this word
    previous_review = session.exec(
        select(ReviewLog).where(ReviewLog.word_id == word.id).order_by(ReviewLog.review_date.desc())
    ).first()
    
    # Calculate next review
    result = calculate_next_review(quality, previous_review)
    
    # Create new review log
    new_review = ReviewLog(
        word_id=word.id,
        review_date=datetime.now(),
        quality=quality,
        ease_factor=result['ease_factor'],
        interval=result['interval'],
        repetitions=result['repetitions']
    )
    session.add(new_review)
    
    # Update user XP
    user = session.exec(select(UserProfile)).first()
    if user:
        xp_gain = {0: 1, 2: 3, 4: 5, 5: 10}.get(quality, 5)
        user.xp += xp_gain
        session.add(user)
    
    session.commit()
    
    # Reset state for next word
    st.session_state.show_answer = False
    st.session_state.current_word_id = None
    st.success(f"¡Bien! +{xp_gain} PE")
    st.rerun()
