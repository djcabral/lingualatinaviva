
"""
Utilidad para mostrar un spinner mientras se inicializa el analizador Stanza
"""

import streamlit as st
import time

def initialize_stanza_with_spinner():
    """
    Inicializa el analizador Stanza con un spinner de carga visible

    Returns:
        tuple: (stanza_analyzer, available) donde available es un booleano
    """
    # Verificar si ya está inicializado
    if 'stanza_analyzer' in st.session_state and 'stanza_available' in st.session_state:
        return st.session_state.stanza_analyzer, st.session_state.stanza_available

    # Mostrar spinner mientras inicializa
    with st.spinner("🧠 **Inicializando analizador de Stanza...**\n\nEste proceso tarda ~20 segundos solo la primera vez."):
        try:
            from utils.stanza_analyzer import StanzaAnalyzer

            if not StanzaAnalyzer.is_available():
                st.warning("⚠️ Stanza no está disponible. Algunas funciones de análisis no estarán disponibles.")
                st.session_state.stanza_analyzer = None
                st.session_state.stanza_available = False
                return None, False

            # Inicializar el analizador
            analyzer = StanzaAnalyzer()

            # Guardar en sesión para no inicializar de nuevo
            st.session_state.stanza_analyzer = analyzer
            st.session_state.stanza_available = True

            st.success("✅ Analizador de Stanza inicializado correctamente")
            return analyzer, True

        except Exception as e:
            st.error(f"❌ Error al inicializar Stanza: {str(e)}")
            st.session_state.stanza_analyzer = None
            st.session_state.stanza_available = False
            return None, False
