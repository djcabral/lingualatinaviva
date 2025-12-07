# TAREA: Curation de Vocabulario Latino

Eres un experto lexicógrafo de latín clásico. Tu tarea es revisar, corregir y completar la siguiente lista de palabras latinas extraídas de una base de datos.

## OBJETIVO

Para cada entrada de vocabulario:

1. **Verificar y Corregir**: Lema (`latin`), Categoría gramatical (`part_of_speech`), Genitivo (si aplica).
2. **Completar**: Definición en español (`definition_es`).
3. **Estandarizar**: Asegurar que los lemas usen la ortografía estándar (con macrones si es posible, o indicalo).

## FORMATO DE ENTRADA

Recibirás un JSON con una lista de objetos `Word`.

```json
[
  {
    "id": 101,
    "latin": "puella",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null
  }
]
```

## FORMATO DE SALIDA

Devuelve **EXACTAMENTE** el mismo formato JSON, pero con los campos corregidos y completados.
NO cambies el `id`.
Si el registro es correcto y está completo, devuélvelo tal cual.

### Campos

- `id`: (Entero, NO MODIFICAR)
- `latin`: Lema principal (Nominativo singular para sustantivos/adj, 1ª persona presente para verbos).
- `part_of_speech`: `noun`, `proper_noun`, `verb`, `adjective`, `adverb`, `preposition`, `conjunction`, `pronoun`, `numeral`, `interjection`.
- `genitive`: (Solo sustantivos) Genitivo singular (ayuda a identificar declinación).
- `definition_es`: Traducción/Definición concisa en español (ej: "niña, muchacha").

## EJEMPLO DE RESPUESTA

```json
[
  {
    "id": 101,
    "latin": "puella",
    "part_of_speech": "noun",
    "genitive": "puellae",
    "definition_es": "niña, muchacha"
  }
]
```

---

# DATOS A CURAR

```json
[
  {
    "id": 556,
    "latin": "Nīlus",
    "part_of_speech": "noun",
    "genitive": "Nīlī",
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 557,
    "latin": "Rhēnus",
    "part_of_speech": "noun",
    "genitive": "Rhēnī",
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 558,
    "latin": "Dānuvius",
    "part_of_speech": "noun",
    "genitive": "Dānuviī",
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 560,
    "latin": "pars",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "review"
  },
  {
    "id": 561,
    "latin": "Belgae",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "review"
  },
  {
    "id": 563,
    "latin": "Europa",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "review"
  },
  {
    "id": 565,
    "latin": "latine",
    "part_of_speech": "adverb",
    "genitive": null,
    "definition_es": null,
    "status": "review"
  },
  {
    "id": 566,
    "latin": "Iulius",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "review"
  },
  {
    "id": 567,
    "latin": "Aemilia",
    "part_of_speech": "proper_noun",
    "genitive": null,
    "definition_es": "Aemilia",
    "status": "review"
  },
  {
    "id": 568,
    "latin": "Marcus",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "review"
  }
]
```