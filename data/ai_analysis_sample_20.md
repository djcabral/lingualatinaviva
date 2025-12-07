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
    "id": 1,
    "latin": "Vincere aut mori.",
    "spanish": "Vencer o morir.",
    "tokens": [
      {
        "idx": 0,
        "word": "Vincere",
        "lemma": "uinco",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "aut",
        "lemma": "aut",
        "pos": "CCONJ",
        "morph": "",
        "dep": "cc",
        "head": 2,
        "current_role": "conjunción_coordinante"
      },
      {
        "idx": 2,
        "word": "mori",
        "lemma": "morior",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Pass",
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
    "id": 2,
    "latin": "Cogito, ergo sum.",
    "spanish": "Pienso, luego existo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Cogito",
        "lemma": "cogito",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
        "head": 0,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "ergo",
        "lemma": "ergo",
        "pos": "ADV",
        "morph": "",
        "dep": "discourse",
        "head": 0,
        "current_role": "marcador_discursivo"
      },
      {
        "idx": 3,
        "word": "sum",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin",
        "dep": "aux:pass",
        "head": 0,
        "current_role": "auxiliar_pasivo"
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
    "id": 3,
    "latin": "Dico te venire.",
    "spanish": "Digo que vienes.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dico",
        "lemma": "dico",
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
        "word": "venire",
        "lemma": "uenio",
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
    "id": 4,
    "latin": "Timeo ne pluat.",
    "spanish": "Temo que llueva.",
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
        "pos": "PART",
        "morph": "",
        "dep": "mark",
        "head": 2,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 2,
        "word": "pluat",
        "lemma": "pluo",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 5,
    "latin": "Si vis pacem, para bellum.",
    "spanish": "Si quieres la paz, prepara la guerra.",
    "tokens": [
      {
        "idx": 0,
        "word": "Si",
        "lemma": "si",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 1,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 1,
        "word": "vis",
        "lemma": "uolo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "advcl",
        "head": 4,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 2,
        "word": "pacem",
        "lemma": "pax",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "xcomp",
        "head": 1,
        "current_role": "complemento_predicativo"
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
        "word": "para",
        "lemma": "paro",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": "bellum",
        "lemma": "bellum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
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
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 6,
    "latin": "Puer, quem vides, amicus meus est.",
    "spanish": "El niño, al cual ves, es mi amigo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puer",
        "lemma": "puer",
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
        "head": 3,
        "current_role": "puntuación"
      },
      {
        "idx": 2,
        "word": "quem",
        "lemma": "qui",
        "pos": "PRON",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "vides",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "advcl:cmp",
        "head": 5,
        "current_role": "otro"
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
        "word": "amicus",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 5,
        "current_role": "predicado"
      },
      {
        "idx": 6,
        "word": "meus",
        "lemma": "meus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 5,
        "current_role": "determinante"
      },
      {
        "idx": 7,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 5,
        "current_role": "cópula"
      },
      {
        "idx": 8,
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
    "id": 7,
    "latin": "Dicit se Romanum esse.",
    "spanish": "Dice que él es romano.",
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
        "morph": "Case=Acc|Person=3",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "Romanum",
        "lemma": "Romanus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
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
    "id": 8,
    "latin": "Rosa est pulchra.",
    "spanish": "La rosa es hermosa.",
    "tokens": [
      {
        "idx": 0,
        "word": "Rosa",
        "lemma": "Rosa",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 2,
        "word": "pulchra",
        "lemma": "pulcher",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
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
    "id": 9,
    "latin": "Puella rosam amat.",
    "spanish": "La niña ama la rosa.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puella",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "rosam",
        "lemma": "rosa",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "amat",
        "lemma": "amo",
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
    "id": 10,
    "latin": "Dominus servum vocat.",
    "spanish": "El señor llama al esclavo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dominus",
        "lemma": "Dominus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "servum",
        "lemma": "seruus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "vocat",
        "lemma": "uoco",
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
    "id": 11,
    "latin": "Puellae rosas amant.",
    "spanish": "Las niñas aman las rosas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puellae",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "rosas",
        "lemma": "rosa",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "amant",
        "lemma": "amo",
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
    "id": 12,
    "latin": "Servus dominum laudat.",
    "spanish": "El esclavo alaba al señor.",
    "tokens": [
      {
        "idx": 0,
        "word": "Servus",
        "lemma": "seruus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 1,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 1,
        "word": "dominum",
        "lemma": "dominus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "laudat",
        "lemma": "laudo",
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
    "id": 13,
    "latin": "Templum est magnum.",
    "spanish": "El templo es grande.",
    "tokens": [
      {
        "idx": 0,
        "word": "Templum",
        "lemma": "templum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
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
    "id": 14,
    "latin": "Pueri templa vident.",
    "spanish": "Los niños ven los templos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Pueri",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "templa",
        "lemma": "templum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "vident",
        "lemma": "uideo",
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
    "id": 15,
    "latin": "Femina puellam vocat.",
    "spanish": "La mujer llama a la niña.",
    "tokens": [
      {
        "idx": 0,
        "word": "Femina",
        "lemma": "femina",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "puellam",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "vocat",
        "lemma": "uoco",
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
    "id": 16,
    "latin": "Nautae navem portant.",
    "spanish": "Los marineros llevan la nave.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nautae",
        "lemma": "nautae",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "navem",
        "lemma": "nauis",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "portant",
        "lemma": "porto",
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
    "id": 17,
    "latin": "Poeta carmina scribit.",
    "spanish": "El poeta escribe poemas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Poeta",
        "lemma": "poeta",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "carmina",
        "lemma": "carmen",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "scribit",
        "lemma": "scribo",
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
    "id": 18,
    "latin": "Rosa puellae est pulchra.",
    "spanish": "La rosa de la niña es hermosa.",
    "tokens": [
      {
        "idx": 0,
        "word": "Rosa",
        "lemma": "Rosa",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "puellae",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 3,
        "current_role": "complemento_del_nombre"
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
        "word": "pulchra",
        "lemma": "pulcher",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
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
    "id": 19,
    "latin": "Dominus servo donum dat.",
    "spanish": "El señor da un regalo al esclavo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dominus",
        "lemma": "Dominus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "servo",
        "lemma": "seruus",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 2,
        "word": "donum",
        "lemma": "donum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 3,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "dat",
        "lemma": "do",
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
    "id": 20,
    "latin": "Liber poetae est bonus.",
    "spanish": "El libro del poeta es bueno.",
    "tokens": [
      {
        "idx": 0,
        "word": "Liber",
        "lemma": "Liber",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "poetae",
        "lemma": "poeta",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 3,
        "current_role": "complemento_del_nombre"
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
        "word": "bonus",
        "lemma": "bonus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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