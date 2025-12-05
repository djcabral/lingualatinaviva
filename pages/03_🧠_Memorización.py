import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui_helpers import load_css, render_page_header, render_sidebar_footer, render_sidebar_config

st.set_page_config(
    page_title="Memorización",
    page_icon="🧠",
    layout="wide"
)

load_css()
render_sidebar_config()
render_page_header("Memorización", "🧠")

# Initialize session state for module selection
if 'memorization_module' not in st.session_state:
    st.session_state.memorization_module = "🎴 Vocabulario (SRS)"

# Module selection with radio buttons
selected_module = st.radio(
    "Selecciona un módulo de memorización:",
    ["🎴 Vocabulario (SRS)", "📚 Diccionario"],
    horizontal=True,
    key='memorization_module',
    label_visibility="collapsed"
)

st.markdown("---")

# Render the selected module
try:
    if selected_module == "🎴 Vocabulario (SRS)":
        import pages.modules.vocab_view as vocab_view
        if hasattr(vocab_view, 'render_content'):
            vocab_view.render_content()
        else:
            st.info("⚠️ Módulo en reestructuración. Por favor espere...")
    
    elif selected_module == "📚 Diccionario":
        import pages.modules.dictionary_view as dictionary_view
        if hasattr(dictionary_view, 'render_content'):
            dictionary_view.render_content()
        else:
            st.info("⚠️ Módulo en reestructuración. Por favor espere...")

except Exception as e:
    st.error(f"❌ Error al cargar el módulo {selected_module}: {str(e)}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())

render_sidebar_footer()
