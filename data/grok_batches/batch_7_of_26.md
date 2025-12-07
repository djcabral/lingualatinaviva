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
    "id": 420,
    "latin": "infernus",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 421,
    "latin": "monasterium",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 422,
    "latin": "abbas",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 423,
    "latin": "oratio",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 424,
    "latin": "missa",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 425,
    "latin": "saeculum",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 426,
    "latin": "amen",
    "part_of_speech": "adverb",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 427,
    "latin": "spiritus",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 428,
    "latin": "sanctus",
    "part_of_speech": "adjective",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  },
  {
    "id": 429,
    "latin": "panis",
    "part_of_speech": "noun",
    "genitive": null,
    "definition_es": null,
    "status": "active"
  }
]
```