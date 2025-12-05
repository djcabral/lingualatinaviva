"""
Vocabulary Practice Module (Refactored)
=======================================
This module implements smart vocabulary practice based on the user's current lesson progress.

SELECTION LOGIC:
1. Get user's current lesson from UserProgressSummary
2. Build selection pool:
   - NEW WORDS: Words from LessonVocabulary for current lesson not yet seen
   - REVIEW WORDS: Words from previous lessons due for SRS review
3. Prioritization:
   - 40% probability: Show new words (if available)
   - 60% probability: Show review words (if due)
   - Fallback: Random from past lessons
"""

import streamlit as st
from sqlmodel import select
from database import (
    get_session, Word, ReviewLog, UserProfile,
    LessonVocabulary, UserVocabularyProgress, UserProgressSummary
)
from utils.srs import calculate_next_review
from datetime import datetime
import random

from utils.i18n import get_text


def get_user_context():
    """Get the user's current learning context"""
    with get_session() as session:
        summary = session.exec(
            select(UserProgressSummary).where(UserProgressSummary.user_id == 1)
        ).first()
        
        if not summary:
            return {"current_lesson": 1, "completed_lessons": [], "max_unlocked": 1}
        
        import json
        completed = json.loads(summary.lessons_completed) if summary.lessons_completed else []
        
        return {
            "current_lesson": summary.current_lesson,
            "completed_lessons": completed,
            "max_unlocked": summary.current_lesson  # Assuming current is the highest unlocked
        }


def get_lesson_words(session, lesson_number: int):
    """Get all words for a specific lesson"""
    lesson_words = session.exec(
        select(LessonVocabulary)
        .where(LessonVocabulary.lesson_number == lesson_number)
        .order_by(LessonVocabulary.presentation_order)
    ).all()
    
    words = []
    for lw in lesson_words:
        word = session.get(Word, lw.word_id)
        if word:
            # Attach metadata for display
            word.is_essential = lw.is_essential
            words.append(word)
    return words


def select_next_card(target_lesson=None):
    """
    Smart card selection based on lesson context.
    If target_lesson is specified, focuses on that lesson.
    Returns a Word object or None.
    """
    context = get_user_context()
    current_lesson = context["current_lesson"]
    completed = context["completed_lessons"]
    
    with get_session() as session:
        # If a specific lesson is targeted
        if target_lesson:
            # Get all words for this lesson
            words = get_lesson_words(session, target_lesson)
            if not words:
                return None
                
            # Simple random choice for now, could be smarter (prioritize unseen)
            return random.choice(words)
            
        # Default "Smart Mode" (mix of new and review)
        new_words = get_new_words(session, current_lesson, limit=10)
        review_words = get_review_words(session, completed, limit=20)
        
        # Prioritization logic
        if new_words and review_words:
            # 40% new, 60% review
            if random.random() < 0.4:
                return random.choice(new_words)
            else:
                return random.choice(review_words)
        elif new_words:
            return random.choice(new_words)
        elif review_words:
            return random.choice(review_words)
        else:
            # Fallback: Any word from completed or current lesson
            all_lesson_words = session.exec(
                select(LessonVocabulary)
                .where(LessonVocabulary.lesson_number <= current_lesson)
            ).all()
            
            if all_lesson_words:
                lw = random.choice(all_lesson_words)
                return session.get(Word, lw.word_id)
            else:
                # Ultimate fallback: any word
                all_words = session.exec(select(Word)).all()
                return random.choice(all_words) if all_words else None


def show_vocabulary():
    st.markdown(f"## 🎴 {get_text('vocabulary', st.session_state.language)}")
    
    # Show lesson context
    context = get_user_context()
    max_lesson = context.get("max_unlocked", 1)
    
    # Lesson Selector
    lesson_options = ["Modo Inteligente (Smart)"] + [f"Lección {i}" for i in range(1, max_lesson + 1)]
    selected_option = st.selectbox(
        "Selecciona qué estudiar:",
        options=lesson_options,
        index=0
    )
    
    target_lesson = None
    if selected_option != "Modo Inteligente (Smart)":
        target_lesson = int(selected_option.split(" ")[1])
        st.caption(f"📘 Practicando vocabulario específico de la **Lección {target_lesson}**")
    else:
        st.caption(f"🧠 Modo Inteligente: Combinando repaso y palabras nuevas de Lección {context['current_lesson']}")
    
    # Reset card if lesson changed
    if "last_lesson_mode" not in st.session_state or st.session_state.last_lesson_mode != selected_option:
        st.session_state.last_lesson_mode = selected_option
        load_new_card(target_lesson)
        st.rerun()

    if "current_word_id" not in st.session_state:
        load_new_card(target_lesson)

    if st.session_state.current_word_id is None:
        st.info("¡No hay palabras disponibles para esta selección! Intenta con otra lección.")
        return

    with get_session() as session:
        word = session.get(Word, st.session_state.current_word_id)
        
        if not word:
            load_new_card(target_lesson)
            st.rerun()
            return

        # Check if essential (need to query LessonVocabulary)
        is_essential = False
        if target_lesson:
            lv = session.exec(
                select(LessonVocabulary)
                .where(LessonVocabulary.lesson_number == target_lesson)
                .where(LessonVocabulary.word_id == word.id)
            ).first()
            if lv and lv.is_essential:
                is_essential = True

        # Card Container
        essential_badge = '<span style="background-color: #FFD700; color: black; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; vertical-align: middle;">⭐ Esencial</span>' if is_essential else ""
        
        st.markdown(
            f"""
            <div class="vocab-card">
                <div class="vocab-latin">{word.latin} {essential_badge}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(get_text('show_answer', st.session_state.language), use_container_width=True):
            st.session_state.show_answer = True

        if st.session_state.get("show_answer", False):
            # Preferir traducción en español
            spanish_translation = word.definition_es or word.translation
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div class="vocab-translation">{spanish_translation}</div>
                    <div class="vocab-pos">{get_text(word.part_of_speech, st.session_state.language)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Show morphology hints if noun or verb
            if word.part_of_speech == "noun" and word.genitive:
                st.caption(f"📖 {word.latin}, {word.genitive} ({word.gender}.) - {word.declension}ª declinación")
            elif word.part_of_speech == "verb" and word.principal_parts:
                st.caption(f"📖 {word.principal_parts}")
            
            st.markdown(f"### {get_text('how_well', st.session_state.language)}")
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                if st.button(f"{get_text('again', st.session_state.language)} (1)", key="btn1"):
                    process_review(word.id, 1)
            with c2:
                if st.button(f"{get_text('hard', st.session_state.language)} (2)", key="btn2"):
                    process_review(word.id, 2)
            with c3:
                if st.button(f"{get_text('good', st.session_state.language)} (3)", key="btn3"):
                    process_review(word.id, 3)
            with c4:
                if st.button(f"{get_text('easy', st.session_state.language)} (4)", key="btn4"):
                    process_review(word.id, 4)


def load_new_card(target_lesson=None):
    word = select_next_card(target_lesson)
    if word:
        st.session_state.current_word_id = word.id
        st.session_state.show_answer = False
    else:
        st.session_state.current_word_id = None


def process_review(word_id, quality):
    """Process review and update SRS data"""
    
    # Determine current target lesson from session state if available
    target_lesson = None
    if "last_lesson_mode" in st.session_state and st.session_state.last_lesson_mode != "Modo Inteligente (Smart)":
        try:
            target_lesson = int(st.session_state.last_lesson_mode.split(" ")[1])
        except:
            pass

    with get_session() as session:
        # Get or create UserVocabularyProgress
        progress = session.exec(
            select(UserVocabularyProgress)
            .where(UserVocabularyProgress.user_id == 1)
            .where(UserVocabularyProgress.word_id == word_id)
        ).first()
        
        if not progress:
            progress = UserVocabularyProgress(
                user_id=1,
                word_id=word_id,
                times_seen=0,
                times_correct=0,
                times_incorrect=0
            )
            session.add(progress)
        
        # Update statistics
        progress.times_seen += 1
        if quality >= 3:
            progress.times_correct += 1
        else:
            progress.times_incorrect += 1
        
        # Calculate mastery
        total = progress.times_correct + progress.times_incorrect
        if total > 0:
            progress.mastery_level = progress.times_correct / total
        
        # Update SRS
        srs_data = calculate_next_review(quality + 1, None)
        progress.ease_factor = srs_data["ease_factor"]
        progress.interval_days = srs_data["interval"]
        progress.next_review_date = srs_data["next_review_date"]
        progress.last_reviewed = datetime.utcnow()
        
        # Mark as learning/mature
        if progress.mastery_level >= 0.95:
            progress.is_learning = False
        if progress.interval_days >= 21:
            progress.is_mature = True
        
        session.add(progress)
        
        # Add to ReviewLog
        log = ReviewLog(
            word_id=word_id,
            quality=quality + 1,
            ease_factor=srs_data["ease_factor"],
            interval=srs_data["interval"],
            repetitions=srs_data["repetitions"]
        )
        session.add(log)
        
        # Update XP
        user = session.exec(select(UserProfile)).first()
        if user:
            user.xp += 10
            session.add(user)
        
        session.commit()
    
    load_new_card(target_lesson)
    st.rerun()
