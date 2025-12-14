
import json
import os

# Define the grammar content structure
grammar_data = {
    "title": "Gramática Rápida",
    "description": "Consulta rápida de gramática latina. Encuentra tablas de declinaciones, conjugaciones y más.",
    "tabs": [
        {
            "id": "declensions",
            "label": "Declinaciones",
            "icon": "🏛️",
            "sections": [
                {
                    "title": "Primera Declinación (-a, -ae) - Femenino",
                    "content": """**Ejemplo:** *puella, puellae* (f) - niña

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nominativo** | puell**a** | puell**ae** |
| **Vocativo** | puell**a** | puell**ae** |
| **Acusativo** | puell**am** | puell**ās** |
| **Genitivo** | puell**ae** | puell**ārum** |
| **Dativo** | puell**ae** | puell**īs** |
| **Ablativo** | puell**ā** | puell**īs** |

💡 Típicamente femenino. Terminación característica: **-a** (nom. sg.)"""
                },
                {
                    "title": "Segunda Declinación (-us, -i / -um, -i)",
                    "content": """**Masculino:** *dominus, dominī* (m) - señor

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | domin**us** | domin**ī** |
| **Voc.** | domin**e** | domin**ī** |
| **Acc.** | domin**um** | domin**ōs** |
| **Gen.** | domin**ī** | domin**ōrum** |
| **Dat.** | domin**ō** | domin**īs** |
| **Abl.** | domin**ō** | domin**īs** |

**Neutro:** *templum, templī* (n) - templo

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | templ**um** | templ**a** |
| **Voc.** | templ**um** | templ**a** |
| **Acc.** | templ**um** | templ**a** |
| **Gen.** | templ**ī** | templ**ōrum** |
| **Dat.** | templ**ō** | templ**īs** |
| **Abl.** | templ**ō** | templ**īs** |

💡 Neutros: Nom. = Acc. = Voc. (en ambos números). Plural siempre en **-a**"""
                },
                {
                    "title": "Tercera Declinación (variada)",
                    "content": """ℹ️ La 3ª declinación tiene dos subtipos según el número de sílabas en nominativo vs genitivo

### Imparisílabos (Genitivo tiene MÁS sílabas)
Ejemplo: *rēx* (1 sílaba) → *rēg-is* (2 sílabas)

**Masculino/Femenino:** *rēx, rēgis* (m) - rey

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **rēx** | rēg**ēs** |
| **Voc.** | **rēx** | rēg**ēs** |
| **Acc.** | rēg**em** | rēg**ēs** |
| **Gen.** | rēg**is** | rēg**um** |
| **Dat.** | rēg**ī** | rēg**ibus** |
| **Abl.** | rēg**e** | rēg**ibus** |

**Neutro:** *nōmen, nōminis* (n) - nombre

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **nōmen** | nōmin**a** |
| **Voc.** | **nōmen** | nōmin**a** |
| **Acc.** | **nōmen** | nōmin**a** |
| **Gen.** | nōmin**is** | nōmin**um** |
| **Dat.** | nōmin**ī** | nōmin**ibus** |
| **Abl.** | nōmin**e** | nōmin**ibus** |

---

### Parisílabos (Genitivo tiene IGUAL sílabas)
Ejemplo: *cīv-is* (2 sílabas) → *cīv-is* (2 sílabas)

**Masculino/Femenino:** *cīvis, cīvis* (c) - ciudadano

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **cīvis** | cīv**ēs** |
| **Voc.** | **cīvis** | cīv**ēs** |
| **Acc.** | cīv**em** | cīv**ēs** |
| **Gen.** | cīv**is** | cīv**ium** |
| **Dat.** | cīv**ī** | cīv**ibus** |
| **Abl.** | cīv**ī** | cīv**ibus** |

**Neutro:** *mare, maris* (n) - mar

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | **mare** | mar**ia** |
| **Voc.** | **mare** | mar**ia** |
| **Acc.** | **mare** | mar**ia** |
| **Gen.** | mar**is** | mar**ium** |
| **Dat.** | mar**ī** | mar**ibus** |
| **Abl.** | mar**ī** | mar**ibus** |

⚠️ **Diferencias clave:**
- **Gen. Pl.:** Imparisílabo = `-um` | Parisílabo = `-ium`
- **Abl. Sg.:** Imparisílabo = `-e` | Parisílabo = `-ī` (M/F puede variar)
- **Nom/Acc Pl. Neutro:** Imparisílabo = `-a` | Parisílabo = `-ia`

💡 Genitivo singular en **-is**. Gran variedad de nominativos."""
                },
                {
                    "title": "Cuarta Declinación (-us, -ūs)",
                    "content": """**Masculino:** *frūctus, frūctūs* (m) - fruto

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | frūct**us** | frūct**ūs** |
| **Voc.** | frūct**us** | frūct**ūs** |
| **Acc.** | frūct**um** | frūct**ūs** |
| **Gen.** | frūct**ūs** | frūct**uum** |
| **Dat.** | frūct**uī** | frūct**ibus** |
| **Abl.** | frūct**ū** | frūct**ibus** |

**Neutro:** *cornū, cornūs* (n) - cuerno

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | corn**ū** | corn**ua** |
| **Voc.** | corn**ū** | corn**ua** |
| **Acc.** | corn**ū** | corn**ua** |
| **Gen.** | corn**ūs** | corn**uum** |
| **Dat.** | corn**ū** | corn**ibus** |
| **Abl.** | corn**ū** | corn**ibus** |

💡 Típicamente masculino. Muy pocos neutros. Genitivo sg.: **-ūs**"""
                },
                {
                    "title": "Quinta Declinación (-ēs, -ēī)",
                    "content": """**Femenino:** *rēs, reī* (f) - cosa

| Caso | Singular | Plural |
|:----:|:--------:|:------:|
| **Nom.** | r**ēs** | r**ēs** |
| **Voc.** | r**ēs** | r**ēs** |
| **Acc.** | r**em** | r**ēs** |
| **Gen.** | r**eī** | r**ērum** |
| **Dat.** | r**eī** | r**ēbus** |
| **Abl.** | r**ē** | r**ēbus** |

💡 Casi todos femeninos. Pocos sustantivos. Importante: *rēs* (cosa), *diēs* (día), *fidēs* (fe), *spēs* (esperanza)"""
                },
                {
                    "title": "Excepciones y Casos Especiales",
                    "content": """### Sustantivos Irregulares Comunes

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
- *domus* (f) - casa (4ª decl. femenino)"""
                }
            ]
        },
        {
            "id": "conjugations",
            "label": "Conjugaciones",
            "icon": "⚔️",
            "sections": [
                {
                    "title": "Sistema de Presente (Presente, Imperfecto, Futuro)",
                    "content": """### Presente de Indicativo Activo

**1ª Conjugación:** *amō, amāre* - amar
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | am**ō** | am**āmus** |
| **2ª** | am**ās** | am**ātis** |
| **3ª** | am**at** | am**ant** |

**2ª Conjugación:** *moneō, monēre* - advertir
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | mone**ō** | mon**ēmus** |
| **2ª** | mon**ēs** | mon**ētis** |
| **3ª** | mon**et** | mon**ent** |

**3ª Conjugación:** *regō, regere* - regir
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | reg**ō** | reg**imus** |
| **2ª** | reg**is** | reg**itis** |
| **3ª** | reg**it** | reg**unt** |

**4ª Conjugación:** *audiō, audīre* - oír
| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | audi**ō** | aud**īmus** |
| **2ª** | aud**īs** | aud**ītis** |
| **3ª** | aud**it** | aud**iunt** |

---

### Imperfecto de Indicativo Activo
💡 Formación: raíz + **-ba-** (1ª/2ª) o **-ēba-** (3ª/4ª) + desinencias

| Persona | 1ª (amō) | 2ª (moneō) | 3ª (regō) | 4ª (audiō) |
|:-------:|:--------:|:----------:|:---------:|:----------:|
| **1ª sg** | amā**bam** | monē**bam** | reg**ēbam** | audi**ēbam** |
| **2ª sg** | amā**bās** | monē**bās** | reg**ēbās** | audi**ēbās** |
| **3ª sg** | amā**bat** | monē**bat** | reg**ēbat** | audi**ēbat** |
| **1ª pl** | amā**bāmus** | monē**bāmus** | reg**ēbāmus** | audi**ēbāmus** |
| **2ª pl** | amā**bātis** | monē**bātis** | reg**ēbātis** | audi**ēbātis** |
| **3ª pl** | amā**bant** | monē**bant** | reg**ēbant** | audi**ēbant** |"""
                },
                {
                    "title": "Sistema de Perfecto",
                    "content": """### Perfecto de Indicativo Activo
💡 Formación: **raíz de perfecto** + desinencias (-ī, -istī, -it, -imus, -istis, -ērunt)

**Ejemplo:** *amāvī* (he amado)

| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | amāv**ī** | amāv**imus** |
| **2ª** | amāv**istī** | amāv**istis** |
| **3ª** | amāv**it** | amāv**ērunt** |

---

### Pluscuamperfecto de Indicativo Activo
💡 Formación: raíz de perfecto + **-eram**

| Persona | Singular | Plural |
|:-------:|:--------:|:------:|
| **1ª** | amāv**eram** | amāv**erāmus** |
| **2ª** | amāv**erās** | amāv**erātis** |
| **3ª** | amāv**erat** | amāv**erant** |

---

### Futuro de Indicativo Activo
💡 1ª/2ª conjugación: raíz + **-b-**; 3ª/4ª: raíz + **-ē-** (excepto 1ª sg.)

| Persona | 1ª (amō) | 2ª (moneō) | 3ª (regō) | 4ª (audiō) |
|:-------:|:--------:|:----------:|:---------:|:----------:|
| **1ª sg** | amā**bō** | monē**bō** | reg**am** | audi**am** |
| **2ª sg** | amā**bis** | monē**bis** | reg**ēs** | audi**ēs** |
| **3ª sg** | amā**bit** | monē**bit** | reg**et** | audi**et** |
| **1ª pl** | amā**bimus** | monē**bimus** | reg**ēmus** | audi**ēmus** |
| **2ª pl** | amā**bitis** | monē**bitis** | reg**ētis** | audi**ētis** |
| **3ª pl** | amā**bunt** | monē**bunt** | reg**ent** | audi**ent** |"""
                },
                {
                    "title": "Verbos Irregulares Importantes",
                    "content": """### sum, esse, fuī (ser/estar)

| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | sum | es | est | sumus | estis | sunt |
| **Imperfecto** | eram | erās | erat | erāmus | erātis | erant |
| **Futuro** | erō | eris | erit | erimus | eritis | erunt |
| **Perfecto** | fuī | fuistī | fuit | fuimus | fuistis | fuērunt |

---

### possum, posse, potuī (poder)
💡 Formación: pot + sum (pot-sum → possum)

| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | possum | potes | potest | possumus | potestis | possunt |
| **Imperfecto** | poteram | poterās | poterat | poterāmus | poterātis | poterant |
| **Futuro** | poterō | poteris | poterit | poterimus | poteritis | poterunt |

---

### eō, īre, iī/īvī, itum (ir)
| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | eō | īs | it | īmus | ītis | eunt |
| **Imperfecto** | ībam | ībās | ībat | ībāmus | ībātis | ībant |
| **Futuro** | ībō | ībis | ībit | ībimus | ībitis | ībunt |

---

### ferō, ferre, tulī, lātum (llevar)
| Tiempo | 1ª sg | 2ª sg | 3ª sg | 1ª pl | 2ª pl | 3ª pl |
|:-------|:------|:------|:------|:------|:------|:------|
| **Presente** | ferō | fers | fert | ferimus | fertis | ferunt |
| **Imperfecto** | ferēbam | ferēbās | ferēbat | ferēbāmus | ferēbātis | ferēbant |

---

**volō / nōlō / mālō**

*volō* (querer)
| Presente |
|:---------|
| volō |
| vīs |
| vult |
| volumus |
| vultis |
| volunt |

*nōlō* (no querer)
| Presente |
|:---------|
| nōlō |
| nōn vīs |
| nōn vult |
| nōlumus |
| nōn vultis |
| nōlunt |

*mālō* (preferir)
| Presente |
|:---------|
| mālō |
| māvīs |
| māvult |
| mālumus |
| māvultis |
| mālunt |"""
                },
                {
                    "title": "Verboides (Formas Nominales del Verbo)",
                    "content": """### Infinitivos

| Conjugación | Presente Activo | Perfecto Activo | Presente Pasivo |
|:-----------:|:----------------|:----------------|:----------------|
| **1ª** | amā**re** | amāv**isse** | amā**rī** |
| **2ª** | monē**re** | monu**isse** | monē**rī** |
| **3ª** | reg**ere** | rēx**isse** | reg**ī** |
| **4ª** | aud**īre** | audīv**isse** | aud**īrī** |

---

### Participios

**Participio Presente Activo:**
- Se forma: raíz + **-ns / -nt-** + terminación
- Ejemplo: *amāns, amantis* (amante, que ama)

**Participio Perfecto Pasivo (PPP):**
- 4ª parte principal
- Ejemplo: *amātus, -a, -um* (amado/a)

**Participio Future Activo:**
- PPP + **-ūrus, -a, -um**
- Ejemplo: *amātūrus, -a, -um* (que va a amar)

---

### Gerundio
**Formación:** raíz + **-nd-** + terminaciones de 2ª declinación neutro

| Caso | Forma | Ejemplo (amō) |
|:-----|:------|:--------------|
| **Gen.** | -**ndī** | amandī (de amar) |
| **Dat.** | -**ndō** | amandō (para amar) |
| **Acc.** | -(ad) **ndum** | (ad) amandum (para amar) |
| **Abl.** | -**ndō** | amandō (por/con amar) |

---

### Gerundivo
**Formación:** raíz + **-ndus, -a, -um** (adjetivo verbal de obligación)

- Ejemplo: *amandus, -a, -um* (que debe ser amado)
- Uso: construcción pasiva de obligación con *sum*
- *Carthāgō dēlenda est* = Cartago debe ser destruida

---

### Supino
**Formación:** PPP sin terminación + **-um** (acusativo) o **-ū** (ablativo)

| Forma | Uso | Ejemplo |
|:------|:----|:--------|
| **Ac. (-um)** | Expresa finalidad con verbos de movimiento | Vēnī **vīsum** (Vine a ver) |
| **Abl. (-ū)** | "En cuanto a..." | Facile **dictū** (Fácil de decir) |"""
                },
                {
                    "title": "Adverbios Más Usados",
                    "content": """### Adverbios de Lugar
- **hīc** - aquí
- **illīc** - allí
- **ibī** - allí
- **ubī** - donde
- **quō** - adonde
- **unde** - de donde
- **longē** - lejos
- **prope** - cerca

### Adverbios de Tiempo
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

### Adverbios de Modo
- **bene** - bien
- **male** - mal
- **multum** - mucho
- **parum** - poco
- **sīc** - así
- **ita** - así
- **maximē** - muchísimo
- **minimē** - nada, en absoluto

### Otros Adverbios Comunes
- **etiam** - también, incluso
- **quoque** - también
- **nōn** - no
- **fortasse** - quizás
- **valdē** - mucho, muy
- **tantum** - solamente
- **circum** - alrededor
- **prope** - casi"""
                }
            ]
        },
        {
            "id": "pronouns",
            "label": "Pronombres",
            "icon": "👤",
            "sections": [
                 {
                    "title": "Pronombres Personales",
                    "content": """**1ª Persona:** ego (yo) / nōs (nosotros)

| Caso | Singular (yo) | Plural (nosotros) |
|:----:|:-------------:|:-----------------:|
| **Nom.** | **ego** | **nōs** |
| **Gen.** | **meī** | **nostrī / nostrum** |
| **Dat.** | **mihi** | **nōbīs** |
| **Acc.** | **mē** | **nōs** |
| **Abl.** | **mē** | **nōbīs** |

**2ª Persona:** tū (tú) / vōs (vosotros)

| Caso | Singular (tú) | Plural (vosotros) |
|:----:|:-------------:|:-----------------:|
| **Nom.** | **tū** | **vōs** |
| **Gen.** | **tuī** | **vestrī / vestrum** |
| **Dat.** | **tibi** | **vōbīs** |
| **Acc.** | **tē** | **vōs** |
| **Abl.** | **tē** | **vōbīs** |"""
                 },
                 {
                    "title": "Pronombre Reflexivo (3ª Persona)",
                    "content": """**sē** (se, a sí mismo/a/os/as)
💡 No tiene Nominativo. Es igual para singular y plural.

| Caso | Forma | Traducción |
|:----:|:-----:|:-----------|
| **Gen.** | **suī** | de sí mismo/a/os/as |
| **Dat.** | **sibi** | para sí mismo... |
| **Acc.** | **sē / sēsē** | a sí mismo... |
| **Abl.** | **sē / sēsē** | con/por sí mismo... |"""
                 },
                 {
                     "title": "Pronombres Demostrativos",
                     "content": """### hic, haec, hoc (este, esta, esto)

| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | hic | haec | hoc | hī | hae | haec |
| **Gen.** | huius | huius | huius | hōrum | hārum | hōrum |
| **Dat.** | huic | huic | huic | hīs | hīs | hīs |
| **Acc.** | hunc | hanc | hoc | hōs | hās | haec |
| **Abl.** | hōc | hāc | hōc | hīs | hīs | hīs |

---

### ille, illa, illud (aquel, aquella, aquello)

| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | ille | illa | illud | illī | illae | illa |
| **Gen.** | illīus | illīus | illīus | illōrum | illārum | illōrum |
| **Dat.** | illī | illī | illī | illīs | illīs | illīs |
| **Acc.** | illum | illam | illud | illōs | illās | illa |
| **Abl.** | illō | illā | illō | illīs | illīs | illīs |

---

### iste, ista, istud (ese, esa, eso)
💡 Se declina igual que *ille*.

| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | iste | ista | istud | istī | istae | ista |
| **Gen.** | istīus | istīus | istīus | istōrum | istārum | istōrum |
| **Dat.** | istī | istī | istī | istīs | istīs | istīs |
| **Acc.** | istum | istam | istud | istōs | istās | ista |
| **Abl.** | istō | istā | istō | istīs | istīs | istīs |

---

### is, ea, id (él, ella, ello / este, ese)
💡 Usado como pronombre personal de 3ª persona o demostrativo débil.

| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | is | ea | id | eī / iī | eae | ea |
| **Gen.** | eius | eius | eius | eōrum | eārum | eōrum |
| **Dat.** | eī | eī | eī | eīs / iīs | eīs / iīs | eīs / iīs |
| **Acc.** | eum | eam | id | eōs | eās | ea |
| **Abl.** | eō | eā | eō | eīs / iīs | eīs / iīs | eīs / iīs |"""
                 },
                 {
                     "title": "Pronombre Relativo",
                     "content": """### quī, quae, quod (que, el cual, quien)

| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | quī | quae | quod | quī | quae | quae |
| **Gen.** | cuius | cuius | cuius | quōrum | quārum | quōrum |
| **Dat.** | cui | cui | cui | quibus | quibus | quibus |
| **Acc.** | quem | quam | quod | quōs | quās | quae |
| **Abl.** | quō | quā | quō | quibus | quibus | quibus |"""
                 },
                 {
                     "title": "Pronombre Interrogativo",
                     "content": """### quis, quid (¿quién?, ¿qué?)
💡 En plural es igual que el relativo (*quī, quae, quae*).

| Caso | Masc./Fem. Sg | Neutro Sg |
|:----:|:-------------:|:---------:|
| **Nom.** | **quis** | **quid** |
| **Gen.** | cuius | cuius |
| **Dat.** | cui | cui |
| **Acc.** | quem | **quid** |
| **Abl.** | quō | quō |"""
                 }
            ]
        },
        {
            "id": "adjectives",
            "label": "Adjetivos",
            "icon": "✨",
            "sections": [
                {
                    "title": "Adjetivos 1ª/2ª Declinación",
                    "content": """**bonus, bona, bonum** (bueno, buena)
💡 Se declina como sustantivos: -us (2ª masc), -a (1ª fem), -um (2ª neut)

| Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |
|:----:|:--------:|:-------:|:--------:|:--------:|:-------:|:--------:|
| **Nom.** | bon**us** | bon**a** | bon**um** | bon**ī** | bon**ae** | bon**a** |
| **Gen.** | bon**ī** | bon**ae** | bon**ī** | bon**ōrum** | bon**ārum** | bon**ōrum** |
| **Dat.** | bon**ō** | bon**ae** | bon**ō** | bon**īs** | bon**īs** | bon**īs** |
| **Acc.** | bon**um** | bon**am** | bon**um** | bon**ōs** | bon**ās** | bon**a** |
| **Abl.** | bon**ō** | bon**ā** | bon**ō** | bon**īs** | bon**īs** | bon**īs** |"""
                },
                {
                    "title": "Adjetivos de 2ª Clase (3ª Declinación)",
                    "content": """Siguen la 3ª declinación de temas en -i (Parisílabos). Abl. sg. en **-ī**, Gen. pl. en **-ium**, Nom/Ac pl. neutro en **-ia**.

### 1. Tres Terminaciones (-er, -is, -e)
**acer, acris, acre** (agudo, enérgico)
Masc: *acer*, Fem: *acris*, Neut: *acre*. (Solo cambia en el Nominativo singular).

### 2. Dos Terminaciones (-is, -e)
**fortis, forte** (fuerte, valiente)
Masc/Fem: *fortis*, Neut: *forte*. (La mayoría son de este tipo).

| Caso | Masc./Fem. Sg | Neutro Sg | Masc./Fem. Pl | Neutro Pl |
|:----:|:-------------:|:---------:|:-------------:|:---------:|
| **Nom.** | fort**is** | fort**e** | fort**ēs** | fort**ia** |
| **Gen.** | fort**is** | fort**is** | fort**ium** | fort**ium** |
| **Dat.** | fort**ī** | fort**ī** | fort**ibus** | fort**ibus** |
| **Acc.** | fort**em** | fort**e** | fort**ēs** | fort**ia** |
| **Abl.** | fort**ī** | fort**ī** | fort**ibus** | fort**ibus** |

### 3. Una Terminación
**fēlīx, fēlīcis** (feliz)
Masc/Fem/Neut: *fēlīx* en el nominativo. Se distinguen en los demás casos.

| Caso | Masc./Fem. Sg | Neutro Sg | Masc./Fem. Pl | Neutro Pl |
|:----:|:-------------:|:---------:|:-------------:|:---------:|
| **Nom.** | fēlīx | fēlīx | fēlīc**ēs** | fēlīc**ia** |
| **Gen.** | fēlīc**is** | fēlīc**is** | fēlīc**ium** | fēlīc**ium** |
| **Acc.** | fēlīc**em** | fēlīx | fēlīc**ēs** | fēlīc**ia** |
| **Abl.** | fēlīc**ī** | fēlīc**ī** | fēlīc**ibus** | fēlīc**ibus** |"""
                },
                {
                    "title": "Grados del Adjetivo (Comparativo y Superlativo)",
                    "content": """### 1. Comparativo de Superioridad
Se forma añadiendo **-ior** (M/F) y **-ius** (N) a la raíz.
**Ejemplo:** *altus* (alto) → *altior, altius* (más alto)
⚠️ Se declina como la 3ª declinación CONSONÁNTICA (Imparisílabo). Abl. sg. en **-e**, Gen. pl. en **-um**.

| Caso | Masc./Fem. Sg | Neutro Sg | Masc./Fem. Pl | Neutro Pl |
|:----:|:-------------:|:---------:|:-------------:|:---------:|
| **Nom.** | altior | altius | altiōr**ēs** | altiōr**a** |
| **Gen.** | altiōr**is** | altiōr**is** | altiōr**um** | altiōr**um** |
| **Acc.** | altiōr**em** | altius | altiōr**ēs** | altiōr**a** |
| **Abl.** | altiōr**e** | altiōr**e** | altiōr**ibus** | altiōr**ibus** |

---

### 2. Superlativo
Se forma generalmente añadiendo **-issimus, -a, -um** a la raíz.
**Ejemplo:** *altus* → *altissimus, -a, -um* (altísimo / el más alto)
💡 Se declina como un adjetivo de 1ª/2ª declinación (*bonus, -a, -um*).

**Excepciones:**
- Adjetivos en **-er**: añaden *-rimus* (*pucher* → *pulcherrimus*)
- Adjetivos en **-lis**: añaden *-limus* (*facilis* → *facillimus*)

---

### 3. Comparación Irregular

| Positivo | Comparativo | Superlativo | Significado |
|:---------|:------------|:------------|:------------|
| **bonus** | melior, -ius | optimus | bueno, mejor, óptimo |
| **malus** | peior, -ius | pessimus | malo, peor, pésimo |
| **magnus** | maior, -ius | maximus | grande, mayor, máximo |
| **parvus** | minor, minus | minimus | pequeño, menor, mínimo |
| **multus** | plūs | plūrimus | mucho, más, muchísimo |"""
                }
            ]
        },
        {
            "id": "syntax",
            "label": "Sintaxis",
            "icon": "📝",
            "sections": [
                {
                    "title": "Los Complementos y los Casos",
                    "content": """### Guía Rápida de Funciones

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
| | **Agente** | Quien hace la acción en pasiva (con *a/ab*). | ¿Por quién? | *Amor __a patre__.* (Soy amado por el padre) |"""
                },
                {
                    "title": "Tipos de Oraciones",
                    "content": """### Según la actitud del hablante
- **Enunciativas:** Afirman o niegan un hecho. (*Puer currit.*)
- **Interrogativas:** Hacen una pregunta. (*Quis venit?* - ¿Quién viene?)
    - Partículas: *-ne* (pregunta general), *nonne* (espera 'sí'), *num* (espera 'no').
- **Imperativas:** Dan una orden. (*Veni huc!* - ¡Ven aquí!)
- **Exclamativas:** Expresan emoción. (*Quam pulchra est!* - ¡Qué hermosa es!)
- **Desiderativas:** Expresan un deseo (usualmente subjuntivo). (*Utinam veniat!* - ¡Ojalá venga!)

---

### Oraciones Compuestas
- **Coordinadas:** Unidas por conjunciones (*et, sed, aut*). Tienen el mismo nivel.
    - *Puer currit __et__ puella saltat.*
- **Subordinadas:** Dependen de una oración principal.
    - **Sustantivas:** Actúan como sujeto u objeto (ej. Infinitivo, *ut* completivo).
    - **Adjetivas (Relativo):** Actúan como adjetivo (*Puer __qui__ currit...*).
    - **Adverbiales:** Actúan como adverbio (Temporal, Causal, Final, etc.)."""
                },
                {
                    "title": "Construcciones Especiales",
                    "content": """### 1. Acusativo + Infinitivo (Oración de Infinitivo)
💡 Muy común con verbos de **lengua** (decir), **entendimiento** (saber, creer) y **sentido** (ver, oír).

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

---

### 2. Doble Acusativo
💡 Algunos verbos piden DOS acusativos: uno de persona y otro de cosa o predicativo.

**Verbos que enseñan / piden / ocultan:**
- *Doceo* (enseñar): *Doceo __pueros__ __grammaticam__.* (Enseño gramática a los niños).
- *Posco* (pedir): *Posco __te__ __pecuniam__.* (Te pido dinero).
- *Celo* (ocultar): *Celo __te__ __veritatem__.* (Te oculto la verdad).

**Verbos que nombran / eligen / hacen (Predicativo):**
- *Appello* (llamar): *Romani __Ciceronem__ __consulem__ creaverunt.* (Los romanos eligieron cónsul a Cicerón).
  - *Ciceronem* = OD
  - *consulem* = Predicativo del OD

---

### 3. Ablativo Absoluto
💡 Construcción independiente que indica las circunstancias (tiempo, causa) de la oración principal.

**Estructura:** [ **Sustantivo en Ablativo** + **Participio en Ablativo** ]

**Cómo traducir:**
- Literal: "Habiendo sido..." o "Siendo..."
- Mejor: "Cuando...", "Como...", "Después de que..."

**Ejemplo:**
> [ *Urbe* *capta* ], hostes discesserunt.
> - *Urbe* = ciudad (abl)
> - *capta* = capturada (part. perf. pasivo abl)
> - Literal: "La ciudad capturada..."
> - Traducción: **Una vez capturada la ciudad**, los enemigos se marcharon."""
                }
            ]
        },
        {
            "id": "spanish",
            "label": "Gramática Española",
            "icon": "🇪🇸",
            "sections": [
                 {
                    "title": "Morfología (Tipos de Palabras)",
                    "content": """![Clasificación de las palabras en español](/assets/images/spanish_morphology.png)

**Puntos clave:**
- **Sustantivo:** Nombra entidades (personas, cosas, ideas).
- **Verbo:** Indica acción o estado. Es el núcleo de la oración.
- **Adjetivo:** Modifica al sustantivo (califica o determina).
- **Adverbio:** Modifica al verbo, adjetivo u otro adverbio."""
                 },
                 {
                    "title": "Elementos de Enlace (Nexos y Preposiciones)",
                    "content": """### Nexos (Conectores)
![Principales conectores](/assets/images/spanish_connectors.png)

### Preposiciones
![Lista de preposiciones](/assets/images/spanish_prepositions.png)

### Subordinantes
![Palabras que introducen subordinación](/assets/images/spanish_subordinators.png)"""
                 },
                 {
                    "title": "La Oración (Simple y Compuesta)",
                    "content": """### Oración Simple
![Estructura de la oración simple](/assets/images/spanish_simple_sentences.png)

---

### Oración Compuesta
![Coordinación vs Subordinación](/assets/images/spanish_compound_sentences.png)"""
                 },
                 {
                    "title": "Oraciones Subordinadas",
                    "content": """### Vista General
![Resumen de oraciones subordinadas en español](/assets/images/spanish_subordinadas_resumen.png)

---

### 1. Sustantivas (Noun Clauses)
💡 Funcionan como un **Sustantivo** dentro de la oración (Sujeto, OD, Atributo, etc.)

![Completivas sustantivas: tipos y ejemplos](/assets/images/spanish_completivas_sustantivas.png)
![Funcionan como un Sustantivo (Sujeto u OD)](/assets/images/spanish_noun_clauses.png)

---

### 2. Adjetivas (Adjective Clauses)
💡 Funcionan como un **Adjetivo**, modificando a un sustantivo anterior (antecedente). Introducidas por 'que', 'quien', 'el cual', 'cuyo', 'donde', 'cuando'.

![Subordinadas adjetivas: especificativas vs explicativas](/assets/images/spanish_adjetivas.png)

---

### 3. Adverbiales (Adverbial Clauses)
💡 Funcionan como un **Adverbio** (indican tiempo, lugar, modo, causa, finalidad, condición, concesión, consecuencia...).

![Los 8 tipos de subordinadas adverbiales](/assets/images/spanish_adverbiales.png)"""
                 }
            ]
        },
        {
            "id": "tips",
            "label": "Consejos",
            "icon": "💡",
            "sections": [
                {
                    "title": "El Método Detective (Paso a Paso)",
                    "content": """Ante una oración latina, no traduzcas palabra por palabra. Sigue este orden lógico:

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
    - El niño (S) ama (V) la rosa (OD)."""
                },
                {
                    "title": "Falsos Amigos y Trampas Comunes",
                    "content": """- **Constat:** No es "consta", sino "cuesta" (dinero) o "es evidente".
- **Tandem:** No es una bicicleta, significa "finalmente".
- **Autem:** No es "auto", significa "sin embargo" o "por otro lado".
- **Enim:** Significa "pues" o "en efecto" (siempre va en segunda posición).
- **Cum:** Puede ser preposición ("con" + Abl) o conjunción ("cuando/como" + Subjuntivo). ¡Mira qué le sigue!
- **Ut:** ¡El camaleón del latín!
    - + Indicativo: "Como" o "Cuando".
    - + Subjuntivo: "Para que" (Final) o "Que" (Completiva/Consecutiva)."""
                },
                {
                    "title": "Estrategia con Participios",
                    "content": """El latín ama los participios. El español prefiere oraciones subordinadas.

**Participio de Presente (*amans*):**
- Traduce como gerundio ("amando") o relativo ("que ama").
- *Puer currens* = El niño corriendo / El niño que corre.

**Participio de Perfecto (*amatus*):**
- Traduce como participio ("amado") o pasiva ("que fue amado").
- *Urbs capta* = La ciudad capturada / La ciudad que fue capturada.

**Participio de Futuro (*amaturus*):**
- Traduce como perífrasis ("que va a amar", "dispuesto a amar").
- *Ave moritura* = Ave que va a morir."""
                }
            ]
        }
    ]
}

# Ensure directory exists
output_dir = "/home/diego/Projects/latin-python/portability/grammar"
os.makedirs(output_dir, exist_ok=True)

# Write to JSON
output_file = os.path.join(output_dir, "grammar.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(grammar_data, f, ensure_ascii=False, indent=2)

print(f"Grammar extracted to {output_file}")
