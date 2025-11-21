import streamlit as st
import sys
import os

root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

st.set_page_config(page_title="Gramática", page_icon="📖", layout="wide")

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif;'>
        📖 Gramática Rápida
    </h1>
    """,
    unsafe_allow_html=True
)

st.info("📚 Consulta rápida de gramática latina. Encuentra tablas de declinaciones, conjugaciones y más.")

# Create tabs for different grammar topics
grammar_tabs = st.tabs(["🏛️ Declinaciones", "⚔️ Conjugaciones", "👤 Pronombres", "✨ Adjetivos", "📝 Sintaxis"])

# ===== TAB 1: DECLENSIONS =====
with grammar_tabs[0]:
    st.markdown("## Declinaciones de Sustantivos")
    
    # 1st Declension
    with st.expander("📗 Primera Declinación (-a, -ae) - Femenino", expanded=True):
        st.markdown("**Ejemplo:** *puella, puellae* (f) - niña")
        
        st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nominativo** | puell**a** | puell**ae** |
| **Vocativo** | puell**a** | puell**ae** |
| **Acusativo** | puell**am** | puell**ās** |
| **Genitivo** | puell**ae** | puell**ārum** |
| **Dativo** | puell**ae** | puell**īs** |
| **Ablativo** | puell**ā** | puell**īs** |
        """)
        
        st.caption("💡 Típicamente femenino. Terminación característica: **-a** (nom. sg.)")
    
    # 2nd Declension
    with st.expander("📘 Segunda Declinación (-us, -i / -um, -i)"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Masculino:** *dominus, dominī* (m) - señor")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | domin**us** | domin**ī** |
| **Voc.** | domin**e** | domin**ī** |
| **Acc.** | domin**um** | domin**ōs** |
| **Gen.** | domin**ī** | domin**ōrum** |
| **Dat.** | domin**ō** | domin**īs** |
| **Abl.** | domin**ō** | domin**īs** |
            """)
        
        with col2:
            st.markdown("**Neutro:** *templum, templī* (n) - templo")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | templ**um** | templ**a** |
| **Voc.** | templ**um** | templ**a** |
| **Acc.** | templ**um** | templ**a** |
| **Gen.** | templ**ī** | templ**ōrum** |
| **Dat.** | templ**ō** | templ**īs** |
| **Abl.** | templ**ō** | templ**īs** |
            """)
        
        st.caption("💡 Neutros: Nom. = Acc. = Voc. (en ambos números). Plural siempre en **-a**")
    
    # 3rd Declension
    with st.expander("📙 Tercera Declinación (variada)"):
        st.info("ℹ️ La 3ª declinación tiene dos subtipos según el número de sílabas en nominativo vs genitivo")
        
        st.markdown("### Imparisílabos (Genitivo tiene MÁS sílabas)")
        st.caption("Ejemplo: *rēx* (1 sílaba) → *rēg-is* (2 sílabas)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Masculino/Femenino:** *rēx, rēgis* (m) - rey")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **rēx** | rēg**ēs** |
| **Voc.** | **rēx** | rēg**ēs** |
| **Acc.** | rēg**em** | rēg**ēs** |
| **Gen.** | rēg**is** | rēg**um** |
| **Dat.** | rēg**ī** | rēg**ibus** |
| **Abl.** | rēg**e** | rēg**ibus** |
            """)
        
        with col2:
            st.markdown("**Neutro:** *nōmen, nōminis* (n) - nombre")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **nōmen** | nōmin**a** |
| **Voc.** | **nōmen** | nōmin**a** |
| **Acc.** | **nōmen** | nōmin**a** |
| **Gen.** | nōmin**is** | nōmin**um** |
| **Dat.** | nōmin**ī** | nōmin**ibus** |
| **Abl.** | nōmin**e** | nōmin**ibus** |
            """)
        
        st.divider()
        
        st.markdown("### Parisílabos (Genitivo tiene IGUAL sílabas)")
        st.caption("Ejemplo: *cīv-is* (2 sílabas) → *cīv-is* (2 sílabas)")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("**Masculino/Femenino:** *cīvis, cīvis* (c) - ciudadano")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **cīvis** | cīv**ēs** |
| **Voc.** | **cīvis** | cīv**ēs** |
| **Acc.** | cīv**em** | cīv**ēs** |
| **Gen.** | cīv**is** | cīv**ium** |
| **Dat.** | cīv**ī** | cīv**ibus** |
| **Abl.** | cīv**ī** | cīv**ibus** |
            """)
        
        with col4:
            st.markdown("**Neutro:** *mare, maris* (n) - mar")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **mare** | mar**ia** |
| **Voc.** | **mare** | mar**ia** |
| **Acc.** | **mare** | mar**ia** |
| **Gen.** | mar**is** | mar**ium** |
| **Dat.** | mar**ī** | mar**ibus** |
| **Abl.** | mar**ī** | mar**ibus** |
            """)
        
        st.warning("""
        **⚠️ Diferencias clave:**
        - **Gen. Pl.:** Imparisílabo = `-um` | Parisílabo = `-ium`
        - **Abl. Sg.:** Imparisílabo = `-e` | Parisílabo = `-ī` (M/F puede variar)
        - **Nom/Acc Pl. Neutro:** Imparisílabo = `-a` | Parisílabo = `-ia`
        """)

        
        st.caption("💡 Genitivo singular en **-is**. Gran variedad de nominativos.")
    
    # 4th Declension
    with st.expander("📕 Cuarta Declinación (-us, -ūs)"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Masculino:** *frūctus, frūctūs* (m) - fruto")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | frūct**us** | frūct**ūs** |
| **Voc.** | frūct**us** | frūct**ūs** |
| **Acc.** | frūct**um** | frūct**ūs** |
| **Gen.** | frūct**ūs** | frūct**uum** |
| **Dat.** | frūct**uī** | frūct**ibus** |
| **Abl.** | frūct**ū** | frūct**ibus** |
            """)
        
        with col2:
            st.markdown("**Neutro:** *cornū, cornūs* (n) - cuerno")
            st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | corn**ū** | corn**ua** |
| **Voc.** | corn**ū** | corn**ua** |
| **Acc.** | corn**ū** | corn**ua** |
| **Gen.** | corn**ūs** | corn**uum** |
| **Dat.** | corn**ū** | corn**ibus** |
| **Abl.** | corn**ū** | corn**ibus** |
            """)
        
        st.caption("💡 Típicamente masculino. Muy pocos neutros. Genitivo sg.: **-ūs**")
    
    # 5th Declension
    with st.expander("📓 Quinta Declinación (-ēs, -ēī)"):
        st.markdown("**Femenino:** *rēs, reī* (f) - cosa")
        st.markdown("""
| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | r**ēs** | r**ēs** |
| **Voc.** | r**ēs** | r**ēs** |
| **Acc.** | r**em** | r**ēs** |
| **Gen.** | r**eī** | r**ērum** |
| **Dat.** | r**eī** | r**ēbus** |
| **Abl.** | r**ē** | r**ēbus** |
        """)
        
        st.caption("💡 Casi todos femeninos. Pocos sustantivos. Importante: *rēs* (cosa), *diēs* (día), *fidēs* (fe), *spēs* (esperanza)")
    
    # Exceptions
    with st.expander("⚠️ Excepciones y Casos Especiales"):
        st.markdown("### Sustantivos Irregulares Comunes")
        
        st.markdown("""
**domus, domūs** (f) - casa (mezcla 2ª y 4ª declinación)
- Gen. sg.: **domūs** o **domī**
- Abl. sg.: **domō** o **domū**
- Locativo: **domī** (en casa)

**vis, vīs** (f) - fuerza (irregular)
- Solo tiene plural completo
- Ac. sg.: **vim**, Abl. sg.: **vī**

**Género excepcional:**
- *humus* (f) - tierra (2ª decl. pero femenino)
- *pinus* (f) - pino (2ª decl. pero femenino)
- *manus* (f) - mano (4ª decl. femenino)
- *domus* (f) - casa (4ª decl. femenino)
        """)

# ===== TAB 2: CONJUGATIONS =====
with grammar_tabs[1]:
    st.markdown("## Conjugaciones Verbales")
    
    # Present System
    with st.expander("🟢 Sistema de Presente (Presente, Imperfecto, Futuro)", expanded=True):
        st.markdown("### Presente de Indicativo Activo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**1ª Conjugación:** *amō, amāre* - amar")
            st.markdown("""
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | am**ō** | am**āmus** |
| **2ª** | am**ās** | am**ātis** |
| **3ª** | am**at** | am**ant** |
            """)
            
            st.markdown("**3ª Conjugación:** *regō, regere* - regir")
            st.markdown("""
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | reg**ō** | reg**imus** |
| **2ª** | reg**is** | reg**itis** |
| **3ª** | reg**it** | reg**unt** |
            """)
        
        with col2:
            st.markdown("**2ª Conjugación:** *moneō, monēre* - advertir")
            st.markdown("""
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | mone**ō** | mon**ēmus** |
| **2ª** | mon**ēs** | mon**ētis** |
| **3ª** | mon**et** | mon**ent** |
            """)
            
            st.markdown("**4ª Conjugación:** *audiō, audīre* - oír")
            st.markdown("""
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | audi**ō** | aud**īmus** |
| **2ª** | aud**īs** | aud**ītis** |
| **3ª** | aud**it** | aud**iunt** |
            """)
        
        st.markdown("---")
        st.markdown("### Imperfecto de Indicativo Activo")
        st.caption("💡 Formación: raíz + **-ba-** (1ª/2ª) o **-ēba-** (3ª/4ª) + desinencias")
        
        st.markdown("""
| Persona | 1ª (amō) | 2ª (moneō) | 3ª (regō) | 4ª (audiō) |
|:-------:|:--------:|:----------:|:---------:|:----------:|
| **1ª sg** | amā**bam** | monē**bam** | reg**ēbam** | audi**ēbam** |
| **2ª sg** | amā**bās** | monē**bās** | reg**ēbās** | audi**ēbās** |
| **3ª sg** | amā**bat** | monē**bat** | reg**ēbat** | audi**ēbat** |
| **1ª pl** | amā**bāmus** | monē**bāmus** | reg**ēbāmus** | audi**ēbāmus** |
| **2ª pl** | amā**bātis** | monē**bātis** | reg**ēbātis** | audi**ēbātis** |
| **3ª pl** | amā**bant** | monē**bant** | reg**ēbant** | audi**ēbant** |
        """)
    
    # Perfect System
    with st.expander("🔵 Sistema de Perfecto (Perfecto, Pluscuamperfecto, Futuro Perfecto)"):
        st.markdown("### Perfecto de Indicativo Activo")
        st.caption("💡 Formación: **raíz de perfecto** + desinencias (-ī, -istī, -it, -imus, -istis, -ērunt)")
        
        st.markdown("**Ejemplo:** *amāvī* (he amado)")
        
        st.markdown("""
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | amāv**ī** | amāv**imus** |
| **2ª** | amāv**istī** | amāv**istis** |
| **3ª** | amāv**it** | amāv**ērunt** |
        """)
        
        st.markdown("---")
        st.markdown("### Pluscuamperfecto de Indicativo Activo")
        st.caption("💡 Formación: raíz de perfecto + **-eram**")
        
        st.markdown("""
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | amāv**eram** | amāv**erāmus** |
| **2ª** | amāv**erās** | amāv**erātis** |
| **3ª** | amāv**erat** | amāv**erant** |
        """)
        
        st.markdown("---")
        st.markdown("###  Futuro de Indicativo Activo")
        st.caption("💡 1ª/2ª conjugación: raíz + **-b-**; 3ª/4ª: raíz + **-ē-** (excepto 1ª sg.)")
        
        st.markdown("""
| Persona | 1ª (amō) | 2ª (moneō) | 3ª (regō) | 4ª (audiō) |
|:-------:|:--------:|:----------:|:---------:|:----------:|
| **1ª sg** | amā**bō** | monē**bō** | reg**am** | audi**am** |
| **2ª sg** | amā**bis** | monē**bis** | reg**ēs** | audi**ēs** |
| **3ª sg** | amā**bit** | monē**bit** | reg**et** | audi**et** |
| **1ª pl** | amā**bimus** | monē**bimus** | reg**ēmus** | audi**ēmus** |
| **2ª pl** | amā**bitis** | monē**bitis** | reg**ētis** | audi**ētis** |
| **3ª pl** | amā**bunt** | monē**bunt** | reg**ent** | audi**ent** |
        """)
    
    # Irregular Verbs
    with st.expander("🔴 Verbos Irregulares Importantes"):
        st.markdown("### sum, esse, fuī (ser/estar)")
        st.markdown("""
| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | sum | es | est | sumus | estis | sunt |
| **Imperfecto** | eram | erās | erat | erāmus | erātis | erant |
| **Futuro** | erō | eris | erit | erimus | eritis | erunt |
| **Perfecto** | fuī | fuistī | fuit | fuimus | fuistis | fuērunt |
        """)
        
        st.markdown("---")
        st.markdown("### possum, posse, potuī (poder)")
        st.caption("💡 Formación: pot + sum (pot-sum → possum)")
        st.markdown("""
| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | possum | potes | potest | possumus | potestis | possunt |
| **Imperfecto** | poteram | poterās | poterat | poterāmus | poterātis | poterant |
| **Futuro** | poterō | poteris | poterit | poterimus | poteritis | poterunt |
        """)
        
        st.markdown("---")
        st.markdown("### eō, īre, iī/īvī, itum (ir)")
        st.markdown("""
| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | eō | īs | it | īmus | ītis | eunt |
| **Imperfecto** | ībam | ībās | ībat | ībāmus | ībātis | ībant |
| **Futuro** | ībō | ībis | ībit | ībimus | ībitis | ībunt |
        """)
        
        st.markdown("---")
        st.markdown("### ferō, ferre, tulī, lātum (llevar)")
        st.markdown("""
| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | ferō | fers | fert | ferimus | fertis | ferunt |
| **Imperfecto** | ferēbam | ferēbās | ferēbat | ferēbāmus | ferēbātis | ferēbant |
        """)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**volō** (querer)")
            st.markdown("""
| Presente |
|:---------|
| volō |
| vīs |
| vult |
| volumus |
| vultis |
| volunt |
            """)
        
        with col2:
            st.markdown("**nōlō** (no querer)")
            st.markdown("""
| Presente |
|:---------|
| nōlō |
| nōn vīs |
| nōn vult |
| nōlumus |
| nōn vultis |
| nōlunt |
            """)
        
        with col3:
            st.markdown("**mālō** (preferir)")
            st.markdown("""
| Presente |
|:---------|
| mālō |
| māvīs |
| māvult |
| mālumus |
| māvultis |
| mālunt |
            """)
    
    # Verbals (Verboides)
    with st.expander("📋 Verboides (Formas Nominales del Verbo)"):
        st.markdown("### Infinitivos")
        st.markdown("""
| Conjugación | Presente Activo | Perfecto Activo | Presente Pasivo |
|:-----------:|:----------------|:----------------|:----------------|
| **1ª** | amā**re** | amāv**isse** | amā**rī** |
| **2ª** | monē**re** | monu**isse** | monē**rī** |
| **3ª** | reg**ere** | rēx**isse** | reg**ī** |
| **4ª** | aud**īre** | audīv**isse** | aud**īrī** |
        """)
        
        st.markdown("---")
        st.markdown("### Participios")
        st.markdown("""
**Participio Presente Activo:**
- Se forma: raíz + **-ns / -nt-** + terminación
- Ejemplo: *amāns, amantis* (amante, que ama)

**Participio Perfecto Pasivo (PPP):**
- 4ª parte principal
- Ejemplo: *amātus, -a, -um* (amado/a)

**Participio Future Activo:**
- PPP + **-ūrus, -a, -um**
- Ejemplo: *amātūrus, -a, -um* (que va a amar)
        """)
        
        st.markdown("---")
        st.markdown("### Gerundio")
        st.markdown("""
**Formación:** raíz + **-nd-** + terminaciones de 2ª declinación neutro

| Caso | Forma | Ejemplo (amō) |
|:-----|:------|:--------------|
| **Gen.** | -**ndī** | amandī (de amar) |
| **Dat.** | -**ndō** | amandō (para amar) |
| **Acc.** | -(ad) **ndum** | (ad) amandum (para amar) |
| **Abl.** | -**ndō** | amandō (por/con amar) |
        """)
        
        st.markdown("---")
        st.markdown("### Gerundivo")
        st.markdown("""
**Formación:** raíz + **-ndus, -a, -um** (adjetivo verbal de obligación)

- Ejemplo: *amandus, -a, -um* (que debe ser amado)
- Uso: construcción pasiva de obligación con *sum*
- *Carthāgō dēlenda est* = Cartago debe ser destruida
        """)
        
        st.markdown("---")
        st.markdown("### Supino")
        st.markdown("""
**Formación:** PPP sin terminación + **-um** (acusativo) o **-ū** (ablativo)

| Forma | Uso | Ejemplo |
|:------|:----|:--------|
| **Ac. (-um)** | Expresa finalidad con verbos de movimiento | Vēnī **vīsum** (Vine a ver) |
| **Abl. (-ū)** | "En cuanto a..." | Facile **dictū** (Fácil de decir) |
        """)
    
    # Add Adverbs section as new tab or expander
    with st.expander("📌 Adverbios Más Usados"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Adverbios de Lugar")
            st.markdown("""
- **hīc** - aquí
- **illīc** - allí
- **ibī** - allí
- **ubī** - donde
- **quō** - adonde
- **unde** - de donde
- **longē** - lejos
- **prope** - cerca
            """)
            
            st.markdown("### Adverbios de Tiempo")
            st.markdown("""
- **nunc** - ahora
- **tunc / tum** - entonces
- **iam** - ya
- **mox** - pronto
- **statim** - inmediatamente
- **semper** - siempre
- **numquam** - nunca
- **saepe** - a menudo
- **hodiē** - hoy
- **herī** - ayer
- **crās** - mañana
            """)
        
        with col2:
            st.markdown("### Adverbios de Modo")
            st.markdown("""
- **bene** - bien
- **male** - mal
- **multum** - mucho
- **parum** - poco
- **sīc** - así
- **ita** - así
- **maximē** - muchísimo
- **minimē** - nada, en absoluto
            """)
            
            st.markdown("### Otros Adverbios Comunes")
            st.markdown("""
- **etiam** - también, incluso
- **quoque** - también
- **nōn** - no
- **fortasse** - quizás
- **valdē** - mucho, muy
- **tantum** - solamente
- **circum** - alrededor
- **prope** - casi
            """)

# ===== TAB 3: PRONOUNS =====
with grammar_tabs[2]:
    st.markdown("## Pronombres")
    
    # Personal Pronouns
    with st.expander("👥 Pronombres Personales", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**1ª Persona:** ego (yo) / nōs (nosotros)")
            st.markdown("""
| Caso | Singular (yo) | Plural (nosotros) |
|:----:|:-------------:|:-----------------:|
| **Nom.** | **ego** | **nōs** |
| **Gen.** | **meī** | **nostrī / nostrum** |
| **Dat.** | **mihi** | **nōbīs** |
| **Acc.** | **mē** | **nōs** |
| **Abl.** | **mē** | **nōbīs** |
            """)
        
        with col2:
            st.markdown("**2ª Persona:** tū (tú) / vōs (vosotros)")
            st.markdown("""
| Caso | Singular (tú) | Plural (vosotros) |
|:----:|:-------------:|:-----------------:|
| **Nom.** | **tū** | **vōs** |
| **Gen.** | **tuī** | **vestrī / vestrum** |
| **Dat.** | **tibi** | **vōbīs** |
| **Acc.** | **tē** | **vōs** |
| **Abl.** | **tē** | **vōbīs** |
            """)
    
    # Demonstrative
    with st.expander("👉 Pronombres Demostrativos"):
        st.markdown("**hic, haec, hoc** (este, esta, esto)")
        
        st.markdown("""
| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | hic | haec | hoc | hī | hae | haec |
| **Gen.** | huius | huius | huius | hōrum | hārum | hōrum |
| **Dat.** | huic | huic | huic | hīs | hīs | hīs |
| **Acc.** | hunc | hanc | hoc | hōs | hās | haec |
| **Abl.** | hōc | hāc | hōc | hīs | hīs | hīs |
        """)

# ===== TAB 4: ADJECTIVES =====
with grammar_tabs[3]:
    st.markdown("## Adjetivos")
    
    with st.expander("⭐ Adjetivos 1ª/2ª Declinación", expanded=True):
        st.markdown("**bonus, bona, bonum** (bueno, buena)")
        st.caption("💡 Se declina como sustantivos: -us (2ª masc), -a (1ª fem), -um (2ª neut)")
        
        st.markdown("""
| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | bon**us** | bon**a** | bon**um** | bon**ī** | bon**ae** | bon**a** |
| **Gen.** | bon**ī** | bon**ae** | bon**ī** | bon**ōrum** | bon**ārum** | bon**ōrum** |
| **Dat.** | bon**ō** | bon**ae** | bon**ō** | bon**īs** | bon**īs** | bon**īs** |
| **Acc.** | bon**um** | bon**am** | bon**um** | bon**ōs** | bon**ās** | bon**a** |
| **Abl.** | bon**ō** | bon**ā** | bon**ō** | bon**īs** | bon**īs** | bon**īs** |
        """)

# ===== TAB 5: BASIC SYNTAX =====
with grammar_tabs[4]:
    st.markdown("## Sintaxis Básica")
    
    with st.expander("📐 Funciones de los Casos", expanded=True):
        st.markdown("""
| Caso | Función Principal | Ejemplo |
|:----:|:------------------|:--------|
| **Nominativo** | Sujeto | *Puella* cantat (La niña canta) |
| **Genitivo** | Posesión, pertenencia | Liber *puellae* (El libro de la niña) |
| **Dativo** | Objeto indirecto | Do librum *puellae* (Doy el libro a la niña) |
| **Acusativo** | Objeto directo | Video *puellam* (Veo a la niña) |
| **Ablativo** | Instrumento, lugar, modo | Cum *puellā* (Con la niña) |
| **Vocativo** | Llamada, invocación | *Puella*, veni! (¡Niña, ven!) |
        """)
    
    with st.expander("📏 Orden de Palabras"):
        st.markdown("""
**Orden típico en latín:** SOV (Sujeto - Objeto - Verbo)

**Ejemplo:**
- *Puella* (S) *rosam* (O) *amat* (V)
- La niña ama la rosa

**Pero el orden es flexible** por las terminaciones de caso.

**Énfasis:** La palabra más importante suele ir al principio o al final.
        """)

st.markdown("---")
st.success("💡 **Tip:** Usa esta sección como referencia rápida mientras practicas en los módulos de Declinatio y Conjugatio.")
