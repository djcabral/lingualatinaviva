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
    "id": 141,
    "latin": "Optimum consilium sequimur.",
    "spanish": "Seguimos el mejor consejo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Optimum",
        "lemma": "bonus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "consilium",
        "lemma": "consilium",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "sequimur",
        "lemma": "sequor",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 142,
    "latin": "Ego te amo.",
    "spanish": "Yo te amo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Ego",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Sing|Person=1",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "amo",
        "lemma": "amo",
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
    "id": 143,
    "latin": "Hic liber meus est, ille tuus.",
    "spanish": "Este libro es mío, aquel es tuyo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Hic",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "liber",
        "lemma": "liber",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "meus",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "modificador_adjetival"
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
        "word": "ille",
        "lemma": "ille",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 6,
        "word": "tuus",
        "lemma": "tuus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
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
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 144,
    "latin": "Quis est ille vir?",
    "spanish": "¿Quién es aquel hombre?",
    "tokens": [
      {
        "idx": 0,
        "word": "Quis",
        "lemma": "quis",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "ille",
        "lemma": "ille",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 3,
        "current_role": "determinante"
      },
      {
        "idx": 3,
        "word": "vir",
        "lemma": "uir",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
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
    "id": 145,
    "latin": "Nemo hoc scit.",
    "spanish": "Nadie sabe esto.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nemo",
        "lemma": "nemo",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
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
        "word": "scit",
        "lemma": "scio",
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
    "id": 146,
    "latin": "Omnes cives pacem desiderant.",
    "spanish": "Todos los ciudadanos desean la paz.",
    "tokens": [
      {
        "idx": 0,
        "word": "Omnes",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 1,
        "word": "cives",
        "lemma": "ciuis",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "pacem",
        "lemma": "pax",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "desiderant",
        "lemma": "desidero",
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
    "id": 147,
    "latin": "Qui venit, amicus meus est.",
    "spanish": "Quien viene es mi amigo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "venit",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "amicus",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "meus",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 5,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
      },
      {
        "idx": 6,
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
    "id": 148,
    "latin": "Ipse imperator milites ducit.",
    "spanish": "El emperador mismo conduce a los soldados.",
    "tokens": [
      {
        "idx": 0,
        "word": "Ipse",
        "lemma": "ipse",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 1,
        "word": "imperator",
        "lemma": "imperator",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "ducit",
        "lemma": "duco",
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
    "id": 149,
    "latin": "Aliquis ianuam pulsat.",
    "spanish": "Alguien golpea la puerta.",
    "tokens": [
      {
        "idx": 0,
        "word": "Aliquis",
        "lemma": "aliquis",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "ianuam",
        "lemma": "ianua",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "pulsat",
        "lemma": "pulso",
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
    "id": 150,
    "latin": "Nihil novi sub sole.",
    "spanish": "Nada nuevo bajo el sol.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nihil",
        "lemma": "nihil",
        "pos": "PRON",
        "morph": "",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "novi",
        "lemma": "nosco",
        "pos": "ADJ",
        "morph": "Case=Gen|Gender=Neut|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "sub",
        "lemma": "sub",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "sole",
        "lemma": "sol",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
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
    "id": 151,
    "latin": "Uter consul victoriam reportavit?",
    "spanish": "¿Cuál cónsul reportó la victoria?",
    "tokens": [
      {
        "idx": 0,
        "word": "Uter",
        "lemma": "uter",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "consul",
        "lemma": "consul",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "victoriam",
        "lemma": "uictoria",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "reportavit",
        "lemma": "reporto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
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
    "id": 152,
    "latin": "Puella ab omnibus amatur.",
    "spanish": "La niña es amada por todos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puella",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
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
        "word": "omnibus",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 3,
        "word": "amatur",
        "lemma": "amo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 153,
    "latin": "Urbs a militibus oppugnabatur.",
    "spanish": "La ciudad era atacada por los soldados.",
    "tokens": [
      {
        "idx": 0,
        "word": "Urbs",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "militibus",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl:agent",
        "head": 3,
        "current_role": "otro"
      },
      {
        "idx": 3,
        "word": "oppugnabatur",
        "lemma": "oppugno",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Pass",
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
    "id": 154,
    "latin": "Roma a Romulo condita est.",
    "spanish": "Roma fue fundada por Rómulo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Roma",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "Romulo",
        "lemma": "Romulus",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 3,
        "word": "condita",
        "lemma": "condo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
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
    "id": 155,
    "latin": "Liber cum diligentia legitur.",
    "spanish": "El libro es leído con diligencia.",
    "tokens": [
      {
        "idx": 0,
        "word": "Liber",
        "lemma": "Liber",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
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
        "word": "diligentia",
        "lemma": "diligentia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "legitur",
        "lemma": "lego",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 156,
    "latin": "Sine aqua vivere non possumus.",
    "spanish": "No podemos vivir sin agua.",
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
        "word": "aqua",
        "lemma": "aqua",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "vivere",
        "lemma": "uiuo",
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
        "word": "possumus",
        "lemma": "possum",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 157,
    "latin": "De pace loquebantur.",
    "spanish": "Hablaban acerca de la paz.",
    "tokens": [
      {
        "idx": 0,
        "word": "De",
        "lemma": "de",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "pace",
        "lemma": "pax",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "loquebantur",
        "lemma": "loquor",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Pass",
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
    "id": 158,
    "latin": "Ex urbe profecti sunt.",
    "spanish": "Partieron de la ciudad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Ex",
        "lemma": "ex",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "urbe",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "profecti",
        "lemma": "proficiscor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 159,
    "latin": "Pro patria pugnant.",
    "spanish": "Luchan por la patria.",
    "tokens": [
      {
        "idx": 0,
        "word": "Pro",
        "lemma": "pro",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "patria",
        "lemma": "patria",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "pugnant",
        "lemma": "pugno",
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
    "id": 160,
    "latin": "In bello multi cadunt.",
    "spanish": "Muchos caen en la guerra.",
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
        "word": "bello",
        "lemma": "bellum",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "multi",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "cadunt",
        "lemma": "cado",
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
    "id": 161,
    "latin": "A Caesare consilium captum est.",
    "spanish": "El plan fue tomado por César.",
    "tokens": [
      {
        "idx": 0,
        "word": "A",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 1,
        "current_role": "preposición"
      },
      {
        "idx": 1,
        "word": "Caesare",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "consilium",
        "lemma": "consilium",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 3,
        "word": "captum",
        "lemma": "capio",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
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
    "id": 162,
    "latin": "Antequam veni, iam discesserat.",
    "spanish": "Antes de que vine, ya se había marchado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Antequam",
        "lemma": "antequam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 1,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "veni",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 4,
        "current_role": "oración_adverbial"
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
        "word": "iam",
        "lemma": "iam",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 4,
        "current_role": "modificador"
      },
      {
        "idx": 4,
        "word": "discesserat",
        "lemma": "discedo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pqp|VerbForm=Fin|Voice=Act",
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
    "id": 163,
    "latin": "Cum puer fueram, ludebam.",
    "spanish": "Cuando había sido niño, jugaba.",
    "tokens": [
      {
        "idx": 0,
        "word": "Cum",
        "lemma": "cum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "puer",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "fueram",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pqp|VerbForm=Fin",
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
        "word": "ludebam",
        "lemma": "ludo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 164,
    "latin": "Postquam epistulam legero, respondebo.",
    "spanish": "Después de que habré leído la carta, responderé.",
    "tokens": [
      {
        "idx": 0,
        "word": "Postquam",
        "lemma": "postquam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "epistulam",
        "lemma": "epistula",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "legero",
        "lemma": "lego",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin|Voice=Act",
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
        "word": "respondebo",
        "lemma": "respondeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin|Voice=Act",
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
    "id": 165,
    "latin": "Si hoc dixeris, errabis.",
    "spanish": "Si hubieres dicho esto, te equivocarás.",
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
        "word": "dixeris",
        "lemma": "dico",
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
        "word": "errabis",
        "lemma": "erro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin|Voice=Act",
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
    "id": 166,
    "latin": "Olim Roma parva oppidum fuerat.",
    "spanish": "Antiguamente Roma había sido un pueblo pequeño.",
    "tokens": [
      {
        "idx": 0,
        "word": "Olim",
        "lemma": "olim",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "Roma",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "parva",
        "lemma": "paruus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "oppidum",
        "lemma": "oppidum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "fuerat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pqp|VerbForm=Fin",
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
    "id": 167,
    "latin": "Nondum cibum ceperant.",
    "spanish": "Todavía no habían tomado alimento.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nondum",
        "lemma": "nondum",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
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
        "word": "ceperant",
        "lemma": "capio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pqp|VerbForm=Fin|Voice=Act",
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
    "id": 168,
    "latin": "Statim ad te venero.",
    "spanish": "Inmediatamente habré venido a ti.",
    "tokens": [
      {
        "idx": 0,
        "word": "Statim",
        "lemma": "statim",
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
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "venero",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin|Voice=Act",
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
    "id": 169,
    "latin": "Semper te amaveram.",
    "spanish": "Siempre te había amado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Semper",
        "lemma": "semper",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 2,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "amaveram",
        "lemma": "amo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pqp|VerbForm=Fin|Voice=Act",
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
    "id": 170,
    "latin": "Mox omnia confecero.",
    "spanish": "Pronto habré terminado todo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Mox",
        "lemma": "mox",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 1,
        "word": "omnia",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "confecero",
        "lemma": "conficio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin|Voice=Act",
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
    "id": 171,
    "latin": "Tum iam domum redierat.",
    "spanish": "Entonces ya había regresado a casa.",
    "tokens": [
      {
        "idx": 0,
        "word": "Tum",
        "lemma": "tum",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "iam",
        "lemma": "iam",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 2,
        "word": "domum",
        "lemma": "domus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "redierat",
        "lemma": "redeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pqp|VerbForm=Fin|Voice=Act",
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
    "id": 172,
    "latin": "Bellum a Romanis geritur.",
    "spanish": "La guerra es llevada a cabo por los romanos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Bellum",
        "lemma": "bellum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "Romanis",
        "lemma": "Romanus",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl:agent",
        "head": 3,
        "current_role": "otro"
      },
      {
        "idx": 3,
        "word": "geritur",
        "lemma": "gero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 173,
    "latin": "Castra moventur.",
    "spanish": "El campamento es movido.",
    "tokens": [
      {
        "idx": 0,
        "word": "Castra",
        "lemma": "Castra",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "moventur",
        "lemma": "moueo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 174,
    "latin": "Consilium bonum capitur.",
    "spanish": "Un buen plan es tomado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Consilium",
        "lemma": "consilium",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 2,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "bonum",
        "lemma": "bonum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 2,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 2,
        "word": "capitur",
        "lemma": "capio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 175,
    "latin": "Veritas quaeritur.",
    "spanish": "La verdad es buscada.",
    "tokens": [
      {
        "idx": 0,
        "word": "Veritas",
        "lemma": "ueritas",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "quaeritur",
        "lemma": "quaero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 176,
    "latin": "Puer a magistro docetur.",
    "spanish": "El niño es enseñado por el maestro.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puer",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "magistro",
        "lemma": "magister",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 3,
        "word": "docetur",
        "lemma": "doceo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 177,
    "latin": "Fabula narratur.",
    "spanish": "La historia es narrada.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fabula",
        "lemma": "fabula",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "narratur",
        "lemma": "narro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 178,
    "latin": "Hostes videntur.",
    "spanish": "Los enemigos son vistos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Hostes",
        "lemma": "hostis",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "videntur",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 179,
    "latin": "Voces audiuntur.",
    "spanish": "Las voces son oídas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Voces",
        "lemma": "",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "audiuntur",
        "lemma": "audio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 180,
    "latin": "Librum legi.",
    "spanish": "El libro es leído.",
    "tokens": [
      {
        "idx": 0,
        "word": "Librum",
        "lemma": "liber",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "legi",
        "lemma": "lego",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 181,
    "latin": "Urbs defenditur.",
    "spanish": "La ciudad es defendida.",
    "tokens": [
      {
        "idx": 0,
        "word": "Urbs",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "defenditur",
        "lemma": "defendo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 182,
    "latin": "Urbs capta est.",
    "spanish": "La ciudad fue capturada.",
    "tokens": [
      {
        "idx": 0,
        "word": "Urbs",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "capta",
        "lemma": "capio",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 183,
    "latin": "Hostes victi sunt.",
    "spanish": "Los enemigos fueron vencidos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Hostes",
        "lemma": "hostis",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "victi",
        "lemma": "uictus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 184,
    "latin": "Epistula missa est.",
    "spanish": "La carta fue enviada.",
    "tokens": [
      {
        "idx": 0,
        "word": "Epistula",
        "lemma": "epistula",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "missa",
        "lemma": "mitto",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 185,
    "latin": "Verba audita sunt.",
    "spanish": "Las palabras fueron oídas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Verba",
        "lemma": "uerbum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "audita",
        "lemma": "audio",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 186,
    "latin": "Consilium inventum est.",
    "spanish": "El plan fue encontrado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Consilium",
        "lemma": "consilium",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "inventum",
        "lemma": "inuenio",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 187,
    "latin": "Caesar occisus est.",
    "spanish": "César fue asesinado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "occisus",
        "lemma": "occido",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 188,
    "latin": "Milites laudati sunt.",
    "spanish": "Los soldados fueron alabados.",
    "tokens": [
      {
        "idx": 0,
        "word": "Milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "laudati",
        "lemma": "laudo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 189,
    "latin": "Opus confectum est.",
    "spanish": "La obra fue terminada.",
    "tokens": [
      {
        "idx": 0,
        "word": "Opus",
        "lemma": "opus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "confectum",
        "lemma": "conficio",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 190,
    "latin": "Libri scripti sunt.",
    "spanish": "Los libros fueron escritos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Libri",
        "lemma": "librus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "scripti",
        "lemma": "scribo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 191,
    "latin": "Porta aperta est.",
    "spanish": "La puerta fue abierta.",
    "tokens": [
      {
        "idx": 0,
        "word": "Porta",
        "lemma": "Porta",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "aperta",
        "lemma": "aperio",
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
        "dep": "aux:pass",
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
    "id": 192,
    "latin": "Milites profecti sunt.",
    "spanish": "Los soldados partieron.",
    "tokens": [
      {
        "idx": 0,
        "word": "Milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "profecti",
        "lemma": "proficiscor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 193,
    "latin": "Hostes secuti sumus.",
    "spanish": "Seguimos a los enemigos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Hostes",
        "lemma": "hostis",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "secuti",
        "lemma": "sequor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "sumus",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin",
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
    "id": 194,
    "latin": "Pueri in horto ludere gaudent.",
    "spanish": "Los niños se alegran de jugar en el jardín.",
    "tokens": [
      {
        "idx": 0,
        "word": "Pueri",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 4,
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
        "word": "ludere",
        "lemma": "ludo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 4,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 4,
        "word": "gaudent",
        "lemma": "gaudeo",
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
    "id": 195,
    "latin": "Nemo mori vult.",
    "spanish": "Nadie quiere morir.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nemo",
        "lemma": "nemo",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "mori",
        "lemma": "morior",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Pass",
        "dep": "ccomp",
        "head": 2,
        "current_role": "oración_completiva"
      },
      {
        "idx": 2,
        "word": "vult",
        "lemma": "uolo",
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
    "id": 196,
    "latin": "Veritatem loquor.",
    "spanish": "Hablo la verdad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Veritatem",
        "lemma": "ueritas",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "loquor",
        "lemma": "loquor",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 197,
    "latin": "Gladio usus est.",
    "spanish": "Usó la espada.",
    "tokens": [
      {
        "idx": 0,
        "word": "Gladio",
        "lemma": "gladius",
        "pos": "PROPN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "usus",
        "lemma": "utor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 198,
    "latin": "In urbem ingressi sunt.",
    "spanish": "Entraron en la ciudad.",
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
        "word": "urbem",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "ingressi",
        "lemma": "ingredior",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 199,
    "latin": "Multa passus sum.",
    "spanish": "Sufrí muchas cosas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Multa",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "passus",
        "lemma": "patior",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "sum",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin",
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
    "id": 200,
    "latin": "Sole oriente proficiscemur.",
    "spanish": "Partiremos al salir el sol.",
    "tokens": [
      {
        "idx": 0,
        "word": "Sole",
        "lemma": "sol",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "oriente",
        "lemma": "oriens",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Masc|Number=Sing|Tense=Pres|VerbForm=Part|Voice=Act",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "proficiscemur",
        "lemma": "proficisco",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 201,
    "latin": "Aude sapere.",
    "spanish": "Atrévete a saber.",
    "tokens": [
      {
        "idx": 0,
        "word": "Aude",
        "lemma": "audeo",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "sapere",
        "lemma": "sapio",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "advcl",
        "head": 0,
        "current_role": "oración_adverbial"
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
    "id": 202,
    "latin": "Volo ut venias.",
    "spanish": "Quiero que vengas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Volo",
        "lemma": "uolo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "venias",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 203,
    "latin": "Timeo ne cadam.",
    "spanish": "Temo caer.",
    "tokens": [
      {
        "idx": 0,
        "word": "Timeo",
        "lemma": "timeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ne",
        "lemma": "ne",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "cadam",
        "lemma": "cado",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 204,
    "latin": "Oportet ut studeas.",
    "spanish": "Es necesario que estudies.",
    "tokens": [
      {
        "idx": 0,
        "word": "Oportet",
        "lemma": "oportet",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "studeas",
        "lemma": "studeo",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "csubj",
        "head": 0,
        "current_role": "sujeto"
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
    "id": 205,
    "latin": "Cum sis bonus, te laudo.",
    "spanish": "Como eres bueno, te alabo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Cum",
        "lemma": "cum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "sis",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "bonus",
        "lemma": "bonus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "advcl",
        "head": 5,
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
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "obj",
        "head": 5,
        "current_role": "objeto_directo"
      },
      {
        "idx": 5,
        "word": "laudo",
        "lemma": "laudo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 206,
    "latin": "Dum spiro, spero.",
    "spanish": "Mientras respiro, espero.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dum",
        "lemma": "dum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 1,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "spiro",
        "lemma": "spiro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 3,
        "current_role": "oración_adverbial"
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
        "word": "spero",
        "lemma": "spero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 207,
    "latin": "Opto ut sis felix.",
    "spanish": "Deseo que seas feliz.",
    "tokens": [
      {
        "idx": 0,
        "word": "Opto",
        "lemma": "opto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "sis",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 3,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": "felix",
        "lemma": "felix",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
    "id": 208,
    "latin": "Nolo ut discedas.",
    "spanish": "No quiero que te marches.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nolo",
        "lemma": "nolo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "discedas",
        "lemma": "discedo",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 209,
    "latin": "Licet tibi ire.",
    "spanish": "Te es permitido ir.",
    "tokens": [
      {
        "idx": 0,
        "word": "Licet",
        "lemma": "licet",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "tibi",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Sing|Person=2",
        "dep": "obl:arg",
        "head": 2,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 2,
        "word": "ire",
        "lemma": "eo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 210,
    "latin": "Metuo ut veniat.",
    "spanish": "Temo que no venga.",
    "tokens": [
      {
        "idx": 0,
        "word": "Metuo",
        "lemma": "metuo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "veniat",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 211,
    "latin": "Cupio ut me ames.",
    "spanish": "Deseo que me ames.",
    "tokens": [
      {
        "idx": 0,
        "word": "Cupio",
        "lemma": "cupio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "me",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=1",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "ames",
        "lemma": "amo",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 212,
    "latin": "Scio te bonum esse.",
    "spanish": "Sé que eres bueno.",
    "tokens": [
      {
        "idx": 0,
        "word": "Scio",
        "lemma": "scio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "bonum",
        "lemma": "bonum",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
      },
      {
        "idx": 3,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
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
    "id": 213,
    "latin": "Dicit se venisse.",
    "spanish": "Dice que ha venido.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dicit",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "se",
        "lemma": "sui",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Plur|Person=3",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "venisse",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Tense=Past|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 214,
    "latin": "Putabam te dormire.",
    "spanish": "Pensaba que dormías.",
    "tokens": [
      {
        "idx": 0,
        "word": "Putabam",
        "lemma": "puto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "dormire",
        "lemma": "dormio",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 215,
    "latin": "Credo Deum esse.",
    "spanish": "Creo que Dios existe.",
    "tokens": [
      {
        "idx": 0,
        "word": "Credo",
        "lemma": "credo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "Deum",
        "lemma": "Deus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 216,
    "latin": "Audivi te aegrotare.",
    "spanish": "Oí que estabas enfermo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Audivi",
        "lemma": "audio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "aegrotare",
        "lemma": "aegroto",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 217,
    "latin": "Postquam venit, gaudebam.",
    "spanish": "Después de que vino, me alegraba.",
    "tokens": [
      {
        "idx": 0,
        "word": "Postquam",
        "lemma": "postquam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 1,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "venit",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 3,
        "current_role": "oración_adverbial"
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
        "word": "gaudebam",
        "lemma": "gaudeo",
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
      }
    ]
  },
  {
    "id": 218,
    "latin": "Priusquam eas, dic mihi.",
    "spanish": "Antes de que vayas, dime.",
    "tokens": [
      {
        "idx": 0,
        "word": "Priusquam",
        "lemma": "priusquam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "eas",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Fem|Number=Plur|Person=3",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
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
        "word": "dic",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "mihi",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Sing|Person=1",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "objeto_indirecto"
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
    "id": 219,
    "latin": "Simulac vidit, credidit.",
    "spanish": "Tan pronto como vio, creyó.",
    "tokens": [
      {
        "idx": 0,
        "word": "Simulac",
        "lemma": "simulac",
        "pos": "ADV",
        "morph": "",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "vidit",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
        "word": "credidit",
        "lemma": "credo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 1,
        "current_role": "elemento_coordinado"
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
    "id": 220,
    "latin": "Intellexi quid faceres.",
    "spanish": "Entendí qué hacías.",
    "tokens": [
      {
        "idx": 0,
        "word": "Intellexi",
        "lemma": "intellego",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "quid",
        "lemma": "quis",
        "pos": "PRON",
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
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 221,
    "latin": "Nescio quis sis.",
    "spanish": "No sé quién eres.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nescio",
        "lemma": "nescio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "quis",
        "lemma": "quis",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
      },
      {
        "idx": 2,
        "word": "sis",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
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
    "id": 222,
    "latin": "Errare humanum est.",
    "spanish": "Errar es humano.",
    "tokens": [
      {
        "idx": 0,
        "word": "Errare",
        "lemma": "erro",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Number=Sing|Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "csubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "humanum",
        "lemma": "humanus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
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
    "id": 223,
    "latin": "Vincere scis, Hannibal.",
    "spanish": "Sabes vencer, Aníbal.",
    "tokens": [
      {
        "idx": 0,
        "word": "Vincere",
        "lemma": "uinco",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 1,
        "current_role": "oración_completiva"
      },
      {
        "idx": 1,
        "word": "scis",
        "lemma": "scio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
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
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "Hannibal",
        "lemma": "Hannibal",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 1,
        "current_role": "vocativo"
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
    "id": 224,
    "latin": "Dulce et decorum est pro patria mori.",
    "spanish": "Dulce y decoroso es morir por la patria.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dulce",
        "lemma": "dulcis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
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
        "word": "decorum",
        "lemma": "decor",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
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
        "word": "pro",
        "lemma": "pro",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 5,
        "current_role": "preposición"
      },
      {
        "idx": 5,
        "word": "patria",
        "lemma": "patria",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 6,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 6,
        "word": "mori",
        "lemma": "morior",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Pass",
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
    "id": 225,
    "latin": "Constat terram rotundam esse.",
    "spanish": "Consta que la tierra es redonda.",
    "tokens": [
      {
        "idx": 0,
        "word": "Constat",
        "lemma": "consto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "terram",
        "lemma": "terra",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "rotundam",
        "lemma": "rotundus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
      },
      {
        "idx": 3,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
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
    "id": 226,
    "latin": "Promittit se venturum esse.",
    "spanish": "Promete que vendrá.",
    "tokens": [
      {
        "idx": 0,
        "word": "Promittit",
        "lemma": "promitto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "venturum",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Case=Acc|Gender=Masc|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
      },
      {
        "idx": 3,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
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
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 227,
    "latin": "Spero te valere.",
    "spanish": "Espero que estés bien.",
    "tokens": [
      {
        "idx": 0,
        "word": "Spero",
        "lemma": "spero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "valere",
        "lemma": "ualeo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 0,
        "current_role": "oración_completiva"
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
    "id": 228,
    "latin": "Videtur esse verum.",
    "spanish": "Parece ser verdad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Videtur",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "verum",
        "lemma": "uerus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "xcomp",
        "head": 0,
        "current_role": "complemento_predicativo"
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
    "id": 229,
    "latin": "Negat se pecuniam cepisse.",
    "spanish": "Niega haber tomado el dinero.",
    "tokens": [
      {
        "idx": 0,
        "word": "Negat",
        "lemma": "nego",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
        "word": "cepisse",
        "lemma": "capio",
        "pos": "VERB",
        "morph": "Tense=Past|VerbForm=Inf|Voice=Act",
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
    "id": 230,
    "latin": "Apparet eum mentiri.",
    "spanish": "Aparece que él miente.",
    "tokens": [
      {
        "idx": 0,
        "word": "Apparet",
        "lemma": "appareo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "eum",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Masc|Number=Sing|Person=3",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "mentiri",
        "lemma": "mentior",
        "pos": "VERB",
        "morph": "Case=Acc|Gender=Neut|Number=Sing|Tense=Pres|VerbForm=Inf|Voice=Pass",
        "dep": "csubj",
        "head": 0,
        "current_role": "sujeto"
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
    "id": 231,
    "latin": "Opinionem meam mutare nolo.",
    "spanish": "No quiero cambiar mi opinión.",
    "tokens": [
      {
        "idx": 0,
        "word": "Opinionem",
        "lemma": "opinio",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "meam",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "mutare",
        "lemma": "muto",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 3,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 3,
        "word": "nolo",
        "lemma": "nolo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 232,
    "latin": "Frater meus est altior quam ego, sed ego sum celerior.",
    "spanish": "Mi hermano es más alto que yo, pero yo soy más rápido.",
    "tokens": [
      {
        "idx": 0,
        "word": "Frater",
        "lemma": "frater",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "meus",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 0,
        "current_role": "modificador_adjetival"
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
        "word": "altior",
        "lemma": "altus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "quam",
        "lemma": "quam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 5,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 5,
        "word": "ego",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Sing|Person=1",
        "dep": "advcl:cmp",
        "head": 3,
        "current_role": "otro"
      },
      {
        "idx": 6,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 10,
        "current_role": "puntuación"
      },
      {
        "idx": 7,
        "word": "sed",
        "lemma": "sed",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 10,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 8,
        "word": "ego",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Sing|Person=1",
        "dep": "nsubj",
        "head": 10,
        "current_role": "sujeto"
      },
      {
        "idx": 9,
        "word": "sum",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 10,
        "current_role": "cópula"
      },
      {
        "idx": 10,
        "word": "celerior",
        "lemma": "celer",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 3,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 11,
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
    "id": 233,
    "latin": "Ille, qui fortis est, non timet.",
    "spanish": "Aquel, que es fuerte, no teme.",
    "tokens": [
      {
        "idx": 0,
        "word": "Ille",
        "lemma": "ille",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 7,
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
        "word": "fortis",
        "lemma": "fortis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "acl:relcl",
        "head": 0,
        "current_role": "oración_de_relativo"
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
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      },
      {
        "idx": 6,
        "word": "non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 7,
        "current_role": "modificador"
      },
      {
        "idx": 7,
        "word": "timet",
        "lemma": "timeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 234,
    "latin": "Milites a duce laudantur, quod fortiter pugnaverunt.",
    "spanish": "Los soldados son alabados por el líder, porque lucharon valientemente.",
    "tokens": [
      {
        "idx": 0,
        "word": "Milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "a",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "duce",
        "lemma": "dux",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "laudantur",
        "lemma": "laudo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
        "head": 7,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "quod",
        "lemma": "quod",
        "pos": "SCONJ",
        "morph": "",
        "dep": "obj",
        "head": 7,
        "current_role": "objeto_directo"
      },
      {
        "idx": 6,
        "word": "fortiter",
        "lemma": "fortiter",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 7,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 7,
        "word": "pugnaverunt",
        "lemma": "pugno",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "acl:relcl",
        "head": 0,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 8,
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
    "id": 235,
    "latin": "Postquam hostes fugerant, Caesar castra movit.",
    "spanish": "Después de que los enemigos habían huido, César movió el campamento.",
    "tokens": [
      {
        "idx": 0,
        "word": "Postquam",
        "lemma": "postquam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "hostes",
        "lemma": "hostis",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "fugerant",
        "lemma": "fugio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pqp|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 6,
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
        "word": "castra",
        "lemma": "castra",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 6,
        "current_role": "objeto_directo"
      },
      {
        "idx": 6,
        "word": "movit",
        "lemma": "moueo",
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
    "id": 236,
    "latin": "Dum libri leguntur, pueri silent.",
    "spanish": "Mientras los libros son leídos, los niños callan.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dum",
        "lemma": "dum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "libri",
        "lemma": "liber",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj:pass",
        "head": 2,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 2,
        "word": "leguntur",
        "lemma": "lego",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "advcl",
        "head": 5,
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
        "word": "pueri",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "silent",
        "lemma": "sileo",
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
    "id": 237,
    "latin": "Urbe capta, milites gaudebant.",
    "spanish": "Capturada la ciudad, los soldados se alegraban.",
    "tokens": [
      {
        "idx": 0,
        "word": "Urbe",
        "lemma": "Urbs",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "capta",
        "lemma": "capio",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
        "word": "milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "gaudebant",
        "lemma": "gaudeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 238,
    "latin": "Proficiscamur ad urbem ut amicos videamus.",
    "spanish": "Partamos a la ciudad para ver a los amigos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Proficiscamur",
        "lemma": "",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
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
        "word": "urbem",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 5,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 4,
        "word": "amicos",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 5,
        "current_role": "objeto_directo"
      },
      {
        "idx": 5,
        "word": "videamus",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 0,
        "current_role": "oración_adverbial"
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
    "id": 239,
    "latin": "Impero tibi ut venias.",
    "spanish": "Te ordeno que vengas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Impero",
        "lemma": "impero",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "tibi",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Sing|Person=2",
        "dep": "obl:arg",
        "head": 0,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 2,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 3,
        "word": "venias",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 240,
    "latin": "Nesciebam quis hoc fecisset.",
    "spanish": "No sabía quién había hecho esto.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nesciebam",
        "lemma": "nescio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "quis",
        "lemma": "quis",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "hoc",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "fecisset",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pqp|VerbForm=Fin|Voice=Act",
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
  }
]