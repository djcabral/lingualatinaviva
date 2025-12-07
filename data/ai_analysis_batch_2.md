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
    "id": 21,
    "latin": "Femina puellae rosam dat.",
    "spanish": "La mujer da una rosa a la niña.",
    "tokens": [
      {
        "idx": 0,
        "word": "Femina",
        "lemma": "femina",
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
        "morph": "Case=Dat|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
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
    "id": 22,
    "latin": "Filia domini est laeta.",
    "spanish": "La hija del señor está alegre.",
    "tokens": [
      {
        "idx": 0,
        "word": "Filia",
        "lemma": "filia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "domini",
        "lemma": "dominus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 0,
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
        "word": "laeta",
        "lemma": "laeto",
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
    "id": 23,
    "latin": "Nauta nautis pecuniam dat.",
    "spanish": "El marinero da dinero a los marineros.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nauta",
        "lemma": "nauta",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "nautis",
        "lemma": "nauta",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Plur",
        "dep": "obl:arg",
        "head": 0,
        "current_role": "complemento_obligatorio"
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
    "id": 24,
    "latin": "Templum deorum est magnum.",
    "spanish": "El templo de los dioses es grande.",
    "tokens": [
      {
        "idx": 0,
        "word": "Templum",
        "lemma": "templum",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "deorum",
        "lemma": "deus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 0,
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
        "word": "magnum",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
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
    "id": 25,
    "latin": "Puer puero librum dat.",
    "spanish": "El niño da un libro al niño.",
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
        "word": "puero",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Masc|Number=Sing",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "librum",
        "lemma": "liber",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
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
    "id": 26,
    "latin": "Servi dominorum laborant.",
    "spanish": "Los esclavos de los señores trabajan.",
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
        "word": "dominorum",
        "lemma": "dominus",
        "pos": "NOUN",
        "morph": "Case=Gen|Gender=Masc|Number=Plur",
        "dep": "nmod",
        "head": 0,
        "current_role": "complemento_del_nombre"
      },
      {
        "idx": 2,
        "word": "laborant",
        "lemma": "laboro",
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
    "id": 27,
    "latin": "Feminae feminis dona dant.",
    "spanish": "Las mujeres dan regalos a las mujeres.",
    "tokens": [
      {
        "idx": 0,
        "word": "Feminae",
        "lemma": "femina",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
        "dep": "amod",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "feminis",
        "lemma": "femina",
        "pos": "NOUN",
        "morph": "Case=Dat|Gender=Fem|Number=Plur",
        "dep": "obl:arg",
        "head": 3,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 2,
        "word": "dona",
        "lemma": "donum",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
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
    "id": 28,
    "latin": "Puella cum amica ambulat.",
    "spanish": "La niña camina con la amiga.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puella",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
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
        "word": "amica",
        "lemma": "amica",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "advcl",
        "head": 3,
        "current_role": "oración_adverbial"
      },
      {
        "idx": 3,
        "word": "ambulat",
        "lemma": "ambulo",
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
    "id": 29,
    "latin": "Serve, veni ad dominum!",
    "spanish": "¡Esclavo, ven al señor!",
    "tokens": [
      {
        "idx": 0,
        "word": "Serve",
        "lemma": "seruus",
        "pos": "NOUN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 2,
        "current_role": "vocativo"
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
        "word": "veni",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "ad",
        "lemma": "ad",
        "pos": "ADP",
        "morph": "",
        "dep": "case",
        "head": 4,
        "current_role": "preposición"
      },
      {
        "idx": 4,
        "word": "dominum",
        "lemma": "dominus",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 5,
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
    "id": 30,
    "latin": "Poeta carmina magna voce cantat.",
    "spanish": "El poeta canta poemas en voz alta.",
    "tokens": [
      {
        "idx": 0,
        "word": "Poeta",
        "lemma": "poeta",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "carmina",
        "lemma": "carmen",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Neut|Number=Plur",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "magna",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 3,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 3,
        "word": "voce",
        "lemma": "uox",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "cantat",
        "lemma": "canto",
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
    "id": 31,
    "latin": "Domine, servus te vocat.",
    "spanish": "Señor, el esclavo te llama.",
    "tokens": [
      {
        "idx": 0,
        "word": "Domine",
        "lemma": "Dominus",
        "pos": "NOUN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 4,
        "current_role": "vocativo"
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
        "word": "servus",
        "lemma": "seruus",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "te",
        "lemma": "tu",
        "pos": "PRON",
        "morph": "Case=Acc|Number=Sing|Person=2",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 4,
        "word": "vocat",
        "lemma": "uoco",
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
    "id": 32,
    "latin": "Femina cum pueris venit.",
    "spanish": "La mujer viene con los niños.",
    "tokens": [
      {
        "idx": 0,
        "word": "Femina",
        "lemma": "femina",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
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
        "word": "pueris",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
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
    "id": 33,
    "latin": "Nauta in nave laborat.",
    "spanish": "El marinero trabaja en la nave.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nauta",
        "lemma": "nauta",
        "pos": "NOUN",
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
        "word": "nave",
        "lemma": "nauis",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "laborat",
        "lemma": "laboro",
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
    "id": 34,
    "latin": "Puellae, rosae sunt pulchrae!",
    "spanish": "¡Niñas, las rosas son hermosas!",
    "tokens": [
      {
        "idx": 0,
        "word": "Puellae",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
        "dep": "vocative",
        "head": 2,
        "current_role": "vocativo"
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
        "word": "rosae",
        "lemma": "rosa",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
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
        "word": "pulchrae",
        "lemma": "pulchrus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 5,
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
    "id": 35,
    "latin": "Puer gladio pugnat.",
    "spanish": "El niño lucha con la espada.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puer",
        "lemma": "puer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "gladio",
        "lemma": "gladius",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
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
    "id": 36,
    "latin": "Amice, librum mihi da!",
    "spanish": "¡Amigo, dame el libro!",
    "tokens": [
      {
        "idx": 0,
        "word": "Amice",
        "lemma": "amicus",
        "pos": "NOUN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "vocative",
        "head": 4,
        "current_role": "vocativo"
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
        "word": "librum",
        "lemma": "liber",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Masc|Number=Sing",
        "dep": "obj",
        "head": 4,
        "current_role": "objeto_directo"
      },
      {
        "idx": 3,
        "word": "mihi",
        "lemma": "ego",
        "pos": "PRON",
        "morph": "Case=Dat|Number=Sing|Person=1",
        "dep": "obl:arg",
        "head": 4,
        "current_role": "objeto_indirecto"
      },
      {
        "idx": 4,
        "word": "da",
        "lemma": "do",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 4,
        "current_role": "predicado"
      },
      {
        "idx": 5,
        "word": "!",
        "lemma": "!",
        "pos": "PUNCT",
        "morph": "",
        "dep": "punct",
        "head": 4,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 37,
    "latin": "Servi in agris laborant.",
    "spanish": "Los esclavos trabajan en los campos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Servi",
        "lemma": "Seruius",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
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
        "word": "agris",
        "lemma": "ager",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
        "dep": "obl",
        "head": 3,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 3,
        "word": "laborant",
        "lemma": "laboro",
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
    "id": 38,
    "latin": "Amo rosas pulchras.",
    "spanish": "Amo las rosas hermosas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Amo",
        "lemma": "amo",
        "pos": "PROPN",
        "morph": "Case=Voc|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "rosas",
        "lemma": "rosa",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "obj",
        "head": 0,
        "current_role": "objeto_directo"
      },
      {
        "idx": 2,
        "word": "pulchras",
        "lemma": "pulcher",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
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
    "id": 39,
    "latin": "Puella cantat et laudat.",
    "spanish": "La niña canta y alaba.",
    "tokens": [
      {
        "idx": 0,
        "word": "Puella",
        "lemma": "puella",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "cantat",
        "lemma": "canto",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
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
        "word": "laudat",
        "lemma": "laudo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
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
    "id": 40,
    "latin": "Servi laborant in agris.",
    "spanish": "Los esclavos trabajan en los campos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Servi",
        "lemma": "Seruius",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 1,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "laborant",
        "lemma": "laboro",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
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
        "word": "agris",
        "lemma": "ager",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Masc|Number=Plur",
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
  }
]