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
render_page_header("Análisis", "🔍")

tabs = st.tabs(["📐 Sintaxis Visual", "🔍 Analizador Morfológico", "📊 Generador de Paradigmas", "✍️ Scriptorium"])

with tabs[0]:
    try:
        import pages.modules.syntax_view as syntax_view
        syntax_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Sintaxis Visual: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[1]:
    try:
        import pages.modules.analyzer_view as analyzer_view
        analyzer_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Analizador Morfológico: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[2]:
    try:
        import pages.modules.paradigm_generator_view as paradigm_generator_view
        paradigm_generator_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Generador de Paradigmas: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[3]:
    try:
        import pages.modules.scriptorium_view as scriptorium_view
        scriptorium_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Scriptorium: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

render_sidebar_footer()

