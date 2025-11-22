import streamlit as st
import sys
import os

root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import get_session
from database.models import Text, TextWordLink, Word, ReviewLog
from utils.text_analyzer import LatinTextAnalyzer
from sqlmodel import select

st.set_page_config(page_title="Lectio", page_icon="📖", layout="wide")

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add custom CSS for interactive text with hover tooltips
def add_interactive_text_css():
    st.markdown("""
    <style>
    .latin-text-container {
        position: relative;
        font-family: 'Cardo', serif;
        font-size: 1.3em;
        line-height: 2.2;
        text-align: justify;
    }
    .interactive-word {
        position: relative;
        cursor: help;
        padding: 2px 4px;
        border-radius: 3px;
        transition: all 0.2s;
        display: inline;
        border-bottom: 2px dotted currentColor;
    }
    .interactive-word:hover {
        background-color: rgba(255, 255, 255, 0.15);
    }
    
    /* Tooltip que aparece al hacer hover */
    .interactive-word .tooltip {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 280px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 15px;
        border-radius: 8px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        transition: opacity 0.3s, visibility 0.3s;
        pointer-events: none;
    }
    
    .interactive-word .tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #764ba2 transparent transparent transparent;
    }
    
    .interactive-word:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
    
    .tooltip-lemma {
        font-size: 1.2em;
        font-weight: bold;
        display: block;
        margin-bottom: 4px;
        font-family: 'Cinzel', serif;
    }
    
    .tooltip-translation {
        font-size: 1em;
        display: block;
        margin-bottom: 6px;
    }
    
    .tooltip-morphology {
        font-size: 0.85em;
        font-style: italic;
        display: block;
        margin-bottom: 4px;
        opacity: 0.9;
    }
    
    .tooltip-pos {
        background: rgba(255,255,255,0.25);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75em;
        display: inline-block;
        margin-top: 4px;
    }
    
    /* Colores según maestría */
    .word-known {
        color: #10b981;
        border-bottom-color: #10b981;
    }
    .word-learning {
        color: #f59e0b;
        border-bottom-color: #f59e0b;
    }
    .word-unknown {
        color: #8b5cf6;
        border-bottom-color: #8b5cf6;
    }
    .word-no-review {
        color: #64748b;
        border-bottom-color: #64748b;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()
add_interactive_text_css()

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif;'>
        📖 Lectio - Lectura Progresiva
    </h1>
    """,
    unsafe_allow_html=True
)

def calculate_mastery(session, text_id):
    """Calculate mastery percentage for a text based on word reviews"""
    links = session.exec(select(TextWordLink).where(TextWordLink.text_id == text_id)).all()
    
    if not links:
        return 0
    
    known_words = 0
    for link in links:
        # Check if word has been reviewed with interval >= 3 days
        latest_review = session.exec(
            select(ReviewLog)
            .where(ReviewLog.word_id == link.word_id)
            .order_by(ReviewLog.review_date.desc())
        ).first()
        
        if latest_review and latest_review.interval >= 3:
            known_words += 1
    
    return int((known_words / len(links)) * 100)

def get_word_mastery(session, word_id):
    """Get mastery level for a specific word"""
    latest_review = session.exec(
        select(ReviewLog)
        .where(ReviewLog.word_id == word_id)
        .order_by(ReviewLog.review_date.desc())
    ).first()
    
    if not latest_review:
        return 0
    
    # Mastery based on interval
    if latest_review.interval >= 7:
        return 100
    elif latest_review.interval >= 3:
        return 70
    elif latest_review.interval >= 1:
        return 40
    else:
        return 20

def render_interactive_text(text_id: int, text_content: str, session):
    """Renderiza texto latino con tooltips hover para análisis morfológico"""
    from utils.lectio_analyzer import get_text_analysis_from_cache
    
    # Intentar obtener análisis CLTK cacheado
    analyzed_text = get_text_analysis_from_cache(session, text_id)
    
    # Si no hay análisis CLTK, usar sistema actual con InflectedForm
    if not analyzed_text:
        analyzed_text = LatinTextAnalyzer.analyze_text(text_content, session)
    
    # Renderizar con tooltips hover
    html_parts = ['<div class="latin-text-container"><p>']
    
    for item in analyzed_text:
        form = item["form"]
        
        if item.get("is_punctuation"):
            html_parts.append(form)
        else:
            # Para análisis CLTK, item ya tiene todos los campos
            # Para análisis InflectedForm, item["analyses"] contiene las opciones
            
            lemma = item.get("lemma")
            translation = item.get("translation")
            pos = item.get("pos")
            morphology = item.get("morphology", {})
            word_id = item.get("word_id")
            
            # Si no hay lemma directamente, buscar en analyses (sistema antiguo)
            if not lemma and item.get("analyses"):
                analyses = item["analyses"]
                if analyses:
                    primary = analyses[0]
                    lemma = primary["lemma"]
                    translation = primary["translation"]
                    pos = primary["pos"]
                    morphology = primary["morphology"]
                    word_id = primary.get("word_id")
            
            if lemma:
                # Determinar color según maestría
                if word_id:
                    mastery = get_word_mastery(session, word_id)
                    if mastery >= 70:
                        css_class = "word-known"
                    elif mastery >= 40:
                        css_class = "word-learning"
                    elif mastery > 0:
                        css_class = "word-unknown"
                    else:
                        css_class = "word-no-review"
                else:
                    # Palabra no en vocabulario (solo CLTK)
                    css_class = "word-no-review"
                
                # Formatear análisis morfológico
                morph_text = LatinTextAnalyzer.format_morphology(morphology, pos)
                
                # Traducir parte del discurso
                pos_map = {
                    "noun": "sustantivo",
                    "verb": "verbo",
                    "adjective": "adjetivo", 
                    "pronoun": "pronombre",
                    "adverb": "adverbio",
                    "preposition": "preposición",
                    "conjunction": "conjunción",
                    "conj": "conjunción",
                    "prep": "preposición",
                    "adv": "adverbio",
                    "proper_noun": "nombre propio"
                }
                pos_display = pos_map.get(pos, pos)
                
                # HTML para palabra con tooltip hover
                word_html = f'''<span class="interactive-word {css_class}">
                    {form}
                    <span class="tooltip">
                        <span class="tooltip-lemma">{lemma}</span>
                        <span class="tooltip-translation">{translation}</span>
                        <span class="tooltip-morphology">{morph_text}</span>
                        <span class="tooltip-pos">{pos_display}</span>
                    </span>
                </span>'''
                
                html_parts.append(word_html)
            else:
                # Palabra desconocida (no en BD ni CLTK)
                html_parts.append(f'<span style="color: #94a3b8; font-style: italic;">{form}</span>')
        
        # Agregar espacio después de palabras (no después de puntuación)
        if not item.get("is_punctuation"):
            html_parts.append(" ")
    
    html_parts.append("</p></div>")
    
    return "".join(html_parts)


# Initialize session state for selected text
if 'selected_text_id' not in st.session_state:
    st.session_state.selected_text_id = None

# Load texts from database
with get_session() as session:
    texts = session.exec(select(Text).order_by(Text.difficulty)).all()
    
    # Check if we're in reading view
    if st.session_state.selected_text_id is not None:
        # READING VIEW - Show selected text with analysis
        selected_text = session.exec(
            select(Text).where(Text.id == st.session_state.selected_text_id)
        ).first()
        
        if selected_text:
            # Back button
            if st.button("⬅️ Volver a la lista de lecciones"):
                st.session_state.selected_text_id = None
                st.rerun()
            
            st.markdown("---")
            
            # Text header
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"## {selected_text.title}")
                if selected_text.author:
                    st.caption(f"📜 {selected_text.author.name}")
            
            with col2:
                mastery = calculate_mastery(session, selected_text.id)
                color = "green" if mastery >= 70 else "orange" if mastery >= 40 else "purple"
                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<span style='color: {color}; font-size: 2em; font-weight: bold;'>{mastery}%</span><br>"
                    f"<small>Maestría</small></div>",
                    unsafe_allow_html=True
                )
            
            st.progress(mastery / 100)
            st.markdown("---")
            
            # Render interactive text with morphological analysis
            interactive_html = render_interactive_text(selected_text.id, selected_text.content, session)
            st.markdown(interactive_html, unsafe_allow_html=True)
            
            # Legend below text
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Leyenda de colores:**
                - <span style='color: #10b981; font-weight: bold;'>●</span> Verde: Palabra bien aprendida (≥70%)
                - <span style='color: #f59e0b; font-weight: bold;'>●</span> Naranja: En progreso (40-70%)
                - <span style='color: #8b5cf6; font-weight: bold;'>●</span> Púrpura: Con dificultades (<40%)
                - <span style='color: #64748b; font-weight: bold;'>●</span> Gris: Aún no estudiada
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                **💡 Ayuda:**
                - Pasa el cursor sobre las palabras para análisis instantáneo
                - Las líneas punteadas indican palabras analizables
                - Los tooltips muestran lema, traducción y gramática
                """)
            
            # Stats and recommendations
            st.markdown("---")
            word_count = session.exec(
                select(TextWordLink).where(TextWordLink.text_id == selected_text.id)
            ).all()
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📊 Este texto contiene **{len(word_count)} palabras únicas** del vocabulario")
            
            with col2:
                if mastery < 70:
                    st.warning("💡 Practica el vocabulario en **Vocabularium** para mejorar tu maestría")
                else:
                    st.success("🎉 ¡Excelente dominio de este texto!")
        
        else:
            st.error("Texto no encontrado")
            if st.button("Volver a la lista"):
                st.session_state.selected_text_id = None
                st.rerun()
    
    else:
        # LIST VIEW - Show all available lessons
        if not texts:
            st.info("No hay textos disponibles. Usa el panel de Admin para añadir textos clásicos.")
            
            # Show sample text
            st.markdown("### 📚 Ejemplo: CAPITVLVM PRIMVM")
            
            sample_text = "Rōma in Italiā est. Italia in Eurōpā est. Graecia in Eurōpā est."
            
            # For preview, use text_id=-1 (will use fallback system)
            interactive_html = render_interactive_text(-1, sample_text, session)
            st.markdown(interactive_html, unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("💡 **Consejo:** Pasa el cursor sobre las palabras para ver su análisis morfológico")
            
            # Compact legend
            st.markdown("""
            **Colores:** 
            <span style='color: #10b981; font-weight: bold;'>●</span> Verde (≥70%) | 
            <span style='color: #f59e0b; font-weight: bold;'>●</span> Naranja (40-70%) | 
            <span style='color: #8b5cf6; font-weight: bold;'>●</span> Púrpura (<40%) | 
            <span style='color: #64748b; font-weight: bold;'>●</span> Gris (sin estudiar)
            """, unsafe_allow_html=True)
        
        else:
            # Show text list (no analysis here for performance)
            st.markdown("### 📚 Lecciones Disponibles")
            st.caption(f"Total: {len(texts)} lecciones • Haz clic para leer con análisis morfológico")
            
            st.markdown("---")
            
            for text in texts:
                mastery = calculate_mastery(session, text.id)
                
                # Card for each text
                col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{text.title}**")
                    if text.author:
                        st.caption(f"📜 {text.author.name}")
                
                with col2:
                    st.metric("Nivel", text.difficulty)
                
                with col3:
                    color = "green" if mastery >= 70 else "orange" if mastery >= 40 else "purple"
                    st.markdown(
                        f"<div style='text-align: center;'>"
                        f"<span style='color: {color}; font-size: 1.5em; font-weight: bold;'>{mastery}%</span><br>"
                        f"<small>Maestría</small></div>",
                        unsafe_allow_html=True
                    )
                
                with col4:
                    if st.button("📖 Leer", key=f"read_{text.id}"):
                        st.session_state.selected_text_id = text.id
                        st.rerun()
                
                # Progress bar
                st.progress(mastery / 100, text=f"Progreso: {mastery}%")
                
                st.markdown("---")
            
            # Help section at bottom
            st.markdown("### 💡 Cómo usar Lectio")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **📖 Lectura Interactiva:**
                - Selecciona una lección haciendo clic en "Leer"
                - Pasa el cursor sobre palabras para análisis instantáneo
                - Los tooltips muestran lema, traducción y morfología
                """)
            
            with col2:
                st.markdown("""
                **🎯 Sistema de Maestría:**
                - Verde (≥70%): Palabras bien dominadas
                - Naranja (40-70%): En proceso de aprendizaje
                - Púrpura (<40%): Necesitan más práctica
                - Gris: Aún no estudiadas
                """)
