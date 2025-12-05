"""
Analysis/Grammar Practice Module (Refactored)
===========================================
This module implements progressive grammar practice based on the user's lesson progress.

PROGRESSION LOGIC:
- L1-L2: Nominative only
- L3: 1st Declension (Nom, Acc, Abl)
- L4: 2nd Declension (all cases)
- L5: Neuter (all cases)
- L6: Adjective agreement
- L7: 3rd Declension
- L13: Passive voice introduction
- L14+: Perfect tenses
- L18+: Subjunctive
"""

import streamlit as st
from sqlmodel import select
from database import (
    get_session, Word, LessonVocabulary, UserProgressSummary
)
from utils.latin_logic import LatinMorphology
import random
import json

from utils.i18n import get_text


# Lesson => Allowed grammar constraints
GRAMMAR_CONSTRAINTS = {
    1: {
        "noun_cases": ["nominative"],
        "noun_numbers": ["singular"],
        "verb_tenses": ["present"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active"]
    },
    2: {
        "noun_cases": ["nominative"],
        "noun_numbers": ["singular", "plural"],
        "verb_tenses": ["present"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active"]
    },
    3: {
        "noun_cases": ["nominative", "accusative", "ablative"],
        "noun_numbers": ["singular", "plural"],
        "verb_tenses": ["present"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active"]
    },
    4: {
        "noun_cases": ["nominative", "genitive", "dative", "accusative", "ablative"],
        "noun_numbers": ["singular", "plural"],
        "verb_tenses": ["present", "imperfect"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active"]
    },
    5: {
        "noun_cases": ["nominative", "genitive", "dative", "accusative", "ablative"],
        "noun_numbers": ["singular", "plural"],
        "verb_tenses": ["present", "imperfect", "future"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active"]
    },
    7: {
        "noun_cases": ["nominative", "genitive", "dative", "accusative", "ablative", "vocative"],
        "noun_numbers": ["singular", "plural"],
        "verb_tenses": ["present", "imperfect", "future", "perfect"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active"]
    },
    13: {
        "noun_cases": ["nominative", "genitive", "dative", "accusative", "ablative", "vocative"],
        "noun_numbers": ["singular", "plural"],
        "verb_tenses": ["present", "imperfect", "future", "perfect", "pluperfect", "future_perfect"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active", "passive"]
    },
    18: {
        "noun_cases": ["nominative", "genitive", "dative", "accusative", "ablative", "vocative"],
        "noun_numbers": ["singular", "plural"],
        "verb_tenses": ["present", "imperfect", "future", "perfect", "pluperfect", "future_perfect"],
        "verb_moods": ["indicative", "subjunctive"],
        "verb_voices": ["active", "passive"]
    }
}


def get_grammar_constraints_for_lesson(lesson_num: int) -> dict:
    """
    Get grammar constraints for a given lesson number.
    Uses the highest available constraint <= lesson_num.
    """
    # Find the highest lesson number in GRAMMAR_CONSTRAINTS that is <= lesson_num
    available_lessons = sorted([l for l in GRAMMAR_CONSTRAINTS.keys() if l <= lesson_num])
    
    if not available_lessons:
        return GRAMMAR_CONSTRAINTS[1]  # Fallback to L1
    
    return GRAMMAR_CONSTRAINTS[available_lessons[-1]]


def get_user_context():
    """Get the user's current learning context"""
    with get_session() as session:
        summary = session.exec(
            select(UserProgressSummary).where(UserProgressSummary.user_id == 1)
        ).first()
        
        if not summary:
            return {"current_lesson": 1}
        
        return {"current_lesson": summary.current_lesson}


def select_word_for_analysis(session, current_lesson: int):
    """
    Select a word appropriate for the user's current lesson.
    Prioritizes words from current and recent lessons.
    """
    # Get words from lessons up to current
    lesson_range = list(range(max(1, current_lesson - 2), current_lesson + 1))
    
    lesson_words = session.exec(
        select(LessonVocabulary)
        .where(LessonVocabulary.lesson_number.in_(lesson_range))
        .where(LessonVocabulary.is_essential == True)
    ).all()
    
    if not lesson_words:
        # Fallback: any word from lessons 1-current
        lesson_words = session.exec(
            select(LessonVocabulary)
            .where(LessonVocabulary.lesson_number <= current_lesson)
        ).all()
    
    if not lesson_words:
        # Ultimate fallback: any word
        return session.exec(select(Word)).first()
    
    lw = random.choice(lesson_words)
    return session.get(Word, lw.word_id)


def generate_noun_form(word: Word, constraints: dict):
    """Generate a valid noun form based on constraints"""
    forms = LatinMorphology.decline_noun(
        word.latin, word.declension, word.gender, 
        word.genitive, word.irregular_forms
    )
    
    if not forms:
        return None, None
    
    # Filter forms by constraints
    allowed_cases = constraints["noun_cases"]
    allowed_numbers = constraints["noun_numbers"]
    
    valid_forms = {}
    for case_key, form_value in forms.items():
        # Parse case_key (e.g., "nominative_singular")
        parts = case_key.split("_")
        if len(parts) >= 2:
            case = parts[0]
            number = parts[1]
            
            if case in allowed_cases and number in allowed_numbers:
                valid_forms[case_key] = form_value
    
    if not valid_forms:
        # Fallback: nominative singular
        return forms.get("nominative_singular", list(forms.values())[0]), "nominative singular"
    
    selected_key = random.choice(list(valid_forms.keys()))
    return valid_forms[selected_key], selected_key.replace("_", " ")


def generate_verb_form(word: Word, constraints: dict):
    """Generate a valid verb form based on constraints"""
    forms = LatinMorphology.conjugate_verb(
        word.latin, word.conjugation, word.principal_parts
    )
    
    if not forms:
        return None, None
    
    # Filter forms by constraints
    valid_forms = {}
    for key, form_value in forms.items():
        # Key format: "tense_mood_voice_person_number"
        # e.g., "present_indicative_active_1_singular"
        parts = key.split("_")
        if len(parts) >= 5:
            tense = parts[0]
            mood = parts[1]
            voice = parts[2]
            
            if (tense in constraints["verb_tenses"] and
                mood in constraints["verb_moods"] and
                voice in constraints["verb_voices"]):
                valid_forms[key] = form_value
    
    if not valid_forms:
        # Fallback: present indicative active
        for key in forms:
            if "present_indicative_active" in key:
                return forms[key], key.replace("_", " ")
        return list(forms.values())[0], list(forms.keys())[0]
    
    selected_key = random.choice(list(valid_forms.keys()))
    return valid_forms[selected_key], selected_key.replace("_", " ")


def show_analysis():
    st.markdown(f"## 🔍 {get_text('analysis', st.session_state.language)}")
    
    # Show lesson context
    context = get_user_context()
    st.caption(f"📘 Analizando gramática hasta la Lección {context['current_lesson']}")
    
    if st.button(get_text('new_form', st.session_state.language)):
        load_analysis_form()
        
    if "analysis_target" not in st.session_state:
        load_analysis_form()

    if st.session_state.get("analysis_form"):
        st.markdown(
            f"""
            <div style="background-color: #fff8f0; border: 2px solid #8b4513; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0;">
                <h2 style="font-size: 2.5em; color: #8b0000;">{st.session_state.analysis_form}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### 🎯 Identifica:")
        st.markdown("- ¿De qué palabra base (lema) viene esta forma?")
        st.markdown("- ¿Qué caso/tiempo/persona/número es?")
        
        with st.expander(get_text('reveal', st.session_state.language)):
            st.markdown(f"### {st.session_state.analysis_target}")
            if st.session_state.get("analysis_hint"):
                st.caption(st.session_state.analysis_hint)


def load_analysis_form():
    """Generate a new analysis exercise based on user's lesson progress"""
    context = get_user_context()
    current_lesson = context["current_lesson"]
    constraints = get_grammar_constraints_for_lesson(current_lesson)
    
    with get_session() as session:
        word = select_word_for_analysis(session, current_lesson)
        
        if not word:
            st.session_state.analysis_form = None
            return
        
        # Generate appropriate form based on word type
        if word.part_of_speech == "noun":
            form, description = generate_noun_form(word, constraints)
            if form:
                st.session_state.analysis_form = form
                st.session_state.analysis_target = f"**{word.latin}**: {description}"
                st.session_state.analysis_hint = f"({word.gender}.) - {word.declension}ª declinación"
            else:
                load_analysis_form()  # Retry
                
        elif word.part_of_speech == "verb":
            form, description = generate_verb_form(word, constraints)
            if form:
                st.session_state.analysis_form = form
                st.session_state.analysis_target = f"**{word.latin}**: {description}"
                st.session_state.analysis_hint = f"Conjugación {word.conjugation}"
            else:
                load_analysis_form()  # Retry
        else:
            # For other parts of speech, just show the word
            st.session_state.analysis_form = word.latin
            st.session_state.analysis_target = f"**{word.latin}**: {word.part_of_speech}"
            st.session_state.analysis_hint = word.translation
