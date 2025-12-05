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
from utils.ui_helpers import render_sidebar_config
render_sidebar_config()
render_page_header("Práctica", "⚔️")

# Initialize session state for module selection
if 'practice_module' not in st.session_state:
    st.session_state.practice_module = "📜 Declinaciones"

# Auto-switch to Challenges if flag is set (from Ludus)
if 'go_to_challenge' in st.session_state and st.session_state['go_to_challenge']:
    st.session_state['go_to_challenge'] = False
    st.session_state.practice_module = "🎯 Desafíos"

# Module selection with radio buttons
selected_module = st.radio(
    "Selecciona un módulo de práctica:",
    ["📜 Declinaciones", "⚔️ Conjugaciones", "🗺️ Aventura", "🎯 Desafíos"],
    horizontal=True,
    key='practice_module',
    label_visibility="collapsed"
)

st.markdown("---")

# Render the selected module
try:
    if selected_module == "📜 Declinaciones":
        import pages.modules.declensions_view as declensions_view
        declensions_view.render_content()
    
    elif selected_module == "⚔️ Conjugaciones":
        import pages.modules.conjugations_view as conjugations_view
        conjugations_view.render_content()
    
    elif selected_module == "🗺️ Aventura":
        import pages.modules.adventure_view as adventure_view
        adventure_view.render_content()
    
    elif selected_module == "🎯 Desafíos":
        import pages.modules.challenges_view as challenges_view
        challenges_view.render_content()

except Exception as e:
    st.error(f"❌ Error al cargar el módulo {selected_module}: {str(e)}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())

render_sidebar_footer()
