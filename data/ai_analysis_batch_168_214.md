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
  }
]