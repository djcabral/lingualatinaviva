"""
Dashboard Unificado - Inicio
Página principal con recomendaciones personalizadas y progreso integrado.
"""

import streamlit as st
import sys
import os
from datetime import datetime

root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

# Import SQLModel components first
from sqlmodel import select

# Then import database models and utilities
from database import UserProfile, UserProgressSummary, get_session, get_json_list
from utils.ui_helpers import load_css
from utils.recommendation_service import generate_recommendations, get_active_recommendations
from utils.unlock_service import get_user_summary, get_vocab_mastery, get_exercises_stats
from utils.ui_components import render_stat_box, render_recommendation_card, render_progress_bar

# Helper functions
def _get_action_label(action: str) -> str:
    """Convierte el action code en una etiqueta amigable"""
    labels = {
        'start_lesson': 'Comenzar Lección',
        'practice_vocab': 'Practicar Vocabulario',
        'improve_vocab': 'Mejorar Vocabulario',
        'start_exercises': 'Comenzar Ejercicios',
        'practice_more': 'Practicar Más',
        'start_reading': 'Comenzar Lectura',
        'analyze_sentences': 'Analizar Oraciones',
        'take_challenge': 'Tomar Desafío',
        'review_grammar': 'Repasar Gramática'
    }
    return labels.get(action, 'Ir')

def _get_action_url(rec_type: str) -> str:
    """Convierte el rec_type en una URL de página"""
    urls = {
        'grammar': 'pages/02_📘_Lecciones.py',
        'vocabulary': 'pages/03_🧠_Memorización.py',
        'exercises': 'pages/04_⚔️_Práctica.py',
        'reading': 'pages/02_📘_Lecciones.py',
        'syntax': 'pages/05_🔍_Análisis.py',
        'challenge': 'pages/04_⚔️_Práctica.py',
        'review': 'pages/02_📘_Lecciones.py'
    }
    return urls.get(rec_type, 'pages/01_🏠_Inicio.py')

st.set_page_config(page_title="Inicio - Lingua Latina Viva", page_icon="🏠", layout="wide")

load_css()

if 'language' not in st.session_state:
    st.session_state.language = 'es'

# Global Config (Font Size)
from utils.ui_helpers import render_sidebar_config
render_sidebar_config()

# Header
st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif; color: #8b4513;'>
        🏠 Hodie - Tu Centro de Aprendizaje
    </h1>
    """,
    unsafe_allow_html=True
)

with get_session() as session:
    # Obtener o crear perfil de usuario
    user = session.exec(select(UserProfile)).first()
    if not user:
        user = UserProfile(username="Discipulus", level=1, xp=0, streak=0)
        session.add(user)
        session.commit()
        session.refresh(user)
    
    # Obtener resumen de progreso
    summary = get_user_summary(session, user.id)
    current_lesson = summary.current_lesson
    
    # ===================
    # SECCIÓN 0: NOTIFICACIONES Y ALERTAS
    # ===================
    
    # Importar función para desbloqueos recientes
    from utils.unlock_service import get_recent_unlocks
    from utils.recommendation_service import get_vocab_due_for_review
    
    # Banner de desbloqueos recientes (últimas 24 horas)
    recent_unlocks = get_recent_unlocks(session, user.id, hours=24)
    
    if recent_unlocks:
        st.markdown("### 🎉 Novedades Recientes")
        for unlock in recent_unlocks[:3]:  # Máximo 3
            time_ago = (datetime.utcnow() - unlock['unlocked_at']).total_seconds() / 3600
            if time_ago < 1:
                time_str = "hace unos minutos"
            elif time_ago < 24:
                time_str = f"hace {int(time_ago)} horas"
            else:
                time_str = "ayer"
            
            st.info(f"{unlock['icon']} **{unlock['item_name']}** - {unlock['detail']} ({time_str})")
        
        st.markdown("---")
    
    # Recordatorio de repaso de vocabulario
    due_vocab = get_vocab_due_for_review(session, user.id)
    
    if due_vocab:
        overdue_count = sum(1 for v in due_vocab if v['days_overdue'] > 0)
        today_count = len(due_vocab) - overdue_count
        
        if overdue_count > 5:
            st.warning(
                f"📚 **¡Atención!** Tienes {overdue_count} palabras vencidas para repasar. "
                f"¡No las dejes olvidar!"
            )
        elif len(due_vocab) >= 10:
            st.info(
                f"📖 Tienes {len(due_vocab)} palabras para repasar hoy. "
                f"Un repaso rápido refrescará tu memoria."
            )
        
        st.markdown("---")
    
    # ===================
    # SECCIÓN 1: TU SITUACIÓN ACTUAL
    # ===================
    
    st.markdown("## 📍 Tu Situación Actual")
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_stat_box(
            value=f"Lección {current_lesson}",
            label="Lección Actual",
            icon="📘"
        )
    
    with col2:
        render_stat_box(
            value=f"{user.level}",
            label="Nivel",
            icon="⭐"
        )
    
    with col3:
        render_stat_box(
            value=f"{user.xp}",
            label="Experiencia",
            icon="🏆"
        )
    
    with col4:
        render_stat_box(
            value=f"{user.streak}",
            label="Racha (días)",
            icon="🔥"
        )
    
    # Barra de progreso de lección actual
    st.markdown(f"### Progreso en Lección {current_lesson}")
    
    # Calcular progreso basado en completitud de actividades
    vocab_mastery = get_vocab_mastery(session, user.id, current_lesson)
    exercise_stats = get_exercises_stats(session, user.id, current_lesson)
    
    # Mostrar detalles de progreso
    col1, col2 = st.columns(2)
    with col1:
        render_progress_bar(
            current=int(vocab_mastery * 100),
            total=100,
            label="Vocabulario Dominado"
        )
    
    with col2:
        if exercise_stats['count'] > 0:
            render_progress_bar(
                current=exercise_stats['count'],
                total=10,
                label=f"Ejercicios Completados ({exercise_stats['accuracy']:.0%} precisión)"
            )
        else:
            st.caption("📜 Ejercicios: No iniciados")
    
    st.markdown("---")
    
    # ===================
    # SECCIÓN 2: PRÓXIMOS PASOS RECOMENDADOS
    # ===================
    
    st.markdown("## 🎯 Próximos Pasos Recomendados")
    
    # Generar recomendaciones
    recommendations = generate_recommendations(session, user.id)
    
    if recommendations:
        for i, rec in enumerate(recommendations):
            rec_data = {
                'priority': rec['priority'],
                'message': rec['message'],
                'action_label': _get_action_label(rec['action']),
                'action_url': _get_action_url(rec['type'])
            }
            render_recommendation_card(rec_data, index=i)
    else:
        st.info("✅ ¡Estás al día! Comienza la siguiente lección o repasa contenido anterior.")
    
    st.markdown("---")
    
    # ===================
    # SECCIÓN 3: TU PROGRESO POR MÓDULO
    # ===================
    
    st.markdown("## 📊 Tu Progreso por Módulo")
    
    tabs = st.tabs(["📘 Gramática", "🎴 Vocabulario", "📜 Ejercicios", "📖 Lecturas", "🎯 Desafíos"])
    
    # Tab: Gramática
    with tabs[0]:
        st.markdown(f"### Lecciones Completadas")
        completed = get_json_list(summary.lessons_completed)
        in_progress = get_json_list(summary.lessons_in_progress)
        
        if completed:
            st.success(f"✅ Completadas: {len(completed)} lecciones")
            st.caption(f"Lecciones: {', '.join(map(str, sorted(completed)))}")
        else:
            st.info("Aún no has completado ninguna lección")
        
        if in_progress:
            st.info(f"⏳ En progreso: Lección {', '.join(map(str, in_progress))}")
        
        if st.button("📘 Ir al Curso de Gramática",key="btn_grammar"):
            st.switch_page("pages/02_📘_Lecciones.py")
    
    # Tab: Vocabulario
    with tabs[1]:
        st.markdown(f"### Estadísticas de Vocabulario")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Palabras Aprendidas", summary.total_words_learned)
            st.caption("(Dominio ≥ 50%)")
        with col2:
            st.metric("Palabras Dominadas", summary.total_words_mastered)
            st.caption("(Dominio ≥ 80%)")
        
        if summary.vocab_mastery_avg > 0:
            st.progress(summary.vocab_mastery_avg, text=f"Dominio Promedio: {summary.vocab_mastery_avg:.0%}")
        
        if st.button("🎴 Practicar Vocabulario", key="btn_vocab"):
            st.switch_page("pages/03_🧠_Memorización.py")
    
    # Tab: Ejercicios
    with tabs[2]:
        st.markdown(f"### Estadísticas de Ejercicios")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Completados", summary.exercises_completed_total)
        with col2:
            if summary.exercises_accuracy_avg > 0:
                st.metric("Precisión Promedio", f"{summary.exercises_accuracy_avg:.0%}")
            else:
                st.info("Aún no has completado ejercicios")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📜 Practicar Declinaciones", key="btn_decl"):
                st.switch_page("pages/04_⚔️_Práctica.py")
        with col2:
            if st.button("⚔️ Practicar Conjugaciones", key="btn_conj"):
                st.switch_page("pages/04_⚔️_Práctica.py")
    
    # Tab: Lecturas
    with tabs[3]:
        st.markdown(f"### Estadísticas de Lecturas")
        
        st.metric("Textos Completados", summary.texts_read_total)
        
        if summary.comprehension_avg > 0:
            st.progress(summary.comprehension_avg, text=f"Comprensión Promedio: {summary.comprehension_avg:.0%}")
        else:
            st.info("Aún no has completado ninguna lectura")
        
        if st.button("📖 Ir a Lecturas", key="btn_reading"):
            st.switch_page("pages/02_📘_Lecciones.py")
    
    # Tab: Desafíos
    with tabs[4]:
        st.markdown(f"### Desafíos Completados")
        
        challenges_passed = get_json_list(summary.challenges_passed)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Desafíos Aprobados", len(challenges_passed))
        with col2:
            st.metric("Intentos Fallidos", summary.challenges_failed_attempts)
        
        if st.button("🎯 Ver Desafíos", key="btn_challenges"):
            st.switch_page("pages/04_⚔️_Práctica.py")
    
    st.markdown("---")
    
    # ===================
    # SECCIÓN 4: MAPA VISUAL DE APRENDIZAJE
    # ===================
    
    with st.expander("🗺️ Mapa de Aprendizaje"):
        st.markdown(f"### Tu Camino de Progresión")
        
        # Mostrar lecciones en grid
        lessons_per_row = 5
        completed_lessons = get_json_list(summary.lessons_completed)
        
        for row_start in range(1, 41, lessons_per_row):
            cols = st.columns(lessons_per_row)
            for i, lesson_num in enumerate(range(row_start, min(row_start + lessons_per_row, 41))):
                with cols[i]:
                    if lesson_num in completed_lessons:
                        st.success(f"✅ L{lesson_num}")
                    elif lesson_num == current_lesson:
                        st.info(f"⏳ L{lesson_num}")
                    elif lesson_num < current_lesson:
                        st.warning(f"📘 L{lesson_num}")
                    else:
                        st.caption(f"🔒 L{lesson_num}")
    
    # ===================
    # ÁREAS DÉBILES (si existen)
    # ===================
    
    weak_areas = get_json_list(summary.weak_areas)
    if weak_areas:
        st.markdown("---")
        st.markdown("## ⚠️ Áreas que Necesitan Atención")
        for area in weak_areas[:3]:
            st.warning(f"📚 {area}")
