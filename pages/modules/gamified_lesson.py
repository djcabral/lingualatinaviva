
import streamlit as st
from sqlmodel import Session, select
from database import get_session, UserLessonProgressV2
from utils.progression_engine import get_lesson_status
from utils.learning_hub_widgets import (
    render_vocabulary_widget, 
    render_practice_content,
    render_final_challenge
)

def render_standard_gamified_lesson(lesson, theory_content=None, practice_content=None, reading_content=None):
    """
    Renders the lesson in a standardized gamified, 3-stage vertical format.
    
    Args:
        lesson: Lesson model instance OR dict with lesson data {id, lesson_number, title, content_markdown}
        theory_content: Callable that renders the theory section
        practice_content: Callable that renders the practice section (Stage 2)
        reading_content: Callable that renders the reading section (Stage 3)
        
    Stage 1: Fundamentos (Theory + Vocab) -> Challenge 1 (Vocab Quiz)
    Stage 2: Estructura (Grammar + Drill) -> Challenge 2 (Structure)
    Stage 3: Aplicación (Reading + Context) -> Challenge 3 (Final Exam)
    """
    # Extract lesson attributes - support both dict and object formats
    if isinstance(lesson, dict):
        lesson_id = lesson['id']
        lesson_number = lesson['lesson_number']
        lesson_title = lesson['title']
        lesson_content_markdown = lesson.get('content_markdown')
    else:
        # SQLAlchemy object - extract immediately to avoid DetachedInstanceError
        lesson_id = lesson.id
        lesson_number = lesson.lesson_number
        lesson_title = lesson.title
        lesson_content_markdown = lesson.content_markdown if hasattr(lesson, 'content_markdown') else None
    
    st.title(f"Lección {lesson_number}: {lesson_title}")
    
    # 1. Get Progress
    user_id = st.session_state.get('user_id', 1)
    with get_session() as session:
        # Check or create V2 progress
        progress = session.exec(
            select(UserLessonProgressV2)
            .where(
                UserLessonProgressV2.user_id == user_id,
                UserLessonProgressV2.lesson_id == lesson_id
            )
        ).first()
        
        # Init progress if it doesn't exist
        if not progress:
            # We don't create it here to avoid side effects on simple view, 
            # but we treat as empty structure
            stage1_done = False
            stage2_done = False
            stage3_done = False
        else:
            stage1_done = progress.theory_completed
            # Consider stage 2 done if completed exercises OR if challenge 2 passed (if we tracked it separately)
            # For now, relying on count
            stage2_done = (progress.exercises_count >= 3)
            stage3_done = progress.challenge_passed
        
    # --- INTER-LESSON LOCKING ---
    if lesson_number > 1:
        prev_lesson_num = lesson_number - 1
        with get_session() as session:
            from database import Lesson
            prev_lesson = session.exec(select(Lesson).where(Lesson.lesson_number == prev_lesson_num)).first()
            if prev_lesson:
                prev_progress = session.exec(
                    select(UserLessonProgressV2)
                    .where(
                        UserLessonProgressV2.user_id == user_id,
                        UserLessonProgressV2.lesson_id == prev_lesson.id
                    )
                ).first()
                
                prev_completed = prev_progress.challenge_passed if prev_progress else False
                
                # Development Override: Allow skipping if dev mode (can simply comment out for prod)
                # prev_completed = True 
                
                if not prev_completed:
                    st.error(f"🔒 La Lección {lesson_number} está bloqueada.")
                    st.info(f"Debes completar el Desafío Final de la Lección {prev_lesson_num} para acceder.")
                    if st.button(f"⬅️ Ir a Lección {prev_lesson_num}"):
                         st.session_state.current_lesson = f"l{prev_lesson_num}"
                         st.rerun()
                    return

    # 2. Render Mission Grid (Dashboard)
    
    # Calculate more granular metrics for the dashboard
    mission_status = {
        "teoria": {"done": stage1_done, "label": "Fundamentos", "icon": "📘", "desc": "Teoría y Conceptos"},
        "vocabulario": {"done": stage1_done, "label": "Vocabulario", "icon": "🧠", "desc": "Memorización"}, 
        "practica": {"done": stage2_done, "label": "Estructura", "icon": "⚔️", "desc": "Ejercicios Prácticos"},
        "lectura": {"done": stage3_done, "label": "Lectura", "icon": "📜", "desc": "Comprensión"}, 
        "desafio": {"done": stage3_done, "label": "Certificación", "icon": "🏆", "desc": "Prueba Final"}
    }
    
    _render_mission_dashboard(mission_status)
    
    st.divider()
    
    # --- STAGE 1: FUNDAMENTOS ---
    _render_stage_1(lesson_number, lesson_content_markdown, stage1_done, theory_content)
    
    st.divider()
    
    # --- STAGE 2: ESTRUCTURA ---
    if stage1_done:
        _render_stage_2(lesson_number, stage2_done, practice_content)
    else:
        reqs = [
            ("Completar Teoría y Vocabulario", stage1_done),
            ("Superar Desafío 1: Vocabulario", False)
        ]
        _render_locked_stage(2, "Estructura y Sintaxis", reqs)
        
    st.divider()
    
    # --- STAGE 3: APLICACIÓN ---
    if stage2_done:
        _render_stage_3(lesson_number, stage3_done, reading_content)
    else:
        reqs = [
            ("Desbloquear Etapa 2", stage1_done),
            ("Completar 3 Ejercicios de Estructura", stage2_done),
            ("Superar Desafío 2: Estructura", False)
        ]
        _render_locked_stage(3, "Lectura y Aplicación", reqs)

def _render_mission_dashboard(mission_status):
    """
    Renders a granular Mission Grid for the lesson.
    """
    st.markdown("""
    <style>
    .mission-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 100%;
        transition: transform 0.2s;
    }
    .mission-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .mission-done {
        background-color: #f0fdf4; /* Green-50 */
        border-color: #bbf7d0;     /* Green-200 */
    }
    .mission-locked {
        background-color: #f9fafb; /* Gray-50 */
        opacity: 0.7;
    }
    .mission-icon {
        font-size: 2rem;
        margin-bottom: 8px;
    }
    .mission-label {
        font-weight: 600;
        font-size: 0.9rem;
        color: #374151;
        margin-bottom: 4px;
    }
    .mission-desc {
        font-size: 0.75rem;
        color: #6b7280;
    }
    .status-badge {
        display: inline-block;
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 99px;
        margin-top: 8px;
    }
    .status-done { background-color: #dcfce7; color: #166534; }
    .status-pending { background-color: #eff6ff; color: #1e40af; }
    .status-locked { background-color: #f3f4f6; color: #6b7280; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🗺️ Tablero de Misiones")
    
    cols = st.columns(len(mission_status))
    
    # Determine first pending item to highlight
    first_pending_found = False
    
    for idx, (key, data) in enumerate(mission_status.items()):
        with cols[idx]:
            is_done = data["done"]
            
            # Logic for "Active" (First pending item)
            is_active = False
            if not is_done and not first_pending_found:
                is_active = True
                first_pending_found = True
            
            # Logic for "Locked" (Pending items after the active one)
            is_locked = not is_done and not is_active
            
            # Styles
            card_cls = "mission-card"
            if is_done: card_cls += " mission-done"
            elif is_locked: card_cls += " mission-locked"
            
            status_text = "COMPLETADO" if is_done else ("EN CURSO" if is_active else "BLOQUEADO")
            status_cls = "status-done" if is_done else ("status-pending" if is_active else "status-locked")
            
            icon = "✅" if is_done else data["icon"]
            if is_locked: icon = "🔒"
            
            st.markdown(f"""
            <div class="{card_cls}">
                <div class="mission-icon">{icon}</div>
                <div class="mission-label">{data['label']}</div>
                <div class="mission-desc">{data['desc']}</div>
                <div class="status-badge {status_cls}">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_stage_1(lesson_number, lesson_content_markdown, is_completed, theory_content=None):
    st.header("1. Fundamentos")
    st.caption("Domina la teoría básica y el vocabulario esencial.")
    
    # Content: Theory
    with st.expander("📖 Teoría de la Lección", expanded=not is_completed):
        if theory_content:
            if callable(theory_content):
                theory_content()
            else:
                st.markdown(theory_content)
        elif lesson_content_markdown:
            st.markdown(lesson_content_markdown)
        else:
            st.warning("No hay contenido teórico disponible.")
            
    # Content: Vocab
    render_vocabulary_widget(lesson_number)
    
    st.markdown("#### 🔒 Desafío 1: El Guardián del Vocabulario")
    if is_completed:
        st.success("✅ ¡Desafío de Vocabulario Completado!")
    else:
        st.info("Para avanzar, debes dominar el vocabulario de esta lección.")
        if st.button("⚔️ Iniciar Desafío de Vocabulario", key=f"chall1_l{lesson_number}"):
             # Logic to launch modal or widget
             st.warning("🚧 Funcionalidad de Desafío en construcción.")
             st.warning("⚔️ Funcionalidad de desafío completa pendiente.")
             # Update progress for testing purposes if clicked
             # _update_progress(lesson_number, "stage1")
             # st.rerun()

def _render_stage_2(lesson_number, is_completed, practice_content=None):
    st.header("2. Estructura")
    st.caption("Pon en práctica la gramática con ejercicios guiados.")
    
    # Content: Practice Widgets
    if practice_content:
        if callable(practice_content):
            try:
                practice_content()
            except Exception as e:
                st.error(f"Error cargando contenido de práctica: {e}")
        else:
            # Assume it's config or similar, fallback
            render_practice_content(lesson_number)
    else:
        render_practice_content(lesson_number)
    
    st.markdown("#### 🔒 Desafío 2: El Constructor")
    if is_completed:
        st.success("✅ ¡Desafío de Estructura Completado!")
    else:
        st.info("Para avanzar, completa 3 ejercicios de construcción correctamente.")
        if st.button("⚔️ Iniciar Desafío de Estructura", key=f"chall2_l{lesson_number}"):
             st.warning("🚧 Funcionalidad de Desafío en construcción.")
             st.warning("⚔️ Funcionalidad de desafío completa pendiente.")
             st.rerun()

def _render_stage_3(lesson_number, is_completed, reading_content=None):
    st.header("3. Aplicación")
    st.caption("Demuestra tu maestría leyendo y traduciendo textos reales.")
    
    # Content: Reading
    if reading_content:
        if callable(reading_content):
            reading_content()
        else:
            st.markdown(reading_content)
    else:
        st.markdown("*(Componente de Lectura no disponible)*")
    
    st.markdown("#### 🔒 Desafío Final: La Prueba")
    if is_completed:
        st.success("🏆 ¡Lección Completada! Has ganado 50 XP.")
        if st.button("➡️ Siguiente Lección"):
            next_lesson_num = lesson_number + 1
            st.session_state.current_lesson = f"l{next_lesson_num}"
            st.rerun()
    else:

        # Define callback for completion
        def on_challenge_complete():
            with get_session() as session:
                from utils.progression_engine import mark_challenge_passed
                mark_challenge_passed(session, user_id=st.session_state.get('user_id', 1), lesson_id=lesson_number)
            
        render_final_challenge(lesson_number, on_complete=on_challenge_complete)

def _render_locked_stage(stage_num, title, requirements_list: list = None):
    """
    Render a locked stage with a requirements checklist.
    requirements_list: list of tuples (description, is_completed)
    """
    st.header(f"{stage_num}. {title}")
    
    st.markdown(
        f"""
        <div style='background: #f8f9fa; border: 2px dashed #dee2e6; padding: 25px; border-radius: 12px; text-align: center; color: #6c757d; margin: 20px 0;'>
            <div style='font-size: 3rem; margin-bottom: 10px;'>🔒</div>
            <h3 style='margin-top: 0;'>Etapa Bloqueada</h3>
            <p>Completa los requisitos previos para acceder.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if requirements_list:
        st.markdown("##### 📋 Requisitos para desbloquear:")
        for req_text, is_done in requirements_list:
            icon = "✅" if is_done else "⬜"
            st.markdown(f"{icon} {req_text}")
            
    st.caption("Sigue practicando en la etapa anterior para avanzar.")

def _update_progress(lesson_id, stage):
    """Temporary helper to update progress in DB for simulation"""
    user_id = st.session_state.get('user_id', 1)
    with get_session() as session:
        progress = session.exec(
            select(UserLessonProgressV2)
            .where(
                UserLessonProgressV2.user_id == user_id,
                UserLessonProgressV2.lesson_id == lesson_id
            )
        ).first()
        
        if not progress:
            progress = UserLessonProgressV2(user_id=user_id, lesson_id=lesson_id)
            session.add(progress)
        
        if stage == "stage1":
            progress.theory_completed = True
        
        session.add(progress)
        session.commit()
