import streamlit as st
import sys
import os
import random
import unicodedata

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word
from sqlmodel import select
from utils.latin_logic import LatinMorphology

def normalize_latin(text):
    """Remove macrons and diacritics from Latin text for comparison"""
    # Normalize to NFD (decomposed form) then remove combining characters
    normalized = unicodedata.normalize('NFD', text)
    # Remove combining diacritical marks (macrons, etc.)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

st.set_page_config(page_title="Declinatio", page_icon="📜", layout="wide")

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
        📜 Declinatio - Declinaciones
    </h1>
    """,
    unsafe_allow_html=True
)

morphology = LatinMorphology()

# Get user level for progressive learning
with get_session() as session:
    from database.models import UserProfile
    user = session.exec(select(UserProfile)).first()
    user_level = user.level if user else 1

st.markdown(f"### 📚 Nivel {user_level} - Sustantivos")

# Select declension filter based on user level
if user_level <= 2:
    available_declensions = ["1", "2"]
    st.info("🎯 Practicando declinaciones 1ª y 2ª (nivel básico)")
elif user_level <= 4:
    available_declensions = ["1", "2", "3"]
    st.info("🎯 Practicando declinaciones 1ª, 2ª y 3ª (nivel intermedio)")
else:
    available_declensions = ["1", "2", "3", "4", "5"]
    st.info("🎯 Practicando todas las declinaciones (nivel avanzado)")

# Get nouns from available declensions
with get_session() as session:
    nouns = session.exec(
        select(Word).where(
            Word.part_of_speech == "noun",
            Word.declension.in_(available_declensions)
        )
    ).all()
    
    if not nouns:
        st.warning("No hay sustantivos disponibles para tu nivel. Usa el panel de Admin para añadirlos.")
        st.stop()
    
    if 'current_noun' not in st.session_state:
        st.session_state.current_noun = random.choice(nouns)
    
    noun = st.session_state.current_noun
    
    
    st.markdown(f"### Declina: **{noun.latin}** ({noun.translation})")
    st.info(f"📋 Declinación: {noun.declension}ª • Género: {noun.gender} • Genitivo: {noun.genitive}")
    
    # Create declension table
    cases = ["nominativus", "vocativus", "accusativus", "genitivus", "dativus", "ablativus"]
    case_labels = ["Nominativus", "Vocativus", "Accusativus", "Genitivus", "Dativus", "Ablativus"]
    
    # Check if it's a pronoun
    if noun.part_of_speech == "pronoun":
        forms = morphology.decline_pronoun(noun.latin)
        if not forms:
            st.warning("Pronombre no reconocido.")
            st.stop()
        st.info(f"📋 Pronombre personal")
    else:
        # Regular noun declension
        if not noun.declension or not noun.gender:
            st.warning("Este sustantivo no tiene declinación o género definido.")
            st.stop()
        
        genitive = noun.genitive if noun.genitive else noun.latin
        forms = morphology.decline_noun(noun.latin, noun.declension, noun.gender, genitive, noun.irregular_forms)
        
        if not forms:
            st.warning("No se pudo generar la declinación para este sustantivo.")
            st.stop()

    
    
    # Check if this is a demonstrative pronoun (has gender forms)
    is_demonstrative = any(key.endswith('_m') or key.endswith('_f') or key.endswith('_n') for key in forms.keys())
    
    # Initialize show_answers state
    if 'show_declension_answers' not in st.session_state:
        st.session_state.show_declension_answers = False
    if 'user_declension_answers' not in st.session_state:
        st.session_state.user_declension_answers = {}
    
    if is_demonstrative:
        # Display with 3 genders
        st.markdown("### Paradigma Completo (m / f / n)")
        
        for case, label in zip(cases, case_labels):
            st.markdown(f"**{label}**")
            col_sg, col_pl = st.columns(2)
            
            with col_sg:
                st.markdown("*Singularis*")
                key_m = f"{case[:3]}_sg_m"
                key_f = f"{case[:3]}_sg_f"
                key_n = f"{case[:3]}_sg_n"
                form_m = forms.get(key_m, "—")
                form_f = forms.get(key_f, "—")
                form_n = forms.get(key_n, "—")
                st.info(f"{form_m} / {form_f} / {form_n}")
            
            with col_pl:
                st.markdown("*Pluralis*")
                key_m = f"{case[:3]}_pl_m"
                key_f = f"{case[:3]}_pl_f"
                key_n = f"{case[:3]}_pl_n"
                form_m = forms.get(key_m, "—")
                form_f = forms.get(key_f, "—")
                form_n = forms.get(key_n, "—")
                st.info(f"{form_m} / {form_f} / {form_n}")
            
            st.markdown("---")
    else:
        # Regular display (nouns and personal pronouns)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Singularis")
            for case, label in zip(cases, case_labels):
                key = f"{case[:3]}_sg"
                correct_form = forms.get(key, "—")
                
                if st.session_state.show_declension_answers:
                    # Show user's answer and correct answer
                    user_answer = st.session_state.user_declension_answers.get(f"input_sg_{case}", "")
                    # Normalize both for comparison (remove macrons)
                    is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                    
                    # Display with color coding
                    if is_correct:
                        st.success(f"✅ {label}: **{correct_form}**")
                    else:
                        st.error(f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**")
                else:
                    # Empty input for practice
                    st.text_input(label, value="", key=f"input_sg_{case}", placeholder="Escribe la forma...")
        
        with col2:
            st.markdown("#### Pluralis")
        for case, label in zip(cases, case_labels):
            key = f"{case[:3]}_pl"
            correct_form = forms.get(key, "—")
            
            if st.session_state.show_declension_answers:
                # Show user's answer and correct answer
                user_answer = st.session_state.user_declension_answers.get(f"input_pl_{case}", "")
                # Normalize both for comparison (remove macrons)
                is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                
                # Display with color coding
                if is_correct:
                    st.success(f"✅ {label}: **{correct_form}**")
                else:
                    st.error(f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**")
            else:
                # Empty input for practice
                st.text_input(label, value="", key=f"input_pl_{case}", placeholder="Escribe la forma...")
    
    # Show XP feedback if available
    if 'xp_feedback' in st.session_state and st.session_state.show_declension_answers:
        st.success(st.session_state.xp_feedback)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✅ Verificar", use_container_width=True):
            # Save user answers
            st.session_state.user_declension_answers = {}
            for case in cases:
                sg_key = f"input_sg_{case}"
                pl_key = f"input_pl_{case}"
                if sg_key in st.session_state:
                    st.session_state.user_declension_answers[sg_key] = st.session_state[sg_key]
                if pl_key in st.session_state:
                    st.session_state.user_declension_answers[pl_key] = st.session_state[pl_key]
            
            # Calculate score and award XP
            correct_count = 0
            total_count = 0
            
            for case in cases:
                # Singular
                sg_key = f"input_sg_{case}"
                user_answer_sg = st.session_state.user_declension_answers.get(sg_key, "")
                correct_form_sg = forms.get(f"{case[:3]}_sg", "")
                if user_answer_sg.strip():  # Solo contar si el usuario respondió
                    total_count += 1
                    if normalize_latin(user_answer_sg.strip()).lower() == normalize_latin(correct_form_sg).lower():
                        correct_count += 1
                
                # Plural
                pl_key = f"input_pl_{case}"
                user_answer_pl = st.session_state.user_declension_answers.get(pl_key, "")
                correct_form_pl = forms.get(f"{case[:3]}_pl", "")
                if user_answer_pl.strip():  # Solo contar si el usuario respondió
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
                        st.session_state.xp_feedback = f"🎉 +{xp_gained} XP ({correct_count}/{total_count} correctas)"
            
            st.session_state.show_declension_answers = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Limpiar", use_container_width=True):
            st.session_state.show_declension_answers = False
            st.session_state.user_declension_answers = {}
            st.rerun()
    
    with col3:
        if st.button("🎲 Nueva Palabra", use_container_width=True):
            st.session_state.current_noun = random.choice(nouns)
            st.session_state.show_declension_answers = False
            st.session_state.user_declension_answers = {}
            st.rerun()
