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
    "id": 61,
    "latin": "Puella pulchra venit.",
    "spanish": "La niña hermosa viene.",
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
        "word": "pulchra",
        "lemma": "pulcher",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "venit",
        "lemma": "uenio",
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
    "id": 62,
    "latin": "Pueri boni dormiunt.",
    "spanish": "Los niños buenos duermen.",
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
        "word": "boni",
        "lemma": "bonus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "dormiunt",
        "lemma": "dormio",
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
    "id": 63,
    "latin": "Puer puellae rosam dat.",
    "spanish": "El niño da una rosa a la niña.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puer",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
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
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "rosam",
        "lemma": "rosa",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
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
    "id": 64,
    "latin": "Magister discipulis libros dat.",
    "spanish": "El maestro da libros a los discípulos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Magister",
        "lemma": "Magister",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "discipulis",
        "lemma": "discipulus",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 2,
        "word": "libros",
        "lemma": "liber",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
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
    "id": 65,
    "latin": "Do tibi donum.",
    "spanish": "Te doy un regalo.",
    "tokens": [
      {
        "idx": 0,
        "word": "Do",
        "lemma": "do",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
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
        "word": "donum",
        "lemma": "donum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
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
    "id": 66,
    "latin": "Mihi est liber.",
    "spanish": "Tengo un libro.",
    "tokens": [
      {
        "idx": 0,
        "word": "Mihi",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Sing|Person=1",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
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
        "word": "liber",
        "lemma": "liber",
        "pos": "ADJ",
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
    "id": 67,
    "latin": "Caesari sunt multi milites.",
    "spanish": "César tiene muchos soldados.",
    "tokens": [
      {
        "idx": 0,
        "word": "Caesari",
        "lemma": "Caesar",
        "pos": "PROPN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
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
        "word": "multi",
        "lemma": "multus",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "det",
        "head": 3,
        "current_role": "determinante"
      },
      {
        "idx": 3,
        "word": "milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 0,
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
    "id": 68,
    "latin": "Domus patris magna est.",
    "spanish": "La casa del padre es grande.",
    "tokens": [
      {
        "idx": 0,
        "word": "Domus",
        "lemma": "domus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "patris",
        "lemma": "pater",
        "pos": "NOUN",
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
    "id": 69,
    "latin": "Liber pueri est novus.",
    "spanish": "El libro del niño es nuevo.",
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
        "word": "pueri",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Voc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
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
        "word": "novus",
        "lemma": "nouus",
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
  },
  {
    "id": 70,
    "latin": "Amor patriae laudabilis est.",
    "spanish": "El amor a la patria es loable.",
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
        "word": "patriae",
        "lemma": "patria",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Fem|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "laudabilis",
        "lemma": "laudabilis",
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
    "id": 71,
    "latin": "Milites iter fecerunt.",
    "spanish": "Los soldados hicieron el viaje.",
    "tokens": [
      {
        "idx": 0,
        "word": "Milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "iter",
        "lemma": "iter",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Sing",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "fecerunt",
        "lemma": "facio",
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
    "id": 72,
    "latin": "Vidi urbem magnam.",
    "spanish": "Vi una gran ciudad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Vidi",
        "lemma": "uideo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "urbem",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "magnam",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
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
    "id": 73,
    "latin": "Dies venit.",
    "spanish": "El día viene.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dies",
        "lemma": "dies",
        "pos": "NOUN",
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
    "id": 74,
    "latin": "Res publica est magna.",
    "spanish": "La república es grande.",
    "tokens": [
      {
        "idx": 0,
        "word": "Res",
        "lemma": "res",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "publica",
        "lemma": "publicus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
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
        "word": "magna",
        "lemma": "magnus",
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
    "id": 75,
    "latin": "Cras te videbo.",
    "spanish": "Mañana te veré.",
    "tokens": [
      {
        "idx": 0,
        "word": "Cras",
        "lemma": "cras",
        "pos": "ADV",
        "morph": "",
        "dep": "advmod",
        "head": 2,
        "current_role": "modificador_adverbial"
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
        "word": "videbo",
        "lemma": "uideo",
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
    "id": 76,
    "latin": "Librum legam.",
    "spanish": "Leeré el libro.",
    "tokens": [
      {
        "idx": 0,
        "word": "Librum",
        "lemma": "liber",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 1,
        "current_role": "objeto_directo"
      },
      {
        "idx": 1,
        "word": "legam",
        "lemma": "lego",
        "pos": "VERB",
        "morph": "Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 77,
    "latin": "Semper amicos amabimus.",
    "spanish": "Siempre amaremos a los amigos.",
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
        "word": "amicos",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Plur",
        "dep": "obj",
        "head": 2,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "amabimus",
        "lemma": "amo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=1|Tense=Fut|VerbForm=Fin|Voice=Act",
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
    "id": 78,
    "latin": "Miles fortis pugnat.",
    "spanish": "El soldado fuerte lucha.",
    "tokens": [
      {
        "idx": 0,
        "word": "Miles",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "fortis",
        "lemma": "fortis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "xcomp",
        "head": 2,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 2,
        "word": "pugnat",
        "lemma": "pugno",
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
    "id": 79,
    "latin": "Omnes homines mortales sunt.",
    "spanish": "Todos los hombres son mortales.",
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
        "word": "homines",
        "lemma": "homo",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "mortales",
        "lemma": "mortalis",
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
    "id": 80,
    "latin": "Urbs ingens est.",
    "spanish": "La ciudad es enorme.",
    "tokens": [
      {
        "idx": 0,
        "word": "Urbs",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "ingens",
        "lemma": "ingens",
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
  }
]