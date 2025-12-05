import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui_helpers import load_css, render_page_header, render_sidebar_footer

st.set_page_config(
    page_title="Análisis",
    page_icon="🔍",
    layout="wide"
)

load_css()
from utils.ui_helpers import render_sidebar_config
render_sidebar_config()
render_page_header("Análisis", "🔍")

# Initialize session state for module selection
if 'analysis_module' not in st.session_state:
    st.session_state.analysis_module = "📐 Sintaxis Visual"

# Module selection with radio buttons
selected_module = st.radio(
    "Selecciona una herramienta de análisis:",
    ["📐 Sintaxis Visual", "🔍 Analizador Morfológico", "✍️ Scriptorium", "📖 Consulta Collatinus"],
    horizontal=True,
    key='analysis_module',
    label_visibility="collapsed"
)

st.markdown("---")

# Render the selected module
try:
    if selected_module == "📐 Sintaxis Visual":
        import pages.modules.syntax_view as syntax_view
        syntax_view.render_content()
    
    elif selected_module == "🔍 Analizador Morfológico":
        import pages.modules.analyzer_view as analyzer_view
        analyzer_view.render_content()
    
    # elif selected_module == "📊 Generador de Paradigmas":
    #     import pages.modules.paradigm_generator_view as paradigm_generator_view
    #     paradigm_generator_view.render_content()
    
    elif selected_module == "✍️ Scriptorium":
        import pages.modules.scriptorium_view as scriptorium_view
        scriptorium_view.render_content()
    
    elif selected_module == "📖 Consulta Collatinus":
        import pages.modules.collatinus_view as collatinus_view
        collatinus_view.render_content()

except Exception as e:
    st.error(f"❌ Error al cargar el módulo {selected_module}: {str(e)}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())

render_sidebar_footer()

