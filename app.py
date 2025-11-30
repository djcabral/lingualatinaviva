import streamlit as st
import sys
import os

# Add paths for imports
# Add paths for imports
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from database.connection import init_db
from utils.i18n import get_text
from utils.ui_helpers import load_css

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
        if st.button("✨ Ingredere (Entrar)", width='stretch'):
            st.session_state.first_visit = False
            st.rerun()
else:
    # Main navigation
    st.sidebar.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            📜 Lingua Latina Viva
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    st.sidebar.info(
        """
        **Navigatio**: Usa el menú de la izquierda para explorar los módulos.
        
        **Módulos Disponibles:**
        - 🏠 Home (Hodie)
        - 🎴 Vocabularium
        - 📜 Declinatio
        - ⚔️ Conjugatio
        - 🔍 Analysis
        - 📖 Lectio
        - ⚙️ Admin
        """
    )
    
    # Main content
    st.markdown(
        """
        <div style='text-align: center; padding: 50px 0;'>
            <h1 style='font-family: "Cinzel", serif; font-size: 3em;'>
                Ave, Discipule!
            </h1>
            <p style='font-family: "Cardo", serif; font-size: 1.5em; font-style: italic;'>
                Elige un módulo del menú lateral para comenzar tu práctica diaria.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Introduction section
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 ¿Qué es Lingua Latina Viva?")
        st.markdown("""
        **Lingua Latina Viva** es un organismo vivo de aprendizaje, estructurado en cuatro pilares fundamentales para cultivar la fluidez real:
        
        ### 1. 📘 Lección (Fundamento)
        La base teórica y la inmersión textual.
        *   **Curso y Lecturas**: Progresión graduada desde oraciones simples hasta textos auténticos.
        *   **Gramática**: Referencia constante de las reglas del juego.
        
        ### 2. 🧠 Memorización (Adquisición)
        La interiorización de los bloques de construcción.
        *   **Vocabulario SRS**: Sistema inteligente para retener palabras a largo plazo.
        *   **Diccionario**: Herramienta de consulta rápida.
        
        ### 3. ⚔️ Práctica (Automatización)
        El gimnasio mental para ganar velocidad y precisión.
        *   **Declinaciones y Conjugaciones**: Ejercicios intensivos de morfología.
        *   **Aventura y Desafíos**: Gamificación para poner a prueba tus habilidades.
        
        ### 4. 🔍 Análisis (Comprensión Profunda)
        La disección de la lengua para entender su lógica interna.
        *   **Sintaxis**: Visualización de la estructura de las oraciones.
        *   **Analizador**: Herramienta para desglosar cualquier palabra.
        
        ---
        **Metodología**: Inspirada en la tradición humanista y el método natural, buscamos que *vivas* la lengua, no solo que la estudies.
        """)
        
        st.markdown("### 🚀 Comienza Ahora")
        st.success("👈 Selecciona un módulo del menú lateral para comenzar tu práctica diaria.")
    
    st.markdown("---")
    
    # Quick stats overview
    from database.connection import get_session
    from sqlmodel import select, func
    # Import through a function to avoid duplicate registration
    from database import UserProfile, Word
    
    with get_session() as session:
        user = session.exec(select(UserProfile)).first()
        if user:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{user.level}</div>
                        <div class="stat-label">Nivel</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{user.streak}</div>
                        <div class="stat-label">Racha (días)</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{user.xp}</div>
                        <div class="stat-label">PE</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col4:
                word_count = session.exec(select(func.count(Word.id))).one()
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-value">{word_count}</div>
                        <div class="stat-label">Vocabula</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Render sidebar footer
    from utils.ui import render_sidebar_footer
    render_sidebar_footer()
