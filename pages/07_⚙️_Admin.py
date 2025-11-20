import streamlit as st
import sys
import os
import csv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word
from sqlmodel import select

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

tabs = st.tabs(["➕ Añadir Palabra", "📚 Ver Vocabulario", "📜 Añadir Texto", "📋 Estadísticas"])

# Tab 1: Add word
with tabs[0]:
    st.markdown("### Añadir Nueva Palabra")
    
    with st.form("add_word"):
        col1, col2 = st.columns(2)
        
        with col1:
            latin = st.text_input("Palabra en latín *")
            translation = st.text_input("Traducción *")
            
            # Map display names (Spanish) to internal values (English)
            pos_options = {
                "Sustantivo": "noun",
                "Verbo": "verb",
                "Adjetivo": "adjective",
                "Adverbio": "adverb",
                "Preposición": "preposition",
                "Conjunción": "conjunction",
                "Pronombre": "pronoun"
            }
            
            pos_display = st.selectbox("Categoría gramatical *", list(pos_options.keys()))
            pos = pos_options[pos_display]
            
            level = st.number_input("Nivel", min_value=1, max_value=10, value=1)
        
        with col2:
            genitive = st.text_input("Genitivo (sustantivos)")
            gender = st.selectbox("Género (sustantivos)", ["", "m", "f", "n"])
            declension = st.selectbox("Declinación (sustantivos)", ["", "1", "2", "3", "4", "5"])
            principal_parts = st.text_input("Partes principales (verbos)")
            conjugation = st.selectbox("Conjugación (verbos)", ["", "1", "2", "3", "4"])
        
        submitted = st.form_submit_button("✅ Añadir Palabra")
        
        if submitted:
            if latin and translation and pos:
                with get_session() as session:
                    new_word = Word(
                        latin=latin,
                        translation=translation,
                        part_of_speech=pos,
                        level=level,
                        genitive=genitive if genitive else None,
                        gender=gender if gender else None,
                        declension=declension if declension else None,
                        principal_parts=principal_parts if principal_parts else None,
                        conjugation=conjugation if conjugation else None
                    )
                    session.add(new_word)
                    session.commit()
                    st.success(f"✨ Palabra '{latin}' añadida correctamente!")
            else:
                st.error("Por favor completa los campos obligatorios (*)")

# Tab 2: View vocabulary
with tabs[1]:
    st.markdown("### Vocabulario Actual")
    
    with get_session() as session:
        words = session.exec(select(Word)).all()
        
        if words:
            st.info(f"Total de palabras: {len(words)}")
            
            # Reverse mapping for display
            pos_map_reverse = {v: k for k, v in pos_options.items()}
            
            # Create dataframe
            data = []
            for word in words[:50]:  # Show first 50
                data.append({
                    "Latín": word.latin,
                    "Traducción": word.translation,
                    "Categoría": pos_map_reverse.get(word.part_of_speech, word.part_of_speech),
                    "Nivel": word.level
                })
            
            st.dataframe(data, use_container_width=True)
            
            if len(words) > 50:
                st.info(f"Mostrando 50 de {len(words)} palabras")
        else:
            st.warning("No hay palabras en la base de datos")

# Tab 3: Add text
with tabs[2]:
    st.markdown("### Añadir Texto Clásico")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        title = st.text_input("Título del texto")
        author = st.text_input("Autor (opcional)")
        content = st.text_area("Contenido (texto en latín)", height=300)
    
    with col2:
        level = st.number_input("Nivel del texto", min_value=1, max_value=10, value=1)
        st.info("💡 El sistema detectará automáticamente las palabras del vocabulario en el texto.")
    
    if st.button("💾 Guardar Texto", use_container_width=True):
        if title and content:
            from database.models import Text, TextWordLink
            import re
            import unicodedata
            
            def normalize_latin(text):
                """Remove macrons and diacritics for matching"""
                normalized = unicodedata.normalize('NFD', text)
                return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')
            
            with get_session() as session:
                # Create the text
                new_text = Text(
                    title=title,
                    author=author if author else None,
                    content=content,
                    level=level
                )
                session.add(new_text)
                session.commit()
                session.refresh(new_text)
                
                # Tokenize the content
                # Remove punctuation and split into words
                words_in_text = re.findall(r'[a-zA-ZāēīōūĀĒĪŌŪ]+', content.lower())
                
                # Count word frequencies
                word_freq = {}
                for w in words_in_text:
                    normalized_w = normalize_latin(w)
                    word_freq[normalized_w] = word_freq.get(normalized_w, 0) + 1
                
                # Match with database words
                all_words = session.exec(select(Word)).all()
                matched_words = []
                unknown_words = set()
                
                for text_word, freq in word_freq.items():
                    matched = False
                    for db_word in all_words:
                        if normalize_latin(db_word.latin.lower()) == text_word:
                            # Create link
                            link = TextWordLink(
                                text_id=new_text.id,
                                word_id=db_word.id,
                                frequency=freq
                            )
                            session.add(link)
                            matched_words.append((db_word.latin, freq))
                            matched = True
                            break
                    
                    if not matched and len(text_word) > 2:  # Ignore very short words
                        unknown_words.add(text_word)
                
                session.commit()
                
                st.success(f"✨ Texto '{title}' guardado correctamente!")
                st.info(f"📊 Palabras vinculadas: {len(matched_words)}")
                
                if matched_words:
                    with st.expander("Ver palabras vinculadas"):
                        for word, freq in sorted(matched_words, key=lambda x: x[1], reverse=True)[:20]:
                            st.write(f"• {word} ({freq}x)")
                
                if unknown_words:
                    st.warning(f"⚠️ {len(unknown_words)} palabras no encontradas en el vocabulario")
                    with st.expander("Ver palabras desconocidas"):
                        for word in sorted(unknown_words)[:30]:
                            st.write(f"• {word}")
                        st.info("💡 Añade estas palabras al vocabulario para mejorar la cobertura del texto.")
        else:
            st.error("Por favor completa el título y el contenido")

# Tab 4: Statistics
with tabs[3]:
    st.markdown("### Estadísticas del Sistema")
    
    with get_session() as session:
        all_words = session.exec(select(Word)).all()
        
        nouns = len([w for w in all_words if w.part_of_speech == "noun"])
        verbs = len([w for w in all_words if w.part_of_speech == "verb"])
        adjectives = len([w for w in all_words if w.part_of_speech == "adjective"])
        others = len(all_words) - nouns - verbs - adjectives
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Palabras", len(all_words))
        with col2:
            st.metric("Sustantivos", nouns)
        with col3:
            st.metric("Verbos", verbs)
        with col4:
            st.metric("Adjetivos", adjectives)
        
        # Words by level
        st.markdown("#### Distribución por Nivel")
        level_dist = {}
        for word in all_words:
            level_dist[word.level] = level_dist.get(word.level, 0) + 1
        
        st.bar_chart(level_dist)
