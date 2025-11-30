import streamlit as st
from sqlmodel import select
from database import get_session
from database import Word
from latin_logic import LatinMorphology
import random
import pandas as pd

from i18n import get_text

def show_declension():
    st.markdown(f"## 📜 {get_text('declension', st.session_state.language)}")
    
    if st.button(get_text('new_word', st.session_state.language)):
        load_noun()
        
    if "decl_word_id" not in st.session_state:
        load_noun()

    if st.session_state.decl_word_id:
        with get_session() as session:
            word = session.get(Word, st.session_state.decl_word_id)
            if word:
                st.markdown(f"### {word.latin}, {word.genitive} ({word.gender})")
                
                forms = LatinMorphology.decline_noun(word.latin, word.declension, word.gender, word.genitive)
                
                if forms:
                    data = {
                        get_text('case', st.session_state.language): [
                            get_text('nominative', st.session_state.language),
                            get_text('genitive', st.session_state.language),
                            get_text('dative', st.session_state.language),
                            get_text('accusative', st.session_state.language),
                            get_text('ablative', st.session_state.language)
                        ],
                        get_text('singular', st.session_state.language): [
                            forms.get("nom_sg", "-"), forms.get("gen_sg", "-"), 
                            forms.get("dat_sg", "-"), forms.get("acc_sg", "-"), 
                            forms.get("abl_sg", "-")
                        ],
                        get_text('plural', st.session_state.language): [
                            forms.get("nom_pl", "-"), forms.get("gen_pl", "-"), 
                            forms.get("dat_pl", "-"), forms.get("acc_pl", "-"), 
                            forms.get("abl_pl", "-")
                        ]
                    }
                    df = pd.DataFrame(data)
                    st.table(df)

def show_conjugation():
    st.markdown(f"## ⚔️ {get_text('conjugation', st.session_state.language)}")
    
    if st.button(get_text('new_word', st.session_state.language)):
        load_verb()
        
    if "conj_word_id" not in st.session_state:
        load_verb()

    if st.session_state.conj_word_id:
        with get_session() as session:
            word = session.get(Word, st.session_state.conj_word_id)
            if word:
                st.markdown(f"### {word.latin} ({word.principal_parts})")
                
                forms = LatinMorphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts)
                
                if forms:
                    # Present
                    st.markdown(f"#### {get_text('present', st.session_state.language)}")
                    data_pres = {
                        get_text('person', st.session_state.language): ["1.", "2.", "3."],
                        get_text('singular', st.session_state.language): [forms.get("pres_1sg"), forms.get("pres_2sg"), forms.get("pres_3sg")],
                        get_text('plural', st.session_state.language): [forms.get("pres_1pl"), forms.get("pres_2pl"), forms.get("pres_3pl")]
                    }
                    st.table(pd.DataFrame(data_pres))

                    # Imperfect
                    st.markdown(f"#### {get_text('imperfect', st.session_state.language)}")
                    data_imp = {
                        get_text('person', st.session_state.language): ["1.", "2.", "3."],
                        get_text('singular', st.session_state.language): [forms.get("imp_1sg"), forms.get("imp_2sg"), forms.get("imp_3sg")],
                        get_text('plural', st.session_state.language): [forms.get("imp_1pl"), forms.get("imp_2pl"), forms.get("imp_3pl")]
                    }
                    st.table(pd.DataFrame(data_imp))
                    
                    # Perfect
                    st.markdown(f"#### {get_text('perfect', st.session_state.language)}")
                    data_perf = {
                        get_text('person', st.session_state.language): ["1.", "2.", "3."],
                        get_text('singular', st.session_state.language): [forms.get("perf_1sg"), forms.get("perf_2sg"), forms.get("perf_3sg")],
                        get_text('plural', st.session_state.language): [forms.get("perf_1pl"), forms.get("perf_2pl"), forms.get("perf_3pl")]
                    }
                    st.table(pd.DataFrame(data_perf))

def load_noun():
    with get_session() as session:
        words = session.exec(select(Word).where(Word.part_of_speech == "noun")).all()
        if words:
            word = random.choice(words)
            st.session_state.decl_word_id = word.id
        else:
            st.session_state.decl_word_id = None

def load_verb():
    with get_session() as session:
        words = session.exec(select(Word).where(Word.part_of_speech == "verb")).all()
        if words:
            word = random.choice(words)
            st.session_state.conj_word_id = word.id
        else:
            st.session_state.conj_word_id = None
