import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Text, TextWordLink, Word, ReviewLog
from sqlmodel import select

st.set_page_config(page_title="Lectio", page_icon="📖", layout="wide")

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
        # Check if word has been reviewed with interval > 3 days
        latest_review = session.exec(
            select(ReviewLog)
            .where(ReviewLog.word_id == link.word_id)
            .order_by(ReviewLog.review_date.desc())
        ).first()
        
        if latest_review and latest_review.interval >= 3:
            known_words += 1
    
    return int((known_words / len(links)) * 100)

# Load texts from database
with get_session() as session:
    texts = session.exec(select(Text).order_by(Text.level)).all()
    
    if not texts:
        st.info("No hay textos disponibles. Usa el panel de Admin para añadir textos clásicos.")
        
        # Show sample text
        st.markdown("### CAPITVLVM PRIMVM: IMPERIVM ROMANVM")
        
        text = """
Rōma in Italiā est. Italia in Eurōpā est. Graecia in Eurōpā est. Italia et Graecia in Eurōpā sunt. Hispānia quoque in Eurōpā est. Hispānia et Italia et Graecia in Eurōpā sunt.

Aegyptus in Eurōpā nōn est, Aegyptus in Āfricā est. Gallia nōn in Āfricā est, Gallia est in Eurōpā. Syria nōn est in Eurōpā, sed in Asiā. Arabia quoque in Asiā est. Syria et Arabia in Asiā sunt. Germānia nōn in Asiā, sed in Eurōpā est. Britannia quoque in Eurōpā est. Germānia et Britannia sunt in Eurōpā.

Estne Gallia in Eurōpā? Gallia in Eurōpā est. Estne Rōma in Galliā? Rōma in Galliā nōn est. Ubi est Rōma? Rōma est in Italiā. Ubi est Italia? Italia in Eurōpā est. Ubi sunt Gallia et Hispānia? Gallia et Hispānia in Eurōpā sunt.
        """
        
        st.markdown(
            f"""
            <div style="font-family: 'Cardo', serif; font-size: 1.2em; line-height: 1.6; text-align: justify; background-color: rgba(255,255,255,0.4); padding: 20px; border-radius: 5px;">
                {text.replace(chr(10), '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        st.info("💡 **Consejo:** Lee en voz alta para practicar la pronunciación. Presta atención a las vocales largas (macrones).")
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
                    st.caption(f"por {text.author}")
            
            with col2:
                st.metric("Nivel", text.level)
            
            with col3:
                color = "green" if mastery >= 70 else "orange" if mastery >= 40 else "red"
                st.markdown(f"<div style='text-align: center;'><span style='color: {color}; font-size: 1.5em; font-weight: bold;'>{mastery}%</span><br><small>Maestría</small></div>", unsafe_allow_html=True)
            
            # Progress bar
            st.progress(mastery / 100)
            
            # Expandable content
            with st.expander(f"📖 Leer '{text.title}'"):
                st.markdown(
                    f"""
                    <div style="font-family: 'Cardo', serif; font-size: 1.2em; line-height: 1.6; text-align: justify; background-color: rgba(255,255,255,0.4); padding: 20px; border-radius: 5px;">
                        {text.content.replace(chr(10), '<br>')}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("---")
                st.info(f"📊 Este texto contiene {len(word_count)} palabras únicas del vocabulario.")
                
                if mastery < 70:
                    st.warning(f"💡 Practica el vocabulario de este texto en el módulo **Vocabularium** (Modo: Preparación de Texto) para mejorar tu maestría.")
            
            st.markdown("---")
