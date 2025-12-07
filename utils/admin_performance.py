"""
Admin Performance Helpers - Cachea queries frecuentes
Usa st.cache_data para reducir consultas repetidas a la BD
"""

import streamlit as st
from database.connection import get_session
from database import Word, Text, Lesson


@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_all_vocabulary():
    """Obtener todo el vocabulario (cacheado)"""
    try:
        with get_session() as session:
            words = session.query(Word).all()
            return [{
                'id': w.id,
                'latin': w.latin,
                'translation': w.translation,
                'part_of_speech': w.part_of_speech,
                'level': w.level,
                'gender': w.gender,
                'genitive': w.genitive
            } for w in words]
    except Exception as e:
        st.error(f"Error al cargar vocabulario: {e}")
        return []


@st.cache_data(ttl=300)
def get_all_texts():
    """Obtener todos los textos (cacheado)"""
    try:
        with get_session() as session:
            texts = session.query(Text).all()
            return [{
                'id': t.id,
                'content': t.content,
                'translation': t.translation,
                'level': t.level,
                'source': t.source,
                'notes': t.notes
            } for t in texts]
    except Exception as e:
        st.error(f"Error al cargar textos: {e}")
        return []


@st.cache_data(ttl=300)
def get_all_lessons():
    """Obtener todas las lecciones (cacheado)"""
    try:
        with get_session() as session:
            lessons = session.query(Lesson).all()
            return [{
                'id': l.id,
                'lesson_number': l.lesson_number,
                'title': l.title,
                'description': l.description
            } for l in lessons]
    except Exception as e:
        st.error(f"Error al cargar lecciones: {e}")
        return []


@st.cache_data(ttl=300)
def get_vocab_stats():
    """Obtener estadísticas de vocabulario (cacheado)"""
    try:
        with get_session() as session:
            total = session.query(Word).count()
            by_level = {}
            for level in range(1, 6):
                count = session.query(Word).filter(Word.level == level).count()
                if count > 0:
                    by_level[f"Nivel {level}"] = count
            
            by_pos = {}
            for pos in ['noun', 'verb', 'adjective', 'adverb', 'preposition']:
                count = session.query(Word).filter(Word.part_of_speech == pos).count()
                if count > 0:
                    by_pos[pos] = count
            
            return {
                'total': total,
                'by_level': by_level,
                'by_pos': by_pos
            }
    except Exception as e:
        st.error(f"Error al cargar estadísticas: {e}")
        return {'total': 0, 'by_level': {}, 'by_pos': {}}


def clear_admin_cache():
    """Limpiar el cache de admin (llamar después de cambios)"""
    st.cache_data.clear()


def invalidate_specific_cache(cache_type: str):
    """Invalidar un cache específico"""
    if cache_type == "vocabulary":
        st.cache_data.clear()
    elif cache_type == "texts":
        st.cache_data.clear()
    elif cache_type == "lessons":
        st.cache_data.clear()
    elif cache_type == "all":
        st.cache_data.clear()
