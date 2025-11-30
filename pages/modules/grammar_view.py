import streamlit as st
import sys
import os
from database.connection import get_session
from utils.i18n import get_text
from utils.ui_helpers import load_css




def render_grammar_content():
    
    # Load CSS
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
    # Create tabs for different grammar topics
    grammar_tabs = st.tabs(["🏛️ Declinaciones", "⚔️ Conjugaciones", "👤 Pronombres", "✨ Adjetivos", "📝 Sintaxis", "💡 Consejos"])
    
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
    
        # Reflexive Pronoun
        with st.expander("🔄 Pronombre Reflexivo (3ª Persona)"):
            st.markdown("**sē** (se, a sí mismo/a/os/as)")
            st.caption("💡 No tiene Nominativo. Es igual para singular y plural.")
            st.markdown("""
    | Caso | Forma | Traducción |
    |:----:|:-----:|:-----------|
    | **Gen.** | **suī** | de sí mismo/a/os/as |
    | **Dat.** | **sibi** | para sí mismo... |
    | **Acc.** | **sē / sēsē** | a sí mismo... |
    | **Abl.** | **sē / sēsē** | con/por sí mismo... |
            """)
    
        # Demonstrative Pronouns
        with st.expander("👉 Pronombres Demostrativos"):
            st.markdown("### hic, haec, hoc (este, esta, esto)")
            st.markdown("""
    | Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
    |:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
    | **Nom.** | hic | haec | hoc | hī | hae | haec |
    | **Gen.** | huius | huius | huius | hōrum | hārum | hōrum |
    | **Dat.** | huic | huic | huic | hīs | hīs | hīs |
    | **Acc.** | hunc | hanc | hoc | hōs | hās | haec |
    | **Abl.** | hōc | hāc | hōc | hīs | hīs | hīs |
            """)
            
            st.divider()
            
            st.markdown("### ille, illa, illud (aquel, aquella, aquello)")
            st.markdown("""
    | Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
    |:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
    | **Nom.** | ille | illa | illud | illī | illae | illa |
    | **Gen.** | illīus | illīus | illīus | illōrum | illārum | illōrum |
    | **Dat.** | illī | illī | illī | illīs | illīs | illīs |
    | **Acc.** | illum | illam | illud | illōs | illās | illa |
    | **Abl.** | illō | illā | illō | illīs | illīs | illīs |
            """)
            
            st.divider()
            
            st.markdown("### iste, ista, istud (ese, esa, eso)")
            st.caption("💡 Se declina igual que *ille*.")
            st.markdown("""
    | Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
    |:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
    | **Nom.** | iste | ista | istud | istī | istae | ista |
    | **Gen.** | istīus | istīus | istīus | istōrum | istārum | istōrum |
    | **Dat.** | istī | istī | istī | istīs | istīs | istīs |
    | **Acc.** | istum | istam | istud | istōs | istās | ista |
    | **Abl.** | istō | istā | istō | istīs | istīs | istīs |
            """)
            
            st.divider()
            
            st.markdown("### is, ea, id (él, ella, ello / este, ese)")
            st.caption("💡 Usado como pronombre personal de 3ª persona o demostrativo débil.")
            st.markdown("""
    | Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
    |:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
    | **Nom.** | is | ea | id | eī / iī | eae | ea |
    | **Gen.** | eius | eius | eius | eōrum | eārum | eōrum |
    | **Dat.** | eī | eī | eī | eīs / iīs | eīs / iīs | eīs / iīs |
    | **Acc.** | eum | eam | id | eōs | eās | ea |
    | **Abl.** | eō | eā | eō | eīs / iīs | eīs / iīs | eīs / iīs |
            """)
    
        # Relative Pronoun
        with st.expander("🔗 Pronombre Relativo"):
            st.markdown("### quī, quae, quod (que, el cual, quien)")
            st.markdown("""
    | Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
    |:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
    | **Nom.** | quī | quae | quod | quī | quae | quae |
    | **Gen.** | cuius | cuius | cuius | quōrum | quārum | quōrum |
    | **Dat.** | cui | cui | cui | quibus | quibus | quibus |
    | **Acc.** | quem | quam | quod | quōs | quās | quae |
    | **Abl.** | quō | quā | quō | quibus | quibus | quibus |
            """)
    
        # Interrogative Pronoun
        with st.expander("❓ Pronombre Interrogativo"):
            st.markdown("### quis, quid (¿quién?, ¿qué?)")
            st.caption("💡 En plural es igual que el relativo (*quī, quae, quae*).")
            st.markdown("""
    | Caso | Masc./Fem. Sg | Neutro Sg |
    |:----:|:-------------:|:---------:|
    | **Nom.** | **quis** | **quid** |
    | **Gen.** | cuius | cuius |
    | **Dat.** | cui | cui |
    | **Acc.** | quem | **quid** |
    | **Abl.** | quō | quō |
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
        
        with st.expander("🌟 Adjetivos de 2ª Clase (3ª Declinación)"):
            st.info("Siguen la 3ª declinación de temas en -i (Parisílabos). Abl. sg. en **-ī**, Gen. pl. en **-ium**, Nom/Ac pl. neutro en **-ia**.")
            
            st.markdown("### 1. Tres Terminaciones (-er, -is, -e)")
            st.markdown("**acer, acris, acre** (agudo, enérgico)")
            st.caption("Masc: *acer*, Fem: *acris*, Neut: *acre*. (Solo cambia en el Nominativo singular).")
            
            st.markdown("### 2. Dos Terminaciones (-is, -e)")
            st.markdown("**fortis, forte** (fuerte, valiente)")
            st.caption("Masc/Fem: *fortis*, Neut: *forte*. (La mayoría son de este tipo).")
            
            st.markdown("""
    | Caso | Masc./Fem. Sg | Neutro Sg | Masc./Fem. Pl | Neutro Pl |
    |:----:|:-------------:|:---------:|:-------------:|:---------:|
    | **Nom.** | fort**is** | fort**e** | fort**ēs** | fort**ia** |
    | **Gen.** | fort**is** | fort**is** | fort**ium** | fort**ium** |
    | **Dat.** | fort**ī** | fort**ī** | fort**ibus** | fort**ibus** |
    | **Acc.** | fort**em** | fort**e** | fort**ēs** | fort**ia** |
    | **Abl.** | fort**ī** | fort**ī** | fort**ibus** | fort**ibus** |
            """)
            
            st.markdown("### 3. Una Terminación")
            st.markdown("**fēlīx, fēlīcis** (feliz)")
            st.caption("Masc/Fem/Neut: *fēlīx* en el nominativo. Se distinguen en los demás casos.")
            st.markdown("""
    | Caso | Masc./Fem. Sg | Neutro Sg | Masc./Fem. Pl | Neutro Pl |
    |:----:|:-------------:|:---------:|:-------------:|:---------:|
    | **Nom.** | fēlīx | fēlīx | fēlīc**ēs** | fēlīc**ia** |
    | **Gen.** | fēlīc**is** | fēlīc**is** | fēlīc**ium** | fēlīc**ium** |
    | **Acc.** | fēlīc**em** | fēlīx | fēlīc**ēs** | fēlīc**ia** |
    | **Abl.** | fēlīc**ī** | fēlīc**ī** | fēlīc**ibus** | fēlīc**ibus** |
            """)
    
        with st.expander("📈 Grados del Adjetivo (Comparativo y Superlativo)"):
            st.markdown("### 1. Comparativo de Superioridad")
            st.markdown("Se forma añadiendo **-ior** (M/F) y **-ius** (N) a la raíz.")
            st.markdown("**Ejemplo:** *altus* (alto) → *altior, altius* (más alto)")
            st.info("⚠️ Se declina como la 3ª declinación CONSONÁNTICA (Imparisílabo). Abl. sg. en **-e**, Gen. pl. en **-um**.")
            
            st.markdown("""
    | Caso | Masc./Fem. Sg | Neutro Sg | Masc./Fem. Pl | Neutro Pl |
    |:----:|:-------------:|:---------:|:-------------:|:---------:|
    | **Nom.** | altior | altius | altiōr**ēs** | altiōr**a** |
    | **Gen.** | altiōr**is** | altiōr**is** | altiōr**um** | altiōr**um** |
    | **Acc.** | altiōr**em** | altius | altiōr**ēs** | altiōr**a** |
    | **Abl.** | altiōr**e** | altiōr**e** | altiōr**ibus** | altiōr**ibus** |
            """)
            
            st.divider()
            
            st.markdown("### 2. Superlativo")
            st.markdown("Se forma generalmente añadiendo **-issimus, -a, -um** a la raíz.")
            st.markdown("**Ejemplo:** *altus* → *altissimus, -a, -um* (altísimo / el más alto)")
            st.caption("Se declina como un adjetivo de 1ª/2ª declinación (*bonus, -a, -um*).")
            
            st.markdown("**Excepciones:**")
            st.markdown("- Adjetivos en **-er**: añaden *-rimus* (*pucher* → *pulcherrimus*)")
            st.markdown("- Adjetivos en **-lis**: añaden *-limus* (*facilis* → *facillimus*)")
            
            st.divider()
            
            st.markdown("### 3. Comparación Irregular")
            st.markdown("""
    | Positivo | Comparativo | Superlativo | Significado |
    |:---------|:------------|:------------|:------------|
    | **bonus** | melior, -ius | optimus | bueno, mejor, óptimo |
    | **malus** | peior, -ius | pessimus | malo, peor, pésimo |
    | **magnus** | maior, -ius | maximus | grande, mayor, máximo |
    | **parvus** | minor, minus | minimus | pequeño, menor, mínimo |
    | **multus** | plūs | plūrimus | mucho, más, muchísimo |
            """)
    
    # ===== TAB 5: SYNTAX =====
    with grammar_tabs[4]:
        st.markdown("## Sintaxis Latina")
        st.info("La sintaxis estudia cómo se combinan las palabras para formar oraciones. En latín, las **desinencias (casos)** son la clave.")
    
        # 1. The Complements
        with st.expander("🧱 Los Complementos y los Casos", expanded=True):
            st.markdown("### Guía Rápida de Funciones")
            st.markdown("""
    | Caso | Función | ¿Qué es? | Pregunta | Ejemplo |
    |:---:|:---|:---|:---|:---|
    | **Nominativo** | **Sujeto** | Quien realiza la acción o de quien se habla. | ¿Quién? | *__Puella__ cantat.* (La niña canta) |
    | | **Atributo** | Cualidad del sujeto con verbos copulativos (sum). | ¿Cómo es? | *Puella __pulchra__ est.* (La niña es hermosa) |
    | **Vocativo** | **Apelación** | A quien nos dirigimos directamente. | — | *__Marce__, veni!* (¡Marco, ven!) |
    | **Acusativo** | **Objeto Directo (OD)** | Recibe la acción directamente. | ¿Qué? / ¿A quién? | *Puer __puellam__ videt.* (El niño ve a la niña) |
    | | **Dirección (CC)** | Hacia dónde se va (con *ad* o *in*). | ¿Adónde? | *__Ad urbem__ eo.* (Voy a la ciudad) |
    | | **Sujeto de Inf.** | En oraciones de Acusativo + Infinitivo. | ¿Quién? | *Dico __te__ bonum esse.* (Digo que tú eres bueno) |
    | **Genitivo** | **Complemento del Nombre (CN)** | Posesión o pertenencia. | ¿De quién? | *Liber __pueri__.* (El libro del niño) |
    | | **Partitivo** | El todo del que se toma una parte. | ¿De qué? | *Pars __militum__.* (Parte de los soldados) |
    | **Dativo** | **Objeto Indirecto (OI)** | Destinatario o beneficiario de la acción. | ¿A quién? / ¿Para quién? | *Do librum __tibi__.* (Te doy el libro a ti) |
    | | **Posesivo** | Con *sum*, indica al poseedor. | ¿De quién? | *Liber est __mihi__.* (Tengo un libro / El libro es para mí) |
    | **Ablativo** | **CC Instrumento** | Con qué se hace la acción. | ¿Con qué? | *__Gladio__ pugnat.* (Lucha con la espada) |
    | | **CC Lugar** | Dónde ocurre (con *in*). | ¿Dónde? | *__In horto__ est.* (Está en el jardín) |
    | | **CC Compañía** | Con quién (con *cum*). | ¿Con quién? | *__Cum amico__ venit.* (Viene con un amigo) |
    | | **Agente** | Quien hace la acción en pasiva (con *a/ab*). | ¿Por quién? | *Amor __a patre__.* (Soy amado por el padre) |
            """)
    
        # 2. Sentence Types
        with st.expander("🏗️ Tipos de Oraciones"):
            st.markdown("### Según la actitud del hablante")
            st.markdown("""
    - **Enunciativas:** Afirman o niegan un hecho. (*Puer currit.*)
    - **Interrogativas:** Hacen una pregunta. (*Quis venit?* - ¿Quién viene?)
        - Partículas: *-ne* (pregunta general), *nonne* (espera 'sí'), *num* (espera 'no').
    - **Imperativas:** Dan una orden. (*Veni huc!* - ¡Ven aquí!)
    - **Exclamativas:** Expresan emoción. (*Quam pulchra est!* - ¡Qué hermosa es!)
    - **Desiderativas:** Expresan un deseo (usualmente subjuntivo). (*Utinam veniat!* - ¡Ojalá venga!)
            """)
            
            st.divider()
            
            st.markdown("### Oraciones Compuestas")
            st.markdown("""
    - **Coordinadas:** Unidas por conjunciones (*et, sed, aut*). Tienen el mismo nivel.
        - *Puer currit __et__ puella saltat.*
    - **Subordinadas:** Dependen de una oración principal.
        - **Sustantivas:** Actúan como sujeto u objeto (ej. Infinitivo, *ut* completivo).
        - **Adjetivas (Relativo):** Actúan como adjetivo (*Puer __qui__ currit...*).
        - **Adverbiales:** Actúan como adverbio (Temporal, Causal, Final, etc.).
            """)
    
        # 3. Special Constructions
        with st.expander("🚀 Construcciones Especiales (¡Claves para traducir!)"):
            st.markdown("### 1. Acusativo + Infinitivo (Oración de Infinitivo)")
            st.info("Muy común con verbos de **lengua** (decir), **entendimiento** (saber, creer) y **sentido** (ver, oír).")
            st.markdown("""
    **Estructura:** Verbo Principal + [ **Sujeto en Acusativo** + **Verbo en Infinitivo** ]
    
    **Cómo traducir:**
    1. Traduce el verbo principal.
    2. Añade un "**que**".
    3. Traduce el Acusativo como **Sujeto**.
    4. Traduce el Infinitivo como un verbo conjugado.
    
    **Ejemplo:**
    > *Video* [ *puerum* *currere* ]
    > - *Video* = Veo
    > - *que*
    > - *puerum* = el niño
    > - *currere* = corre
    > = **Veo que el niño corre.**
            """)
            
            st.divider()
            
            st.markdown("### 2. Doble Acusativo")
            st.info("Algunos verbos piden DOS acusativos: uno de persona y otro de cosa o predicativo.")
            st.markdown("""
    **Verbos que enseñan / piden / ocultan:**
    - *Doceo* (enseñar): *Doceo __pueros__ __grammaticam__.* (Enseño gramática a los niños).
    - *Posco* (pedir): *Posco __te__ __pecuniam__.* (Te pido dinero).
    - *Celo* (ocultar): *Celo __te__ __veritatem__.* (Te oculto la verdad).
    
    **Verbos que nombran / eligen / hacen (Predicativo):**
    - *Appello* (llamar): *Romani __Ciceronem__ __consulem__ creaverunt.* (Los romanos eligieron cónsul a Cicerón).
      - *Ciceronem* = OD
      - *consulem* = Predicativo del OD
            """)
            
            st.divider()
            
            st.markdown("### 3. Ablativo Absoluto")
            st.info("Construcción independiente que indica las circunstancias (tiempo, causa) de la oración principal.")
            st.markdown("""
    **Estructura:** [ **Sustantivo en Ablativo** + **Participio en Ablativo** ]
    
    **Cómo traducir:**
    - Literal: "Habiendo sido..." o "Siendo..."
    - Mejor: "Cuando...", "Como...", "Después de que..."
    
    **Ejemplo:**
    > [ *Urbe* *capta* ], hostes discesserunt.
    > - *Urbe* = ciudad (abl)
    > - *capta* = capturada (part. perf. pasivo abl)
    > - Literal: "La ciudad capturada..."
    > - Traducción: **Una vez capturada la ciudad**, los enemigos se marcharon.
            """)
    
    # ===== TAB 6: TRANSLATION TIPS =====
    with grammar_tabs[5]:
        st.markdown("## 💡 Consejos para el Traductor")
        
        with st.expander("🕵️ El Método Detective (Paso a Paso)", expanded=True):
            st.markdown("""
    Ante una oración latina, no traduzcas palabra por palabra. Sigue este orden lógico:
    
    1.  **🔍 Busca el VERBO:** Es el corazón de la oración.
        - ¿Es singular o plural? (Te dice el número del sujeto).
        - ¿Es activo o pasivo?
        - ¿Es transitivo (busca OD) o copulativo (busca Atributo)?
    
    2.  **👤 Busca el SUJETO (Nominativo):**
        - Debe concordar con el verbo en número.
        - Si no hay Nominativo explícito, el sujeto está en el verbo (él/ella/ello).
    
    3.  **📦 Busca el OBJETO DIRECTO (Acusativo):**
        - Solo si el verbo es transitivo.
        - Responde a "¿Qué?" o "¿A quién?".
    
    4.  **🎁 Busca los COMPLEMENTOS (Resto de casos):**
        - Dativo (¿Para quién?).
        - Ablativo (¿Con qué? ¿Dónde? ¿Cuándo?).
    
    5.  **🧩 Encaja las piezas:**
        - *Puer* (S) *rosam* (OD) *amat* (V).
        - El niño (S) ama (V) la rosa (OD).
            """)
    
        with st.expander("⚠️ Falsos Amigos y Trampas Comunes"):
            st.markdown("""
    - **Constat:** No es "consta", sino "cuesta" (dinero) o "es evidente".
    - **Tandem:** No es una bicicleta, significa "finalmente".
    - **Autem:** No es "auto", significa "sin embargo" o "por otro lado".
    - **Enim:** Significa "pues" o "en efecto" (siempre va en segunda posición).
    - **Cum:** Puede ser preposición ("con" + Abl) o conjunción ("cuando/como" + Subjuntivo). ¡Mira qué le sigue!
    - **Ut:** ¡El camaleón del latín!
        - + Indicativo: "Como" o "Cuando".
        - + Subjuntivo: "Para que" (Final) o "Que" (Completiva/Consecutiva).
            """)
    
        with st.expander("⚔️ Estrategia con Participios"):
            st.markdown("""
    El latín ama los participios. El español prefiere oraciones subordinadas.
    
    **Participio de Presente (*amans*):**
    - Traduce como gerundio ("amando") o relativo ("que ama").
    - *Puer currens* = El niño corriendo / El niño que corre.
    
    **Participio de Perfecto (*amatus*):**
    - Traduce como participio ("amado") o pasiva ("que fue amado").
    - *Urbs capta* = La ciudad capturada / La ciudad que fue capturada.
    
    **Participio de Futuro (*amaturus*):**
    - Traduce como perífrasis ("que va a amar", "dispuesto a amar").
    - *Ave moritura* = Ave que va a morir.
            """)
