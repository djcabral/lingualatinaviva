# TAREA: Análisis Sintáctico de Oraciones Latinas

Eres un experto en gramática latina clásica. Tu tarea es analizar las siguientes oraciones latinas y asignar funciones sintácticas a cada palabra.

## FORMATO DE ENTRADA
Recibirás oraciones en este formato JSON:
```json
{
  "id": 1,
  "latin": "Puella rosam videt.",
  "spanish": "La niña ve la rosa.",
  "tokens": [
    {"idx": 0, "word": "Puella", "lemma": "puella", "pos": "NOUN", "morph": "Case=Nom|Gender=Fem|Number=Sing", "dep": "nsubj", "head": 2, "current_role": "sujeto"},
    ...
  ]
}
```

## ROLES SINTÁCTICOS DISPONIBLES
Usa EXACTAMENTE estas etiquetas (en español, con guiones bajos):

### Sujeto y Predicado
- `sujeto` - Nominativo que realiza la acción
- `sujeto_paciente` - Sujeto de voz pasiva
- `predicado` - Verbo principal (ROOT)
- `cópula` - Verbo copulativo (sum, esse)
- `auxiliar` - Verbo auxiliar

### Objetos
- `objeto_directo` - Acusativo, ¿qué?
- `objeto_indirecto` - Dativo, ¿a quién?
- `complemento_predicativo` - Predicativo del sujeto u objeto

### Complementos
- `complemento_circunstancial` - Ablativo/oblicuo: cómo, cuándo, dónde, con qué
- `complemento_del_nombre` - Genitivo que modifica sustantivo

### Modificadores
- `modificador_adjetival` - Adjetivo que modifica sustantivo
- `modificador_adverbial` - Adverbio que modifica verbo

### Oraciones Subordinadas
- `oración_completiva` - Subordinada sustantiva
- `oración_de_relativo` - Con pronombre relativo
- `oración_adverbial` - Subordinada circunstancial

### Conjunciones y Conectores
- `conjunción_coordinante` - et, aut, sed
- `conjunción_subordinante` - ut, cum, si
- `elemento_coordinado` - Elemento unido por conjunción

### Otros
- `preposición` - Introduce complementos
- `determinante` - Determina al sustantivo
- `aposición` - Explicación de otro sustantivo
- `vocativo` - Llamada o invocación
- `puntuación` - Signos de puntuación

## FORMATO DE RESPUESTA
Para CADA oración, devuelve un JSON con tu análisis corregido:

```json
{
  "id": 1,
  "corrections": [
    {"idx": 0, "current_role": "sujeto", "correct_role": "sujeto", "is_correct": true},
    {"idx": 1, "current_role": "objeto_directo", "correct_role": "objeto_directo", "is_correct": true},
    {"idx": 2, "current_role": "predicado", "correct_role": "predicado", "is_correct": true},
    {"idx": 3, "current_role": "puntuación", "correct_role": "puntuación", "is_correct": true}
  ],
  "notes": "Análisis correcto. Oración simple SVO."
}
```

## CRITERIOS DE EVALUACIÓN
1. **Sujeto**: Nominativo que concuerda con el verbo en persona y número
2. **Objeto Directo**: Acusativo que recibe la acción directa
3. **Objeto Indirecto**: Dativo, beneficiario de la acción
4. **Complemento Circunstancial**: Ablativos y sintagmas preposicionales
5. **Predicado**: El verbo principal en forma finita (ROOT)
6. **Cópula**: Específicamente formas de "sum, esse"

## INSTRUCCIONES ADICIONALES
- Si el análisis actual es correcto, marca `is_correct: true`
- Si hay error, indica el rol correcto en `correct_role`
- Presta especial atención a:
  - Distinción entre sujeto activo y pasivo
  - Diferencia entre cópula (sum) y auxiliar
  - Identificación de subordinadas (completivas, relativas, adverbiales)
  - Ablativos absolutos
  - Acusativo + Infinitivo

---

# ORACIONES A ANALIZAR

[
  {
    "id": 441,
    "latin": "Et dimitte nobis debita nostra.",
    "spanish": "Y perdónanos nuestras deudas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 1,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 1,
        "word": "dimitte",
        "lemma": "dimitto",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "nobis",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Plur|Person=1",
        "dep": "obl:arg",
        "head": 1,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 3,
        "word": "debita",
        "lemma": "debeo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "nostra",
        "lemma": "noster",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "det",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 442,
    "latin": "Sicut et nos dimittimus debitoribus nostris.",
    "spanish": "Así como nosotros perdonamos a nuestros deudores.",
    "tokens": [
      {
        "idx": 0,
        "word": "Sicut",
        "lemma": "sicut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "et",
        "lemma": "et",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:emph",
        "head": 2,
        "current_role": "modificador"
      },
      {
        "idx": 2,
        "word": "nos",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Plur|Person=1",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "dimittimus",
        "lemma": "dimitto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "debitoribus",
        "lemma": "debitor",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 5,
        "word": "nostris",
        "lemma": "noster",
        "pos": "DET",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 4,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 6,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 443,
    "latin": "Et ne nos inducas in tentationem.",
    "spanish": "Y no nos dejes caer en la tentación.",
    "tokens": [
      {
        "idx": 0,
        "word": "Et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 3,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 1,
        "word": "ne",
        "lemma": "ne",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "nos",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Plur|Person=1",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "inducas",
        "lemma": "induco",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 5,
        "current_role": "preposición"
      },
      {
        "idx": 5,
        "word": "tentationem",
        "lemma": "tentatio",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 6,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 444,
    "latin": "Sed libera nos a malo.",
    "spanish": "Mas líbranos del mal.",
    "tokens": [
      {
        "idx": 0,
        "word": "Sed",
        "lemma": "sed",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 1,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 1,
        "word": "libera",
        "lemma": "liber",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "nos",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Plur|Person=1",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 4,
        "current_role": "preposición"
      },
      {
        "idx": 4,
        "word": "malo",
        "lemma": "malum",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl:arg",
        "head": 1,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 445,
    "latin": "Gloria Patri et Filio et Spiritui Sancto.",
    "spanish": "Gloria al Padre y al Hijo y al Espíritu Santo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Gloria",
        "lemma": "gloria",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "Patri",
        "lemma": "pater",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 3,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 3,
        "word": "Filio",
        "lemma": "filius",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 1,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 4,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 5,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 5,
        "word": "Spiritui",
        "lemma": "spiritus",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 1,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 6,
        "word": "Sancto",
        "lemma": "sanctus",
        "pos": "ADJ",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 5,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 7,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 446,
    "latin": "Hypotheses non fingo.",
    "spanish": "No invento hipótesis.",
    "tokens": [
      {
        "idx": 0,
        "word": "Hypotheses",
        "lemma": "hypothesis",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "vocative",
        "head": 2,
        "current_role": "vocativo"
      },
      {
        "idx": 1,
        "word": "non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 2,
        "current_role": "modificador"
      },
      {
        "idx": 2,
        "word": "fingo",
        "lemma": "fingo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 447,
    "latin": "Eppur si muove.",
    "spanish": "Y sin embargo se mueve.",
    "tokens": [
      {
        "idx": 0,
        "word": "Eppur",
        "lemma": "eppurs",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "si",
        "lemma": "si",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "muove",
        "lemma": "muoveo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 0,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 448,
    "latin": "Natura abhorret a vacuo.",
    "spanish": "La naturaleza aborrece el vacío.",
    "tokens": [
      {
        "idx": 0,
        "word": "Natura",
        "lemma": "natura",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "abhorret",
        "lemma": "abhorreo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "vacuo",
        "lemma": "uacuus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 1,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 449,
    "latin": "Homo homini lupus.",
    "spanish": "El hombre es un lobo para el hombre.",
    "tokens": [
      {
        "idx": 0,
        "word": "Homo",
        "lemma": "homo",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "homini",
        "lemma": "homo",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "lupus",
        "lemma": "lupus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 450,
    "latin": "Scientia potentia est.",
    "spanish": "El conocimiento es poder.",
    "tokens": [
      {
        "idx": 0,
        "word": "Scientia",
        "lemma": "scientia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "potentia",
        "lemma": "potentia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 451,
    "latin": "Tabula rasa.",
    "spanish": "Tabla rasa (hoja en blanco).",
    "tokens": [
      {
        "idx": 0,
        "word": "Tabula",
        "lemma": "tabula",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "rasa",
        "lemma": "rado",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 452,
    "latin": "Lex parsimoniae.",
    "spanish": "Ley de la parsimonia (Navaja de Ockham).",
    "tokens": [
      {
        "idx": 0,
        "word": "Lex",
        "lemma": "lex",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "parsimoniae",
        "lemma": "parsimonia",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 453,
    "latin": "Systema Naturae.",
    "spanish": "Sistema de la Naturaleza.",
    "tokens": [
      {
        "idx": 0,
        "word": "Systema",
        "lemma": "systema",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "Naturae",
        "lemma": "Natura",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 454,
    "latin": "Philosophiae Naturalis Principia Mathematica.",
    "spanish": "Principios Matemáticos de la Filosofía Natural.",
    "tokens": [
      {
        "idx": 0,
        "word": "Philosophiae",
        "lemma": "philosophia",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 2,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 1,
        "word": "Naturalis",
        "lemma": "naturalis",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "Principia",
        "lemma": "principium",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "Mathematica",
        "lemma": "mathematica",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 455,
    "latin": "Quousque tandem abutere, Catilina, patientia nostra?",
    "spanish": "¿Hasta cuándo abusarás, Catilina, de nuestra paciencia?",
    "tokens": [
      {
        "idx": 0,
        "word": "Quousque",
        "lemma": "quousque",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 1,
        "word": "tandem",
        "lemma": "tandem",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 2,
        "word": "abutere",
        "lemma": "abutor",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "Catilina",
        "lemma": "Catilina",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 2,
        "current_role": "vocativo"
      },
      {
        "idx": 5,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 6,
        "current_role": "puntuación"
      },
      {
        "idx": 6,
        "word": "patientia",
        "lemma": "patientia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 7,
        "word": "nostra",
        "lemma": "noster",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 6,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 8,
        "word": "?",
        "lemma": "?",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 456,
    "latin": "Lucius Catilina, nobili genere natus, fuit magna vi animi.",
    "spanish": "Lucio Catilina, nacido de noble linaje, fue de gran fuerza de espíritu.",
    "tokens": [
      {
        "idx": 0,
        "word": "Lucius",
        "lemma": "Lucius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 9,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Catilina",
        "lemma": "Catilina",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "flat:name",
        "head": 0,
        "current_role": "nombre_compuesto"
      },
      {
        "idx": 2,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "nobili",
        "lemma": "nobilis",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "amod",
        "head": 4,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "genere",
        "lemma": "genus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 5,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 5,
        "word": "natus",
        "lemma": "nascor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "acl",
        "head": 0,
        "current_role": "oración_adjetiva"
      },
      {
        "idx": 6,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
      },
      {
        "idx": 7,
        "word": "fuit",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 9,
        "current_role": "cópula"
      },
      {
        "idx": 8,
        "word": "magna",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 9,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 9,
        "word": "vi",
        "lemma": "uis",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 9,
        "current_role": "predicado"
      },
      {
        "idx": 10,
        "word": "animi",
        "lemma": "animus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 9,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 11,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 9,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 457,
    "latin": "Arma virumque cano, Troiae qui primus ab oris venit.",
    "spanish": "Canto a las armas y al hombre que vino primero desde las costas de Troya.",
    "tokens": [
      {
        "idx": 0,
        "word": "Arma",
        "lemma": "arma",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "virum",
        "lemma": "uir",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 2,
        "word": "que",
        "lemma": "que",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 1,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 3,
        "word": "cano",
        "lemma": "cano",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "Troiae",
        "lemma": "Troia",
        "pos": "PROPN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 6,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 10,
        "current_role": "sujeto"
      },
      {
        "idx": 7,
        "word": "primus",
        "lemma": "primus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "advcl:pred",
        "head": 10,
        "current_role": "otro"
      },
      {
        "idx": 8,
        "word": "ab",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 9,
        "current_role": "preposición"
      },
      {
        "idx": 9,
        "word": "oris",
        "lemma": "ora",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Plur",
        "dep": "nmod",
        "head": 7,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 10,
        "word": "venit",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "acl:relcl",
        "head": 5,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 11,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 458,
    "latin": "Carpe diem, quam minimum credula postero.",
    "spanish": "Aprovecha el día, confiando lo menos posible en el mañana.",
    "tokens": [
      {
        "idx": 0,
        "word": "Carpe",
        "lemma": "Carpus",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "diem",
        "lemma": "dies",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "quam",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "advmod",
        "head": 4,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 4,
        "word": "minimum",
        "lemma": "minimus",
        "pos": "ADV",
        "morph": "",
        "dep": "amod",
        "head": 5,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 5,
        "word": "credula",
        "lemma": "credulus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 6,
        "word": "postero",
        "lemma": "posterus",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 7,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 459,
    "latin": "Dies irae, dies illa, solvet saeclum in favilla.",
    "spanish": "Día de ira, aquel día, disolverá el mundo en cenizas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dies",
        "lemma": "dies",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 6,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "irae",
        "lemma": "ira",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "dies",
        "lemma": "dies",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 4,
        "word": "illa",
        "lemma": "ille",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 3,
        "current_role": "determinante"
      },
      {
        "idx": 5,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 6,
        "current_role": "puntuación"
      },
      {
        "idx": 6,
        "word": "solvet",
        "lemma": "soluo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 6,
        "current_role": "predicado"
      },
      {
        "idx": 7,
        "word": "saeclum",
        "lemma": "saeclum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 6,
        "current_role": "objeto_directo"
      },
      {
        "idx": 8,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 9,
        "current_role": "preposición"
      },
      {
        "idx": 9,
        "word": "favilla",
        "lemma": "fauilla",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 6,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 10,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 6,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 460,
    "latin": "Rōma in Italiā est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Roma",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "Italia",
        "lemma": "Italia",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 461,
    "latin": "Italia in Eurōpā est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Italia",
        "lemma": "Italia",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "Europa",
        "lemma": "Europa",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 462,
    "latin": "Rōma magna urbs est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Roma",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "magna",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "urbs",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 463,
    "latin": "Incolae Rōmae Rōmānī sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Incolae",
        "lemma": "incola",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Romae",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Loc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "Romani",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 464,
    "latin": "Rōmānī Latīnē loquuntur.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romani",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Latine",
        "lemma": "latine",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 2,
        "word": "loquuntur",
        "lemma": "loquor",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 465,
    "latin": "Iūlius pater est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Iulius",
        "lemma": "Iulius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "pater",
        "lemma": "pater",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "appos",
        "head": 0,
        "current_role": "aposición"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 466,
    "latin": "Aemilia māter est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Aemilia",
        "lemma": "Aemilia",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "mater",
        "lemma": "mater",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 467,
    "latin": "Mārcus et Quīntus fīliī sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Marcus",
        "lemma": "Marcus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 2,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 2,
        "word": "Quintus",
        "lemma": "Quintus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": "filii",
        "lemma": "filius",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 468,
    "latin": "Iūlia fīlia est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Iulia",
        "lemma": "iulius",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "filia",
        "lemma": "filia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 469,
    "latin": "Familia Iūliī magna est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Familia",
        "lemma": "familia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Iulii",
        "lemma": "Iulius",
        "pos": "PROPN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "magna",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 470,
    "latin": "Iūlius fīliōs et fīliam amat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Iulius",
        "lemma": "Iulius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "filios",
        "lemma": "filius",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 3,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 3,
        "word": "filiam",
        "lemma": "filia",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 1,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 4,
        "word": "amat",
        "lemma": "amo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 471,
    "latin": "Discipulī in scholā sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Discipuli",
        "lemma": "discipulus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "schola",
        "lemma": "schola",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 472,
    "latin": "Magister discipulōs docet.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Magister",
        "lemma": "Magister",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "discipulos",
        "lemma": "discipulus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "docet",
        "lemma": "doceo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 473,
    "latin": "Discipulī magistrum audiunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Discipuli",
        "lemma": "discipulus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "magistrum",
        "lemma": "magister",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "audiunt",
        "lemma": "audio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 474,
    "latin": "Magister fābulam nārrat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Magister",
        "lemma": "Magister",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "fabulam",
        "lemma": "fabula",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "narrat",
        "lemma": "narro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 475,
    "latin": "Discipulī fābulam audiunt et gaudent.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Discipuli",
        "lemma": "discipulus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "fabulam",
        "lemma": "fabula",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "audiunt",
        "lemma": "audio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 4,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 4,
        "word": "gaudent",
        "lemma": "gaudeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 2,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 476,
    "latin": "Forum Rōmānum magnum est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Forum",
        "lemma": "Forum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Romanum",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "magnum",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 477,
    "latin": "Mercātōrēs in forō sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Mercatores",
        "lemma": "mercator",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "foro",
        "lemma": "forum",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 478,
    "latin": "Cīvēs mercātōribus pecūniam dant.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Cives",
        "lemma": "ciuis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "mercatoribus",
        "lemma": "mercator",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 2,
        "word": "pecuniam",
        "lemma": "pecunia",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "dant",
        "lemma": "do",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 479,
    "latin": "Mercātōrēs cīvibus mercem vendunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Mercatores",
        "lemma": "mercator",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "civibus",
        "lemma": "ciuis",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "mercem",
        "lemma": "merx",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "vendunt",
        "lemma": "uendo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 480,
    "latin": "Forum semper plēnum est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Forum",
        "lemma": "Forum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "semper",
        "lemma": "semper",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 2,
        "current_role": "modificador"
      },
      {
        "idx": 2,
        "word": "plenum",
        "lemma": "plenus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 481,
    "latin": "Iuppiter rēx deōrum est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Iuppiter",
        "lemma": "Iuppiter",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "rex",
        "lemma": "rex",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "appos",
        "head": 0,
        "current_role": "aposición"
      },
      {
        "idx": 2,
        "word": "deorum",
        "lemma": "deus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 482,
    "latin": "Iūnō rēgīna deōrum est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Iuno",
        "lemma": "Iuno",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "regina",
        "lemma": "regina",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "deorum",
        "lemma": "deus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 483,
    "latin": "Mārs deus bellī est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Mars",
        "lemma": "Mars",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "deus",
        "lemma": "deus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "belli",
        "lemma": "bellum",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Neut|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 484,
    "latin": "Venus dea amōris est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Venus",
        "lemma": "Uenus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "dea",
        "lemma": "dea",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "amoris",
        "lemma": "amor",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 485,
    "latin": "Rōmānī multōs deōs colunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romani",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "multos",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 2,
        "current_role": "determinante"
      },
      {
        "idx": 2,
        "word": "deos",
        "lemma": "deus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "colunt",
        "lemma": "colo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 486,
    "latin": "Iūlius cēnam parat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Iulius",
        "lemma": "Iulius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "cenam",
        "lemma": "cena",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "parat",
        "lemma": "paro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 487,
    "latin": "Servī cibum afferunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Servi",
        "lemma": "Seruius",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "cibum",
        "lemma": "cibus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "afferunt",
        "lemma": "affero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 488,
    "latin": "Familia in triclīniō cēnat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Familia",
        "lemma": "familia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "triclinio",
        "lemma": "triclinium",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "cenat",
        "lemma": "ceno",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 489,
    "latin": "Aemilia vīnum miscet.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Aemilia",
        "lemma": "Aemilia",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "vinum",
        "lemma": "uinum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "miscet",
        "lemma": "misceo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 490,
    "latin": "Post cēnam Iūlius fābulam nārrat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Post",
        "lemma": "post",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "cenam",
        "lemma": "cena",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "Iulius",
        "lemma": "Iulius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "fabulam",
        "lemma": "fabula",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "narrat",
        "lemma": "narro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 491,
    "latin": "Mārcus cum patre Rōmam it.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Marcus",
        "lemma": "Marcus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "cum",
        "lemma": "cum",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "patre",
        "lemma": "pater",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "Romam",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "it",
        "lemma": "eo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 492,
    "latin": "Via longa est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Via",
        "lemma": "uia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "longa",
        "lemma": "longus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 493,
    "latin": "In viā multōs viātōrēs vident.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "In",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "via",
        "lemma": "uia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "multos",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 3,
        "current_role": "determinante"
      },
      {
        "idx": 3,
        "word": "viatores",
        "lemma": "uiator",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "vident",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 494,
    "latin": "Tandem ad portam urbis perveniunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Tandem",
        "lemma": "tandem",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 4,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "ad",
        "lemma": "ad",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "portam",
        "lemma": "porta",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "urbis",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 2,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 4,
        "word": "perveniunt",
        "lemma": "peruenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 495,
    "latin": "Mārcus laetus est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Marcus",
        "lemma": "Marcus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "laetus",
        "lemma": "laetus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 496,
    "latin": "Annus quattuor tempora habet:",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Annus",
        "lemma": "annus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "quattuor",
        "lemma": "quatuor",
        "pos": "NUM",
        "morph": "",
        "dep": "nummod",
        "head": 2,
        "current_role": "modificador_numeral"
      },
      {
        "idx": 2,
        "word": "tempora",
        "lemma": "tempus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "habet",
        "lemma": "habeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ":",
        "lemma": ":",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 497,
    "latin": "vēr, aestās, autumnus, hiems.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "ver",
        "lemma": "uer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "aestas",
        "lemma": "aestas",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "autumnus",
        "lemma": "autumnus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 5,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 6,
        "current_role": "puntuación"
      },
      {
        "idx": 6,
        "word": "hiems",
        "lemma": "hiems",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 7,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 498,
    "latin": "Vēre flōrēs florent.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Vere",
        "lemma": "uere",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 1,
        "word": "flores",
        "lemma": "flos",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "florent",
        "lemma": "floreo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 499,
    "latin": "Aestāte sol calidus est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Aestate",
        "lemma": "aestas",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "sol",
        "lemma": "sol",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "calidus",
        "lemma": "calidus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 500,
    "latin": "Autumnō frūctūs mātūrēscunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Autumno",
        "lemma": "autumno",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "fructus",
        "lemma": "fructus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "maturescunt",
        "lemma": "maturesco",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 501,
    "latin": "Hieme nix cadit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Hieme",
        "lemma": "hiems",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "nix",
        "lemma": "nix",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "cadit",
        "lemma": "cado",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 502,
    "latin": "Mīlitēs Rōmānī fortēs sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Romani",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "fortes",
        "lemma": "fortis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 503,
    "latin": "Gladiōs et scūta portant.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Gladios",
        "lemma": "gladius",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 2,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 2,
        "word": "scuta",
        "lemma": "scutum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": "portant",
        "lemma": "porto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 504,
    "latin": "Imperātor mīlitēs dūcit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Imperator",
        "lemma": "imperator",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "ducit",
        "lemma": "duco",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 505,
    "latin": "Mīlitēs imperātōrī pārent.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "imperatori",
        "lemma": "imperator",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "obl:arg",
        "head": 2,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 2,
        "word": "parent",
        "lemma": "pareo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 506,
    "latin": "Legiō Rōmāna invicta est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Legio",
        "lemma": "Legio",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Romana",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "invicta",
        "lemma": "inuictus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 507,
    "latin": "Mārcus Gāiō amīcō suō salūtem dīcit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Marcus",
        "lemma": "Marcus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Gaio",
        "lemma": "Gaius",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "flat:name",
        "head": 0,
        "current_role": "nombre_compuesto"
      },
      {
        "idx": 2,
        "word": "amico",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 5,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 3,
        "word": "suo",
        "lemma": "suus",
        "pos": "DET",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "salutem",
        "lemma": "salus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 5,
        "current_role": "objeto_directo"
      },
      {
        "idx": 5,
        "word": "dicit",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 508,
    "latin": "Valēsne?",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Valesne",
        "lemma": "ualesne",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "?",
        "lemma": "?",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 509,
    "latin": "Ego valeō.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Ego",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Sing|Person=1",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "valeo",
        "lemma": "ualeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 510,
    "latin": "Hodiē in hortō lūsī. Crās ad tē veniam.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Hodie",
        "lemma": "hodie",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "horto",
        "lemma": "hortus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "lusi",
        "lemma": "ludo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "Cras",
        "lemma": "cras",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 8,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 6,
        "word": "ad",
        "lemma": "ad",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 7,
        "current_role": "preposición"
      },
      {
        "idx": 7,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "obl",
        "head": 8,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 8,
        "word": "veniam",
        "lemma": "uenia",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 8,
        "current_role": "predicado"
      },
      {
        "idx": 9,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 8,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 511,
    "latin": "Valē, amīce!",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Vale",
        "lemma": "ualeo",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "amice",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 0,
        "current_role": "vocativo"
      },
      {
        "idx": 3,
        "word": "!",
        "lemma": "!",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 512,
    "latin": "Rōmulus et Remus gemīnī erant.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romulus",
        "lemma": "Romulus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 2,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 2,
        "word": "Remus",
        "lemma": "Remi",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": "gemini",
        "lemma": "geminus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "erant",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 513,
    "latin": "Lupa eōs nūtrīvit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Lupa",
        "lemma": "lupa",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "eos",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Masc|Number=Plur|Person=3",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "nutrivit",
        "lemma": "nutrio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 514,
    "latin": "Posteā Rōmulus urbem condidit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Postea",
        "lemma": "postea",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "Romulus",
        "lemma": "Romulus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "urbem",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "condidit",
        "lemma": "condo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 515,
    "latin": "Urbs Rōma vocāta est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Urbs",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 2,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "Roma",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "vocata",
        "lemma": "uoco",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 2,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 516,
    "latin": "Rōmulus prīmus rēx Rōmānōrum fuit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romulus",
        "lemma": "Romulus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "primus",
        "lemma": "primus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "rex",
        "lemma": "rex",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "appos",
        "head": 0,
        "current_role": "aposición"
      },
      {
        "idx": 3,
        "word": "Romanorum",
        "lemma": "Romanus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 2,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 4,
        "word": "fuit",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 517,
    "latin": "Hannibal dux Carthāginiēnsium fuit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Hannibal",
        "lemma": "Hannibal",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "dux",
        "lemma": "dux",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "appos",
        "head": 0,
        "current_role": "aposición"
      },
      {
        "idx": 2,
        "word": "Carthaginiensium",
        "lemma": "Carthaginiensis",
        "pos": "PROPN",
        "morph": "Case=Gen|Gender=Neut|Number=Plur",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 3,
        "word": "fuit",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 518,
    "latin": "Cum elephantīs Alpēs trānsiit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Cum",
        "lemma": "cum",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "elephantis",
        "lemma": "elephantus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 2,
        "word": "Alpes",
        "lemma": "Alpes",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "transiit",
        "lemma": "transeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 519,
    "latin": "Rōmānōs multīs proeliīs superāvit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romanos",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "multis",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Neut|Number=Plur",
        "dep": "det",
        "head": 2,
        "current_role": "determinante"
      },
      {
        "idx": 2,
        "word": "proeliis",
        "lemma": "proelium",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "superavit",
        "lemma": "supero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 520,
    "latin": "Tamen Rōmam capere nōn potuit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Tamen",
        "lemma": "tamen",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 4,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 1,
        "word": "Romam",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "capere",
        "lemma": "capio",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 4,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 3,
        "word": "non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 4,
        "current_role": "modificador"
      },
      {
        "idx": 4,
        "word": "potuit",
        "lemma": "possum",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 521,
    "latin": "In forō cīvēs conveniēbant.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "In",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "foro",
        "lemma": "forum",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "cives",
        "lemma": "ciuis",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "conveniebant",
        "lemma": "conuenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 522,
    "latin": "Ōrātor verba faciēbat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Orator",
        "lemma": "orator",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "verba",
        "lemma": "uerbum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "faciebat",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 523,
    "latin": "Populus ōrātōrem audīvit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Populus",
        "lemma": "populus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "oratorem",
        "lemma": "orator",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "audivit",
        "lemma": "audio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 524,
    "latin": "Aliquī laudāvērunt, aliquī vituperāvērunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Aliqui",
        "lemma": "aliqui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "laudaverunt",
        "lemma": "laudo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "aliqui",
        "lemma": "aliqui",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "vituperaverunt",
        "lemma": "uitupero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 1,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 525,
    "latin": "Sīc erat lībertās Rōmāna.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Sic",
        "lemma": "sic",
        "pos": "ADV",
        "morph": "",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "erat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 0,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "libertas",
        "lemma": "libertas",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "Romana",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 526,
    "latin": "Aenēās Trōiā fūgit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Aeneas",
        "lemma": "Aeneas",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Troia",
        "lemma": "Troia",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "fugit",
        "lemma": "fugio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 527,
    "latin": "Per maria multa errāvit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Per",
        "lemma": "per",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "maria",
        "lemma": "mare",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "multa",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "erravit",
        "lemma": "erro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 528,
    "latin": "Tandem ad Ītaliam pervēnit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Tandem",
        "lemma": "tandem",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 3,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 1,
        "word": "ad",
        "lemma": "ad",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "Italiam",
        "lemma": "Italia",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "pervenit",
        "lemma": "peruenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 529,
    "latin": "Ibi novam patriam invēnit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Ibi",
        "lemma": "ibi",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:lmod",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "novam",
        "lemma": "nouus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "patriam",
        "lemma": "patria",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "invenit",
        "lemma": "inuenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 530,
    "latin": "Rōmānī ab Aenēā oriundī sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romani",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "advcl:pred",
        "head": 3,
        "current_role": "otro"
      },
      {
        "idx": 1,
        "word": "ab",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "Aenea",
        "lemma": "Aeneas",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "oriundi",
        "lemma": "oriundus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 3,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 531,
    "latin": "Gallia omnis in partēs trēs dīvīsa est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Gallia",
        "lemma": "Gallia",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 5,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "omnis",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 0,
        "current_role": "determinante"
      },
      {
        "idx": 2,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "partes",
        "lemma": "pars",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obl",
        "head": 5,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "tres",
        "lemma": "tres",
        "pos": "NUM",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "nummod",
        "head": 3,
        "current_role": "modificador_numeral"
      },
      {
        "idx": 5,
        "word": "divisa",
        "lemma": "diuido",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 5,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 7,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 532,
    "latin": "Ūnam partem Belgae incolunt, aliam Aquītānī, tertiam Celtae.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Unam",
        "lemma": "unus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "nummod",
        "head": 1,
        "current_role": "modificador_numeral"
      },
      {
        "idx": 1,
        "word": "partem",
        "lemma": "pars",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "Belgae",
        "lemma": "Belgae",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "incolunt",
        "lemma": "incolo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "aliam",
        "lemma": "alius",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 6,
        "word": "Aquitani",
        "lemma": "Aquitani",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 5,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 7,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 9,
        "current_role": "puntuación"
      },
      {
        "idx": 8,
        "word": "tertiam",
        "lemma": "tertius",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 9,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 9,
        "word": "Celtae",
        "lemma": "Celtae",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "conj",
        "head": 2,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 10,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 533,
    "latin": "Hī omnēs linguā et lēgibus differunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Hi",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "omnes",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "lingua",
        "lemma": "lingua",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 5,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 4,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 4,
        "word": "legibus",
        "lemma": "lex",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Plur",
        "dep": "conj",
        "head": 2,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 5,
        "word": "differunt",
        "lemma": "differo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 534,
    "latin": "Amīcitia nihil aliud est nisi omnium dīvīnārum hūmānārumque rērum cum benevolentiā et cāritāte cōnsēnsiō.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Amicitia",
        "lemma": "amicitia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "nihil",
        "lemma": "nihil",
        "pos": "PRON",
        "morph": "",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "aliud",
        "lemma": "alius",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 3,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": "nisi",
        "lemma": "nisi",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 6,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 5,
        "word": "omnium",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Gen|Gender=Fem|Number=Plur",
        "dep": "det",
        "head": 6,
        "current_role": "determinante"
      },
      {
        "idx": 6,
        "word": "divinarum",
        "lemma": "diuinus",
        "pos": "ADJ",
        "morph": "Case=Gen|Gender=Fem|Number=Plur",
        "dep": "advcl",
        "head": 1,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 7,
        "word": "humanarum",
        "lemma": "humanus",
        "pos": "ADJ",
        "morph": "Case=Gen|Gender=Fem|Number=Plur",
        "dep": "conj",
        "head": 6,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 8,
        "word": "que",
        "lemma": "que",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 7,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 9,
        "word": "rerum",
        "lemma": "res",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Plur",
        "dep": "nmod",
        "head": 7,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 10,
        "word": "cum",
        "lemma": "cum",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 11,
        "current_role": "preposición"
      },
      {
        "idx": 11,
        "word": "benevolentia",
        "lemma": "beneuolentia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 14,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 12,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 13,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 13,
        "word": "caritate",
        "lemma": "caritas",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 11,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 14,
        "word": "consensio",
        "lemma": "consensio",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 1,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 15,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 535,
    "latin": "Sine amīcitiā vīta nūlla est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Sine",
        "lemma": "sino",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "amicitia",
        "lemma": "amicitia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "vita",
        "lemma": "uita",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "nulla",
        "lemma": "nullus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 2,
        "current_role": "determinante"
      },
      {
        "idx": 4,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 536,
    "latin": "Porsenna rēx urbem oppugnābat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Porsenna",
        "lemma": "Porsenna",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "rex",
        "lemma": "rex",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "urbem",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "oppugnabat",
        "lemma": "oppugno",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 537,
    "latin": "Horātius sōlus in ponte stetit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Horatius",
        "lemma": "Horatius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "solus",
        "lemma": "solus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 0,
        "current_role": "determinante"
      },
      {
        "idx": 2,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "ponte",
        "lemma": "pons",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "stetit",
        "lemma": "sto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 538,
    "latin": "Hostēs sustinuit dum pōns ā tergō solvitur.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Hostes",
        "lemma": "hostis",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "sustinuit",
        "lemma": "sustineo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "dum",
        "lemma": "dum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 6,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 3,
        "word": "pons",
        "lemma": "pons",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 6,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 4,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 5,
        "current_role": "preposición"
      },
      {
        "idx": 5,
        "word": "tergo",
        "lemma": "tergum",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl:arg",
        "head": 6,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 6,
        "word": "solvitur",
        "lemma": "soluo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "advcl",
        "head": 1,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 7,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 539,
    "latin": "Deinde in flūmen dēsiluit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Deinde",
        "lemma": "deinde",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 3,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 1,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "flumen",
        "lemma": "flumen",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "desiluit",
        "lemma": "desilio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 540,
    "latin": "Catilīna rem pūblicam dēlēre voluit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Catilina",
        "lemma": "Catilina",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "rem",
        "lemma": "res",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "publicam",
        "lemma": "publica",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "delere",
        "lemma": "deleo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 4,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 4,
        "word": "voluit",
        "lemma": "uolo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  }
]