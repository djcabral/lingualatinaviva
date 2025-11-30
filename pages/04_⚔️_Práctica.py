import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui_helpers import load_css, render_page_header, render_sidebar_footer

st.set_page_config(
    page_title="Práctica",
    page_icon="⚔️",
    layout="wide"
)

load_css()
render_page_header("Práctica", "⚔️")

tabs = st.tabs(["📜 Declinaciones", "⚔️ Conjugaciones", "🗺️ Aventura", "🎯 Desafíos"])

# Auto-switch to Challenges tab if flag is set
if 'go_to_challenge' in st.session_state and st.session_state['go_to_challenge']:
    st.session_state['go_to_challenge'] = False
    # Force switch to tab index 3 (Desafíos)
    st.session_state['active_tab'] = 3

with tabs[0]:
    try:
        import pages.modules.declensions_view as declensions_view
        declensions_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Declinaciones: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[1]:
    try:
        import pages.modules.conjugations_view as conjugations_view
        conjugations_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Conjugaciones: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[2]:
    try:
        import pages.modules.adventure_view as adventure_view
        adventure_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Aventura: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[3]:
    try:
        import pages.modules.challenges_view as challenges_view
        challenges_view.render_content()
    except Exception as e:
        st.error(f"Error al cargar Desafíos: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

render_sidebar_footer()
