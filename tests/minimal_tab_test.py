"""
Minimal Streamlit test to reproduce tab rendering issue
Run with: streamlit run minimal_tab_test.py
"""
import streamlit as st

st.set_page_config(page_title="Tab Test", layout="wide")

st.title("Minimal Tab Test")

tabs = st.tabs(["📚 Dictionary Test", "⚔️ Conjugations Test", "🗺️ Adventure Test", "🎯 Challenges Test"])

with tabs[0]:
    st.header("Dictionary Tab")
    try:
        import pages.modules.dictionary_view as dictionary_view
        st.success("✅ Dictionary imported")
        dictionary_view.render_content()
    except Exception as e:
        st.error(f"❌ Dictionary failed: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[1]:
    st.header("Conjugations Tab")
    try:
        import pages.modules.conjugations_view as conjugations_view
        st.success("✅ Conjugations imported")
        conjugations_view.render_content()
    except Exception as e:
        st.error(f"❌ Conjugations failed: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[2]:
    st.header("Adventure Tab")
    try:
        import pages.modules.adventure_view as adventure_view
        st.success("✅ Adventure imported")
        adventure_view.render_content()
    except Exception as e:
        st.error(f"❌ Adventure failed: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

with tabs[3]:
    st.header("Challenges Tab")
    try:
        import pages.modules.challenges_view as challenges_view
        st.success("✅ Challenges imported")
        challenges_view.render_content()
    except Exception as e:
        st.error(f"❌ Challenges failed: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
