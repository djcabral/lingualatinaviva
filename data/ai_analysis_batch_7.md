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
    "id": 121,
    "latin": "Dies meliores venient.",
    "spanish": "Vendrán días mejores.",
    "tokens": [
      {
        "idx": 0,
        "word": "Dies",
        "lemma": "dies",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "meliores",
        "lemma": "melior",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "xcomp",
        "head": 2,
        "current_role": "complemento_predicativo"
      },
      {
        "idx": 2,
        "word": "venient",
        "lemma": "uenio",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Plur|Person=3|Tense=Fut|VerbForm=Fin|Voice=Act",
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
    "id": 122,
    "latin": "Magna spes in corde manebit.",
    "spanish": "Una gran esperanza permanecerá en el corazón.",
    "tokens": [
      {
        "idx": 0,
        "word": "Magna",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "spes",
        "lemma": "spes",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
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
        "word": "corde",
        "lemma": "cor",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "manebit",
        "lemma": "maneo",
        "pos": "VERB",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin|Voice=Act",
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
    "id": 123,
    "latin": "Brevis vita est.",
    "spanish": "La vida es breve.",
    "tokens": [
      {
        "idx": 0,
        "word": "Brevis",
        "lemma": "breuis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 0,
        "current_role": "predicado"
      },
      {
        "idx": 1,
        "word": "vita",
        "lemma": "uita",
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
    "id": 124,
    "latin": "Tristis historia nos movet.",
    "spanish": "La historia triste nos conmueve.",
    "tokens": [
      {
        "idx": 0,
        "word": "Tristis",
        "lemma": "tristis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "historia",
        "lemma": "historia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
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
        "word": "movet",
        "lemma": "moueo",
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
    "id": 125,
    "latin": "Acer vir in proelio stat.",
    "spanish": "El hombre ardiente permanece en la batalla.",
    "tokens": [
      {
        "idx": 0,
        "word": "Acer",
        "lemma": "acer",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "vir",
        "lemma": "uir",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 4,
        "current_role": "sujeto"
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
        "word": "proelio",
        "lemma": "proelium",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Neut|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "stat",
        "lemma": "sto",
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
    "id": 126,
    "latin": "Facilis via ducit ad urbem.",
    "spanish": "El camino fácil conduce a la ciudad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Facilis",
        "lemma": "facilis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "via",
        "lemma": "uia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
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
        "word": "urbem",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 2,
        "current_role": "complemento_circunstancial"
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
    "id": 127,
    "latin": "Fortes milites vincunt.",
    "spanish": "Los soldados valientes vencen.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fortes",
        "lemma": "fortis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
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
        "word": "vincunt",
        "lemma": "uinco",
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
    "id": 128,
    "latin": "Breves dies fugaces sunt.",
    "spanish": "Los días breves son fugaces.",
    "tokens": [
      {
        "idx": 0,
        "word": "Breves",
        "lemma": "breuis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "dies",
        "lemma": "dies",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "fugaces",
        "lemma": "fugax",
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
    "id": 129,
    "latin": "Tristis nuntius venit.",
    "spanish": "Llega una noticia triste.",
    "tokens": [
      {
        "idx": 0,
        "word": "Tristis",
        "lemma": "tristis",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "nuntius",
        "lemma": "nuntius",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
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
    "id": 130,
    "latin": "Viri acres non cedunt.",
    "spanish": "Los hombres ardientes no ceden.",
    "tokens": [
      {
        "idx": 0,
        "word": "Viri",
        "lemma": "uir",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "nsubj",
        "head": 3,
        "current_role": "sujeto"
      },
      {
        "idx": 1,
        "word": "acres",
        "lemma": "acer",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "amod",
        "head": 0,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "non",
        "lemma": "non",
        "pos": "PART",
        "morph": "",
        "dep": "advmod:neg",
        "head": 3,
        "current_role": "modificador"
      },
      {
        "idx": 3,
        "word": "cedunt",
        "lemma": "cedo",
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
    "id": 131,
    "latin": "Faciles artes discimus.",
    "spanish": "Aprendemos las artes fáciles.",
    "tokens": [
      {
        "idx": 0,
        "word": "Faciles",
        "lemma": "facilis",
        "pos": "ADJ",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "artes",
        "lemma": "ars",
        "pos": "NOUN",
        "morph": "Case=Acc|Gender=Fem|Number=Plur",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "discimus",
        "lemma": "disco",
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
    "id": 132,
    "latin": "Marcus altior quam Iulius est.",
    "spanish": "Marco es más alto que Julio.",
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
        "word": "altior",
        "lemma": "altus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "quam",
        "lemma": "quam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 3,
        "word": "Iulius",
        "lemma": "Iulius",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "advcl:cmp",
        "head": 1,
        "current_role": "otro"
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
    "id": 133,
    "latin": "Roma maior quam Athenae est.",
    "spanish": "Roma es mayor que Atenas.",
    "tokens": [
      {
        "idx": 0,
        "word": "Roma",
        "lemma": "Roma",
        "pos": "PROPN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 1,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 1,
        "word": "maior",
        "lemma": "magnus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 1,
        "current_role": "predicado"
      },
      {
        "idx": 2,
        "word": "quam",
        "lemma": "quam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 3,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 3,
        "word": "Athenae",
        "lemma": "Athenae",
        "pos": "PROPN",
        "morph": "Case=Loc|Gender=Fem|Number=Sing",
        "dep": "advcl:cmp",
        "head": 1,
        "current_role": "otro"
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
    "id": 134,
    "latin": "Nihil est melius quam pax.",
    "spanish": "Nada es mejor que la paz.",
    "tokens": [
      {
        "idx": 0,
        "word": "Nihil",
        "lemma": "nihil",
        "pos": "PRON",
        "morph": "Case=Nom",
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
        "word": "melius",
        "lemma": "melior",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Neut|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "quam",
        "lemma": "quam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 4,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 4,
        "word": "pax",
        "lemma": "pax",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "advcl:cmp",
        "head": 2,
        "current_role": "otro"
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
    "id": 135,
    "latin": "Haec via longissima omnium est.",
    "spanish": "Este camino es el más largo de todos.",
    "tokens": [
      {
        "idx": 0,
        "word": "Haec",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 1,
        "word": "via",
        "lemma": "uia",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "longissima",
        "lemma": "longissimus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "omnium",
        "lemma": "omnis",
        "pos": "DET",
        "morph": "Case=Gen|Gender=Neut|Number=Plur",
        "dep": "cop",
        "head": 2,
        "current_role": "cópula"
      },
      {
        "idx": 4,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
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
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 136,
    "latin": "Fortissimi milites victoriam petunt.",
    "spanish": "Los soldados más valientes buscan la victoria.",
    "tokens": [
      {
        "idx": 0,
        "word": "Fortissimi",
        "lemma": "fortissimus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
        "dep": "amod",
        "head": 1,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "milites",
        "lemma": "miles",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Plur",
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
        "word": "petunt",
        "lemma": "peto",
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
    "id": 137,
    "latin": "Facilius est dicere quam facere.",
    "spanish": "Es más fácil decir que hacer.",
    "tokens": [
      {
        "idx": 0,
        "word": "Facilius",
        "lemma": "facile",
        "pos": "ADV",
        "morph": "",
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
        "word": "dicere",
        "lemma": "dico",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "csubj",
        "head": 0,
        "current_role": "sujeto"
      },
      {
        "idx": 3,
        "word": "quam",
        "lemma": "quam",
        "pos": "SCONJ",
        "morph": "",
        "dep": "mark",
        "head": 4,
        "current_role": "conjunción_subordinante"
      },
      {
        "idx": 4,
        "word": "facere",
        "lemma": "facio",
        "pos": "VERB",
        "morph": "Tense=Pres|VerbForm=Inf|Voice=Act",
        "dep": "ccomp",
        "head": 2,
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
    "id": 138,
    "latin": "Iulia pulcherrima puella est.",
    "spanish": "Julia es una niña hermosísima.",
    "tokens": [
      {
        "idx": 0,
        "word": "Iulia",
        "lemma": "iulius",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 1,
        "word": "pulcherrima",
        "lemma": "pulcherrimus",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Fem|Number=Sing",
        "dep": "amod",
        "head": 2,
        "current_role": "modificador_adjetival"
      },
      {
        "idx": 2,
        "word": "puella",
        "lemma": "puella",
        "pos": "NOUN",
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
    "id": 139,
    "latin": "Hic liber difficilior illo est.",
    "spanish": "Este libro es más difícil que aquel.",
    "tokens": [
      {
        "idx": 0,
        "word": "Hic",
        "lemma": "hic",
        "pos": "DET",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "det",
        "head": 1,
        "current_role": "determinante"
      },
      {
        "idx": 1,
        "word": "liber",
        "lemma": "liber",
        "pos": "NOUN",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "nsubj",
        "head": 2,
        "current_role": "sujeto"
      },
      {
        "idx": 2,
        "word": "difficilior",
        "lemma": "difficilior",
        "pos": "ADJ",
        "morph": "Case=Nom|Gender=Masc|Number=Sing",
        "dep": "ROOT",
        "head": 2,
        "current_role": "predicado"
      },
      {
        "idx": 3,
        "word": "illo",
        "lemma": "ille",
        "pos": "DET",
        "morph": "Case=Abl|Gender=Masc|Number=Sing",
        "dep": "obl:arg",
        "head": 2,
        "current_role": "complemento_obligatorio"
      },
      {
        "idx": 4,
        "word": "est",
        "lemma": "sum",
        "pos": "AUX",
        "morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
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
        "head": 2,
        "current_role": "puntuación"
      }
    ]
  },
  {
    "id": 140,
    "latin": "Plures homines in urbe habitant.",
    "spanish": "Más hombres habitan en la ciudad.",
    "tokens": [
      {
        "idx": 0,
        "word": "Plures",
        "lemma": "plus",
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
        "head": 4,
        "current_role": "sujeto"
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
        "word": "urbe",
        "lemma": "urbs",
        "pos": "NOUN",
        "morph": "Case=Abl|Gender=Fem|Number=Sing",
        "dep": "obl",
        "head": 4,
        "current_role": "complemento_circunstancial"
      },
      {
        "idx": 4,
        "word": "habitant",
        "lemma": "habito",
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
  }
]