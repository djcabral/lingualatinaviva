import streamlit as st
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word
from sqlmodel import select
from utils.latin_logic import LatinMorphology

# Translation dictionaries
POS_TRANSLATIONS = {
    "noun": "Sustantivo",
    "verb": "Verbo",
    "adjective": "Adjetivo",
    "adverb": "Adverbio",
    "preposition": "Preposición",
    "pronoun": "Pronombre",
    "conjunction": "Conjunción"
}

GENDER_TRANSLATIONS = {
    "m": "masculino",
    "f": "femenino",
    "n": "neutro"
}

def translate_pos(pos: str) -> str:
    """Translate part of speech to Spanish"""
    return POS_TRANSLATIONS.get(pos, pos)

def translate_gender(gender: str) -> str:
    """Translate gender abbreviation to full Spanish word"""
    return GENDER_TRANSLATIONS.get(gender, gender)

st.set_page_config(page_title="Analysis", page_icon="🔍", layout="wide")

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
        🔍 Analysis - Análisis Morfológico
    </h1>
    """,
    unsafe_allow_html=True
)

morphology = LatinMorphology()

if 'current_word_analysis' not in st.session_state:
    st.session_state.current_word_analysis = None
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

# Get a random word
with get_session() as session:
    all_words = session.exec(select(Word)).all()
    
    if not all_words:
        st.warning("No hay palabras en la base de datos.")
        st.stop()
    
    if st.session_state.current_word_analysis is None:
        st.session_state.current_word_analysis = random.choice(all_words)
    
    word = st.session_state.current_word_analysis
    
    # Display word
    st.markdown(
        f"""
        <div class="vocab-card">
            <div class="vocab-latin">{word.latin}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
    
    # Check if word is invariable
    if word.is_invariable:
        st.markdown("### 📋 Palabra Invariable")
        st.info(
            f"**Tipo:** {translate_pos(word.part_of_speech)}  \n"
            f"**Significado:** {word.translation}  \n"
            f"**Categoría:** {word.category if word.category else 'N/A'}  \n\n"
            f"Esta palabra es **invariable**, es decir, no se declina ni se conjuga. Siempre se usa en la misma forma: **{word.latin}**"
        )
        
        st.markdown("---")
        if st.button("🎲 Nueva Palabra", use_container_width=True):
            st.session_state.current_word_analysis = random.choice(all_words)
            st.session_state.current_form_analysis = None
            st.session_state.show_analysis_result = False
            st.rerun()
        st.stop()
    
    # Generate all forms for the word
    forms = {}
    if word.part_of_speech == "noun":
        if word.declension and word.gender:
            genitive = word.genitive if word.genitive else word.latin
            forms = morphology.decline_noun(word.latin, word.declension, word.gender, genitive)
    elif word.part_of_speech == "verb":
        if word.conjugation and word.principal_parts:
            forms = morphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts)
            
    if not forms:
        st.warning("No se pudieron generar formas para esta palabra. Intenta con otra.")
        if st.button("🎲 Nueva Palabra"):
            st.session_state.current_word_analysis = random.choice(all_words)
            st.session_state.current_form_analysis = None
            st.rerun()
        st.stop()

    # Select a random form to analyze if not already selected
    if 'current_form_analysis' not in st.session_state or st.session_state.current_form_analysis is None:
        # Filter out empty forms
        valid_forms = [(k, v) for k, v in forms.items() if v]
        if valid_forms:
            selected_tag, selected_form = random.choice(valid_forms)
            # Normalize for comparison to handle syncretism (e.g. puella vs puellā)
            normalized_selected = morphology.normalize_latin(selected_form)
            st.session_state.current_form_analysis = {
                "form": selected_form,
                "target_tag": selected_tag, # One of the valid tags, used for initial selection
                "all_valid_tags": [k for k, v in forms.items() if morphology.normalize_latin(v) == normalized_selected] # All tags that match this form (ignoring macrons)
            }
        else:
            st.error("Error generando formas.")
            st.stop()
            
    current_form = st.session_state.current_form_analysis["form"]
    valid_tags = st.session_state.current_form_analysis["all_valid_tags"]
    
    st.markdown(f"### Analiza la forma: **{current_form}**")
    st.info(f"Palabra base: **{word.latin}** ({word.translation}) - {translate_pos(word.part_of_speech)}")
    
    # Analysis form
    col1, col2 = st.columns(2)
    
    user_selection = {}
    
    with col1:
        if word.part_of_speech == "noun":
            case = st.selectbox("Caso", ["Nominativo", "Vocativo", "Acusativo", "Genitivo", "Dativo", "Ablativo"])
            number = st.selectbox("Número", ["Singular", "Plural"])
            
            # Map to internal tags
            case_map = {
                "Nominativo": "nom", "Vocativo": "voc", "Acusativo": "acc", 
                "Genitivo": "gen", "Dativo": "dat", "Ablativo": "abl"
            }
            number_map = {"Singular": "sg", "Plural": "pl"}
            
            user_tag = f"{case_map[case]}_{number_map[number]}"
            
        elif word.part_of_speech == "verb":
            tense = st.selectbox("Tiempo", ["Presente", "Imperfecto", "Perfecto"])
            person = st.selectbox("Persona", ["1ª", "2ª", "3ª"])
            number = st.selectbox("Número", ["Singular", "Plural"])
            
            tense_map = {"Presente": "pres", "Imperfecto": "imp", "Perfecto": "perf"}
            number_map = {"Singular": "sg", "Plural": "pl"}
            person_map = {"1ª": "1", "2ª": "2", "3ª": "3"}
            
            user_tag = f"{tense_map[tense]}_{person_map[person]}{number_map[number]}"
    
    with col2:
        st.markdown("#### Posibles análisis:")
        if st.button("✅ Verificar Análisis", use_container_width=True):
            st.session_state.show_analysis_result = True
            
        if st.session_state.get('show_analysis_result', False):
            if user_tag in valid_tags:
                st.success("✅ ¡Correcto!")
                st.markdown("**Esta forma corresponde a:**")
            else:
                st.error("❌ Incorrecto")
                st.markdown("**La forma correcta sería:**")
                
            # Show all valid possibilities
            for tag in valid_tags:
                parts = tag.split('_')
                if word.part_of_speech == "noun":
                    # nom_sg -> Nominativo Singular
                    case_rev = {"nom": "Nominativo", "voc": "Vocativo", "acc": "Acusativo", "gen": "Genitivo", "dat": "Dativo", "abl": "Ablativo"}
                    num_rev = {"sg": "Singular", "pl": "Plural"}
                    st.info(f"• {case_rev[parts[0]]} {num_rev[parts[1]]}")
                elif word.part_of_speech == "verb":
                    # pres_1sg -> Presente 1ª Singular
                    tense_rev = {"pres": "Presente", "imp": "Imperfecto", "perf": "Perfecto"}
                    num_rev = {"sg": "Singular", "pl": "Plural"}
                    # parts: [tense, person+number] e.g. ['pres', '1sg']
                    p_n = parts[1]
                    person = p_n[0]
                    number = p_n[1:]
                    st.info(f"• {tense_rev[parts[0]]} {person}ª Persona {num_rev[number]}")

    st.markdown("---")
    if st.button("🎲 Nueva Palabra / Forma", use_container_width=True):
        st.session_state.current_word_analysis = random.choice(all_words)
        st.session_state.current_form_analysis = None
        st.session_state.show_analysis_result = False
        st.rerun()
