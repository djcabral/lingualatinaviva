# Plan de Mejora: Análisis Sintáctico Pedagógico
**Objetivo:** Transformar el módulo de análisis sintáctico de Lingua Latina Viva para que refleje las prácticas tradicionales de enseñanza del latín, similares a las que utilizan los profesores en cursos académicos.

---

## 📚 Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Análisis de Prácticas Pedagógicas Tradicionales](#análisis-de-prácticas-pedagógicas-tradicionales)
3. [Estado Actual vs. Estado Deseado](#estado-actual-vs-estado-deseado)
4. [Componentes a Implementar](#componentes-a-implementar)
5. [Diseño de Base de Datos](#diseño-de-base-de-datos)
6. [Interfaz de Usuario](#interfaz-de-usuario)
7. [Flujo de Anotación Manual](#flujo-de-anotación-manual)
8. [Plan de Implementación](#plan-de-implementación)
9. [Recursos y Referencias](#recursos-y-referencias)

---

## 🎯 Visión General

### Problema Actual
El módulo **Syntaxis** utiliza el análisis automático de LatinCy (POS tagging, dependency parsing), pero carece de las **anotaciones pedagógicas tradicionales** que los profesores de latín emplean para enseñar a leer y comprender textos clásicos.

### Solución Propuesta
Crear un sistema híbrido que combine:
1. **Análisis automático** (LatinCy) como base
2. **Anotaciones manuales** de construcciones sintácticas clásicas
3. **Sistema de explicaciones** en lenguaje natural
4. **Diagramas pedagógicos** tradicionales (Reed-Kellogg, árboles de constituyentes)
5. **Ejercicios interactivos** basados en el análisis

---

## 📖 Análisis de Prácticas Pedagógicas Tradicionales

### ¿Qué hacen los profesores de latín al analizar oraciones?

#### 1. **Identificación de la Estructura Base**
**Ejemplo:** *Puella in horto ambulat.*

Un profesor tradicional identifica:
- **Sujeto:** *puella* (nominativo singular)
- **Predicado verbal:** *ambulat* (3ª persona singular, presente activo)
- **Complemento circunstancial de lugar:** *in horto* (ablativo con preposición)

**Explicación:** "La niña camina en el jardín. El sujeto es 'puella' (quién realiza la acción), el verbo es 'ambulat' (qué hace), y 'in horto' nos dice dónde ocurre la acción."

#### 2. **Análisis de Casos (Función Sintáctica)**
Para cada sustantivo/adjetivo en la oración, se identifica:
- **Caso morfológico:** Nominativo, Genitivo, Dativo, Acusativo, Ablativo, Vocativo
- **Función sintáctica:** Sujeto, CD, CI, Complemento del nombre, etc.
- **Relación con otros elementos:** ¿De qué depende? ¿A qué modifica?

**Ejemplo:** *Magister pueris libros dat.*
- *magister* - Nominativo → **Sujeto**
- *pueris* - Dativo → **Complemento Indirecto** (a quién da)
- *libros* - Acusativo → **Complemento Directo** (qué da)
- *dat* - Verbo → **Núcleo del predicado**

#### 3. **Construcciones Sintácticas Clásicas**
Los profesores identifican y explican construcciones específicas del latín:

##### a) **Ablativo Absoluto**
**Ejemplo:** *Caesare duce, milites fortiter pugnaverunt.*
- "Siendo César el líder" (ablativo absoluto)
- "Los soldados lucharon valientemente"

**Explicación:** Construcción participial independiente que expresa circunstancia (tiempo, causa, concesión). Formada por sustantivo + participio, ambos en ablativo.

##### b) **Acusativo con Infinitivo (ACI)**
**Ejemplo:** *Scio te venire.*
- "Sé que tú vienes"

**Explicación:** El verbo principal (*scio*) rige una oración subordinada con sujeto en acusativo (*te*) e infinitivo (*venire*).

##### c) **Dativo Posesivo**
**Ejemplo:** *Mihi est liber.*
- "Tengo un libro" (literalmente: "A mí hay un libro")

**Explicación:** El dativo expresa posesión con el verbo *sum*.

##### d) **Genitivo Objetivo y Subjetivo**
**Ejemplo:** *Amor patriae* (amor a la patria - objetivo) vs. *Amor matris* (amor de la madre - subjetivo/objetivo ambiguo)

##### e) **Oración de Relativo**
**Ejemplo:** *Puer qui curreret* (el niño que corría)

**Explicación:** Pronombre relativo *qui* en función de sujeto de la subordinada.

##### f) **Subordinadas Circunstanciales**
- **Temporal:** *Cum Caesar venit, omnes fugerunt.* (Cuando César vino...)
- **Causal:** *Quod laborabat, victus est.* (Porque trabajaba...)
- **Final:** *Venit ut videat.* (Viene para ver)
- **Consecutiva:** *Tam fortis erat ut vinceret.* (Era tan fuerte que venció)
- **Condicional:** *Si venis, gaudebo.* (Si vienes, me alegraré)
- **Concesiva:** *Quamquam fessus erat, pugnavit.* (Aunque estaba cansado...)

#### 4. **Concordancias**
Identificación explícita de concordancias:
- **Sujeto-Verbo:** Número y persona
- **Sustantivo-Adjetivo:** Género, número, caso
- **Relativo-Antecedente:** Género y número (caso según función)

**Ejemplo:** *Puella pulchra rosam amat.*
- *puella* (fem., nom. sg.) concuerda con *pulchra* (fem., nom. sg.)
- *puella* (3ª sg.) concuerda con *amat* (3ª sg.)

#### 5. **Orden de Palabras y Énfasis**
El latín tiene orden flexible. Los profesores explican:
- **Orden neutro:** SOV (Sujeto-Objeto-Verbo)
- **Orden enfático:** Elemento enfatizado al principio
- **Hipérbaton:** Separación de palabras relacionadas para efecto estilístico

**Ejemplo:** 
- *Puella rosam amat.* (orden neutro)
- *Rosam puella amat.* (énfasis en "la rosa")

#### 6. **Diagramas Tradicionales**

##### Diagrama Reed-Kellogg
```
     puella | ambulat
            |    \
            |     in horto
```

##### Árbol de Constituyentes
```
           Oración
          /   |    \
        SN    SP    SV
        |     |     |
     puella  in   ambulat
              |
            horto
```

---

## 🔄 Estado Actual vs. Estado Deseado

### Estado Actual ✅
**Módulo Syntaxis proporciona:**
- Tokenización de oraciones
- POS tagging (categorías gramaticales: NOUN, VERB, ADJ, etc.)
- Dependency parsing (relaciones: nsubj, obj, obl, etc.)
- Lematización
- Análisis morfológico (Case, Gender, Number, Tense, etc.)
- Diagrama SVG de dependencias (displaCy)
- Filtros por nivel y fuente

**Visualizaciones:**
1. **Análisis Visual:** Palabras coloreadas por categoría gramatical
2. **Árbol de Dependencias:** Diagrama SVG automático
3. **Detalles Gramaticales:** Tabla con morfología palabra por palabra

### Limitaciones del Estado Actual ⚠️
1. **Sin identificación explícita de funciones sintácticas tradicionales**
   - No aparece "Sujeto", "Complemento Directo", "Complemento Indirecto"
   - Solo etiquetas de dependencias (nsubj, obj, iobj) que no son pedagógicas

2. **Sin reconocimiento de construcciones clásicas**
   - No identifica ablativos absolutos
   - No detecta ACIs
   - No señala subordinadas circunstanciales

3. **Sin explicaciones en lenguaje natural**
   - No hay texto que explique "por qué" algo cumple cierta función
   - No hay guías de lectura

4. **Sin concordancias explícitas**
   - No visualiza relaciones de concordancia sujeto-verbo
   - No marca concordancias sustantivo-adjetivo

5. **Sin parsing tradicional (SN, SV, SP)**
   - No hay estructura de constituyentes
   - No hay análisis por sintagmas

### Estado Deseado 🎯
**El módulo Syntaxis debe:**

1. **Mostrar análisis sintáctico tradicional**
   - Sujeto, Predicado nominal/verbal
   - Complemento Directo, Indirecto, Circunstancial
   - Atributo, Complemento del Nombre
   - Aposiciones

2. **Identificar y anotar construcciones clásicas**
   - Ablativo absoluto (con explicación)
   - ACI (Acusativo con Infinitivo)
   - Dativo posesivo, agente, ético
   - Genitivo objetivo/subjetivo
   - Subordinadas (temporal, final, causal, etc.)

3. **Generar explicaciones pedagógicas**
   - Texto en español explicando cada construcción
   - Guías de traducción paso a paso
   - Notas sobre excepciones y casos especiales

4. **Visualizar concordancias**
   - Resaltar elementos concordantes con colores/flechas
   - Explicar reglas de concordancia activas

5. **Ofrecer múltiples vistas**
   - Vista de dependencias (actual, LatinCy)
   - Vista de constituyentes (SN, SV, SP)
   - Vista de funciones sintácticas tradicionales
   - Diagrama Reed-Kellogg (opcional)

6. **Permitir anotación manual**
   - Herramienta para profesores/editores
   - Corrección de análisis automáticos
   - Adición de construcciones no detectadas

7. **Generar ejercicios automáticos**
   - "Identifica el sujeto de esta oración"
   - "¿Qué función cumple 'pueris' en esta frase?"
   - "Encuentra el ablativo absoluto"

---

## 🔧 Componentes a Implementar

### 1. Sistema de Funciones Sintácticas Tradicionales

#### Tabla de Mapeo: Etiquetas UD → Funciones Tradicionales
```python
DEPENDENCY_TO_FUNCTION = {
    # Universal Dependencies → Función Pedagógica
    "nsubj": "Sujeto",
    "obj": "Complemento Directo",
    "iobj": "Complemento Indirecto",
    "obl": "Complemento Circunstancial",  # Requiere análisis del caso
    "nmod": "Complemento del Nombre",
    "amod": "Adjetivo Modificador",
    "advmod": "Adverbio Modificador",
    "det": "Determinante",
    "case": "Preposición",
    "cc": "Conjunción",
    "conj": "Elemento Coordinado",
    "acl": "Oración Subordinada Adjetiva",
    "advcl": "Oración Subordinada Adverbial",
    "ccomp": "Oración Subordinada Completiva",
    "xcomp": "Complemento Predicativo",
    "aux": "Verbo Auxiliar",
    "cop": "Cópula",
    "mark": "Marca Subordinante",
    "appos": "Aposición",
    "vocative": "Vocativo",
    # ...
}
```

#### Refinamiento Basado en Morfología
Para `"obl"` (Complemento Circunstancial), se debe especificar según el caso:
```python
def refine_obl_function(word_case, preposition=None):
    if preposition:
        return f"Complemento Circunstancial ({preposition})"
    elif word_case == "Abl":
        return "Complemento Circunstancial de Modo/Instrumento/Lugar"
    elif word_case == "Acc":
        return "Complemento Circunstancial de Extensión"
    # ...
```

### 2. Detector de Construcciones Clásicas

#### 2.1 Ablativo Absoluto
**Patrón:**
- Sustantivo/Pronombre en ablativo
- Participio en ablativo
- Concordancia en género, número, caso
- Independencia sintáctica del resto de la oración

**Algoritmo:**
```python
def detect_ablative_absolute(sentence_tokens):
    """
    Detecta ablativos absolutos en la oración.
    
    Returns:
        List[Dict]: [
            {
                "type": "ablative_absolute",
                "tokens": [3, 4],  # Índices de tokens involucrados
                "subject": "Caesare",
                "participle": "duce",
                "translation": "Siendo César el líder",
                "explanation": "Construcción participial independiente..."
            }
        ]
    """
    constructions = []
    
    for i, token in enumerate(sentence_tokens):
        if token.morph.get("Case") == "Abl":
            # Buscar participio concordante en ablativo
            for j in range(i-2, i+3):  # Ventana de búsqueda
                if j < 0 or j >= len(sentence_tokens):
                    continue
                candidate = sentence_tokens[j]
                if (candidate.pos_ == "VERB" and
                    "Part" in candidate.morph.get("VerbForm", "") and
                    candidate.morph.get("Case") == "Abl" and
                    is_concordant(token, candidate)):
                    
                    # Verificar independencia sintáctica
                    if not depends_on_main_verb(token, sentence_tokens):
                        constructions.append({
                            "type": "ablative_absolute",
                            "tokens": [i, j],
                            "subject": token.text,
                            "participle": candidate.text,
                            # ...
                        })
    
    return constructions
```

#### 2.2 Acusativo con Infinitivo (ACI)
**Patrón:**
- Verbo de lengua, pensamiento o percepción (dico, puto, video, etc.)
- Sustantivo/pronombre en acusativo (sujeto de la subordinada)
- Infinitivo (verbo de la subordinada)

**Ejemplo:** *Scio **(te venire)** = Sé que tú vienes

```python
def detect_aci(sentence_tokens):
    """Detecta construcciones de Acusativo con Infinitivo."""
    ACI_VERBS = ["dico", "scio", "puto", "video", "audio", "sentio", "credo", ...]
    
    constructions = []
    
    for i, token in enumerate(sentence_tokens):
        if token.lemma_ in ACI_VERBS:
            # Buscar acusativo + infinitivo como complementos
            accusative = None
            infinitive = None
            
            for child in token.children:
                if child.morph.get("Case") == "Acc" and child.dep_ == "nsubj":
                    accusative = child
                if "Inf" in child.morph.get("VerbForm", ""):
                    infinitive = child
            
            if accusative and infinitive:
                constructions.append({
                    "type": "accusativus_cum_infinitivo",
                    "main_verb": token.text,
                    "subject_acc": accusative.text,
                    "infinitive": infinitive.text,
                    # ...
                })
    
    return constructions
```

#### 2.3 Subordinadas Circunstanciales
**Marcadores de subordinación:**
- **Temporal:** *cum*, *dum*, *postquam*, *antequam*, *ubi*
- **Causal:** *quod*, *quia*, *quoniam*, *cum* (con subjuntivo)
- **Final:** *ut*, *ne*, *quo*
- **Consecutiva:** *ut* (con indicativo después de *tam*, *ita*, *tantus*)
- **Condicional:** *si*, *nisi*, *ni*
- **Concesiva:** *quamquam*, *etsi*, *cum* (con subjuntivo)

```python
SUBORDINATE_MARKERS = {
    "cum": "temporal|causal|concesiva",  # Requiere análisis del modo
    "ut": "final|consecutiva",
    "quod": "causal|completiva",
    "si": "condicional",
    # ...
}

def detect_subordinate_clauses(sentence_tokens):
    """Detecta oraciones subordinadas circunstanciales."""
    constructions = []
    
    for i, token in enumerate(sentence_tokens):
        if token.lemma_ in SUBORDINATE_MARKERS:
            # Identificar el tipo según el contexto
            clause_type = determine_clause_type(token, sentence_tokens)
            
            # Encontrar el verbo de la subordinada
            subordinate_verb = find_subordinate_verb(token)
            
            constructions.append({
                "type": f"subordinate_{clause_type}",
                "marker": token.text,
                "verb": subordinate_verb.text,
                # ...
            })
    
    return constructions
```

### 3. Generador de Explicaciones

#### Sistema de Plantillas
```python
EXPLANATIONS = {
    "ablative_absolute": """
    **Ablativo Absoluto**
    
    Esta construcción consta de un sustantivo ({subject}) y un participio ({participle}), 
    ambos en caso ablativo. Es independiente sintácticamente del resto de la oración y 
    expresa una circunstancia de {circumstance} (tiempo, causa, condición, concesión).
    
    **Traducción:** {translation}
    
    **Nota:** El ablativo absoluto es una construcción muy común en latín clásico y tiene 
    equivalentes en español como el gerundio o una oración subordinada.
    """,
    
    "accusativus_cum_infinitivo": """
    **Acusativo con Infinitivo (ACI)**
    
    El verbo principal '{main_verb}' (verbo de {verb_type}) rige una oración subordinada 
    con sujeto en acusativo ('{subject_acc}') e infinitivo ('{infinitive}').
    
    **Traducción:** {translation}
    
    **Estructura:** {main_verb} + [que] + {subject_translation} + {infinitive_translation}
    """,
    
    # ...
}
```

### 4. Detector de Concordancias

```python
def find_concordances(sentence_tokens):
    """
    Identifica concordancias sujeto-verbo y sustantivo-adjetivo.
    
    Returns:
        List[Dict]: [
            {
                "type": "subject_verb",
                "tokens": [0, 4],
                "feature": "Number",
                "value": "Sing"
            },
            {
                "type": "noun_adjective",
                "tokens": [1, 2],
                "features": ["Gender", "Number", "Case"],
                "values": ["Fem", "Sing", "Nom"]
            }
        ]
    """
    concordances = []
    
    # Concordancia sujeto-verbo
    for token in sentence_tokens:
        if token.dep_ == "nsubj":
            verb = token.head
            if (token.morph.get("Number") == verb.morph.get("Number") and
                token.morph.get("Person") == verb.morph.get("Person")):
                
                concordances.append({
                    "type": "subject_verb",
                    "tokens": [token.i, verb.i],
                    "feature": "Number+Person",
                    "value": f"{token.morph.get('Number')}, {token.morph.get('Person')}"
                })
    
    # Concordancia sustantivo-adjetivo
    for token in sentence_tokens:
        if token.pos_ == "ADJ":
            noun = token.head
            if noun.pos_ in ["NOUN", "PROPN"]:
                concordances.append({
                    "type": "noun_adjective",
                    "tokens": [noun.i, token.i],
                    "features": ["Gender", "Number", "Case"],
                    "values": [
                        noun.morph.get("Gender"),
                        noun.morph.get("Number"),
                        noun.morph.get("Case")
                    ]
                })
    
    return concordances
```

---

## 🗄️ Diseño de Base de Datos

### Nuevas Tablas/Campos

#### 1. Extensión de `SentenceAnalysis`
```python
class SentenceAnalysis(SQLModel, table=True):
    # ... campos existentes ...
    
    # NUEVOS CAMPOS:
    
    # Funciones sintácticas tradicionales (JSON)
    # {"0": "Sujeto", "1": "Adjetivo", "4": "Complemento Directo", ...}
    traditional_functions: Optional[str] = None
    
    # Construcciones clásicas detectadas (JSON detallado)
    # [
    #   {
    #     "type": "ablative_absolute",
    #     "tokens": [5, 6],
    #     "explanation": "...",
    #     "translation": "..."
    #   }
    # ]
    classical_constructions: Optional[str] = None
    
    # Concordancias identificadas (JSON)
    concordances: Optional[str] = None
    
    # Explicación pedagógica general (texto largo)
    pedagogical_explanation: Optional[str] = None
    
    # Guía de traducción paso a paso
    translation_guide: Optional[str] = None
    
    # Diagrama Reed-Kellogg (SVG o texto ASCII)
    reed_kellogg_diagram: Optional[str] = None
    
    # Nivel de anotación manual (0-100%)
    manual_annotation_level: int = 0  # 0 = totalmente automático, 100 = totalmente manual
    
    # Anotador (para control de calidad)
    annotated_by: Optional[str] = None
    annotated_at: Optional[datetime] = None
```

#### 2. Nueva Tabla: `ConstructionPattern`
Para almacenar patrones de construcciones sintácticas:

```python
class ConstructionPattern(SQLModel, table=True):
    """
    Catálogo de construcciones sintácticas clásicas con sus patrones.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    name: str                          # "ablative_absolute", "aci", etc.
    display_name_es: str               # "Ablativo Absoluto"
    display_name_la: str               # "Ablativus Absolutus"
    
    complexity_level: int = 1          # 1-10
    
    description_es: str                # Explicación detallada en español
    pattern_definition: str (JSON)     # Definición del patrón para detección
    
    example_latin: str                 # Ejemplo canónico
    example_translation: str           # Traducción del ejemplo
    example_explanation: str           # Explicación del ejemplo
    
    pedagogical_notes: Optional[str]   # Notas para profesores
    common_errors: Optional[str]       # Errores comunes de estudiantes
    
    references: Optional[str]          # Referencias bibliográficas
```

#### 3. Nueva Tabla: `SyntacticExercise`
Para ejercicios generados automáticamente:

```python
class SyntacticExercise(SQLModel, table=True):
    """
    Ejercicios interactivos basados en análisis sintáctico.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    sentence_id: int = Field(foreign_key="sentenceanalysis.id")
    
    exercise_type: str                 # "identify_subject", "find_construction", etc.
    question: str                      # "¿Cuál es el sujeto de esta oración?"
    correct_answer: str (JSON)         # ["puella"] o {"token_indices": [0]}
    explanation: str                   # Por qué esa es la respuesta correcta
    
    difficulty: int = 1                # 1-5
    hints: Optional[str] (JSON)        # Pistas opcionales
    
    # Estadísticas
    times_attempted: int = 0
    times_correct: int = 0
    success_rate: float = 0.0
```

---

## 🎨 Interfaz de Usuario

### Mejoras en el Módulo Syntaxis

#### Vista 1: **Análisis Tradicional** (NUEVA)
```
┌─────────────────────────────────────────────────┐
│  Oración: Puella in horto ambulat.              │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Puella]        → Sujeto (Nom. Sg. Fem.)      │
│   └─ núcleo del sintagma nominal               │
│                                                 │
│  [in horto]      → Compl. Circunstancial Lugar │
│   ├─ in: preposición                           │
│   └─ horto: ablativo sg. masc.                 │
│                                                 │
│  [ambulat]       → Predicado Verbal             │
│   └─ 3ª persona sg., presente activo           │
│                                                 │
│  Concordancias:                                 │
│    • puella (3ª sg.) ↔ ambulat (3ª sg.)        │
│                                                 │
│  Traducción: "La niña camina en el jardín."    │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Vista 2: **Construcciones Clásicas** (NUEVA)
```
┌──────────────────────────────────────────────────┐
│  Oración: Caesare duce, milites fortiter         │
│           pugnaverunt.                           │
├──────────────────────────────────────────────────┤
│                                                  │
│  🔍 Construcciones Detectadas:                   │
│                                                  │
│  1. ABLATIVO ABSOLUTO ⭐                         │
│     └─ "Caesare duce"                           │
│     └─ Traducción: "Siendo César el líder"      │
│     └─ Función: Circunstancia temporal/causal   │
│                                                  │
│     Explicación:                                 │
│     El ablativo absoluto es una construcción    │
│     participial independiente del resto de la   │
│     oración. Consta de un sustantivo (Caesare)  │
│     y un participio (duce), ambos en ablativo.  │
│                                                  │
│     [Ver más detalles] [Ejercicios sobre esto]  │
│                                                  │
└──────────────────────────────────────────────────┘
```

#### Vista 3: **Guía de Traducción** (NUEVA)
```
┌──────────────────────────────────────────────────┐
│  📖 Guía de Traducción Paso a Paso              │
├──────────────────────────────────────────────────┤
│                                                  │
│  Paso 1: Identifica el verbo principal          │
│  ──────────────────────────────────────────      │
│  → "pugnaverunt" (lucharon)                     │
│                                                  │
│  Paso 2: Encuentra el sujeto                     │
│  ──────────────────────────────────────────      │
│  → "milites" (los soldados)                     │
│                                                  │
│  Paso 3: Analiza las construcciones especiales   │
│  ──────────────────────────────────────────      │
│  → "Caesare duce" = ablativo absoluto           │
│     "Siendo César el líder" o "Con César        │
│     como líder"                                 │
│                                                  │
│  Paso 4: Identifica modificadores                │
│  ──────────────────────────────────────────      │
│  → "fortiter" (adverbio) modifica "pugnaverunt" │
│     "valientemente"                             │
│                                                  │
│  Paso 5: Construye la traducción                 │
│  ──────────────────────────────────────────      │
│  "Con César como líder, los soldados             │
│   lucharon valientemente."                      │
│                                                  │
└──────────────────────────────────────────────────┘
```

#### Vista 4: **Ejercicios Interactivos** (NUEVA)
```
┌──────────────────────────────────────────────────┐
│  ✏️ Practica con esta oración                    │
├──────────────────────────────────────────────────┤
│                                                  │
│  Oración: Puella rosam amat.                    │
│                                                  │
│  Pregunta 1 de 3:                                │
│  ¿Cuál es el sujeto de esta oración?            │
│                                                  │
│  [ ] rosam                                       │
│  [✓] puella                                      │
│  [ ] amat                                        │
│                                                  │
│  [Verificar Respuesta]                           │
│                                                  │
│  💡 Pista: El sujeto está en caso nominativo.   │
│                                                  │
└──────────────────────────────────────────────────┘
```

#### Vista Actualizada: **Detalles Gramaticales** (MEJORADA)
Tabla ampliada con nueva columna "Función Sintáctica":

| Palabra | Lema | Categoría | Morfología | Función Sintáctica | Dependencia UD |
|---------|------|-----------|------------|-------------------|----------------|
| Puella | puella | Sustantivo | Nom.Sg.Fem. | **Sujeto** | nsubj |
| rosam | rosa | Sustantivo | Acc.Sg.Fem. | **Complemento Directo** | obj |
| amat | amo | Verbo | 3Sg.Pres.Act. | **Predicado Verbal** | ROOT |

### Nueva Página: **Herramienta de Anotación Manual**

Para profesores/editores que quieran corregir o enriquecer análisis automáticos:

```
┌──────────────────────────────────────────────────────────────┐
│  ⚙️ Anotación Manual - Editor de Sintaxis                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Oración ID: 42                                              │
│  Texto: Caesare duce, milites fortiter pugnaverunt.         │
│                                                              │
│  ┌─────────────────────────────────────────┐                │
│  │  Análisis Automático (LatinCy):         │                │
│  │  [Ver análisis...]                      │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
│  Funciones Sintácticas:                                      │
│  ┌───────┬─────────┬───────────────────────┐                │
│  │ Tokén │ Palabra │ Función               │                │
│  ├───────┼─────────┼───────────────────────┤                │
│  │   0   │ Caesare │ [Abl. Abs. - Sujeto]▼ │                │
│  │   1   │ duce    │ [Abl. Abs. - Partic.]▼│                │
│  │   2   │ milites │ [Sujeto]▼             │                │
│  ...                                                         │
│  └───────┴─────────┴───────────────────────┘                │
│                                                              │
│  Construcciones Clásicas:                                    │
│  [+ Añadir Construcción]                                     │
│                                                              │
│  1. Ablativo Absoluto                                        │
│     Tokens: 0, 1 (Caesare duce)                             │
│     [Editar] [Eliminar]                                      │
│                                                              │
│  Explicación Pedagógica:                                     │
│  ┌─────────────────────────────────────────┐                │
│  │ [Área de texto para escribir            │                │
│  │  explicación en lenguaje natural...]    │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
│  [💾 Guardar Anotaciones]  [🔄 Restaurar Automático]        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Anotación Manual

### Proceso Propuesto

1. **Importación de Textos**
   - Se importa un texto latino desde archivo `.txt`
   - Se segmenta en oraciones

2. **Análisis Automático Inicial**
   - LatinCy procesa todas las oraciones
   - Se genera el análisis base (POS, dependencies, morph)
   - Se ejecutan detectores de construcciones

3. **Revisión Manual (Opcional)**
   - Profesor/editor revisa el análisis automático
   - Corrige errores de LatinCy
   - Añade construcciones no detectadas
   - Escribe explicaciones pedagógicas
   - Marca la oración como "verificada"

4. **Publicación para Estudiantes**
   - Oraciones verificadas aparecen en el módulo Syntaxis
   - Los estudiantes pueden explorar el análisis completo
   - Los ejercicios se generan automáticamente

### Niveles de Calidad

- **Nivel 0 (Automático):** Solo análisis de LatinCy, sin revisión
- **Nivel 1 (Semi-revisado):** Funciones sintácticas corregidas manualmente
- **Nivel 2 (Revisado):** + Construcciones verificadas
- **Nivel 3 (Completo):** + Explicaciones pedagógicas escritas
- **Nivel 4 (Premium):** + Ejercicios personalizados, diagrams Reed-Kellogg

---

## 📅 Plan de Implementación

### Fase 1: Fundamentos (Semana 1-2)
**Objetivo:** Establecer la base de datos y detección básica.

- [ ] Extender modelo `SentenceAnalysis` con nuevos campos
- [ ] Crear tabla `ConstructionPattern`
- [ ] Crear tabla `SyntacticExercise`
- [ ] Ejecutar migración de base de datos
- [ ] Implementar mapeo `DEPENDENCY_TO_FUNCTION`
- [ ] Actualizar vista "Detalles Gramaticales" con columna "Función Sintáctica"

**Entregables:**
- Base de datos actualizada
- Funciones sintácticas tradicionales visibles en UI

### Fase 2: Detectores de Construcciones (Semana 2-3)
**Objetivo:** Implementar detectores automáticos de construcciones clásicas.

- [ ] Implementar detector de **Ablativo Absoluto**
- [ ] Implementar detector de **ACI** (Acusativo con Infinitivo)
- [ ] Implementar detector de **Dativo Posesivo**
- [ ] Implementar detector de **Subordinadas Circunstanciales**
- [ ] Implementar detector de **Concordancias**
- [ ] Crear sistema de plantillas de explicaciones
- [ ] Poblar tabla `ConstructionPattern` con patrones comunes

**Entregables:**
- Módulo `utils/syntax_detectors.py` con todos los detectores
- Vista "Construcciones Clásicas" funcional

### Fase 3: Interfaz de Usuario (Semana 3-4)
**Objetivo:** Crear vistas pedagógicas en el módulo Syntaxis.

- [ ] Añadir pestaña **"Análisis Tradicional"** en Syntaxis
- [ ] Añadir pestaña **"Construcciones Clásicas"** en Syntaxis
- [ ] Añadir pestaña **"Guía de Traducción"** en Syntaxis
- [ ] Mejorar visualización de concordancias (colores/flechas)
- [ ] Implementar filtro por tipo de construcción

**Entregables:**
- UI completa con 5 pestañas (Análisis Visual, Árbol, Tradicional, Construcciones, Guía)
- Navegación intuitiva

### Fase 4: Generador de Explicaciones (Semana 4-5)
**Objetivo:** Sistema de explicaciones en lenguaje natural.

- [ ] Diseñar plantillas de explicaciones para cada construcción
- [ ] Implementar generador de explicaciones con variables dinámicas
- [ ] Crear generador de "Guía de Traducción Paso a Paso"
- [ ] Integrar explicaciones en la UI

**Entregables:**
- Sistema de explicaciones funcionando
- Guías de traducción generadas automáticamente

### Fase 5: Herramienta de Anotación Manual (Semana 5-6)
**Objetivo:** Permitir revisión y corrección manual.

- [ ] Crear página `10_✏️_Anotador.py`
- [ ] Implementar editor de funciones sintácticas
- [ ] Implementar editor de construcciones
- [ ] Implementar área de explicación pedagógica
- [ ] Sistema de control de calidad (nivel de anotación)
- [ ] Registro de anotador y fecha

**Entregables:**
- Herramienta de anotación completa
- Workflow de revisión manual establecido

### Fase 6: Ejercicios Interactivos (Semana 6-7)
**Objetivo:** Generar ejercicios automáticos basados en análisis.

- [ ] Implementar generador de ejercicios "Identifica el sujeto"
- [ ] Implementar generador "Encuentra el complemento directo"
- [ ] Implementar generador "Identifica la construcción"
- [ ] Implementar verificador de respuestas
- [ ] Integrar ejercicios en pestaña nueva "Practica"
- [ ] Sistema de puntuación y estadísticas

**Entregables:**
- 5+ tipos de ejercicios funcionando
- Integración con sistema de XP/gamificación

### Fase 7: Testing y Refinamiento (Semana 7-8)
**Objetivo:** Validar con corpus real y ajustar.

- [ ] Procesar 100+ oraciones de *Familia Romana*
- [ ] Revisar y corregir detección automática
- [ ] Ajustar umbrales de detección
- [ ] Validar con profesores de latín (feedback externo)
- [ ] Documentar casos límite y excepciones

**Entregables:**
- Sistema validado con corpus real
- Documentación de precisión y limitaciones

### Fase 8: Funcionalidades Avanzadas (Semana 8+)
**Objetivo:** Características premium opcionales.

- [ ] Implementar diagramas Reed-Kellogg (generación automática)
- [ ] Análisis por constituyentes (SN, SV, SP)
- [ ] Exportación de análisis (PDF, imagen)
- [ ] Comparación lado a lado (latín | traducción | análisis)
- [ ] Modo de estudio guiado (lectura asistida)

**Entregables:**
- Herramientas avanzadas opcionales
- Sistema completo de análisis sintáctico pedagógico

---

## 📚 Recursos y Referencias

### Bibliografía Recomendada

1. **Allen, J. H., & Greenough, J. B.** (1903). *Allen and Greenough's New Latin Grammar*. Ginn & Company.
   - Gramática de referencia clásica

2. **Woodcock, E. C.** (1959). *A New Latin Syntax*. Bristol Classical Press.
   - Análisis detallado de construcciones sintácticas

3. **Gildersleeve, B. L., & Lodge, G.** (1895). *Gildersleeve's Latin Grammar*. Macmillan.
   - Gramática tradicional con énfasis en sintaxis

4. **Ørberg, H. H.** (1955). *Lingua Latina per se Illustrata: Pars I - Familia Romana*.
   - Método inductivo, contexto pedagógico moderno

### Herramientas de Referencia

- **LatinCy:** https://github.com/diyclassics/LatinCy
- **Perseus Digital Library:** http://www.perseus.tufts.edu/
- **Didacterion:** https://www.didacterion.com/ (diccionario con morfología)
- **Whitaker's Words:** http://archives.nd.edu/words.html

### Anotadores Existentes (Inspiración)

- **Proiel Treebank:** Corpus anotado de textos latinos con dependencias
- **ITTB (Index Thomisticus Treebank):** Latín medieval anotado
- **Perseus Ancient Greek and Latin Dependency Treebanks**

---

## 🎯 Criterios de Éxito

### Métricas de Calidad

1. **Precisión de Detección Automática:**
   - Funciones sintácticas: ≥85% precisión vs. anotación manual
   - Ablativo absoluto: ≥90% recall
   - ACI: ≥85% recall
   - Subordinadas: ≥80% precisión

2. **Usabilidad:**
   - Profesores pueden anotar una oración en <5 minutos
   - Estudiantes entienden explicaciones (validar con usuarios reales)
   - Navegación intuitiva (test con usuarios)

3. **Coverage:**
   - Al menos 500 oraciones anotadas de *Familia Romana*
   - Cobertura de 15+ tipos de construcciones clásicas
   - Ejercicios disponibles para el 80% de oraciones anotadas

4. **Rendimiento:**
   - Análisis automático de una oración: <2 segundos
   - Carga de página Syntaxis: <3 segundos
   - Respuesta de ejercicio interactivo: <0.5 segundos

---

## 📝 Notas Finales

### Limitaciones Esperadas

1. **LatinCy no es perfecto:**
   - Puede cometer errores en POS tagging (especialmente con palabras raras)
   - Dependency parsing tiene ~85-90% de precisión en el mejor caso
   - Requiere revisión manual para calidad óptima

2. **Construcciones complejas:**
   - Hipérbaton extremo puede confundir detectores automáticos
   - Elipsis (palabras omitidas) no se detecta bien
   - Figuras retóricas (quiasmo, anáfora) están fuera del alcance

3. **Subjetividad pedagógica:**
   - Diferentes profesores pueden analizar la misma oración de formas ligeramente distintas
   - El sistema debe ser flexible y permitir múltiples interpretaciones válidas

### Próximos Pasos Inmediatos

1. Revisar y aprobar este plan con el usuario
2. Comenzar Fase 1: Actualizar base de datos
3. Implementar mapeo básico de funciones sintácticas
4. Mostrar resultados iniciales en la UI

---

**Documento creado:** 23 de noviembre de 2025  
**Autor:** Equipo de desarrollo Lingua Latina Viva  
**Estado:** Borrador para revisión
