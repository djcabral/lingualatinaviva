import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui_helpers import load_css, render_page_header, render_sidebar_footer
from database.connection import get_session

# Import modules from original files (we will need to refactor slightly or import functions)
# Since we can't easily import from other pages, we might need to copy logic or refactor pages into modules.
# For now, to be safe and "organic", I will use a tab structure that imports the logic if possible, 
# OR I will simply replicate the logic in a cleaner way.
# Given the complexity, I will create a wrapper that uses the existing logic by importing it if it was in a module, 
# but since they are pages, I should probably move the core logic to `src/views` or similar if I were refactoring deeply.
# However, to do this "organically" and quickly without breaking everything, I will copy the core `main` logic 
# from the pages into functions here, or better yet, I will rename the files to be modules and import them.

# STRATEGY: 
# 1. Rename existing pages to be importable modules (e.g. `pages/02_📘_Curso.py` -> `modules/course_view.py`)
# 2. Import these modules in the new `pages/02_📘_Lecciones.py`
# This is cleaner. But I can't move files easily with `write_to_file`.
# I will use `run_command` to move files.

st.set_page_config(
    page_title="Lecciones",
    page_icon="📘",
    layout="wide"
)

load_css()
render_page_header("Lecciones", "📘")

# Tabs for the 3 sub-sections
tabs = st.tabs(["📘 Curso Estructurado", "📖 Lecturas Graduadas", "⚖️ Referencia Gramatical"])

with tabs[0]:
    # Logic from 02_📘_Curso.py
    # I will need to dynamically load or execute the content. 
    # For now, I will put a placeholder and then fill it with the content of the original file
    # adapted to be inside a tab (removing set_page_config).
    import pages.modules.course_view as course_view
    course_view.render_course_content()

with tabs[1]:
    # Logic from 06_📖_Lecturas.py
    import pages.modules.readings_view as readings_view
    readings_view.render_readings_content()

with tabs[2]:
    # Logic from 12_⚖️_Gramatica_Ref.py
    import pages.modules.grammar_view as grammar_view
    grammar_view.render_grammar_content()

render_sidebar_footer()
