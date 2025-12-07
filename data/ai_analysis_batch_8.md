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
  }
]