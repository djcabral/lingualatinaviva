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

# Add custom CSS for interactive text
def add_interactive_text_css():
    st.markdown("""
    <style>
    .interactive-word {
        cursor: pointer;
        padding: 2px 4px;
        border-radius: 3px;
        transition: all 0.2s;
        display: inline-block;
        margin: 0 1px;
    }
    .interactive-word:hover {
        background-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
    }
    .word-known {
        color: #10b981;
        font-weight: 500;
    }
    .word-learning {
        color: #f59e0b;
        font-weight: 500;
    }
    .word-unknown {
        color: #ef4444;
        font-weight: 500;
    }
    .word-invariable {
        color: #94a3b8;
    }
    .analysis-popup {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .analysis-popup strong {
        font-size: 1.2em;
        display: block;
        margin-bottom: 5px;
    }
    .morphology-tag {
        background: rgba(255,255,255,0.2);
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 0.9em;
        display: inline-block;
        margin: 2px;
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

def render_interactive_text(text_content: str, session):
    """Renderiza texto latino con análisis interactivo palabra por palabra"""
    
    # Analizar el texto
    analyzed_text = LatinTextAnalyzer.analyze_text(text_content, session)
    
    # Dividir en oraciones para mejor formato
    sentences = []
    current_sentence = []
    
    for item in analyzed_text:
        current_sentence.append(item)
        if item.get("is_punctuation") and item["form"] in ".!?":
            sentences.append(current_sentence)
            current_sentence = []
    
    if current_sentence:  # Agregar última oración si no termina en puntuación
        sentences.append(current_sentence)
    
    # Renderizar oraciones
    html_parts = ["<div style='font-family: \"Cardo\", serif; font-size: 1.2em; line-height: 2; text-align: justify;'>"]
    
    for sentence in sentences:
        html_parts.append("<p>")
        for item in sentence:
            form = item["form"]
            
            if item.get("is_punctuation"):
                html_parts.append(form)
            else:
                analyses = item["analyses"]
                
                if analyses:
                    # Palabra analizada
                    primary = analyses[0]  # Tomar el análisis más probable
                    
                    # Determinar color según maestría
                    mastery = get_word_mastery(session, primary["word_id"])
                    if mastery >= 70:
                        css_class = "word-known"
                    elif mastery >= 40:
                        css_class = "word-learning"
                    else:
                        css_class = "word-unknown"
                    
                    # Crear ID único para este análisis
                    word_id = f"word_{item['position']}"
                    
                    # Formatear análisis morfológico
                    morph_text = LatinTextAnalyzer.format_morphology(
                        primary["morphology"], 
                        primary["pos"]
                    )
                    
                    # HTML para palabra interactiva
                    word_html = f'''<span class="interactive-word {css_class}" 
                        onclick="document.getElementById('{word_id}_analysis').style.display = 
                        document.getElementById('{word_id}_analysis').style.display === 'none' ? 'block' : 'none'">
                        {form}
                    </span>'''
                    
                    html_parts.append(word_html)
                    
                    # Popup de análisis (inicialmente oculto)
                    analysis_html = f'''
                    <div id="{word_id}_analysis" class="analysis-popup" style="display: none;">
                        <strong>{primary["lemma"]}</strong>
                        <div>{primary["translation"]}</div>
                        <div><em>{morph_text}</em></div>
                        <span class="morphology-tag">{primary["pos"]}</span>
                    </div>
                    '''
                    html_parts.append(analysis_html)
                else:
                    # Palabra desconocida (no en BD)
                    html_parts.append(f'<span style="color: #94a3b8;">{form}</span>')
            
            html_parts.append(" ")
        html_parts.append("</p>")
    
    html_parts.append("</div>")
    
    return "".join(html_parts)

# Load texts from database
with get_session() as session:
    texts = session.exec(select(Text).order_by(Text.difficulty)).all()
    
    if not texts:
        st.info("No hay textos disponibles. Usa el panel de Admin para añadir textos clásicos.")
        
        # Show sample text with interactive analysis
        st.markdown("### CAPITVLVM PRIMVM: IMPERIVM ROMANVM")
        
        sample_text = "Rōma in Italiā est. Italia in Eurōpā est. Graecia in Eurōpā est. Italia et Graecia in Eurōpā sunt."
        
        interactive_html = render_interactive_text(sample_text, session)
        st.markdown(interactive_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("💡 **Consejo:** Haz click en cualquier palabra para ver su análisis morfológico completo.")
        
        # Leyenda de colores
        st.markdown("""
        **Leyenda de colores:**
        - <span style='color: #10b981; font-weight: bold;'>Verde</span>: Palabra conocida (maestría ≥70%)
        - <span style='color: #f59e0b; font-weight: bold;'>Naranja</span>: Palabra en aprendizaje (maestría 40-70%)
        - <span style='color: #ef4444; font-weight: bold;'>Rojo</span>: Palabra desconocida (maestría <40%)
        - <span style='color: #94a3b8;'>Gris</span>: Palabra no en vocabulario
        """, unsafe_allow_html=True)
    else:
        # Show text list with mastery scores
        st.markdown("### Textos Disponibles")
        
        for text in texts:
            mastery = calculate_mastery(session, text.id)
            
            # Get word count
            word_count = session.exec(
                select(TextWordLink).where(TextWordLink.text_id == text.id)
            ).all()
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{text.title}**")
                if text.author:
                    st.caption(f"por {text.author.name}")
            
            with col2:
                st.metric("Nivel", text.difficulty)
            
            with col3:
                color = "green" if mastery >= 70 else "orange" if mastery >= 40 else "red"
                st.markdown(f"<div style='text-align: center;'><span style='color: {color}; font-size: 1.5em; font-weight: bold;'>{mastery}%</span><br><small>Maestría</small></div>", unsafe_allow_html=True)
            
            # Progress bar
            st.progress(mastery / 100)
            
            # Expandable content with interactive text
            with st.expander(f"📖 Leer '{text.title}'"):
                # Render interactive text
                interactive_html = render_interactive_text(text.content, session)
                st.markdown(interactive_html, unsafe_allow_html=True)
                
                st.markdown("---")
                st.info(f"📊 Este texto contiene {len(word_count)} palabras únicas del vocabulario.")
                
                # Tips
                st.markdown("""
                💡 **Ayuda:**
                - **Haz click** en cualquier palabra para ver su análisis morfológico
                - Los colores indican tu nivel de maestría con cada palabra
                - Las palabras grises no están en tu vocabulario activo
                """)
                
                if mastery < 70:
                    st.warning(f"💡 Practica el vocabulario de este texto en el módulo **Vocabularium** para mejorar tu maestría.")
            
            st.markdown("---")
