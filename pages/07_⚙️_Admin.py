import streamlit as st
import sys
import os
import json
import re
import unicodedata
from sqlmodel import select

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word, Text, TextWordLink

st.set_page_config(page_title="Admin", page_icon="⚙️", layout="wide")

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
        ⚙️ Admin - Panel de Administración
    </h1>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
section = st.sidebar.radio(
    "Sección",
    ["Vocabulario", "Textos", "Estadísticas"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("Usa este panel para gestionar el contenido de la aplicación.")

def normalize_latin(text):
    """Remove macrons and diacritics for matching"""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

# --- SECTION: VOCABULARY ---
if section == "Vocabulario":
    st.markdown("## 📚 Gestión de Vocabulario")
    
    vocab_tabs = st.tabs(["➕ Sustantivos", "➕ Verbos", "➕ Otros", "📋 Lista Completa"])
    
    # --- Tab: Nouns ---
    with vocab_tabs[0]:
        st.markdown("### Añadir Sustantivo")
        with st.form("add_noun"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Nominativo Singular *")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="noun_level")
            
            with col2:
                genitive = st.text_input("Genitivo Singular *")
                gender = st.selectbox("Género *", ["m", "f", "n"])
                declension = st.selectbox("Declinación *", ["1", "2", "3", "4", "5"])
                irregular_forms = st.text_area("Formas Irregulares (JSON)", help='Ejemplo: {"dat_pl": "filiābus"}', key="noun_irr")
            
            submitted = st.form_submit_button("✅ Guardar Sustantivo")
            
            if submitted:
                if latin and translation and genitive and gender and declension:
                    irregular_json = None
                    if irregular_forms:
                        try:
                            json.loads(irregular_forms)
                            irregular_json = irregular_forms
                        except json.JSONDecodeError:
                            st.error("❌ JSON inválido")
                            st.stop()
                    
                    with get_session() as session:
                        word = Word(
                            latin=latin, translation=translation, part_of_speech="noun", level=level,
                            genitive=genitive, gender=gender, declension=declension,
                            irregular_forms=irregular_json, category="noun"
                        )
                        session.add(word)
                        session.commit()
                        st.success(f"Sustantivo '{latin}' añadido.")
                else:
                    st.error("Faltan campos obligatorios.")

    # --- Tab: Verbs ---
    with vocab_tabs[1]:
        st.markdown("### Añadir Verbo")
        with st.form("add_verb"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Presente 1ª Persona (o Infinitivo) *")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="verb_level")
            
            with col2:
                principal_parts = st.text_input("Partes Principales *", help="Ej: amo, amare, amavi, amatum")
                conjugation = st.selectbox("Conjugación *", ["1", "2", "3", "4", "irregular"])
                irregular_forms = st.text_area("Formas Irregulares (JSON)", help='Ejemplo: {"pres_3sg": "est"}', key="verb_irr")
            
            submitted = st.form_submit_button("✅ Guardar Verbo")
            
            if submitted:
                if latin and translation and principal_parts and conjugation:
                    irregular_json = None
                    if irregular_forms:
                        try:
                            json.loads(irregular_forms)
                            irregular_json = irregular_forms
                        except json.JSONDecodeError:
                            st.error("❌ JSON inválido")
                            st.stop()
                            
                    with get_session() as session:
                        word = Word(
                            latin=latin, translation=translation, part_of_speech="verb", level=level,
                            principal_parts=principal_parts, conjugation=conjugation,
                            irregular_forms=irregular_json, category="verb"
                        )
                        session.add(word)
                        session.commit()
                        st.success(f"Verbo '{latin}' añadido.")
                else:
                    st.error("Faltan campos obligatorios.")

    # --- Tab: Others ---
    with vocab_tabs[2]:
        st.markdown("### Añadir Otra Palabra")
        with st.form("add_other"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Palabra (Latín) *")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="other_level")
            
            with col2:
                pos_options = {
                    "Adjetivo": "adjective", "Adverbio": "adverb", 
                    "Preposición": "preposition", "Conjunción": "conjunction", 
                    "Pronombre": "pronoun"
                }
                pos_display = st.selectbox("Tipo *", list(pos_options.keys()))
                pos = pos_options[pos_display]
                
                is_invariable = st.checkbox("Es invariable", value=(pos in ["adverb", "preposition", "conjunction"]))
            
            submitted = st.form_submit_button("✅ Guardar Palabra")
            
            if submitted:
                if latin and translation:
                    with get_session() as session:
                        word = Word(
                            latin=latin, translation=translation, part_of_speech=pos, level=level,
                            is_invariable=is_invariable, category=pos
                        )
                        session.add(word)
                        session.commit()
                        st.success(f"Palabra '{latin}' añadida.")
                else:
                    st.error("Faltan campos obligatorios.")

    # --- Tab: List ---
    with vocab_tabs[3]:
        st.markdown("### Lista de Vocabulario")
        with get_session() as session:
            words = session.exec(select(Word)).all()
            if words:
                # Filter
                filter_text = st.text_input("🔍 Buscar palabra", "")
                filtered_words = [w for w in words if filter_text.lower() in w.latin.lower() or filter_text.lower() in w.translation.lower()] if filter_text else words
                
                data = []
                for w in filtered_words:
                    data.append({
                        "ID": w.id,
                        "Latín": w.latin,
                        "Traducción": w.translation,
                        "Tipo": w.part_of_speech,
                        "Nivel": w.level
                    })
                st.dataframe(data, use_container_width=True)
            else:
                st.info("No hay palabras.")

# --- SECTION: TEXTS ---
elif section == "Textos":
    st.markdown("## 📜 Gestión de Textos")
    
    text_tabs = st.tabs(["➕ Añadir Texto", "📚 Ver Textos"])
    
    with text_tabs[0]:
        st.markdown("### Nuevo Texto")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            title = st.text_input("Título")
            author = st.text_input("Autor")
            content = st.text_area("Contenido (Latín)", height=300)
        
        with col2:
            level = st.number_input("Nivel", 1, 10, 1)
            st.info("El sistema analizará el texto y vinculará el vocabulario automáticamente.")
        
        if st.button("💾 Guardar Texto", use_container_width=True):
            if title and content:
                with get_session() as session:
                    new_text = Text(title=title, author=author, content=content, difficulty=level)
                    session.add(new_text)
                    session.commit()
                    session.refresh(new_text)
                    
                    # Tokenize and Link
                    words_in_text = re.findall(r'[a-zA-ZāēīōūĀĒĪŌŪ]+', content.lower())
                    word_freq = {}
                    for w in words_in_text:
                        nw = normalize_latin(w)
                        word_freq[nw] = word_freq.get(nw, 0) + 1
                    
                    all_words = session.exec(select(Word)).all()
                    linked_count = 0
                    
                    for text_word, freq in word_freq.items():
                        for db_word in all_words:
                            if normalize_latin(db_word.latin.lower()) == text_word:
                                link = TextWordLink(text_id=new_text.id, word_id=db_word.id, frequency=freq)
                                session.add(link)
                                linked_count += 1
                                break
                    session.commit()
                    st.success(f"Texto guardado. {linked_count} palabras vinculadas.")
            else:
                st.error("Título y contenido requeridos.")

    with text_tabs[1]:
        st.markdown("### Textos Existentes")
        with get_session() as session:
            texts = session.exec(select(Text)).all()
            for t in texts:
                with st.expander(f"{t.title} (Nivel {t.difficulty})"):
                    st.write(t.content[:200] + "...")
                    st.caption(f"Autor: {t.author or 'Desconocido'}")

# --- SECTION: STATS ---
elif section == "Estadísticas":
    st.markdown("## 📋 Estadísticas del Corpus")
    
    with get_session() as session:
        all_words = session.exec(select(Word)).all()
        texts = session.exec(select(Text)).all()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Palabras", len(all_words))
        col2.metric("Total Textos", len(texts))
        
        # Breakdown
        pos_counts = {}
        for w in all_words:
            pos_counts[w.part_of_speech] = pos_counts.get(w.part_of_speech, 0) + 1
        
        st.markdown("### Distribución por Tipo")
        st.bar_chart(pos_counts)
