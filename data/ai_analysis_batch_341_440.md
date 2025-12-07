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
    "id": 341,
    "latin": "Eo Romam.",
    "spanish": "Voy a Roma.",
    "tokens": [
      {
        "idx": 0,
        "word": "Eo",
        "lemma": "eo",
        "pos": "ADV",
        "morph": "",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "Romam",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl:arg",
        "head": 0,
        "current_role": "complemento_obligatorio"
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
    "id": 342,
    "latin": "Redeo domum.",
    "spanish": "Regreso a casa.",
    "tokens": [
      {
        "idx": 0,
        "word": "Redeo",
        "lemma": "redeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "domum",
        "lemma": "domus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
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
    "id": 343,
    "latin": "Hostes perierunt.",
    "spanish": "Los enemigos perecieron.",
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
        "word": "perierunt",
        "lemma": "pereo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 344,
    "latin": "Fero et ferior.",
    "spanish": "Golpeo y soy golpeado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fero",
        "lemma": "fero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
        "word": "ferior",
        "lemma": "ferus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
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
    "id": 345,
    "latin": "Tolle, lege.",
    "spanish": "Toma, lee.",
    "tokens": [
      {
        "idx": 0,
        "word": "Tolle",
        "lemma": "tollo",
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
        "word": "lege",
        "lemma": "lex",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
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
    "id": 346,
    "latin": "Auxilium afferte!",
    "spanish": "¡Traed ayuda!",
    "tokens": [
      {
        "idx": 0,
        "word": "Auxilium",
        "lemma": "auxilium",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "afferte",
        "lemma": "affero",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "!",
        "lemma": "!",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 347,
    "latin": "Confer haec cum illis.",
    "spanish": "Compara estas cosas con aquellas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Confer",
        "lemma": "confero",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "haec",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "cum",
        "lemma": "cum",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "illis",
        "lemma": "ille",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
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
    "id": 348,
    "latin": "Exeunt omnes.",
    "spanish": "Salen todos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Exeunt",
        "lemma": "exeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "omnes",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
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
    "id": 349,
    "latin": "Fiat lux.",
    "spanish": "Hágase la luz.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fiat",
        "lemma": "fio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "lux",
        "lemma": "lux",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
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
    "id": 350,
    "latin": "Consul, urbem videns, laetus erat.",
    "spanish": "El cónsul, viendo la ciudad, estaba contento.",
    "tokens": [
      {
        "idx": 0,
        "word": "Consul",
        "lemma": "consul",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
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
        "word": "videns",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Pres|VerbForm=Part|Voice=Act",
        "dep": "advcl",
        "head": 5,
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
        "word": "laetus",
        "lemma": "laetus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": "erat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
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
        "head": 5,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 351,
    "latin": "Sole oriente, consul laetus erat.",
    "spanish": "Al salir el sol, el cónsul estaba contento.",
    "tokens": [
      {
        "idx": 0,
        "word": "Sole",
        "lemma": "sol",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "oriente",
        "lemma": "oriens",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Masc|Number=Sing|Tense=Pres|VerbForm=Part|Voice=Act",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
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
        "word": "consul",
        "lemma": "consul",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
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
        "word": "erat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
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
    "id": 352,
    "latin": "Cupidus urbis videndae sum.",
    "spanish": "Estoy deseoso de ver la ciudad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Cupidus",
        "lemma": "cupidus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 2,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "urbis",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "obl:arg",
        "head": 0,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 2,
        "word": "videndae",
        "lemma": "uidendus",
        "pos": "VERB",
        "morph": "Case=Gen|Gender=Fem|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "sum",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin",
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
    "id": 353,
    "latin": "Pugnandum est pro patria.",
    "spanish": "Se debe luchar por la patria.",
    "tokens": [
      {
        "idx": 0,
        "word": "Pugnandum",
        "lemma": "pugno",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
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
        "dep": "aux:pass",
        "head": 0,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 2,
        "word": "pro",
        "lemma": "pro",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "patria",
        "lemma": "patria",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
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
    "id": 354,
    "latin": "Cum Caesar venisset, omnes gaudebant.",
    "spanish": "Cuando César hubo llegado, todos se alegraban.",
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
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "venisset",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pqp|VerbForm=Fin|Voice=Act",
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
        "word": "omnes",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "gaudebant",
        "lemma": "gaudeo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 355,
    "latin": "Milites pugnabant ut urbem defenderent.",
    "spanish": "Los soldados luchaban para defender la ciudad.",
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
        "word": "pugnabant",
        "lemma": "pugno",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "ut",
        "lemma": "ut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 4,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 3,
        "word": "urbem",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "defenderent",
        "lemma": "defendo",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 1,
        "current_role": "oración_adverbial"
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
    "id": 356,
    "latin": "Si hoc dixisses, erravisses.",
    "spanish": "Si hubieras dicho esto, te habrías equivocado.",
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
        "word": "dixisses",
        "lemma": "dico",
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
        "word": "erravisses",
        "lemma": "erro",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pqp|VerbForm=Fin|Voice=Act",
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
    "id": 357,
    "latin": "Caesar dixit se Romam iturum esse.",
    "spanish": "César dijo que él iría a Roma.",
    "tokens": [
      {
        "idx": 0,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "dixit",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
        "word": "Romam",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl:arg",
        "head": 4,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 4,
        "word": "iturum",
        "lemma": "eo",
        "pos": "VERB",
        "morph": "Case=Acc|Gender=Masc|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Act",
        "dep": "ccomp",
        "head": 1,
        "current_role": "oración_completiva"
      },
      {
        "idx": 5,
        "word": "esse",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Tense=Pres|VerbForm=Inf",
        "dep": "aux",
        "head": 4,
        "current_role": "auxiliar"
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
    "id": 358,
    "latin": "Fiat voluntas tua.",
    "spanish": "Hágase tu voluntad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fiat",
        "lemma": "fio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "voluntas",
        "lemma": "uoluntas",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "tua",
        "lemma": "tuus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "modificador_adjetival"
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
    "id": 359,
    "latin": "Gallia est omnis divisa in partes tres.",
    "spanish": "Toda la Galia está dividida en tres partes.",
    "tokens": [
      {
        "idx": 0,
        "word": "Gallia",
        "lemma": "Gallia",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 3,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 2,
        "word": "omnis",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 3,
        "word": "divisa",
        "lemma": "diuido",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
        "word": "partes",
        "lemma": "pars",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 6,
        "word": "tres",
        "lemma": "tres",
        "pos": "NUM",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "nummod",
        "head": 5,
        "current_role": "modificador_numeral"
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
    "id": 360,
    "latin": "Belgae unam partem incolunt.",
    "spanish": "Los belgas habitan una parte.",
    "tokens": [
      {
        "idx": 0,
        "word": "Belgae",
        "lemma": "Belgae",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "unam",
        "lemma": "unus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "nummod",
        "head": 2,
        "current_role": "modificador_numeral"
      },
      {
        "idx": 2,
        "word": "partem",
        "lemma": "pars",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
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
    "id": 361,
    "latin": "Aquitani aliam partem incolunt.",
    "spanish": "Los aquitanos habitan otra parte.",
    "tokens": [
      {
        "idx": 0,
        "word": "Aquitani",
        "lemma": "Aquitani",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "aliam",
        "lemma": "alius",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 2,
        "current_role": "determinante"
      },
      {
        "idx": 2,
        "word": "partem",
        "lemma": "pars",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
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
    "id": 362,
    "latin": "Horum omnium fortissimi sunt Belgae.",
    "spanish": "De todos estos, los más fuertes son los belgas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Horum",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Gen|Gender=Neut|Number=Plur",
        "dep": "nmod",
        "head": 2,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 1,
        "word": "omnium",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 0,
        "current_role": "determinante"
      },
      {
        "idx": 2,
        "word": "fortissimi",
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
        "word": "Belgae",
        "lemma": "Belgae",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
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
    "id": 363,
    "latin": "Helvetii cum Germanis contendunt.",
    "spanish": "Los helvecios luchan con los germanos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Helvetii",
        "lemma": "Heluetii",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
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
        "word": "Germanis",
        "lemma": "Germani",
        "pos": "PROPN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "contendunt",
        "lemma": "contendo",
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
    "id": 364,
    "latin": "Caesar legatos ad eum misit.",
    "spanish": "César envió embajadores a él.",
    "tokens": [
      {
        "idx": 0,
        "word": "Caesar",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "legatos",
        "lemma": "legatus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "ad",
        "lemma": "ad",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 3,
        "current_role": "preposición"
      },
      {
        "idx": 3,
        "word": "eum",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Masc|Number=Sing|Person=3",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "misit",
        "lemma": "mitto",
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
    "id": 365,
    "latin": "Flumen Rhenus agros dividit.",
    "spanish": "El río Rin divide los campos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Flumen",
        "lemma": "flumen",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "Rhenus",
        "lemma": "Rhenus",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "agros",
        "lemma": "ager",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "dividit",
        "lemma": "diuido",
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
    "id": 366,
    "latin": "Milites castra posuerunt.",
    "spanish": "Los soldados establecieron el campamento.",
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
        "word": "castra",
        "lemma": "castra",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "posuerunt",
        "lemma": "pono",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 367,
    "latin": "Imperator copias eduxit.",
    "spanish": "El general sacó las tropas.",
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
        "word": "copias",
        "lemma": "copia",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "eduxit",
        "lemma": "educo",
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
    "id": 368,
    "latin": "Caesar in Galliam venit.",
    "spanish": "César vino a la Galia.",
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
        "word": "Galliam",
        "lemma": "Gallia",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "venit",
        "lemma": "uenio",
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
    "id": 369,
    "latin": "Quousque tandem abutere patientia nostra?",
    "spanish": "¿Hasta cuándo abusarás de nuestra paciencia?",
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
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "patientia",
        "lemma": "patientia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "nostra",
        "lemma": "noster",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 5,
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
    "id": 370,
    "latin": "O tempora, o mores!",
    "spanish": "¡Oh tiempos, oh costumbres!",
    "tokens": [
      {
        "idx": 0,
        "word": "O",
        "lemma": "o",
        "pos": "INTJ",
        "morph": "",
        "dep": "advmod:emph",
        "head": 1,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "tempora",
        "lemma": "tempus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
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
        "head": 4,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "o",
        "lemma": "o",
        "pos": "INTJ",
        "morph": "",
        "dep": "advmod:emph",
        "head": 4,
        "current_role": "modificador"
      },
      {
        "idx": 4,
        "word": "mores",
        "lemma": "mos",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "appos",
        "head": 1,
        "current_role": "aposición"
      },
      {
        "idx": 5,
        "word": "!",
        "lemma": "!",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 371,
    "latin": "Senatus haec intellegit.",
    "spanish": "El senado entiende estas cosas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Senatus",
        "lemma": "senatus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "haec",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "intellegit",
        "lemma": "intellego",
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
    "id": 372,
    "latin": "Consul videt.",
    "spanish": "El cónsul (lo) ve.",
    "tokens": [
      {
        "idx": 0,
        "word": "Consul",
        "lemma": "consul",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "videt",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 373,
    "latin": "Hic tamen vivit.",
    "spanish": "Este, sin embargo, vive.",
    "tokens": [
      {
        "idx": 0,
        "word": "Hic",
        "lemma": "hic",
        "pos": "ADV",
        "morph": "",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "tamen",
        "lemma": "tamen",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 2,
        "word": "vivit",
        "lemma": "uiuo",
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
    "id": 374,
    "latin": "Vivit? Immo vero etiam in senatum venit.",
    "spanish": "¿Vive? Más aún, incluso viene al senado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Vivit",
        "lemma": "uiuo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
      },
      {
        "idx": 2,
        "word": "Immo",
        "lemma": "immo",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 7,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 3,
        "word": "vero",
        "lemma": "uero",
        "pos": "ADV",
        "morph": "",
        "dep": "discourse",
        "head": 7,
        "current_role": "marcador_discursivo"
      },
      {
        "idx": 4,
        "word": "etiam",
        "lemma": "etiam",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:emph",
        "head": 6,
        "current_role": "modificador"
      },
      {
        "idx": 5,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 6,
        "current_role": "preposición"
      },
      {
        "idx": 6,
        "word": "senatum",
        "lemma": "senatus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 7,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 7,
        "word": "venit",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
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
    "id": 375,
    "latin": "Nos autem viri fortes sumus.",
    "spanish": "Nosotros, en cambio, somos hombres fuertes.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nos",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Nom|Number=Plur|Person=1",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "autem",
        "lemma": "autem",
        "pos": "PART",
        "morph": "",
        "dep": "discourse",
        "head": 2,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 2,
        "word": "viri",
        "lemma": "uir",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "fortes",
        "lemma": "fortis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "sumus",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin",
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
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 376,
    "latin": "Catilina, nobiscum esse non potes.",
    "spanish": "Catilina, no puedes estar con nosotros.",
    "tokens": [
      {
        "idx": 0,
        "word": "Catilina",
        "lemma": "Catilina",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "nobiscum",
        "lemma": "nobiscus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "xcomp",
        "head": 5,
        "current_role": "complemento_predicativo"
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
        "word": "non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 5,
        "current_role": "modificador"
      },
      {
        "idx": 5,
        "word": "potes",
        "lemma": "possum",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 377,
    "latin": "Egredere ex urbe, Catilina.",
    "spanish": "Sal de la ciudad, Catilina.",
    "tokens": [
      {
        "idx": 0,
        "word": "Egredere",
        "lemma": "egredero",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "ex",
        "lemma": "ex",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 2,
        "current_role": "preposición"
      },
      {
        "idx": 2,
        "word": "urbe",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
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
        "head": 0,
        "current_role": "vocativo"
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
    "id": 378,
    "latin": "Patria te odit ac metuit.",
    "spanish": "La patria te odia y te teme.",
    "tokens": [
      {
        "idx": 0,
        "word": "Patria",
        "lemma": "patria",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
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
        "word": "odit",
        "lemma": "odi",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "ac",
        "lemma": "ac",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 4,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 4,
        "word": "metuit",
        "lemma": "metuo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 379,
    "latin": "Lucius Catilina nobili genere natus est.",
    "spanish": "Lucio Catilina nació de noble linaje.",
    "tokens": [
      {
        "idx": 0,
        "word": "Lucius",
        "lemma": "Lucius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 4,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "Catilina",
        "lemma": "Catilina",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj:pass",
        "head": 4,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 2,
        "word": "nobili",
        "lemma": "nobilis",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "amod",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "genere",
        "lemma": "genus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "natus",
        "lemma": "nascor",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 380,
    "latin": "Fuit magna vi animi et corporis.",
    "spanish": "Fue de gran fuerza de espíritu y de cuerpo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fuit",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 1,
        "word": "magna",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "vi",
        "lemma": "uis",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "animi",
        "lemma": "animus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 2,
        "current_role": "complemento_del_nombre"
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
        "word": "corporis",
        "lemma": "corpus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Neut|Number=Sing",
        "dep": "conj",
        "head": 3,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 6,
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
    "id": 381,
    "latin": "Ingenio malo pravoque erat.",
    "spanish": "Era de carácter malo y depravado.",
    "tokens": [
      {
        "idx": 0,
        "word": "Ingenio",
        "lemma": "ingenium",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "malo",
        "lemma": "malum",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "pravo",
        "lemma": "prauus",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": "que",
        "lemma": "que",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 2,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 4,
        "word": "erat",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 0,
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
    "id": 382,
    "latin": "Huic ab adulescentia bella intestina grata fuerunt.",
    "spanish": "A este, desde la adolescencia, le fueron gratas las guerras civiles.",
    "tokens": [
      {
        "idx": 0,
        "word": "Huic",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Dat|Gender=Fem|Number=Sing",
        "dep": "obl:arg",
        "head": 5,
        "current_role": "complemento_obligatorio"
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
        "word": "adulescentia",
        "lemma": "adulescentia",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "bella",
        "lemma": "bellum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "intestina",
        "lemma": "intestinus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Plur",
        "dep": "amod",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 5,
        "word": "grata",
        "lemma": "gratus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Plur",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": "fuerunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin",
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
        "head": 5,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 383,
    "latin": "Corpus patiens inediae erat.",
    "spanish": "Su cuerpo era capaz de soportar el ayuno.",
    "tokens": [
      {
        "idx": 0,
        "word": "Corpus",
        "lemma": "corpus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "patiens",
        "lemma": "patiens",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "inediae",
        "lemma": "inedia",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 3,
        "word": "erat",
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
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 384,
    "latin": "Alieni appetens, sui profusus.",
    "spanish": "Deseoso de lo ajeno, derrochador de lo propio.",
    "tokens": [
      {
        "idx": 0,
        "word": "Alieni",
        "lemma": "Alienus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "appetens",
        "lemma": "appeteo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Pres|VerbForm=Part|Voice=Act",
        "dep": "acl",
        "head": 0,
        "current_role": "oración_adjetiva"
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
        "word": "sui",
        "lemma": "suus",
        "pos": "PRON",
        "morph": "Case=Gen|Number=Sing|Person=3",
        "dep": "det",
        "head": 4,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "profusus",
        "lemma": "profusus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 385,
    "latin": "Satis eloquentiae, sapientiae parum.",
    "spanish": "Suficiente elocuencia, poca sabiduría.",
    "tokens": [
      {
        "idx": 0,
        "word": "Satis",
        "lemma": "satis",
        "pos": "ADV",
        "morph": "",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "eloquentiae",
        "lemma": "eloquentia",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "obl:arg",
        "head": 0,
        "current_role": "complemento_obligatorio"
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
        "word": "sapientiae",
        "lemma": "sapientia",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 4,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 4,
        "word": "parum",
        "lemma": "parum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "advmod",
        "head": 0,
        "current_role": "modificador_adverbial"
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
    "id": 386,
    "latin": "Vastus animus immoderata cupiebat.",
    "spanish": "Su espíritu insaciable deseaba cosas desmesuradas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Vastus",
        "lemma": "uastus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "animus",
        "lemma": "animus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "immoderata",
        "lemma": "immoderatus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "xcomp",
        "head": 3,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 3,
        "word": "cupiebat",
        "lemma": "cupio",
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
    "id": 387,
    "latin": "Civitas corrupta erat.",
    "spanish": "La ciudad estaba corrompida.",
    "tokens": [
      {
        "idx": 0,
        "word": "Civitas",
        "lemma": "ciuitas",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 1,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 1,
        "word": "corrupta",
        "lemma": "corrumpo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
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
    "id": 388,
    "latin": "Divitiae morum bonorum ruinam effecerunt.",
    "spanish": "Las riquezas causaron la ruina de las buenas costumbres.",
    "tokens": [
      {
        "idx": 0,
        "word": "Divitiae",
        "lemma": "divitius",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "morum",
        "lemma": "mos",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 3,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "bonorum",
        "lemma": "bonus",
        "pos": "ADJ",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "ruinam",
        "lemma": "ruina",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "effecerunt",
        "lemma": "efficio",
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
    "id": 389,
    "latin": "Vivamus, mea Lesbia, atque amemus.",
    "spanish": "Vivamos, mi Lesbia, y amemos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Vivamus",
        "lemma": "uiuo",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "mea",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "Lesbia",
        "lemma": "Lesbia",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 4,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 6,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "atque",
        "lemma": "atque",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 6,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 6,
        "word": "amemus",
        "lemma": "amo",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 390,
    "latin": "Da mihi basia mille.",
    "spanish": "Dame mil besos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Da",
        "lemma": "do",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "mihi",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Sing|Person=1",
        "dep": "obl:arg",
        "head": 0,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 2,
        "word": "basia",
        "lemma": "basia",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "mille",
        "lemma": "mille",
        "pos": "NUM",
        "morph": "Number=Plural",
        "dep": "nummod",
        "head": 2,
        "current_role": "modificador_numeral"
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
    "id": 391,
    "latin": "Soles occidere et redire possunt.",
    "spanish": "Los soles pueden ponerse y volver.",
    "tokens": [
      {
        "idx": 0,
        "word": "Soles",
        "lemma": "sol",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "occidere",
        "lemma": "occido",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 4,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 2,
        "word": "et",
        "lemma": "et",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 4,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 3,
        "word": "redire",
        "lemma": "redeo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "xcomp",
        "head": 4,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 4,
        "word": "possunt",
        "lemma": "possum",
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
    "id": 392,
    "latin": "Nobis una nox dormienda est.",
    "spanish": "Nosotros debemos dormir una sola noche.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nobis",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Plur|Person=1",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "una",
        "lemma": "unus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nummod",
        "head": 2,
        "current_role": "modificador_numeral"
      },
      {
        "idx": 2,
        "word": "nox",
        "lemma": "nox",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj:pass",
        "head": 3,
        "current_role": "sujeto_paciente"
      },
      {
        "idx": 3,
        "word": "dormienda",
        "lemma": "dormiendus",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Fem|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
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
    "id": 393,
    "latin": "Lugete, o Veneres Cupidinesque.",
    "spanish": "Llorad, oh Venus y Cupidos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Lugete",
        "lemma": "lugeo",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
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
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "o",
        "lemma": "o",
        "pos": "INTJ",
        "morph": "",
        "dep": "advmod:emph",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 3,
        "word": "Veneres",
        "lemma": "Venus",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "amod",
        "head": 4,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "Cupidines",
        "lemma": "cupido",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 5,
        "word": "que",
        "lemma": "que",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 4,
        "current_role": "conjunción_coordinante"
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
    "id": 394,
    "latin": "Passer mortuus est meae puellae.",
    "spanish": "El gorrión de mi niña ha muerto.",
    "tokens": [
      {
        "idx": 0,
        "word": "Passer",
        "lemma": "passer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "mortuus",
        "lemma": "morior",
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
        "word": "meae",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 4,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "puellae",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
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
    "id": 395,
    "latin": "Miser Catulle, desinas ineptire.",
    "spanish": "Miserable Catulo, deja de hacer tonterías.",
    "tokens": [
      {
        "idx": 0,
        "word": "Miser",
        "lemma": "miser",
        "pos": "ADJ",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "Catulle",
        "lemma": "Catullus",
        "pos": "PROPN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
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
        "word": "desinas",
        "lemma": "desino",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "ineptire",
        "lemma": "ineptio",
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
    "id": 396,
    "latin": "Nulli se dicit mulier mea nubere malle.",
    "spanish": "Mi mujer dice que prefiere no casarse con nadie.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nulli",
        "lemma": "nullus",
        "pos": "DET",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "obl:arg",
        "head": 2,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 1,
        "word": "se",
        "lemma": "sui",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=3",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "dicit",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "mulier",
        "lemma": "mulier",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "mea",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 5,
        "word": "nubere",
        "lemma": "nubo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 6,
        "current_role": "oración_completiva"
      },
      {
        "idx": 6,
        "word": "malle",
        "lemma": "malo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 2,
        "current_role": "oración_completiva"
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
    "id": 397,
    "latin": "Sed mulier cupido quod dicit amanti...",
    "spanish": "Pero lo que la mujer dice a su amante deseoso...",
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
        "word": "mulier",
        "lemma": "mulier",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "cupido",
        "lemma": "cupido",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "quod",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "dicit",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "acl:relcl",
        "head": 2,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 5,
        "word": "amanti",
        "lemma": "amo",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "ccomp",
        "head": 4,
        "current_role": "oración_completiva"
      },
      {
        "idx": 6,
        "word": "...",
        "lemma": "...siastes",
        "pos": "X",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 398,
    "latin": "Arma virumque cano.",
    "spanish": "Canto a las armas y al hombre.",
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
    "id": 399,
    "latin": "Troiae qui primus ab oris venit.",
    "spanish": "Quien vino primero desde las costas de Troya.",
    "tokens": [
      {
        "idx": 0,
        "word": "Troiae",
        "lemma": "Troia",
        "pos": "PROPN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "primus",
        "lemma": "primus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "advcl:pred",
        "head": 5,
        "current_role": "otro"
      },
      {
        "idx": 3,
        "word": "ab",
        "lemma": "ab",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 4,
        "current_role": "preposición"
      },
      {
        "idx": 4,
        "word": "oris",
        "lemma": "ora",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Plur",
        "dep": "nmod",
        "head": 2,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 5,
        "word": "venit",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "acl:relcl",
        "head": 0,
        "current_role": "oración_de_relativo"
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
    "id": 400,
    "latin": "Multum ille et terris iactatus et alto.",
    "spanish": "Él, muy sacudido tanto en tierra como en alta mar.",
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
  },
  {
    "id": 401,
    "latin": "Tantae molis erat Romanam condere gentem.",
    "spanish": "De tan gran esfuerzo era fundar la nación romana.",
    "tokens": [
      {
        "idx": 0,
        "word": "Tantae",
        "lemma": "tantus",
        "pos": "DET",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "molis",
        "lemma": "moles",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
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
        "dep": "cop",
        "head": 1,
        "current_role": "cópula"
      },
      {
        "idx": 3,
        "word": "Romanam",
        "lemma": "romanus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 5,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 4,
        "word": "condere",
        "lemma": "condo",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "csubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "gentem",
        "lemma": "gens",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
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
    "id": 402,
    "latin": "O fortunati, quorum iam moenia surgunt!",
    "spanish": "¡Oh afortunados, cuyas murallas ya se levantan!",
    "tokens": [
      {
        "idx": 0,
        "word": "O",
        "lemma": "o",
        "pos": "INTJ",
        "morph": "",
        "dep": "advmod:emph",
        "head": 1,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "fortunati",
        "lemma": "fortunatus",
        "pos": "ADJ",
        "morph": "Case=Voc|Gender=Masc|Number=Plur",
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
        "head": 6,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "quorum",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 5,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 4,
        "word": "iam",
        "lemma": "iam",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 6,
        "current_role": "modificador"
      },
      {
        "idx": 5,
        "word": "moenia",
        "lemma": "moenia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Plur",
        "dep": "nsubj",
        "head": 6,
        "current_role": "sujeto"
      },
      {
        "idx": 6,
        "word": "surgunt",
        "lemma": "surgo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "acl:relcl",
        "head": 1,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 7,
        "word": "!",
        "lemma": "!",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 403,
    "latin": "Timeo Danaos et dona ferentes.",
    "spanish": "Temo a los griegos incluso cuando traen regalos.",
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
        "word": "Danaos",
        "lemma": "Danaus",
        "pos": "PROPN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 0,
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
        "word": "dona",
        "lemma": "donum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "ferentes",
        "lemma": "fero",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Masc|Number=Plur|Tense=Pres|VerbForm=Part|Voice=Act",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
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
    "id": 404,
    "latin": "Dux femina facti.",
    "spanish": "Una mujer fue la líder de la hazaña.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dux",
        "lemma": "dux",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "femina",
        "lemma": "femina",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "facti",
        "lemma": "factum",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Neut|Number=Sing",
        "dep": "acl",
        "head": 1,
        "current_role": "oración_adjetiva"
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
    "id": 405,
    "latin": "Amor omnibus idem.",
    "spanish": "El amor es el mismo para todos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Amor",
        "lemma": "amor",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "omnibus",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "idem",
        "lemma": "idem",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
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
    "id": 406,
    "latin": "Labor omnia vincit.",
    "spanish": "El trabajo lo vence todo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Labor",
        "lemma": "labor",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
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
        "word": "vincit",
        "lemma": "uincio",
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
    "id": 407,
    "latin": "Fama, malum qua non aliud velocius ullum.",
    "spanish": "La Fama, mal del cual ningún otro es más veloz.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fama",
        "lemma": "fama",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
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
        "word": "malum",
        "lemma": "malum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": "qua",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 5,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 5,
        "current_role": "modificador"
      },
      {
        "idx": 5,
        "word": "aliud",
        "lemma": "alius",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "acl:relcl",
        "head": 2,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 6,
        "word": "velocius",
        "lemma": "uelocius",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "orphan",
        "head": 5,
        "current_role": "huérfano"
      },
      {
        "idx": 7,
        "word": "ullum",
        "lemma": "ullus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "det",
        "head": 2,
        "current_role": "determinante"
      },
      {
        "idx": 8,
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
    "id": 408,
    "latin": "Carpe diem.",
    "spanish": "Aprovecha el día.",
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
    "id": 409,
    "latin": "Nunc est bibendum.",
    "spanish": "Ahora hay que beber.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nunc",
        "lemma": "nunc",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 2,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 2,
        "current_role": "auxiliar_pasivo"
      },
      {
        "idx": 2,
        "word": "bibendum",
        "lemma": "bibo",
        "pos": "VERB",
        "morph": "Case=Nom|Gender=Neut|Mood=Gdv|Number=Sing|Tense=Fut|VerbForm=Part|Voice=Pass",
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
    "id": 410,
    "latin": "Aurea mediocritas.",
    "spanish": "La dorada medianía.",
    "tokens": [
      {
        "idx": 0,
        "word": "Aurea",
        "lemma": "aureus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "mediocritas",
        "lemma": "mediocritas",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
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
    "id": 411,
    "latin": "Eheu fugaces, Postume, labuntur anni.",
    "spanish": "Ay, Póstumo, los años fugaces se escapan.",
    "tokens": [
      {
        "idx": 0,
        "word": "Eheu",
        "lemma": "eheu",
        "pos": "INTJ",
        "morph": "",
        "dep": "advmod:emph",
        "head": 5,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "fugaces",
        "lemma": "fugax",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "vocative",
        "head": 5,
        "current_role": "vocativo"
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
        "word": "Postume",
        "lemma": "postumus",
        "pos": "PROPN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "conj",
        "head": 1,
        "current_role": "elemento_coordinado"
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
        "word": "labuntur",
        "lemma": "labor",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": "anni",
        "lemma": "annus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
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
    "id": 412,
    "latin": "Non omnis moriar.",
    "spanish": "No moriré del todo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 1,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "omnis",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "moriar",
        "lemma": "morior",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 413,
    "latin": "Exegi monumentum aere perennius.",
    "spanish": "He levantado un monumento más duradero que el bronce.",
    "tokens": [
      {
        "idx": 0,
        "word": "Exegi",
        "lemma": "exigo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "monumentum",
        "lemma": "monumentum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "aere",
        "lemma": "aes",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "perennius",
        "lemma": "perennus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
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
    "id": 414,
    "latin": "Beatus ille qui procul negotiis...",
    "spanish": "Dichoso aquel que lejos de los negocios...",
    "tokens": [
      {
        "idx": 0,
        "word": "Beatus",
        "lemma": "beatus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
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
        "word": "procul",
        "lemma": "procul",
        "pos": "ADV",
        "morph": "",
        "dep": "acl:relcl",
        "head": 0,
        "current_role": "oración_de_relativo"
      },
      {
        "idx": 4,
        "word": "negotiis",
        "lemma": "negotium",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Plur",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 5,
        "word": "...",
        "lemma": "...archia",
        "pos": "X",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 415,
    "latin": "Odi profanum vulgus.",
    "spanish": "Odio al vulgo profano.",
    "tokens": [
      {
        "idx": 0,
        "word": "Odi",
        "lemma": "odi",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "profanum",
        "lemma": "profanus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "vulgus",
        "lemma": "uulgus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "nsubj",
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
    "id": 416,
    "latin": "Pulvis et umbra sumus.",
    "spanish": "Somos polvo y sombra.",
    "tokens": [
      {
        "idx": 0,
        "word": "Pulvis",
        "lemma": "puluis",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
        "word": "umbra",
        "lemma": "umbra",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": "sumus",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin",
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
    "id": 417,
    "latin": "In nova fert animus mutatas dicere formas.",
    "spanish": "Mi espíritu me lleva a hablar de formas transformadas en cuerpos nuevos.",
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
        "word": "nova",
        "lemma": "nouus",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "fert",
        "lemma": "fero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "animus",
        "lemma": "animus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "mutatas",
        "lemma": "muto",
        "pos": "VERB",
        "morph": "Case=Acc|Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "acl",
        "head": 6,
        "current_role": "oración_adjetiva"
      },
      {
        "idx": 5,
        "word": "dicere",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "csubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 6,
        "word": "formas",
        "lemma": "forma",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 5,
        "current_role": "objeto_directo"
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
    "id": 418,
    "latin": "Primus amor Phoebi Daphne fuit.",
    "spanish": "El primer amor de Febo fue Dafne.",
    "tokens": [
      {
        "idx": 0,
        "word": "Primus",
        "lemma": "primus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "amor",
        "lemma": "amor",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "Phoebi",
        "lemma": "Phoebus",
        "pos": "PROPN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 3,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 3,
        "word": "Daphne",
        "lemma": "Daphne",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "fuit",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
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
    "id": 419,
    "latin": "Pater, fer opem!",
    "spanish": "¡Padre, trae ayuda!",
    "tokens": [
      {
        "idx": 0,
        "word": "Pater",
        "lemma": "pater",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "fer",
        "lemma": "fero",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "opem",
        "lemma": "ops",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "!",
        "lemma": "!",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 420,
    "latin": "Vix prece finita, torpor occupat artus.",
    "spanish": "Apenas terminada la súplica, un torpor ocupa sus miembros.",
    "tokens": [
      {
        "idx": 0,
        "word": "Vix",
        "lemma": "uix",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 5,
        "current_role": "modificador_adverbial"
      },
      {
        "idx": 1,
        "word": "prece",
        "lemma": "prex",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 5,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 2,
        "word": "finita",
        "lemma": "finio",
        "pos": "VERB",
        "morph": "Case=Abl|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass",
        "dep": "acl",
        "head": 1,
        "current_role": "oración_adjetiva"
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
        "word": "torpor",
        "lemma": "torpor",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "occupat",
        "lemma": "occupo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": "artus",
        "lemma": "artus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 5,
        "current_role": "sujeto"
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
    "id": 421,
    "latin": "Omnia vincit Amor.",
    "spanish": "El Amor lo vence todo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Omnia",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "vincit",
        "lemma": "uincio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "Amor",
        "lemma": "amor",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
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
    "id": 422,
    "latin": "Tempus edax rerum.",
    "spanish": "El tiempo, devorador de las cosas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Tempus",
        "lemma": "tempus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "edax",
        "lemma": "edax",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "rerum",
        "lemma": "res",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Plur",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
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
    "id": 423,
    "latin": "Video meliora proboque, deteriora sequor.",
    "spanish": "Veo lo mejor y lo apruebo, pero sigo lo peor.",
    "tokens": [
      {
        "idx": 0,
        "word": "Video",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "meliora",
        "lemma": "melior",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "probo",
        "lemma": "probo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "conj",
        "head": 0,
        "current_role": "elemento_coordinado"
      },
      {
        "idx": 3,
        "word": "que",
        "lemma": "que",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 2,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 4,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 0,
        "current_role": "puntuación"
      },
      {
        "idx": 5,
        "word": "deteriora",
        "lemma": "deterior",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 6,
        "current_role": "objeto_directo"
      },
      {
        "idx": 6,
        "word": "sequor",
        "lemma": "sequor",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Pass",
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
    "id": 424,
    "latin": "Donec eris felix, multos numerabis amicos.",
    "spanish": "Mientras seas feliz, contarás muchos amigos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Donec",
        "lemma": "donec",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "eris",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "felix",
        "lemma": "felix",
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
        "head": 5,
        "current_role": "puntuación"
      },
      {
        "idx": 4,
        "word": "multos",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 5,
        "current_role": "objeto_directo"
      },
      {
        "idx": 5,
        "word": "numerabis",
        "lemma": "numero",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": "amicos",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 5,
        "current_role": "objeto_directo"
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
    "id": 425,
    "latin": "Gutta cavat lapidem.",
    "spanish": "La gota horada la piedra.",
    "tokens": [
      {
        "idx": 0,
        "word": "Gutta",
        "lemma": "gutta",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "cavat",
        "lemma": "cauo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "lapidem",
        "lemma": "lapis",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
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
    "id": 426,
    "latin": "Ars latet arte sua.",
    "spanish": "El arte se oculta con su propio arte.",
    "tokens": [
      {
        "idx": 0,
        "word": "Ars",
        "lemma": "ars",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "latet",
        "lemma": "lateo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "arte",
        "lemma": "ars",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 1,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "sua",
        "lemma": "suus",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "det",
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
        "head": 1,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 427,
    "latin": "Dies irae, dies illa.",
    "spanish": "Día de ira, aquel día.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dies",
        "lemma": "dies",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
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
    "id": 428,
    "latin": "O Fortuna, velut luna statu variabilis.",
    "spanish": "Oh Fortuna, variable como la luna.",
    "tokens": [
      {
        "idx": 0,
        "word": "O",
        "lemma": "o",
        "pos": "INTJ",
        "morph": "",
        "dep": "advmod:emph",
        "head": 1,
        "current_role": "modificador"
      },
      {
        "idx": 1,
        "word": "Fortuna",
        "lemma": "fortuna",
        "pos": "PROPN",
        "morph": "Case=Voc|Gender=Fem|Number=Sing",
        "dep": "vocative",
        "head": 6,
        "current_role": "vocativo"
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
        "word": "velut",
        "lemma": "uelut",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 4,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 4,
        "word": "luna",
        "lemma": "luna",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "appos",
        "head": 1,
        "current_role": "aposición"
      },
      {
        "idx": 5,
        "word": "statu",
        "lemma": "status",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 6,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 6,
        "word": "variabilis",
        "lemma": "uariabilis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
    "id": 429,
    "latin": "Gaudeamus igitur, iuvenes dum sumus.",
    "spanish": "Alegrémonos pues, mientras somos jóvenes.",
    "tokens": [
      {
        "idx": 0,
        "word": "Gaudeamus",
        "lemma": "",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "igitur",
        "lemma": "igitur",
        "pos": "PART",
        "morph": "",
        "dep": "discourse",
        "head": 0,
        "current_role": "modificador_adverbial"
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
        "word": "iuvenes",
        "lemma": "iuuenis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "dum",
        "lemma": "dum",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 5,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 5,
        "word": "sumus",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin",
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
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 430,
    "latin": "Ubi sunt qui ante nos in mundo fuere?",
    "spanish": "¿Dónde están los que fueron antes de nosotros en el mundo?",
    "tokens": [
      {
        "idx": 0,
        "word": "Ubi",
        "lemma": "ubi",
        "pos": "ADV",
        "morph": "",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "sunt",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 0,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "ante",
        "lemma": "ante",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 4,
        "current_role": "preposición"
      },
      {
        "idx": 4,
        "word": "nos",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Plur|Person=1",
        "dep": "nsubj",
        "head": 6,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 6,
        "current_role": "preposición"
      },
      {
        "idx": 6,
        "word": "mundo",
        "lemma": "mundus",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 0,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 7,
        "word": "fuere",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin",
        "dep": "cop",
        "head": 6,
        "current_role": "cópula"
      },
      {
        "idx": 8,
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
    "id": 431,
    "latin": "Stabat Mater dolorosa.",
    "spanish": "Estaba la Madre dolorosa.",
    "tokens": [
      {
        "idx": 0,
        "word": "Stabat",
        "lemma": "sto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "Mater",
        "lemma": "mater",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "dolorosa",
        "lemma": "dolorosus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
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
    "id": 432,
    "latin": "Veni, Creator Spiritus.",
    "spanish": "Ven, Espíritu Creador.",
    "tokens": [
      {
        "idx": 0,
        "word": "Veni",
        "lemma": "uenio",
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
        "word": "Creator",
        "lemma": "Creator",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 0,
        "current_role": "vocativo"
      },
      {
        "idx": 3,
        "word": "Spiritus",
        "lemma": "spiritus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nmod",
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
        "head": 0,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 433,
    "latin": "Confiteor Deo omnipotenti.",
    "spanish": "Confieso a Dios todopoderoso.",
    "tokens": [
      {
        "idx": 0,
        "word": "Confiteor",
        "lemma": "confiteor",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "Deo",
        "lemma": "Deus",
        "pos": "PROPN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "obl:arg",
        "head": 0,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 2,
        "word": "omnipotenti",
        "lemma": "omnipotens",
        "pos": "ADJ",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
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
    "id": 434,
    "latin": "Requiem aeternam dona eis, Domine.",
    "spanish": "Dales, Señor, el descanso eterno.",
    "tokens": [
      {
        "idx": 0,
        "word": "Requiem",
        "lemma": "requies",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "aeternam",
        "lemma": "aeternus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "dona",
        "lemma": "donum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "eis",
        "lemma": "is",
        "pos": "PRON",
        "morph": "Case=Dat|Gender=Masc|Number=Plur|Person=3",
        "dep": "obl:arg",
        "head": 2,
        "current_role": "complemento_obligatorio"
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
        "word": "Domine",
        "lemma": "Dominus",
        "pos": "NOUN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 2,
        "current_role": "vocativo"
      },
      {
        "idx": 6,
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
    "id": 435,
    "latin": "Te Deum laudamus.",
    "spanish": "A ti, Dios, te alabamos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "Deum",
        "lemma": "Deus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "laudamus",
        "lemma": "laudo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 436,
    "latin": "Salve, Regina, mater misericordiae.",
    "spanish": "Salve, Reina, madre de misericordia.",
    "tokens": [
      {
        "idx": 0,
        "word": "Salve",
        "lemma": "salvo",
        "pos": "NOUN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
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
        "word": "Regina",
        "lemma": "regina",
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
        "word": "mater",
        "lemma": "mater",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "appos",
        "head": 2,
        "current_role": "aposición"
      },
      {
        "idx": 5,
        "word": "misericordiae",
        "lemma": "misericordia",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 4,
        "current_role": "complemento_del_nombre"
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
    "id": 437,
    "latin": "Pater noster, qui es in caelis.",
    "spanish": "Padre nuestro, que estás en los cielos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Pater",
        "lemma": "pater",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "noster",
        "lemma": "noster",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": ",",
        "lemma": ",",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 6,
        "current_role": "puntuación"
      },
      {
        "idx": 3,
        "word": "qui",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 6,
        "current_role": "sujeto"
      },
      {
        "idx": 4,
        "word": "es",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 6,
        "current_role": "cópula"
      },
      {
        "idx": 5,
        "word": "in",
        "lemma": "in",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 6,
        "current_role": "preposición"
      },
      {
        "idx": 6,
        "word": "caelis",
        "lemma": "caelum",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Plur",
        "dep": "acl:relcl",
        "head": 0,
        "current_role": "oración_de_relativo"
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
    "id": 438,
    "latin": "Sanctificetur nomen tuum.",
    "spanish": "Santificado sea tu nombre.",
    "tokens": [
      {
        "idx": 0,
        "word": "Sanctificetur",
        "lemma": "sanctifico",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "nomen",
        "lemma": "nomen",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "tuum",
        "lemma": "tuus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "modificador_adjetival"
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
    "id": 439,
    "latin": "Adveniat regnum tuum.",
    "spanish": "Venga tu reino.",
    "tokens": [
      {
        "idx": 0,
        "word": "Adveniat",
        "lemma": "aduenio",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "regnum",
        "lemma": "regnum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "tuum",
        "lemma": "tuus",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "modificador_adjetival"
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
    "id": 440,
    "latin": "Panem nostrum quotidianum da nobis hodie.",
    "spanish": "Danos hoy nuestro pan de cada día.",
    "tokens": [
      {
        "idx": 0,
        "word": "Panem",
        "lemma": "panis",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "nostrum",
        "lemma": "noster",
        "pos": "DET",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "quotidianum",
        "lemma": "quotidianus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "da",
        "lemma": "do",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 3,
        "current_role": "predicado"
      },
      {
        "idx": 4,
        "word": "nobis",
        "lemma": "nos",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Plur|Person=1",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 5,
        "word": "hodie",
        "lemma": "hodie",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod:tmod",
        "head": 3,
        "current_role": "modificador"
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
  }
]