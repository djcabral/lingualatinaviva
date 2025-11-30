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

from i18n import get_text


def get_user_context():
    """Get the user's current learning context"""
    with get_session() as session:
        summary = session.exec(
            select(UserProgressSummary).where(UserProgressSummary.user_id == 1)
        ).first()
        
        if not summary:
            return {"current_lesson": 1, "completed_lessons": []}
        
        import json
        completed = json.loads(summary.lessons_completed) if summary.lessons_completed else []
        
        return {
            "current_lesson": summary.current_lesson,
            "completed_lessons": completed
        }


def get_new_words(session, current_lesson: int, limit=10):
    """
    Get new words from the current lesson that haven't been practiced yet.
    Prioritizes high-frequency words (most used in classical texts).
    """
    # Get essential words from current lesson, ordered by frequency
    lesson_words = session.exec(
        select(LessonVocabulary)
        .where(LessonVocabulary.lesson_number == current_lesson)
        .where(LessonVocabulary.is_essential == True)
        .order_by(LessonVocabulary.presentation_order)  # Lower = more frequent
    ).all()
    
    if not lesson_words:
        return []
    
    # Filter out words already seen
    new_words = []
    for lw in lesson_words:
        progress = session.exec(
            select(UserVocabularyProgress)
            .where(UserVocabularyProgress.user_id == 1)
            .where(UserVocabularyProgress.word_id == lw.word_id)
        ).first()
        
        if not progress or progress.times_seen == 0:
            word = session.get(Word, lw.word_id)
            if word:
                new_words.append(word)
                if len(new_words) >= limit:
                    break  # Stop after limit (already ordered by frequency)
    
    return new_words


def get_review_words(session, completed_lessons: list, limit=20):
    """
    Get words from completed lessons that are due for review (SRS).
    """
    if not completed_lessons:
        return []
    
    # Get all words from completed lessons
    lesson_words = session.exec(
        select(LessonVocabulary)
        .where(LessonVocabulary.lesson_number.in_(completed_lessons))
    ).all()
    
    due_words = []
    now = datetime.utcnow()
    
    for lw in lesson_words:
        progress = session.exec(
            select(UserVocabularyProgress)
            .where(UserVocabularyProgress.user_id == 1)
            .where(UserVocabularyProgress.word_id == lw.word_id)
        ).first()
        
        if progress and progress.times_seen > 0:
            # Check if due for review
            if progress.next_review_date and progress.next_review_date <= now:
                word = session.get(Word, lw.word_id)
                if word:
                    due_words.append(word)
            # If no next_review_date but seen, include with lower priority
            elif not progress.next_review_date and progress.times_seen < 3:
                word = session.get(Word, lw.word_id)
                if word:
                    due_words.append(word)
    
    return due_words[:limit]


def select_next_card():
    """
    Smart card selection based on lesson context.
    Returns a Word object or None.
    """
    context = get_user_context()
    current_lesson = context["current_lesson"]
    completed = context["completed_lessons"]
    
    with get_session() as session:
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
    st.caption(f"📘 Practicando desde la Lección {context['current_lesson']}")
    
    if "current_word_id" not in st.session_state:
        load_new_card()

    if st.session_state.current_word_id is None:
        st.warning(get_text('no_words', st.session_state.language))
        return

    with get_session() as session:
        word = session.get(Word, st.session_state.current_word_id)
        
        if not word:
            load_new_card()
            st.rerun()
            return

        # Card Container
        st.markdown(
            f"""
            <div class="vocab-card">
                <div class="vocab-latin">{word.latin}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(get_text('show_answer', st.session_state.language), use_container_width=True):
            st.session_state.show_answer = True

        if st.session_state.get("show_answer", False):
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div class="vocab-translation">{word.translation}</div>
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


def load_new_card():
    word = select_next_card()
    if word:
        st.session_state.current_word_id = word.id
        st.session_state.show_answer = False
    else:
        st.session_state.current_word_id = None


def process_review(word_id, quality):
    """Process review and update SRS data"""
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
    
    load_new_card()
    st.rerun()
