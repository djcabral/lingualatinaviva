# Guía del Usuario: Carga de Ejercicios y Desafíos

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Tipos de Desafíos](#tipos-de-desafíos)
3. [Creación Manual de Desafíos](#creación-manual-de-desafíos)
4. [Configuración de Progresión](#configuración-de-progresión)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Los **desafíos** son ejercicios gamificados que permiten a los estudiantes practicar diferentes aspectos del latín de manera estructurada y progresiva. Este documento explica cómo crear y gestionar desafíos personalizados.

### ¿Qué son los Desafíos?

- Ejercicios interactivos organizados por nivel (1-10)
- Sistema de progresión estricta con prerequisitos
- Recompensas de XP y estrellas
- 6 tipos diferentes de desafíos

---

## Tipos de Desafíos

### 1. 📜 Declinación (`declension`)

Practica la declinación completa de sustantivos, adjetivos o pronombres.

**Campos de configuración (`config` JSON)**:
```json
{
  "word_latin": "puella",
  "cases": ["nominativus", "accusativus", "genitivus"],  // o "all" para todos
  "numbers": ["singular", "plural"]  // o solo uno
}
```

### 2. ⚔️ Conjugación (`conjugation`)

Practica la conjugación de verbos en diferentes tiempos y modos.

**Campos de configuración**:
```json
{
  "word_latin": "amo",
  "tense": "present",
  "voice": "active",
  "mood": "indicative",
  "persons": ["1", "2", "3"],
  "numbers": ["singular", "plural"]
}
```

### 3. 🎯 Opción Múltiple (`multiple_choice`)

Preguntas con múltiples opciones de respuesta.

**Campos de configuración**:
```json
{
  "question": "¿Cuál es el genitivo singular de 'puella'?",
  "options": ["puellae", "puellam", "puellā", "puellās"],
  "correct_answer": "puellae",
  "explanation": "'puellae' es el genitivo singular de la 1ª declinación"
}
```

### 4. 🌍 Traducción (`translation`)

Traduce frases del español al latín o viceversa.

**Campos de configuración**:
```json
{
  "source_text": "La niña es buena",
  "target_language": "latin",
  "expected_answer": "Puella bona est",
  "alternatives": ["Bona est puella", "Est puella bona"]
}
```

### 5. 🔍 Análisis Sintáctico (`syntax`)

Identifica funciones sintácticas en oraciones latinas.

**Campos de configuración**:
```json
{
  "sentence": "Puella rosam amat",
  "tasks": [
    {"element": "puella", "question": "función", "answer": "sujeto"},
    {"element": "rosam", "question": "caso", "answer": "acusativo"},
    {"element": "amat", "question": "tiempo", "answer": "presente"}
  ]
}
```

### 6. 🧩 Ordenar Palabras (`sentence_order`)

Ordena palabras para formar una oración correcta.

**Campos de configuración**:
```json
{
  "correct_sentence": "Puella rosam amat",
  "scrambled_words": ["amat", "puella", "rosam"],
  "distractors": ["puer", "videt"]  // palabras extra opcionales
}
```

### 7. 🔗 Emparejar (`match_pairs`)

Empareja términos latinos con sus traducciones o formas.

**Campos de configuración**:
```json
{
  "pairs": [
    {"latin": "puella", "spanish": "niña"},
    {"latin": "rosa", "spanish": "rosa"},
    {"latin": "amo", "spanish": "amar"}
  ]
}
```

---

## Creación Manual de Desafíos

### Usando el Panel Admin

1. **Acceder al Panel Admin**
   - Ir a la página `⚙️ Admin`
   - Introducir contraseña (por defecto: `admin123`)

2. **Navegar a Gestión de Desafíos**
   - Buscar la sección de "Desafíos" o "Challenges"
   - Click en "➕ Crear Nuevo Desafío"

3. **Completar Formulario**

   **Campos Obligatorios**:
   - `Título`: Nombre descriptivo del desafío
   - `Descripción`: Explicación de qué practica
   - `Tipo`: Seleccionar del menú desplegable
   - `Nivel`: 1-10
   - `Recompensa XP`: Puntos que otorga (sugerido: 10-50)

   **Campos Opcionales**:
   - `Prerequisitos`: IDs de desafíos que deben completarse antes
   - `Tema gramatical`: Ej: "1ª declinación", "presente indicativo"

4. **Configurar el Desafío (JSON)**

   En el campo `config`, ingresar la configuración en formato JSON según el tipo de desafío (ver ejemplos arriba).

   > **⚠️ Importante**: El JSON debe estar correctamente formateado. Usa un validador JSON si tienes dudas.

5. **Guardar**
   - Click en "💾 Guardar Desafío"
   - El sistema validará la configuración
   - Si hay errores, se mostrarán mensajes específicos

---

## Configuración de Progresión

### Sistema de Prerequisitos

Los prerequisitos controlan qué desafíos deben completarse antes de desbloquear otros.

**Formato del campo `requires_challenge_ids`** (JSON string):
```json
"[1, 2, 3]"
```

Esto significa que los desafíos 1, 2 y 3 deben completarse antes de que este desafío se desbloquee.

### Ejemplo de Progresión

```
Nivel 1:
 Desafío 1: Declinación de 'puella' (sin prerequisitos)
 Desafío 2: Declinación de 'rosa' (prerequisito: [1])
 Desafío 3: Quiz 1ª declinación (prerequisitos: [1, 2])

Nivel 2:
 Desafío 4: Declinación de 'dominus' (prerequisitos: [3])
 ...
```

### Recomendaciones de XP

| Tipo de Desafío | XP Sugerido |
|-----------------|-------------|
| Declinación básica (3 casos) | 10-15 XP |
| Declinación completa (6 casos) | 20-30 XP |
| Conjugación (un tiempo) | 15-20 XP |
| Opción múltiple (fácil) | 5-10 XP |
| Traducción | 20-30 XP |
| Análisis sintáctico | 25-40 XP |

---

## Ejemplos Prácticos

### Ejemplo 1: Desafío de Declinación Básico

```json
{
  "title": "Declinación de puella - Casos Básicos",
  "description": "Declina 'puella' en los 3 casos fundamentales (Nom, Acc, Gen) en singular y plural",
  "challenge_type": "declension",
  "level": 1,
  "xp_reward": 15,
  "config": "{\"word_latin\": \"puella\", \"cases\": [\"nominativus\", \"accusativus\", \"genitivus\"], \"numbers\": [\"singular\", \"plural\"]}",
  "requires_challenge_ids": null,
  "grammar_topic": "1ª declinación - femenino"
}
```

### Ejemplo 2: Desafío de Conjugación

```json
{
  "title": "Presente Indicativo de 'amo'",
  "description": "Conjuga el verbo 'amo' en presente indicativo activo",
  "challenge_type": "conjugation",
  "level": 2,
  "xp_reward": 20,
  "config": "{\"word_latin\": \"amo\", \"tense\": \"present\", \"voice\": \"active\", \"mood\": \"indicative\", \"persons\": [\"1\", \"2\", \"3\"], \"numbers\": [\"singular\", \"plural\"]}",
  "requires_challenge_ids": "[1]",
  "grammar_topic": "1ª conjugación - presente"
}
```

### Ejemplo 3: Opción Múltiple

```json
{
  "title": "Quiz: Casos Latinos",
  "description": "Identifica el caso correcto de las formas latinas",
  "challenge_type": "multiple_choice",
  "level": 1,
  "xp_reward": 10,
  "config": "{\"question\": \"¿En qué caso está 'puellam'?\", \"options\": [\"Nominativo\", \"Acusativo\", \"Genitivo\", \"Dativo\"], \"correct_answer\": \"Acusativo\", \"explanation\": \"'puellam' es el acusativo singular de puella\"}",
  "requires_challenge_ids": "[1]",
  "grammar_topic": "Casos gramaticales"
}
```

### Ejemplo 4: Ordenar Palabras

```json
{
  "title": "Construye una oración en latín",
  "description": "Ordena las palabras para formar la oración 'La niña ama la rosa'",
  "challenge_type": "sentence_order",
  "level": 2,
  "xp_reward": 15,
  "config": "{\"correct_sentence\": \"Puella rosam amat\", \"scrambled_words\": [\"rosam\", \"amat\", \"puella\"], \"distractors\": [\"puer\", \"videt\"]}",
  "requires_challenge_ids": "[1, 2]",
  "grammar_topic": "Orden de palabras - SOV"
}
```

---

## Solución de Problemas

### Error: "JSON inválido en campo config"

**Causa**: El JSON no está correctamente formateado.

**Solución**:
1. Copia el contenido del campo `config`
2. Pégalo en un validador JSON online (ej: jsonlint.com)
3. Corrige los errores señalados
4. Vuelve a pegar el JSON corregido

### Error: "Palabra no encontrada en la base de datos"

**Causa**: La palabra especificada en `word_latin` no existe en el vocabulario.

**Solución**:
1. Ir a `Admin` → `Vocabulario` → `Lista Completa`
2. Buscar la palabra
3. Si no existe, añadirla primero antes de crear el desafío

### Error: "Prerequisitos no válidos"

**Causa**: Uno o más IDs de prerequisitos no existen.

**Solución**:
1. Verificar que los IDs existen en la tabla de desafíos
2. Asegurarse que el formato es un array JSON: `"[1, 2, 3]"`

### El desafío no se muestra en el Mapa

**Posibles causas**:
1. **Prerequisitos no cumplidos**: El usuario aún no completó los desafíos requeridos
2. **Nivel muy alto**: El desafío requiere un nivel de usuario superior al actual
3. **No guardado correctamente**: Verificar que se guardó sin errores

**Solución**: Revisar los logs y la configuración del desafío.

---

## Recursos Adicionales

- Ver [PROJECT_STATUS.md](file:///home/diego/Projects/latin-python/docs/PROJECT_STATUS.md) para información técnica detallada
- Consultar [ARCHITECTURE.md](file:///home/diego/Projects/latin-python/docs/ARCHITECTURE.md) para entender la estructura de la base de datos
- Revisar `utils/challenge_engine.py` para ver cómo se verifican las respuestas

---

## Contacto y Soporte

Si encuentras problemas o necesitas ayuda adicional, consulta la documentación técnica o revisa el código fuente en el repositorio del proyecto.

---

<div style="text-align: center; margin-top: 40px; padding: 20px; background: rgba(139,69,19,0.1); border-radius: 10px;">
  <p style="font-size: 1.2em;">📜 <strong>Lingua Latina Viva</strong></p>
  <p style="font-style: italic;">"Non scholae, sed vitae discimus"</p>
</div>
