import streamlit as st
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from database.connection import init_db, get_session
from utils.i18n import get_text
from utils.ui_helpers import load_css
from utils.progression_engine import get_lesson_status, get_next_step_recommendation, get_overall_progress
from database import UserProfile
from sqlmodel import select

# Page configuration
st.set_page_config(
    page_title="Lingua Latina Viva",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# Initialize database
init_db()

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'es'
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1  # Default user

# Splash screen for first visit
if st.session_state.first_visit:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 80vh; flex-direction: column;">
            <div style="background: linear-gradient(135deg, rgba(139,69,19,0.1), rgba(160,82,45,0.1));
                        padding: 60px;
                        border-radius: 20px;
                        border: 3px solid rgba(139,69,19,0.3);
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                        text-align: center;
                        max-width: 700px;">
                <h1 style="font-family: 'Cinzel', serif; 
                           font-size: 3.5em; 
                           margin-bottom: 30px;">
                    📜 Lingua Latina Viva 📜
                </h1>
                <p style="font-family: 'Cardo', serif; 
                          font-size: 2em; 
                          font-style: italic;
                          margin-bottom: 40px;
                          line-height: 1.6;">
                    "Ave, discipule.<br>Incipiamus iter per linguam aeternam."
                </p>
                <p style="font-family: 'Lato', sans-serif;
                          font-size: 1.1em;">
                    Bienvenido/a • Welcome • Willkommen
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("✨ Ingredere (Entrar)", use_container_width=True):
            st.session_state.first_visit = False
            st.rerun()
else:
    # Main navigation sidebar
    st.sidebar.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            📜 Lingua Latina Viva
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    # Global Config
    from utils.ui_helpers import render_sidebar_config
    render_sidebar_config()
    
    # ======================================================================
    # DASHBOARD DE PROGRESO VISUAL
    # ======================================================================
    
    with get_session() as session:
        user_id = st.session_state.user_id
        
        # Obtener perfil de usuario
        user_profile = session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()
        if not user_profile:
            # Crear usuario por defecto si no existe
            user_profile = UserProfile(id=user_id, username="Discipulus", level=1, xp=0, streak=0)
            session.add(user_profile)
            session.commit()
            session.refresh(user_profile)
        
        # Obtener progreso general
        overall_progress = get_overall_progress(session, user_id, total_lessons=30)
        current_lesson = overall_progress['current_lesson']
        lessons_completed = overall_progress['lessons_completed']
        total_progress_pct = int(overall_progress['total_progress'] * 100)
        
        # Header con estadísticas generales
        st.markdown(
            f"""
            <div style='text-align: center; padding: 30px 0 20px 0;'>
                <h1 style='font-family: "Cinzel", serif; font-size: 2.5em; margin-bottom: 10px;'>
                    🏛️ Tu Iter per Latinam
                </h1>
                <p style='font-family: "Cardo", serif; font-size: 1.2em; color: #666; font-style: italic;'>
                    Lección {current_lesson} de 30 • {lessons_completed} completadas
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Barra de progreso global
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown(
                f"""
                <div style='text-align: center; margin-bottom: 30px;'>
                    <div style='font-size: 0.9em; color: #666; margin-bottom: 8px;'>Progreso General: {total_progress_pct}%</div>
                    <div style='width: 100%; background-color: #e0e0e0; border-radius: 10px; height: 20px; overflow: hidden;'>
                        <div style='width: {total_progress_pct}%; background: linear-gradient(90deg, #8B4513, #A0522D); height: 100%; transition: width 0.5s ease;'></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Estadísticas rápidas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Nivel", user_profile.level)
        with col2:
            st.metric("⭐ XP", f"{user_profile.xp:,}")
        with col3:
            st.metric("🔥 Racha", f"{user_profile.streak} días")
        with col4:
            st.metric("✅ Completadas", f"{lessons_completed}/30")
        
        st.markdown("---")
        
        # Obtener recomendación para la lección actual
        recommendation = get_next_step_recommendation(session, user_id, current_lesson)
        
        if recommendation:
            # Banner de recomendación destacado
            priority_colors = {
                'high': '#8B4513',
                'medium': '#D2691E',
                'low': '#DEB887'
            }
            color = priority_colors.get(recommendation['priority'], '#8B4513')
            
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, {color}15, {color}25);
                            border-left: 5px solid {color};
                            padding: 20px;
                            border-radius: 10px;
                            margin-bottom: 30px;'>
                    <div style='font-size: 1.3em; font-weight: bold; color: {color}; margin-bottom: 10px;'>
                        🎯 {recommendation['title']}
                    </div>
                    <div style='font-size: 1.1em; color: #333;'>
                        {recommendation['message']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Lección completada
            st.success(f"🏆 ¡Felicitaciones! Completaste la Lección {current_lesson}. Avanza a la siguiente lección.")
        
        # Mapa de lecciones (grid de cards)
        st.markdown("### 📚 Mapa de Lecciones")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # CSS para forzar altura uniforme en los botones del mapa
        st.markdown("""
        <style>
        /* Target buttons inside columns in the main area */
        div[data-testid="column"] .stButton button,
        div[data-testid="stColumn"] .stButton button {
            height: 120px !important;
            min-height: 120px !important;
            max-height: 120px !important;
            width: 100% !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
            border-radius: 12px !important;
            padding: 5px !important;
            margin-bottom: 10px !important;
            line-height: 1.3 !important;
        }
        
        div[data-testid="column"] .stButton button:hover,
        div[data-testid="stColumn"] .stButton button:hover {
            transform: translateY(-5px) !important;
            z-index: 10 !important;
        }
        
        /* Ensure content inside button is centered and wraps */
        div[data-testid="column"] .stButton button p,
        div[data-testid="stColumn"] .stButton button p,
        div[data-testid="column"] .stButton button div,
        div[data-testid="stColumn"] .stButton button div {
            font-size: 1.05em !important;
            font-weight: 600 !important;
            line-height: 1.3 !important;
            text-align: center !important;
            white-space: normal !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # Configuración de lecciones (primeras 10 para demostración)
        LESSON_TITLES = {
            1: "Primera Declinación",
            2: "El Sujeto (Nominativo)",
            3: "Segunda Declinación",
            4: "El Complemento (Acusativo)",
            5: "Presente Indicativo (1ª y 2ª)",
            6: "La Posesión (Genitivo)",
            7: "El Destinatario (Dativo)",
            8: "El Complemento Circunstancial (Ablativo)",
            9: "Tercera Declinación (Consonántica)",
            10: "Imperfecto Indicativo",
            11: "Presente Indicativo (3ª y 4ª)",
            12: "Tercera Declinación (Vocálica)",
            13: "Pronombres Personales",
            14: "Futuro Imperfecto",
            15: "Adjetivos de 1ª y 2ª",
            16: "Perfecto Indicativo",
            17: "Adjetivos de 3ª",
            18: "Pluscuamperfecto Indicativo",
            19: "Pronombres y Adjetivos Demostrativos",
            20: "Futuro Perfecto",
            21: "Participios",
            22: "Ablativo Absoluto",
            23: "Pronombres Relativos",
            24: "Subordinadas Adjetivas",
            25: "Subjuntivo Presente e Imperfecto",
            26: "Subordinadas Sustantivas",
            27: "Oraciones Condicionales",
            28: "Subordinadas Adjetivas Avanzadas",
            29: "Estilo Indirecto",
            30: "Métrica y Síntesis"
        }
        
        # Crear grid de lecciones (5 columnas para una cuadrícula perfecta de 30 lecciones)
        num_cols = 5
        total_lessons = 30
        
        # Iterar sobre las filas
        for row_start in range(1, total_lessons + 1, num_cols):
            cols = st.columns(num_cols)
            for i, col in enumerate(cols):
                lesson_num = row_start + i
                if lesson_num > total_lessons:
                    break
                
                with col:
                    # Obtener estado de la lección
                    lesson_status = get_lesson_status(session, user_id, lesson_num)
                    overall = lesson_status['overall_progress']
                    
                    # Determinar estado visual
                    is_current = (lesson_num == current_lesson)
                    is_completed = (overall >= 1.0)
                    is_locked = (lesson_num > current_lesson and lesson_num != 1) # Asegurar L1 siempre abierta
                    
                    # Colores y Textos según estado (para tooltip)
                    if is_completed:
                        icon = "✅"
                        status_text = "Completada"
                        btn_type = "secondary" 
                        # Hack visual: usaremos CSS para pintar los bordes si es necesario, 
                        # pero por ahora confiamos en el icono
                    elif is_current:
                        icon = "🔄"
                        status_text = f"En progreso: {int(overall * 100)}%"
                        btn_type = "primary"
                    elif is_locked:
                        icon = "🔒"
                        status_text = "Bloqueada"
                        btn_type = "secondary"
                    else:
                        is_locked = False # Safety fallback
                        icon = "📘"
                        status_text = "Disponible"
                        btn_type = "secondary"
                    
                    # Renderizar card como botón
                    lesson_title = LESSON_TITLES.get(lesson_num, f"Lección {lesson_num}")
                    
                    # Construir la etiqueta del botón con saltos de línea para forzar estructura
                    # Line 1: Icon + L#
                    # Line 2: Title
                    btn_label = f"{icon} L{lesson_num}\n{lesson_title}"
                    
                    if st.button(
                        btn_label, 
                        key=f"nav_l{lesson_num}", 
                        disabled=is_locked, 
                        use_container_width=True,
                        type=btn_type,
                        help=f"Estado: {status_text}"
                    ):
                        st.session_state.current_lesson = f"l{lesson_num}"
                        st.switch_page("pages/02_📘_Lecciones.py")
        
        st.markdown("---")
        
        # Sección de ayuda rápida
        st.markdown("### 💡 ¿Cómo funciona?")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Sistema de Progresión Orgánica:**
            
            Cada lección tiene 5 pasos que debes completar en orden:
            
            1. 📖 **Teoría**: Lee el contenido
            2. 🧠 **Vocabulario**: Domina el 50% de las palabras
            3. ✍️ **Ejercicios**: Completa 3 sesiones de práctica
            4. 📜 **Lectura**: Lee textos auténticos
            5. 🏆 **Desafío**: Supera el examen final
            
            Solo podrás avanzar al siguiente paso cuando completes el anterior.
            """)
        
        with col2:
            st.success("""
            **Navegación:**
            
            - 📚 **Curso**: Ve al módulo de lecciones para estudiar teoría
            - 🧠 **Memorización**: Practica vocabulario con flashcards SRS
            - ⚔️ **Práctica**: Completa ejercicios y desafíos
            - 📖 **Lecturas**: Lee textos latinos auténticos
            
            Usa el menú lateral para navegar entre módulos.
            """)

    # Render sidebar footer
    from utils.ui import render_sidebar_footer
    render_sidebar_footer()
