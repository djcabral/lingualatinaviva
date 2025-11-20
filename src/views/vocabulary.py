import streamlit as st
from sqlmodel import select
from database import get_session
from database.models import Word, ReviewLog, UserProfile
from srs import calculate_next_review
import random

from i18n import get_text

def show_vocabulary():
    st.markdown(f"## 🎴 {get_text('vocabulary', st.session_state.language)}")
    
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
    with get_session() as session:
        words = session.exec(select(Word)).all()
        if words:
            word = random.choice(words)
            st.session_state.current_word_id = word.id
            st.session_state.show_answer = False
        else:
            st.session_state.current_word_id = None

def process_review(word_id, quality):
    # Calculate SRS
    # In a real app, we would fetch the previous log. 
    # For this demo, we calculate from scratch or simplified state.
    srs_data = calculate_next_review(quality + 1) # Adjust to 0-5 scale if needed
    
    with get_session() as session:
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
