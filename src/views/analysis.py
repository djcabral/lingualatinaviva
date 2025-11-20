import streamlit as st
from sqlmodel import select
from database import get_session
from database.models import Word
from latin_logic import LatinMorphology
import random

from i18n import get_text

def show_analysis():
    st.markdown(f"## 🔍 {get_text('analysis', st.session_state.language)}")
    
    if st.button(get_text('new_form', st.session_state.language)):
        load_analysis_form()
        
    if "analysis_target" not in st.session_state:
        load_analysis_form()

    if st.session_state.get("analysis_form"):
        st.markdown(
            f"""
            <div style="background-color: #fff8f0; border: 2px solid #8b4513; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0;">
                <h2 style="font-size: 2.5em; color: #8b0000;">{st.session_state.analysis_form}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.expander(get_text('reveal', st.session_state.language)):
            st.markdown(f"### {st.session_state.analysis_target}")

def load_analysis_form():
    with get_session() as session:
        words = session.exec(select(Word)).all()
        if not words:
            return

        word = random.choice(words)
        
        if word.part_of_speech == "noun":
            forms = LatinMorphology.decline_noun(word.latin, word.declension, word.gender, word.genitive)
            if forms:
                case = random.choice(list(forms.keys()))
                form = forms[case]
                st.session_state.analysis_form = form
                st.session_state.analysis_target = f"{word.latin}: {case} ({word.gender})"
            else:
                load_analysis_form()
                
        elif word.part_of_speech == "verb":
            forms = LatinMorphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts)
            if forms:
                key = random.choice(list(forms.keys()))
                form = forms[key]
                st.session_state.analysis_form = form
                st.session_state.analysis_target = f"{word.latin}: {key}"
            else:
                load_analysis_form()
        else:
            load_analysis_form()
