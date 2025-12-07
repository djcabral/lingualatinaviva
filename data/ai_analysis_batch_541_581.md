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
    "id": 541,
    "latin": "Cicerō coniūrātiōnem dētēxit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Cicero",
        "lemma": "Cicero",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "coniurationem",
        "lemma": "coniuratio",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "detexit",
        "lemma": "detego",
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
    "id": 542,
    "latin": "In senātū ōrātiōnem habuit:",
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
        "word": "senatu",
        "lemma": "senatus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "orationem",
        "lemma": "oratio",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "habuit",
        "lemma": "habeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 543,
    "latin": "'Quōusque tandem abūtēre, Catilīna, patientiā nostrā?",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "'Quous",
        "lemma": "'Quous",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      },
      {
        "idx": 1,
        "word": "que",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "tandem",
        "lemma": "tandem",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 3,
        "word": "abutere",
        "lemma": "abutor",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
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
        "word": "Catilina",
        "lemma": "Catilina",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 3,
        "current_role": "vocativo"
      },
      {
        "idx": 6,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 7,
        "current_role": "puntuación"
      },
      {
        "idx": 7,
        "word": "patientia",
        "lemma": "patientia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 8,
        "word": "nostra",
        "lemma": "noster",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 7,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 9,
        "word": "?",
        "lemma": "?",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 544,
    "latin": "'",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "'",
        "lemma": "'",
        "pos": "PUNCT",
        "morph": "",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      }
    ]
  },
  {
    "id": 545,
    "latin": "Mīlitat omnis amāns, et habet sua castra Cupīdō.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Militat",
        "lemma": "milito",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "omnis",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 2,
        "current_role": "determinante"
      },
      {
        "idx": 2,
        "word": "amans",
        "lemma": "amans",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 5,
        "current_role": "puntuación"
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
        "word": "habet",
        "lemma": "habeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 6,
        "word": "sua",
        "lemma": "suus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "det",
        "head": 7,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 7,
        "word": "castra",
        "lemma": "castra",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 5,
        "current_role": "objeto_directo"
      },
      {
        "idx": 8,
        "word": "Cupido",
        "lemma": "Cupido",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 9,
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
    "id": 546,
    "latin": "Quae bellō est habilis, Vēnerī quoque convenit aetās.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Quae",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "bello",
        "lemma": "bellum",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": "habilis",
        "lemma": "habilis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
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
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "Veneri",
        "lemma": "Uenerus",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Fem|Number=Sing",
        "dep": "obl:arg",
        "head": 7,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 6,
        "word": "quoque",
        "lemma": "quoque",
        "pos": "ADV",
        "morph": "",
        "dep": "discourse",
        "head": 7,
        "current_role": "marcador_discursivo"
      },
      {
        "idx": 7,
        "word": "convenit",
        "lemma": "conuenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 3,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 8,
        "word": "aetas",
        "lemma": "aetas",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 7,
        "current_role": "sujeto"
      },
      {
        "idx": 9,
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
    "id": 547,
    "latin": "Turpe senex mīles, turpe senīlis amor.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Turpe",
        "lemma": "turpis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "senex",
        "lemma": "senex",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "miles",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
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
        "word": "turpe",
        "lemma": "turpis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 5,
        "word": "senilis",
        "lemma": "senilis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 6,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 6,
        "word": "amor",
        "lemma": "amor",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
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
    "id": 548,
    "latin": "Nōn quī parum habet, sed quī plūs cupit, pauper est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "parum",
        "lemma": "parum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "advmod",
        "head": 3,
        "current_role": "modificador_adverbial"
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
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 8,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "sed",
        "lemma": "sed",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 8,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 6,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 8,
        "current_role": "sujeto"
      },
      {
        "idx": 7,
        "word": "plus",
        "lemma": "plus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 8,
        "current_role": "objeto_directo"
      },
      {
        "idx": 8,
        "word": "cupit",
        "lemma": "cupio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 3,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 9,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 8,
        "current_role": "puntuación"
      },
      {
        "idx": 10,
        "word": "pauper",
        "lemma": "pauper",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 3,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 11,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 10,
        "current_role": "cópula"
      },
      {
        "idx": 12,
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
    "id": 549,
    "latin": "Dīvitiās nōn quī habet, sed quī cupit, carēre potuit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Divitias",
        "lemma": "diuitia",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 2,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "habet",
        "lemma": "habeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 10,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 4,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 7,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "sed",
        "lemma": "sed",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 7,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 6,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 7,
        "current_role": "sujeto"
      },
      {
        "idx": 7,
        "word": "cupit",
        "lemma": "cupio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 3,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 8,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 9,
        "word": "carere",
        "lemma": "careo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 10,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 10,
        "word": "potuit",
        "lemma": "possum",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 10,
        "current_role": "predicado"
      },
      {
        "idx": 11,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 10,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 550,
    "latin": "Hīs rēbus cognitīs, Caesar exercitum trāns Rhēnum dūxit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "His",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Fem|Number=Plur",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 1,
        "word": "rebus",
        "lemma": "res",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Plur",
        "dep": "nsubj:pass",
        "head": 2,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 2,
        "word": "cognitis",
        "lemma": "cognosco",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "advcl:abs",
        "head": 8,
        "current_role": "otro"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 8,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "exercitum",
        "lemma": "exercitus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 8,
        "current_role": "objeto_directo"
      },
      {
        "idx": 6,
        "word": "trans",
        "lemma": "trans",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 7,
        "current_role": "preposición"
      },
      {
        "idx": 7,
        "word": "Rhenum",
        "lemma": "Rhenus",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 8,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 8,
        "word": "duxit",
        "lemma": "duco",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 551,
    "latin": "Germānī, adventū Caesaris cognitō, in silvās fūgērunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Germani",
        "lemma": "Germani",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 8,
        "current_role": "sujeto"
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
        "word": "adventu",
        "lemma": "aduentus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 4,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 3,
        "word": "Caesaris",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 2,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 4,
        "word": "cognito",
        "lemma": "cognosco",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Neut|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "advcl:abs",
        "head": 8,
        "current_role": "otro"
      },
      {
        "idx": 5,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      },
      {
        "idx": 6,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 7,
        "current_role": "preposición"
      },
      {
        "idx": 7,
        "word": "silvas",
        "lemma": "silua",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obl",
        "head": 8,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 8,
        "word": "fugerunt",
        "lemma": "fugio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 552,
    "latin": "Caesar pontem rescindit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "pontem",
        "lemma": "pons",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "rescindit",
        "lemma": "rescindo",
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
    "id": 553,
    "latin": "Rōmulō rēgnante, urbs crēscēbat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romulo",
        "lemma": "Romulus",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "regnante",
        "lemma": "regno",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Masc|Number=Sing|Tense=Pres|VerbForm=Part|Voice=Act",
        "dep": "advcl:abs",
        "head": 4,
        "current_role": "otro"
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
        "word": "urbs",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "crescebat",
        "lemma": "cresco",
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
    "id": 554,
    "latin": "Multī hominēs Rōmam veniēbant.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Multi",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 1,
        "word": "homines",
        "lemma": "homo",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "Romam",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "veniebant",
        "lemma": "uenio",
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
    "id": 555,
    "latin": "Rōmulus, senātōribus convocātīs, lēgēs tulit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Romulus",
        "lemma": "Romulus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 6,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "senatoribus",
        "lemma": "senator",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 3,
        "word": "convocatis",
        "lemma": "conuoco",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "advcl:abs",
        "head": 6,
        "current_role": "otro"
      },
      {
        "idx": 4,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "leges",
        "lemma": "lex",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 6,
        "current_role": "objeto_directo"
      },
      {
        "idx": 6,
        "word": "tulit",
        "lemma": "fero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 6,
        "current_role": "predicado"
      },
      {
        "idx": 7,
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
    "id": 556,
    "latin": "Populus lēgēs accēpit.",
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
        "word": "leges",
        "lemma": "lex",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "accepit",
        "lemma": "accipio",
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
    "id": 557,
    "latin": "Officium est id quod faciendum est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Officium",
        "lemma": "officium",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 0,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "id",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Neut|Number=Sing|Person=3",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "quod",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 4,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 4,
        "word": "faciendum",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "acl:relcl",
        "head": 2,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 5,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 4,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 6,
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
    "id": 558,
    "latin": "Sunt autem officiā gerenda cum dignitāte.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 3,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 1,
        "word": "autem",
        "lemma": "autem",
        "pos": "PART",
        "morph": "",
        "dep": "discourse",
        "head": 3,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 2,
        "word": "officia",
        "lemma": "officium",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 3,
        "word": "gerenda",
        "lemma": "gerendus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Mood=Gdv|Number=Plur|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "cum",
        "lemma": "cum",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 5,
        "current_role": "preposición"
      },
      {
        "idx": 5,
        "word": "dignitate",
        "lemma": "dignitas",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
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
    "id": 559,
    "latin": "Nēmō enim est quī officiīs sē exsolvere possit.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Nemo",
        "lemma": "nemo",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Sing",
        "dep": "nsubj",
        "head": 7,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "enim",
        "lemma": "enim",
        "pos": "PART",
        "morph": "",
        "dep": "discourse",
        "head": 7,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 7,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 7,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "officiis",
        "lemma": "officium",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Plur",
        "dep": "obl",
        "head": 6,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 5,
        "word": "se",
        "lemma": "sui",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=3",
        "dep": "obj",
        "head": 6,
        "current_role": "objeto_directo"
      },
      {
        "idx": 6,
        "word": "exsolvere",
        "lemma": "exsolvo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 7,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 7,
        "word": "possit",
        "lemma": "possum",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 7,
        "current_role": "predicado"
      },
      {
        "idx": 8,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 7,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 560,
    "latin": "Hannibal Alpēs trānsitūrus erat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Hannibal",
        "lemma": "Hannibal",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "Alpes",
        "lemma": "Alpes",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "transiturus",
        "lemma": "transeo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "erat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "aux",
        "head": 2,
        "current_role": "auxiliar"
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
    "id": 561,
    "latin": "Mīlitēs sequendī erant.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "sequendi",
        "lemma": "sequor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Mood=Gdv|Number=Plur|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "erant",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "aux",
        "head": 1,
        "current_role": "auxiliar"
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
    "id": 562,
    "latin": "Rōma dēfendenda erat.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Roma",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "defendenda",
        "lemma": "defendendus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "erat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 1,
        "current_role": "auxiliar_pasivo"
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
    "id": 563,
    "latin": "Victōria adipīscenda erat cīvibus.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Victoria",
        "lemma": "Uictoria",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "adipiscenda",
        "lemma": "adipiscendus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "erat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 1,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 3,
        "word": "civibus",
        "lemma": "ciuis",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "obl:arg",
        "head": 1,
        "current_role": "complemento_obligatorio"
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
    "id": 564,
    "latin": "Cum Caesar Galliam petīvisset, Helvētiī dē fīnibus suīs exīre cōnstituērunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Cum",
        "lemma": "cum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "Galliam",
        "lemma": "Gallia",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "petivisset",
        "lemma": "peto",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pqp|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 10,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 4,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "Helvetii",
        "lemma": "Heluetii",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 10,
        "current_role": "sujeto"
      },
      {
        "idx": 6,
        "word": "de",
        "lemma": "de",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 7,
        "current_role": "preposición"
      },
      {
        "idx": 7,
        "word": "finibus",
        "lemma": "finis",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 9,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 8,
        "word": "suis",
        "lemma": "suus",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 7,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 9,
        "word": "exire",
        "lemma": "exeo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 10,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 10,
        "word": "constituerunt",
        "lemma": "constituo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 10,
        "current_role": "predicado"
      },
      {
        "idx": 11,
        "word": ".",
        "lemma": ".",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 10,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 565,
    "latin": "Cum profectī essent, Caesar eōs secūtus est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Cum",
        "lemma": "cum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 1,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "profecti",
        "lemma": "proficiscor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "advcl",
        "head": 6,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 2,
        "word": "essent",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Sub|Number=Plur|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 1,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 6,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "eos",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Masc|Number=Plur|Person=3",
        "dep": "obj",
        "head": 6,
        "current_role": "objeto_directo"
      },
      {
        "idx": 6,
        "word": "secutus",
        "lemma": "sequor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 6,
        "current_role": "predicado"
      },
      {
        "idx": 7,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 6,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 8,
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
    "id": 566,
    "latin": "Lēgātī dīxērunt sē pācem petere.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Legati",
        "lemma": "legatus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "dixerunt",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "se",
        "lemma": "sui",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=3",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "pacem",
        "lemma": "pax",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "petere",
        "lemma": "peto",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 1,
        "current_role": "oración_completiva"
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
    "id": 567,
    "latin": "Negāvērunt sē bellum velle.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Negaverunt",
        "lemma": "nego",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "se",
        "lemma": "sui",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=3",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "bellum",
        "lemma": "bellum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "velle",
        "lemma": "uolo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 568,
    "latin": "Affirmāvērunt rēgem suum amīcum populī Rōmānī esse.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Affirmaverunt",
        "lemma": "affirmo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "regem",
        "lemma": "rex",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "suum",
        "lemma": "suus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "amicum",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "populi",
        "lemma": "populus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 3,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 5,
        "word": "Romani",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 4,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 6,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
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
    "id": 569,
    "latin": "Sī hoc fēcerīs, laetus erō.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Si",
        "lemma": "si",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "hoc",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "feceris",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 4,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "laetus",
        "lemma": "laetus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": "ero",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin",
        "dep": "cop",
        "head": 4,
        "current_role": "cópula"
      },
      {
        "idx": 6,
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
    "id": 570,
    "latin": "Sī hoc facerēs, laetus essem.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Si",
        "lemma": "si",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "hoc",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "faceres",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 4,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "laetus",
        "lemma": "laetus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": "essem",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Sub|Number=Sing|Person=1|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 4,
        "current_role": "cópula"
      },
      {
        "idx": 6,
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
    "id": 571,
    "latin": "Sī hoc fēcissēs, laetus fuissem.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Si",
        "lemma": "si",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "hoc",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "fecisses",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pqp|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 4,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "laetus",
        "lemma": "laetus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": "fuissem",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Sub|Number=Sing|Person=1|Tense=Pqp|VerbForm=Fin",
        "dep": "cop",
        "head": 4,
        "current_role": "cópula"
      },
      {
        "idx": 6,
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
    "id": 572,
    "latin": "Condiciōnēs dīversae sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Condiciones",
        "lemma": "condicio",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "diversae",
        "lemma": "diversus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
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
    "id": 573,
    "latin": "Is quī sapit, felix est.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Is",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "sapit",
        "lemma": "sapio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "acl:relcl",
        "head": 0,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "felix",
        "lemma": "felix",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 4,
        "current_role": "cópula"
      },
      {
        "idx": 6,
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
    "id": 574,
    "latin": "Quod faciendum est, faciāmus.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Quod",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "faciendum",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "ccomp",
        "head": 4,
        "current_role": "oración_completiva"
      },
      {
        "idx": 2,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 1,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "faciamus",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 575,
    "latin": "Quae vēra sunt, dīcenda sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Quae",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Neut|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "vera",
        "lemma": "uerus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Plur",
        "dep": "csubj:pass",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "dicenda",
        "lemma": "dicendus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Mood=Gdv|Number=Plur|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 4,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 6,
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
    "id": 576,
    "latin": "Quōrum virtūs clāra est, laudandī sunt.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Quorum",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 1,
        "word": "virtus",
        "lemma": "uirtus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "clara",
        "lemma": "clarus",
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
        "word": "laudandi",
        "lemma": "laudo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Mood=Gdv|Number=Plur|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "conj",
        "head": 2,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 6,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
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
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 577,
    "latin": "Caesar in commentāriīs scrīpsit Gallōs fortēs esse.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
        "word": "commentariis",
        "lemma": "commentarius",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "scripsit",
        "lemma": "scribo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "Gallos",
        "lemma": "Gallus",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "fortes",
        "lemma": "fortis",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "ccomp",
        "head": 3,
        "current_role": "oración_completiva"
      },
      {
        "idx": 6,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
        "dep": "cop",
        "head": 5,
        "current_role": "cópula"
      },
      {
        "idx": 7,
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
    "id": 578,
    "latin": "Dīxit sē eōs victūrum esse.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Dixit",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "se",
        "lemma": "sui",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=3",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "eos",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Masc|Number=Plur|Person=3",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "victurum",
        "lemma": "uicio",
        "pos": "VERB",
        "morph": "Case=Acc|Gender=Masc|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
      },
      {
        "idx": 4,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
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
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 579,
    "latin": "Narrāvit Germānōs trans Rhēnum habitāre.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Narravit",
        "lemma": "narro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "Germanos",
        "lemma": "Germani",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "trans",
        "lemma": "trans",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "Rhenum",
        "lemma": "Rhenus",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "habitare",
        "lemma": "habito",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 580,
    "latin": "Arma virumque canō, Trōiae quī prīmus ab ōrīs Ītaliam fātō profugus Lāvīniaque vēnit lītora.",
    "spanish": "",
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
        "head": 12,
        "current_role": "sujeto"
      },
      {
        "idx": 7,
        "word": "primus",
        "lemma": "primus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 12,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 8,
        "word": "ab",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 10,
        "current_role": "preposición"
      },
      {
        "idx": 9,
        "word": "oris",
        "lemma": "ora",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Plur",
        "dep": "nmod",
        "head": 10,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 10,
        "word": "Italiam",
        "lemma": "Italia",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl:lmod",
        "head": 12,
        "current_role": "modificador"
      },
      {
        "idx": 11,
        "word": "fato",
        "lemma": "fatum",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 12,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 12,
        "word": "profugus",
        "lemma": "profugus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "acl:relcl",
        "head": 5,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 13,
        "word": "Lavinia",
        "lemma": "Lauinia",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 12,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 14,
        "word": "que",
        "lemma": "que",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 15,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 15,
        "word": "venit",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "acl:relcl",
        "head": 0,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 16,
        "word": "litora",
        "lemma": "litus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 15,
        "current_role": "objeto_directo"
      },
      {
        "idx": 17,
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
    "id": 581,
    "latin": "Multum ille et terrīs iactātus et altō.",
    "spanish": "",
    "tokens": [
      {
        "idx": 0,
        "word": "Multum",
        "lemma": "multum",
        "pos": "ADV",
        "morph": "",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ille",
        "lemma": "ille",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
        "word": "terris",
        "lemma": "terra",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Plur",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "iactatus",
        "lemma": "iactatus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 5,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 6,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 6,
        "word": "alto",
        "lemma": "altus",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 4,
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
  }
]