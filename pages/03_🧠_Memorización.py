import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui_helpers import load_css, render_page_header, render_sidebar_footer

st.set_page_config(
    page_title="Memorización",
    page_icon="🧠",
    layout="wide"
)

load_css()
render_page_header("Memorización", "🧠")

tabs = st.tabs(["🎴 Vocabulario (SRS)", "📚 Diccionario"])

with tabs[0]:
    import pages.modules.vocab_view as vocab_view
    # We need to ensure the module has a function to render content without set_page_config
    if hasattr(vocab_view, 'render_content'):
        vocab_view.render_content()
    else:
        # Fallback if I haven't refactored the module yet (which I haven't)
        # I will need to refactor the modules next.
        st.info("Módulo en reestructuración. Por favor espere...")

with tabs[1]:
    import pages.modules.dictionary_view as dictionary_view
    if hasattr(dictionary_view, 'render_content'):
        dictionary_view.render_content()
    else:
        st.info("Módulo en reestructuración. Por favor espere...")

render_sidebar_footer()
