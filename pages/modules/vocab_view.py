import streamlit as st
import sys
import os
import random
from datetime import datetime, timedelta


from database.connection import get_session
from database import Word, ReviewLog, UserProfile, Text, TextWordLink, LessonVocabulary, UserProgressSummary
from sqlmodel import select
from utils.i18n import get_text
from utils.srs import calculate_next_review
from utils.gamification import process_xp_gain
from utils.ui_helpers import load_css
from utils.ui_components import render_flashcard
import json


def render_content():
    
    # Load CSS
    load_css()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'es'
    
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'current_word_id' not in st.session_state:
        st.session_state.current_word_id = None
    if 'study_mode' not in st.session_state:
        st.session_state.study_mode = 'general'
    if 'selected_text_id' not in st.session_state:
        st.session_state.selected_text_id = None
    
    st.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            🎴 Vocabularium - Flashcards SRS
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    # Study Mode Selector
    with get_session() as session:
        # Get user's current lesson
        progress_summary = session.exec(select(UserProgressSummary).where(UserProgressSummary.user_id == 1)).first()
        current_lesson = progress_summary.current_lesson if progress_summary else 1
        
        texts = session.exec(select(Text)).all()
        
        # Banner contextual
        st.info(f"📚 **Estás en Lección {current_lesson}** | El vocabulario se filtrará automáticamente a menos que elijas otra opción.")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            mode = st.radio(
                "Modo de Estudio:",
                ["lesson", "general", "text_prep"],
                format_func=lambda x: f"📘 Lección {current_lesson}" if x == "lesson" else ("📚 General (SRS)" if x == "general" else "📖 Preparación de Texto"),
                horizontal=True,
                key="mode_selector"
            )
            st.session_state.study_mode = mode
        
        with col2:
            if mode == "lesson":
                lesson_filter = st.selectbox(
                    "Lección:",
                    options=list(range(1, 41)),
                    index=current_lesson - 1,
                    key="lesson_filter"
                )
                st.session_state.selected_lesson = lesson_filter
            elif mode == "text_prep":
                if texts:
                    text_options = {t.id: f"{t.title} ({t.author.name if t.author else 'Anónimo'})" for t in texts}
                    selected = st.selectbox(
                        "Selecciona un texto:",
                        options=list(text_options.keys()),
                        format_func=lambda x: text_options[x]
                    )
                    st.session_state.selected_text_id = selected
                else:
                    st.warning("No hay textos disponibles. Añade textos en el panel de Admin.")
                    st.stop()
        
        with col3:
            if mode == "lesson":
                # Mostrar progreso de vocabulario de la lección
                lesson_vocab_links = session.exec(
                    select(LessonVocabulary).where(LessonVocabulary.lesson_number == lesson_filter)
                ).all()
                if lesson_vocab_links:
                    st.metric("Palabras", len(lesson_vocab_links))
                else:
                    st.caption("Sin vocab asignado")
    
    
    st.markdown("---")
    
    # Contextual navigation links
    if st.session_state.study_mode == "lesson":
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.page_link("pages/02_📘_Lecciones.py", label="Volver al Curso", icon="📘")
            st.page_link("pages/04_⚔️_Práctica.py", label="Practicar Declinaciones", icon="📜")
            st.page_link("pages/02_📘_Lecciones.py", label="Ir a Lecturas", icon="📖")
        st.markdown("---")
    
    
    # Define handle_review BEFORE using it
    def handle_review(session, word, quality):
        """Handle SRS review logic"""
        # Get previous review for this word
        previous_review = session.exec(
            select(ReviewLog).where(ReviewLog.word_id == word.id).order_by(ReviewLog.review_date.desc())
        ).first()
        
        # Calculate next review
        result = calculate_next_review(quality, previous_review)
        
        # Create new review log
        new_review = ReviewLog(
            word_id=word.id,
            review_date=datetime.now(),
            quality=quality,
            ease_factor=result['ease_factor'],
            interval=result['interval'],
            repetitions=result['repetitions']
        )
        session.add(new_review)
        
        # Update user XP
        user = session.exec(select(UserProfile)).first()
        if user:
            xp_gain = {0: 1, 2: 3, 4: 5, 5: 10}.get(quality, 5)
            new_level, leveled_up = process_xp_gain(session, user, xp_gain)
            
            if leveled_up:
                st.balloons()
                st.success(f"🎉 ¡FELICIDADES! Has alcanzado el Nivel {new_level}!")
        
        # Reset state for next word
        st.session_state.show_answer = False
        st.session_state.current_word_id = None
        st.success(f"¡Bien! +{xp_gain} XP")
        st.rerun()
    
    with get_session() as session:
        # OPTIMIZATION: Check if we already have a word to avoid expensive queries
        word = None
        if st.session_state.current_word_id is not None:
            word = session.get(Word, st.session_state.current_word_id)
            # If word not found (deleted?), reset
            if not word:
                st.session_state.current_word_id = None
    
        # Only run selection logic if we need a new word
        if st.session_state.current_word_id is None:
            
            # --- WORD SELECTION LOGIC ---
            
            # 1. Check for due reviews first (SRS)
            due_word_ids = []
            
            if st.session_state.study_mode in ["general", "lesson"]:
                # Get the latest review for each word
                all_reviews = session.exec(
                    select(ReviewLog).order_by(ReviewLog.review_date.desc())
                ).all()
                
                latest_reviews = {}
                for review in all_reviews:
                    if review.word_id not in latest_reviews:
                        latest_reviews[review.word_id] = review
                
                # Find due words
                now = datetime.utcnow()
                for word_id, review in latest_reviews.items():
                    next_review = review.review_date + timedelta(days=review.interval)
                    if next_review <= now:
                        due_word_ids.append(word_id)
                        
            # 2. Select word
            
            # MODE: LESSON - Practice vocabulary from specific lesson
            if st.session_state.study_mode == "lesson":
                lesson_num = st.session_state.get('selected_lesson', 1)
                lesson_vocab_links = session.exec(
                    select(LessonVocabulary).where(LessonVocabulary.lesson_number == lesson_num)
                ).all()
                lesson_word_ids = [link.word_id for link in lesson_vocab_links]
                
                if not lesson_word_ids:
                    st.warning(f"⚠️ La Lección {lesson_num} no tiene vocabulario asignado aún.")
                    st.info("💡 **Sugerencia:** Cambia a modo 'General' o contacta al administrador.")
                    st.stop()
                
                # Priority 1: Due reviews from this lesson
                lesson_due = [wid for wid in due_word_ids if wid in lesson_word_ids]
                if lesson_due:
                    st.info(f"📝 Tienes {len(lesson_due)} palabras de Lección {lesson_num} para repasar.")
                    word = session.get(Word, random.choice(lesson_due))
                else:
                    # Priority 2: New words from this lesson (not yet reviewed)
                    reviewed_ids = list(latest_reviews.keys()) if 'latest_reviews' in locals() else []
                    new_lesson_words = [wid for wid in lesson_word_ids if wid not in reviewed_ids]
                    
                    if new_lesson_words:
                        word = session.get(Word, random.choice(new_lesson_words))
                    else:
                        # All words reviewed, show random from lesson
                        word = session.get(Word, random.choice(lesson_word_ids))
                        st.success(f"✅ ¡Has visto todas las palabras de Lección {lesson_num}!")
            
            # PRIORITY 1: Due Reviews (SRS) - Mode GENERAL
            elif due_word_ids and st.session_state.study_mode == "general":
                st.info(f"📝 Tienes {len(due_word_ids)} palabras para repasar hoy.")
                word_id = random.choice(due_word_ids)
                word = session.get(Word, word_id)
                
            # PRIORITY 2: New Words (if no reviews due) - Mode GENERAL
            elif st.session_state.study_mode == "general":
                priority_tier = st.sidebar.selectbox(
                    "🎯 Prioridad de Aprendizaje",
                    [100, 500, 1000, 2000, 5000, "Todas"],
                    format_func=lambda x: f"Top {x} palabras más usadas" if isinstance(x, int) else "Todas las palabras"
                )
                
                query = select(Word).where(Word.status == 'active')
                
                # Exclude words that have already been reviewed (and are not due)
                reviewed_word_ids = list(latest_reviews.keys()) if 'latest_reviews' in locals() else []
                if reviewed_word_ids:
                    query = query.where(Word.id.not_in(reviewed_word_ids))
                
                if isinstance(priority_tier, int):
                    query = query.where(Word.frequency_rank_global <= priority_tier)
                    query = query.where(Word.frequency_rank_global > 0)
                    
                potential_words = session.exec(query).all()
                
                if potential_words:
                    potential_words.sort(key=lambda w: w.frequency_rank_global if w.frequency_rank_global else 99999)
                    candidates = potential_words[:50]
                    word = random.choice(candidates)
                else:
                    st.success("¡Has estudiado todas las palabras nuevas de este nivel! 🎉")
                
            else:  # text_prep
                if st.session_state.selected_text_id:
                    links = session.exec(
                        select(TextWordLink).where(TextWordLink.text_id == st.session_state.selected_text_id)
                    ).all()
                    word_ids = [link.word_id for link in links]
                    if word_ids:
                        word = session.get(Word, random.choice(word_ids))
                    else:
                        st.info("Este texto no tiene palabras vinculadas aún.")
                        st.stop()
                else:
                    st.warning("Selecciona un texto para estudiar.")
                    st.stop()
            
            if word:
                st.session_state.current_word_id = word.id
            else:
                st.warning("No hay palabras disponibles con los filtros actuales.")
                st.stop()
        
        if word is None:
            st.error("Error cargando palabra")
            st.stop()
        
        # --- SIDEBAR TRANSLATION EDITOR ---
        if st.session_state.get('is_admin', False):
            with st.sidebar:
                st.divider()
                st.markdown("### 🔧 Corrector Rápido")
                st.info("Edita la traducción de la tarjeta actual.")
                
                current_translation = word.translation or ""
                # Use a key based on word ID to ensure it resets when word changes
                new_translation = st.text_input(
                    "Traducción:", 
                    value=current_translation,
                    key=f"trans_edit_{word.id}"
                )
                
                if st.button("💾 Guardar Cambios", key=f"save_{word.id}"):
                    if new_translation and new_translation != current_translation:
                        word.translation = new_translation
                        session.add(word)
                        session.commit()
                        st.success("¡Actualizado!")
                        st.rerun()
    
        
        # Display word card
        
        # Homonym handling
        display_word = word.latin
        disambiguation_hint = ""
        
        if any(char.isdigit() for char in word.latin):
            # Strip digits for display
            display_word = ''.join([c for c in word.latin if not c.isdigit()])
            
            # Generate hint based on POS
            if word.part_of_speech == 'verb':
                if word.conjugation:
                    disambiguation_hint = f"({word.conjugation})"
                elif word.principal_parts:
                    # Try to show just the infinitive if possible, or full parts
                    parts = word.principal_parts.split(', ')
                    if len(parts) >= 2:
                        disambiguation_hint = f"({parts[1]})"
                    else:
                        disambiguation_hint = f"({word.principal_parts})"
            
            elif word.part_of_speech == 'noun':
                if word.genitive:
                    disambiguation_hint = f"(Gen: {word.genitive})"
                elif word.declension:
                    disambiguation_hint = f"({word.declension} decl.)"
                    
            elif word.part_of_speech == 'adjective':
                 if word.genitive: # e.g. felix, felicis
                    disambiguation_hint = f"({word.genitive})"
        
        # Determine if we show translation/details (Answer Side)
        translation_text = None
        pos_text = None
        
        if st.session_state.show_answer:
            translation_text = word.definition_es or word.translation
            pos_text = get_text(word.part_of_speech, st.session_state.language)
            
        # Render using standardized component
        render_flashcard(
            latin_text=display_word,
            hint=disambiguation_hint,
            translation=translation_text,
            part_of_speech=pos_text
        )
        
        # Show answer button
        if not st.session_state.show_answer:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("📖 " + get_text('show_answer', st.session_state.language), width='stretch'):
                    st.session_state.show_answer = True
                    st.rerun()
        else:
            # Show additional info (Genitive, Principal Parts) - outside the card
            if word.genitive:
                st.info(f"**Genitivo:** {word.genitive}")
            if word.principal_parts:
                st.info(f"**Partes principales:** {word.principal_parts}")
            
            st.markdown("---")
            st.markdown(f"**{get_text('how_well', st.session_state.language)}**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("❌ " + get_text('again', st.session_state.language), width='stretch'):
                    handle_review(session, word, 0)
            
            with col2:
                if st.button("😓 " + get_text('hard', st.session_state.language), width='stretch'):
                    handle_review(session, word, 2)
            
            with col3:
                if st.button("✅ " + get_text('good', st.session_state.language), width='stretch'):
                    handle_review(session, word, 4)
            
            with col4:
                if st.button("⭐ " + get_text('easy', st.session_state.language), width='stretch'):
                    handle_review(session, word, 5)
    
    # Render sidebar footer
    from utils.ui import render_sidebar_footer
    render_sidebar_footer()
