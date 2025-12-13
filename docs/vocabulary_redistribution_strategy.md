# Mapeo de Vocabulario por Lección

## Objetivo

Redistribuir 724 palabras actuales (84% en L1) a través de las lecciones L1-L30, asignando 15-30 palabras por lección según el contenido gramatical.

## Criterios de Asignación

### Lección 1: Primeros Pasos (alfabeto, pronunciación, conceptos básicos)

**Vocabulario target: 20 palabras**

Palabras esenciales para primeras oraciones:

- Sustantivos 1ª declinación femeninos (5): `puella`, `rosa`, `agricola`, `ancilla`, `nauta`
- Sustantivos 2ª declinación masculinos (3): `dominus`, `servus`, `amicus`
- Verbo SUM presente (formas): `sum`, `es`, `est`
- Adjetivos básicos (3): `bonus`, `magnus`, `parvus`
- Conjunciones básicas (2): `et`, `sed`
- Preposiciones básicas (2): `in`, `cum`

### Lección 2: El Sujeto (Nominativo)

**Vocabulario target: 20 palabras**

Enfoque en sujetos y verbos presentantes:

- Sustantivos comunes como sujetos (10)
- Verbos transitivos básicos (5): `amat`, `vocat`, `portat`
- Adjetivos de concordancia (5)

### Lección 3: Primera Declinación y SUM

**Vocabulario target: 25 palabras**

Solo sustantivos de 1ª declinación + formas completas de SUM:

- Sustantivos -a, -ae femeninos (15)
- Sustantivos -a, -ae masculinos excepción (5): `agricola`, `nauta`, `poēta`
- Formas completas SUM (5): todas las personas singular/plural

### Lección 4: Segunda Declinación y Objeto

**Vocabulario target: 25 palabras**

Sustantivos 2ª declinación + verbos transitivos:

- Sustantivos -us masculinos (10)
- Sustantivos -um neutros (5)
- Verbos transitivos (10): requieren acusativo

### Lección 5: El Neutro

**Vocabulario target: 20 palabras**

Enfoque en sustantivos neutros:

- Neutros 2ª declinación -um (10)
- Neutros 3ª declinación comunes (5)
- Adjetivos que concuerdan con neutros (5)

### Lecciones 6-10: Consolidación, 3ª/4ª/5ª Declinación

**Vocabulario target: 20-25 palabras/lección**

- L6: Adjetivos 1ª clase (concordancia)
- L7: Sustantivos 3ª declinación (consonánticos)
- L8: Sustantivos 4ª declinación + Pretérito Perfecto
- L9: Sustantivos 5ª declinación + Futuro
- L10: Adjetivos 2ª clase (3ª declinación)

### Lecciones 11-13: Comparación, Pronombres, Pasiva

**Vocabulario target: 20 palabras/lección**

- L11: Adjetivos comparativos/superlativos + numerales básicos
- L12: Pronombres personales, demostrativos, relativos
- L13: Verbos pasivos frecuentes + complementos de ablativo

### Lecciones 14-20: Sistema Verbal Completo

**Vocabulario target: 15-20 palabras/lección**

Vocabulario enfocado en construcciones verbales:

- L14-16: Verbos con tiempos compuestos
- L17: Verbos deponentes comunes (20)
- L18-19: Verbos que usan subjuntivo
- L20: Verbos de AcI (dicendi, sentiendi, declarandi)

### Lecciones 21-24: Formas Nominales del Verbo

**Vocabulario target: 15-20 palabras/lección**

- L21: Verbos con participios frecuentes
- L22: Construcciones de ablativo absoluto
- L23: Verbos con gerundio/gerundivo
- L24: Construcciones perifrásticas

### Lecciones 25-30: Sintaxis Avanzada

**Vocabulario target: 15-20 palabras/lección**

Vocabulario para textos auténticos y sintaxis compleja:

- L25: Conjunciones coordinantes y subordinantes
- L26: Verbos con completivas (ut/ne)
- L27: Vocabulario de condicionales
- L28: Pronombres relativos y correlativos
- L29: Vocabulario de estilo indirecto
- L30: Vocabulario de métrica y poesía

---

## Próximo Paso

**Acción requerida**: Crear CSV `data/vocabulary_by_lesson.csv` con columnas:

- `latin` (forma del diccionario)
- `current_lesson` (nivel actual, casi siempre 1)
- `new_lesson` (1-30 según criterios arriba)
- `reason` (breve explicación: "sustantivo 1ª decl.", "verbo transitivo L2", etc.)

Este CSV alimentará el script `redistribute_vocabulary.py`.

---

## Notas Importantes

1. **Nombres propios**: Mover a lecciones de autores (L31-40) o distribuir en lecciones de lecturas
2. **Partículas invariables**: Distribuir en lecciones donde se usan (conjunciones, preposiciones)
3. **Verbos irregulares**: `sum`, `possum`, `eo`, `fero`, `volo` → lecciones tempranas (son frecuentísimos)
4. **Frecuencia**: Priorizar palabras de alta frecuencia en lecciones tempranas
