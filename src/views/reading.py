import streamlit as st

from utils.i18n import get_text

def show_reading():
    st.markdown(f"## 📖 {get_text('reading', st.session_state.language)}")
    
    st.markdown("### CAPITVLVM PRIMVM: IMPERIVM ROMANVM")
    
    text = """
Rōma in Italiā est. Italia in Eurōpā est. Graecia in Eurōpā est. Italia et Graecia in Eurōpā sunt. Hispānia quoque in Eurōpā est. Hispānia et Italia et Graecia in Eurōpā sunt.

Aegyptus in Eurōpā nōn est, Aegyptus in Āfricā est. Gallia nōn in Āfricā est, Gallia est in Eurōpā. Syria nōn est in Eurōpā, sed in Asiā. Arabia quoque in Asiā est. Syria et Arabia in Asiā sunt. Germānia nōn in Asiā, sed in Eurōpā est. Britannia quoque in Eurōpā est. Germānia et Britannia sunt in Eurōpā.

Estne Gallia in Eurōpā? Gallia in Eurōpā est. Estne Rōma in Galliā? Rōma in Galliā nōn est. Ubi est Rōma? Rōma est in Italiā. Ubi est Italia? Italia in Eurōpā est. Ubi sunt Gallia et Hispānia? Gallia et Hispānia in Eurōpā sunt.

Estne Nīlus in Eurōpā? Nīlus in Eurōpā nōn est. Ubi est Nīlus? Nīlus in Āfricā est. Rhēnus ubi est? Rhēnus est in Germāniā. Nīlus fluvius est. Rhēnus fluvius est. Nīlus et Rhēnus fluviī sunt. Dānuvius quoque fluvius est. Rhēnus et Dānuvius sunt fluviī in Germāniā. Tiberis fluvius in Italiā est.

Nīlus fluvius magnus est. Tiberis nōn est fluvius magnus, Tiberis fluvius parvus est. Rhēnus nōn est fluvius parvus, sed fluvius magnus. Nīlus et Rhēnus fluviī magnī sunt. Dānuvius quoque fluvius magnus est.

Corsica īnsula est. Corsica et Sardinia et Sicilia īnsulae sunt. Britannia quoque īnsula est. Italia īnsula nōn est. Sicilia īnsula magna est. Melita īnsula parva est. Britannia nōn īnsula parva, sed īnsula magna est. Sicilia et Sardinia īnsulae magnae sunt. Melita nōn est īnsula magna.
    """
    
    st.markdown(
        f"""
        <div style="font-family: 'Cardo', serif; font-size: 1.2em; line-height: 1.6; text-align: justify; background-color: rgba(255,255,255,0.4); padding: 20px; border-radius: 5px;">
            {text.replace(chr(10), '<br>')}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.info(get_text('tip_reading', st.session_state.language))
