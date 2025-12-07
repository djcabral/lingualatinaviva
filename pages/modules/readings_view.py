import streamlit as st
import sys
import os



from database.connection import get_session
from database import Word, Text, TextWordLink, ReviewLog, UserProfile
from utils.text_analyzer import LatinTextAnalyzer
from utils.text_cache import get_text_analysis_from_cache
from utils.i18n import get_text
from utils.ui_helpers import load_css
from sqlmodel import select



# Load CSS


# Add custom CSS for interactive text with hover tooltips
def add_interactive_text_css(font_size=1.3):
    """Add CSS with dynamic font size parameter"""
    st.markdown(f"""
    <style>
    .latin-text-container {{
        position: relative;
        font-family: 'Cardo', 'Georgia', serif;
        font-size: {font_size * 1.5}em;
        line-height: 2.5;
        text-align: justify;
        padding: 1.5rem;
        background: rgba(0, 0, 0, 0.03);
        border-radius: 8px;
    }}
    .interactive-word {{
        position: relative;
        cursor: help;
        padding: 3px 5px;
        border-radius: 3px;
        transition: all 0.2s;
        display: inline;
        border-bottom: 2px dotted currentColor;
    }}
    .interactive-word:hover {{
        background-color: rgba(100, 100, 255, 0.15);
    }}
    
    /* Tooltip que aparece al hacer hover */
    .interactive-word .tooltip {{
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 280px;
        max-width: 90vw;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 15px;
        border-radius: 8px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        transition: opacity 0.3s, visibility 0.3s;
        pointer-events: none;
        white-space: normal;
        word-wrap: break-word;
    }}
    
    /* Ajustar tooltip cuando está cerca del borde izquierdo */
    .latin-text-container .interactive-word:first-child .tooltip,
    .interactive-word:nth-child(-n+3) .tooltip {{
        left: 0;
        transform: translateX(0);
    }}
    
    /* Flecha del tooltip */
    .interactive-word .tooltip::after {{
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #764ba2 transparent transparent transparent;
    }}
    
    /* Flecha también se ajusta cuando está a la izquierda */
    .latin-text-container .interactive-word:first-child .tooltip::after,
    .interactive-word:nth-child(-n+3) .tooltip::after {{
        left: 20px;
    }}
    
    /* Mostrar tooltip al hacer hover */
    .interactive-word:hover .tooltip {{
        visibility: visible;
        opacity: 1;
    }}
    
    .tooltip-lemma {{
        font-size: 1.2em;
        font-weight: bold;
        display: block;
        margin-bottom: 4px;
        font-family: 'Cinzel', serif;
    }}
    
    .tooltip-translation {{
        font-size: 1em;
        display: block;
        margin-bottom: 6px;
    }}
    
    .tooltip-morphology {{
        font-size: 0.85em;
        font-style: italic;
        display: block;
        margin-bottom: 4px;
        opacity: 0.9;
    }}
    
    .tooltip-pos {{
        background: rgba(255,255,255,0.25);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75em;
        display: inline-block;
        margin-top: 4px;
    }}
    
    /* Colores según maestría - MÁS OSCUROS PARA MEJOR LEGIBILIDAD */
    .word-known {{
        color: #059669;
        border-bottom-color: #059669;
    }}
    .word-learning {{
        color: #d97706;
        border-bottom-color: #d97706;
    }}
    .word-unknown {{
        color: #7c3aed;
        border-bottom-color: #7c3aed;
    }}
    .word-no-review {{
        color: #1e293b;
        border-bottom-color: #475569;
    }}
    </style>
    """, unsafe_allow_html=True)

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
    from utils.text_cache import get_text_analysis_from_cache
    
    # Intentar obtener análisis CLTK cacheado
    analyzed_text = get_text_analysis_from_cache(session, text_id)
    
    # Si no hay análisis CLTK, usar sistema actual con InflectedForm
    if not analyzed_text:
        analyzed_text = LatinTextAnalyzer.analyze_text(text_content, session)
    
    # Renderizar con tooltips hover - ESTILOS INLINE para forzar visualización
    html_parts = ['<div class="latin-text-container" style="font-size: 24px; line-height: 2.0; color: #1a1a1a; background: #fafafa; border-radius: 8px;"><p>']
    
    is_first_word = True
    prev_was_punctuation = False
    
    for item in analyzed_text:
        form = item["form"]
        
        if item.get("is_punctuation"):
            # Puntuación: sin espacio antes, pero marcar para espacio después
            html_parts.append(form)
            prev_was_punctuation = True
        else:
            # Palabra: añadir espacio ANTES (excepto si es la primera palabra)
            if not is_first_word:
                html_parts.append(" ")
            is_first_word = False
            prev_was_punctuation = False
            
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
                    translation = primary.get("translation", "[...]")
                    pos = primary.get("pos", "unknown")
                    morphology = primary.get("morphology", {})
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
                
                # HTML para palabra con tooltip hover - SIN ESPACIOS INTERNOS para evitar problemas de espaciado
                word_html = f'<span class="interactive-word {css_class}" style="color: #1a1a1a !important;">{form}<span class="tooltip"><span class="tooltip-lemma">{lemma}</span><span class="tooltip-translation">{translation}</span><span class="tooltip-morphology">{morph_text}</span><span class="tooltip-pos">{pos_display}</span></span></span>'
                
                html_parts.append(word_html)
            else:
                # Palabra desconocida (no en BD ni CLTK)
                html_parts.append(f'<span style="color: #1a1a1a;">{form}</span>')
    
    html_parts.append("</p></div>")
    
    return "".join(html_parts)

def render_readings_content():
    # Page config and header handled by parent
    import json
    
    # Load user preferences
    # Note: Global font size is already loaded in session_state by render_sidebar_config
    preferences = {}
    font_size = 1.3  # default
    
    # Add custom CSS for interactive text with hover tooltips
    add_interactive_text_css(font_size)
    
    # --- SIDEBAR CONFIGURATION ---
    # Global font size is now handled by render_sidebar_config in the parent page
    # We just need to use the current font size for the text container
    
    font_size = 1.3 # Default fallback
    if 'global_font_size' in st.session_state:
        # Scale slightly larger for reading text vs UI text
        font_size = st.session_state.global_font_size * 1.2
    
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
                
                # --- SIDEBAR VOCABULARY EDITOR ---
                with st.sidebar:
                    st.divider()
                    st.markdown("### 🔧 Corrector Rápido")
                    st.info("Corrige traducciones mientras lees.")
                    
                    # Get analysis data for the editor
                    analysis_data = get_text_analysis_from_cache(session, selected_text.id)
                    
                    if analysis_data:
                        # Filter valid words with IDs
                        valid_words = []
                        seen_ids = set()
                        
                        for item in analysis_data:
                            # Handle both direct structure and 'analyses' list structure
                            wid = item.get("word_id")
                            latin = item.get("lemma")
                            trans = item.get("translation")
                            
                            if not wid and item.get("analyses"):
                                primary = item["analyses"][0]
                                wid = primary.get("word_id")
                                latin = primary.get("lemma")
                                trans = primary.get("translation")
                                
                            if wid and latin and wid not in seen_ids:
                                valid_words.append((wid, latin, trans))
                                seen_ids.add(wid)
                        
                        # Sort by Latin word
                        valid_words.sort(key=lambda x: x[1])
                        
                        if valid_words:
                            selected_word_tuple = st.selectbox(
                                "Selecciona palabra:",
                                options=valid_words,
                                format_func=lambda x: f"{x[1]} ({x[2][:20]}...)" if x[2] else f"{x[1]}"
                            )
                            
                            if selected_word_tuple:
                                wid, latin, trans = selected_word_tuple
                                st.markdown(f"**Latín:** {latin}")
                                
                                new_trans = st.text_input("Traducción:", value=trans if trans else "")
                                
                                if st.button("💾 Guardar Corrección"):
                                    if new_trans:
                                        word_to_update = session.get(Word, wid)
                                        if word_to_update:
                                            word_to_update.translation = new_trans
                                            session.add(word_to_update)
                                            session.commit()
                                            st.success("¡Guardado!")
                                            st.rerun()
                            else:
                                st.caption("No hay palabras válidas seleccionadas.")
                    else:
                        st.caption("No hay datos de análisis disponibles.")
                
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
                st.markdown("### 📚 Ejemplo: CAPITVLVM PRIMUM")
                
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
                # Show text list grouped by level for better organization
                st.markdown("### 📚 Lecturas Disponibles")
                st.caption(f"Total: {len(texts)} textos • Haz clic para leer con análisis morfológico")
                
                # Group texts by difficulty ranges
                basic = [t for t in texts if t.difficulty <= 10]
                intermediate = [t for t in texts if 11 <= t.difficulty <= 20]
                advanced = [t for t in texts if t.difficulty >= 21]
                
                tabs = st.tabs(["🌱 Básico (1-10)", "💎 Intermedio (11-20)", "🏆 Avanzado (21-30)"])
                
                for tab_idx, (tab, text_group) in enumerate(zip(tabs, [basic, intermediate, advanced])):
                    with tab:
                        if not text_group:
                            st.info("No hay textos en este nivel.")
                            continue
                        
                        for text in text_group:
                            mastery = calculate_mastery(session, text.id)
                            
                            with st.container():
                                col1, col2, col3 = st.columns([5, 1, 1])
                                
                                with col1:
                                    st.markdown(f"**L{text.difficulty}: {text.title}**")
                                
                                with col2:
                                    color = "green" if mastery >= 70 else "orange" if mastery >= 40 else "gray"
                                    st.markdown(f"<span style='color: {color}; font-weight: bold;'>{mastery}%</span>", unsafe_allow_html=True)
                                
                                with col3:
                                    if st.button("📖", key=f"read_{text.id}", help="Leer"):
                                        st.session_state.selected_text_id = text.id
                                        st.rerun()
                            
                            st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #333;'>", unsafe_allow_html=True)
                
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
