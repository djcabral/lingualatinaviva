import streamlit as st
from sqlmodel import select
from database import get_session
from database import UserProfile

from i18n import get_text

def show_dashboard():
    st.markdown(f"# 🏛️ {get_text('app_title', st.session_state.language)}")
    st.markdown("### *Per aspera ad astra*")
    
    with get_session() as session:
        user = session.exec(select(UserProfile)).first()
        if not user:
            user = UserProfile(username="Discipulus", level=1, xp=0, streak=0)
    
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f"""
                <div class="stat-box">
                    <div class="stat-value">{user.level}</div>
                    <div class="stat-label">{get_text('level', st.session_state.language)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col2:
            st.markdown(
                f"""
                <div class="stat-box">
                    <div class="stat-value">{user.streak}</div>
                    <div class="stat-label">{get_text('days', st.session_state.language)} (Racha)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col3:
            st.markdown(
                f"""
                <div class="stat-box">
                    <div class="stat-value">{user.xp}</div>
                    <div class="stat-label">{get_text('xp', st.session_state.language)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown(f"### {get_text('today_tasks', st.session_state.language)}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"📝 **{get_text('vocabulary', st.session_state.language)}**: 20 {get_text('vocab_due', st.session_state.language)}")
        st.info(f"📜 **{get_text('declension', st.session_state.language)}**: {get_text('decl_task', st.session_state.language)}")
    with c2:
        st.info(f"⚔️ **{get_text('conjugation', st.session_state.language)}**: {get_text('conj_task', st.session_state.language)}")
        st.info(f"📖 **{get_text('reading', st.session_state.language)}**: {get_text('read_task', st.session_state.language)}")
