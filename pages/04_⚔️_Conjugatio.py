import streamlit as st
import sys
import os
import random
import unicodedata

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word, UserProfile
from sqlmodel import select
from utils.latin_logic import LatinMorphology

def normalize_latin(text):
    """Remove macrons and diacritics from Latin text for comparison"""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

st.set_page_config(page_title="Conjugatio", page_icon="⚔️", layout="wide")

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif; color: #8b4513;'>
        ⚔️ Conjugatio - Conjugaciones
    </h1>
    """,
    unsafe_allow_html=True
)

morphology = LatinMorphology()

# Get user level for progressive learning
with get_session() as session:
    user = session.exec(select(UserProfile)).first()
    user_level = user.level if user else 1

st.markdown(f"### 📚 Nivel {user_level} - Verbos")

# Tense translation map
TENSE_MAP = {
    "Praesens": "Presente",
    "Imperfectum": "Imperfecto",
    "Perfectum": "Perfecto"
}

# Progressive tense introduction based on level
if user_level <= 2:
    available_tenses = ["Praesens"]
    st.info("🎯 Nivel básico: Solo presente de indicativo (activo)")
elif user_level <= 4:
    available_tenses = ["Praesens", "Imperfectum"]
    st.info("🎯 Nivel intermedio: Presente e imperfecto de indicativo (activo)")
elif user_level <= 6:
    available_tenses = ["Praesens", "Imperfectum", "Perfectum"]
    st.info("🎯 Nivel intermedio-avanzado: Presente, imperfecto y perfecto de indicativo (activo)")
else:
    available_tenses = ["Praesens", "Imperfectum", "Perfectum"]
    st.info("🎯 Nivel avanzado: Todos los tiempos del indicativo activo")

# Select tense and voice
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    # Use format_func to display Spanish names
    tense_selection = st.selectbox(
        "⏱️ Tiempo verbal", 
        available_tenses, 
        format_func=lambda x: TENSE_MAP.get(x, x),
        key="tense_select"
    )

with col2:
    voice_selection = st.selectbox(
        "🎭 Voz",
        ["Activa", "Pasiva"],
        key="voice_select"
    )

with col3:
    # Mode selector for advanced levels
    if user_level >= 4:
        mode_selection = st.selectbox(
            "📖 Modo",
            ["Indicativo", "Subjuntivo"],
            key="mode_select"
        )
    else:
        mode_selection = "Indicativo"  # Default for lower levels

# Get verbs
with get_session() as session:
    verbs = session.exec(select(Word).where(Word.part_of_speech == "verb")).all()
    
    if not verbs:
        st.warning("No hay verbos en la base de datos. Usa el panel de Admin para añadirlos.")
        st.stop()
    
    if 'current_verb' not in st.session_state:
        st.session_state.current_verb = random.choice(verbs)
    
    verb = st.session_state.current_verb
    
    st.markdown(f"### Conjuga: **{verb.latin}** ({verb.translation})")
    
    if verb.principal_parts:
        st.info(f"📋 Partes principales: **{verb.principal_parts}** • Conjugación: {verb.conjugation}ª")
    else:
        st.warning("Este verbo no tiene partes principales definidas.")
    
    # Get full conjugation table
    if not verb.principal_parts or not verb.conjugation:
        st.error("Este verbo no tiene información completa para conjugarse.")
        st.stop()
    
    forms = morphology.conjugate_verb(verb.latin, verb.conjugation, verb.principal_parts, verb.irregular_forms)
    
    if not forms:
        st.error("No se pudo generar la conjugación para este verbo.")
        st.stop()
    
    # Map tense, voice, and mood to form keys
    tense_lower = tense_selection.lower()
    voice_es = voice_selection  # "Activa" or "Pasiva"
    mode_es = mode_selection  # "Indicativo" or "Subjuntivo"
    
    if tense_lower == "praesens":
        prefix = "pres"
        tense_es = "Presente"
    elif tense_lower == "imperfectum":
        prefix = "imp"
        tense_es = "Imperfecto"
    elif tense_lower == "perfectum":
        prefix = "perf"
        tense_es = "Perfecto"
    else:
        prefix = "pres"
        tense_es = "Presente"
    
    # Add "_subj" suffix for subjunctive mood (not available for perfect)
    if mode_es == "Subjuntivo":
        if prefix == "perf":
            st.warning("⚠️ El perfecto de subjuntivo no está disponible aún. Usa Presente o Imperfecto.")
            st.stop()
        prefix = prefix + "_subj"
    
    # Add "_pass" suffix for passive voice
    if voice_es == "Pasiva":
        prefix = prefix + "_pass"
    
    tense_display = f"{tense_es} de {mode_es} ({voice_es})"
    st.markdown(f"**{tense_display}**")
    
    # Initialize show_answers state
    if 'show_conjugation_answers' not in st.session_state:
        st.session_state.show_conjugation_answers = False
    if 'user_conjugation_answers' not in st.session_state:
        st.session_state.user_conjugation_answers = {}
    
    # Create conjugation table
    persons = ["1ª persona", "2ª persona", "3ª persona"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Singularis")
        for i, person in enumerate(persons, 1):
            key = f"{prefix}_{i}sg"
            correct_form = forms.get(key, "—")
            
            if st.session_state.show_conjugation_answers:
                # Show user's answer and correct answer
                user_answer = st.session_state.user_conjugation_answers.get(f"input_sg_{i}", "")
                is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                
                if is_correct:
                    st.success(f"✅ {person}: **{correct_form}**")
                else:
                    st.error(f"❌ {person}: '{user_answer}' → **{correct_form}**")
            else:
                # Empty input for practice
                st.text_input(person, value="", key=f"input_sg_{i}", placeholder="Escribe la forma...")
    
    with col2:
        st.markdown("#### Pluralis")
        for i, person in enumerate(persons, 1):
            key = f"{prefix}_{i}pl"
            correct_form = forms.get(key, "—")
            
            if st.session_state.show_conjugation_answers:
                # Show user's answer and correct answer
                user_answer = st.session_state.user_conjugation_answers.get(f"input_pl_{i}", "")
                is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                
                if is_correct:
                    st.success(f"✅ {person}: **{correct_form}**")
                else:
                    st.error(f"❌ {person}: '{user_answer}' → **{correct_form}**")
            else:
                # Empty input for practice
                st.text_input(person, value="", key=f"input_pl_{i}", placeholder="Escribe la forma...")
    
    # Show XP feedback if available
    if 'xp_feedback_conjugation' in st.session_state and st.session_state.show_conjugation_answers:
        st.success(st.session_state.xp_feedback_conjugation)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✅ Verificar", use_container_width=True):
            # Save user answers
            st.session_state.user_conjugation_answers = {}
            for i in range(1, 4):
                sg_key = f"input_sg_{i}"
                pl_key = f"input_pl_{i}"
                if sg_key in st.session_state:
                    st.session_state.user_conjugation_answers[sg_key] = st.session_state[sg_key]
                if pl_key in st.session_state:
                    st.session_state.user_conjugation_answers[pl_key] = st.session_state[pl_key]
            
            # Calculate score and award XP
            correct_count = 0
            total_count = 0
            
            for i in range(1, 4):
                # Singular
                sg_key = f"input_sg_{i}"
                user_answer_sg = st.session_state.user_conjugation_answers.get(sg_key, "")
                correct_form_sg = forms.get(f"{prefix}_{i}sg", "")
                if user_answer_sg.strip():
                    total_count += 1
                    if normalize_latin(user_answer_sg.strip()).lower() == normalize_latin(correct_form_sg).lower():
                        correct_count += 1
                
                # Plural
                pl_key = f"input_pl_{i}"
                user_answer_pl = st.session_state.user_conjugation_answers.get(pl_key, "")
                correct_form_pl = forms.get(f"{prefix}_{i}pl", "")
                if user_answer_pl.strip():
                    total_count += 1
                    if normalize_latin(user_answer_pl.strip()).lower() == normalize_latin(correct_form_pl).lower():
                        correct_count += 1
            
            # Award XP: 5 points per correct answer
            xp_gained = correct_count * 5
            
            if xp_gained > 0:
                with get_session() as session:
                    user = session.exec(select(UserProfile)).first()
                    if user:
                        user.xp += xp_gained
                        session.add(user)
                        session.commit()
                        st.session_state.xp_feedback_conjugation = f"🎉 +{xp_gained} XP ({correct_count}/{total_count} correctas)"
            
            st.session_state.show_conjugation_answers = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Limpiar", use_container_width=True):
            st.session_state.show_conjugation_answers = False
            st.session_state.user_conjugation_answers = {}
            st.rerun()
    
    with col3:
        if st.button("🎲 Nuevo Verbo", use_container_width=True):
            st.session_state.current_verb = random.choice(verbs)
            st.session_state.show_conjugation_answers = False
            st.session_state.user_conjugation_answers = {}
            st.rerun()

