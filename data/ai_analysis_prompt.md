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

