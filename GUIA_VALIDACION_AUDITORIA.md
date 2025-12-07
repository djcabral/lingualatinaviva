# 🔍 Sistema de Validación y Auditoría - Asistentes de Carga

## Descripción General

El sistema de validación y auditoría proporciona tres capas de protección para garantizar la integridad de los datos:

1. **Validación de Duplicados** ✔️ - Detecta datos ya existentes en la BD
2. **Validación de Completitud** ✔️ - Asegura que la información sea completa y de calidad
3. **Sistema de Auditoría** 📋 - Registra quién cargó qué y cuándo

---

## 1. Validación de Duplicados

### ¿Qué hace?

Detecta si los datos que el usuario intenta cargar ya existen en la base de datos.

### Para Vocabulario

**Busca por:**
- Coincidencia exacta de palabra en latín
- Similitud de palabras (85%+) en modo flexible

**Ejemplos:**
- Si intentas cargar "puella" y ya existe → **DUPLICADO**
- Si intentas cargar "puela" (similar a "puella") → **ADVERTENCIA** en modo flexible

### Para Oraciones

**Busca por:**
- Texto exacto de la oración
- Reconoce incluso pequeñas variaciones de puntuación

**Ejemplo:**
```
Oración a cargar: "Magister discipulos docet."
Ya existe: "Magister discipulos docet."
Resultado: DUPLICADO DETECTADO
```

### Para Textos

**Busca por:**
- Título exacto
- Combinación título + autor

**Ejemplo:**
```
Título: "Fabula de Aesopo"
Autor: "Aesopus"
Si ya existe con estos datos → DUPLICADO
```

---

## 2. Validación de Completitud

### ¿Qué hace?

Verifica que los datos sean completos y cumplan con estándares de calidad.

### Para Vocabulario

**Campos Obligatorios:**
- ✅ Palabra en latín
- ✅ Traducción
- ✅ Categoría gramatical (POS)

**Campos Recomendados (según POS):**
- **Para sustantivos:** Genitivo, género, declinación
- **Para verbos:** Partes principales, conjugación
- **Otros:** Nivel de dificultad

**Puntuación de Completitud:**
- 100% = Todos los campos obligatorios + importantes presentes
- 75% = Solo obligatorios
- < 75% = Incompleto

**Ejemplos de Validación:**

✅ **VÁLIDO - 100% Completo:**
```
Palabra: "puella"
Traducción: "niña"
POS: "noun"
Genitivo: "puellae"
Género: "f"
Declinación: "1"
```

⚠️ **VÁLIDO CON ADVERTENCIA - 75% Completo:**
```
Palabra: "puella"
Traducción: "niña"
POS: "noun"
[Falta: Genitivo, Género]
```

❌ **INVÁLIDO:**
```
Palabra: "puella"
[Falta: Traducción, POS]
```

### Para Oraciones

**Campos Obligatorios:**
- ✅ Texto en latín
- ✅ Traducción
- ✅ Nivel de dificultad

**Validaciones Adicionales:**
- Longitud mínima: 5 caracteres
- Puntuación apropiada (. ! ?)
- Traducción coherente

**Ejemplos:**

✅ **VÁLIDO:**
```
Latín: "Magister discipulos docet."
Traducción: "El maestro enseña a los discípulos."
Nivel: 1
Longitud: ✓ > 5 caracteres
Puntuación: ✓ Termina en punto
```

❌ **INVÁLIDO:**
```
Latín: "magister"  [Solo 1 palabra]
Traducción: "teacher"
→ Error: Texto demasiado corto (< 5 caracteres)
```

### Para Textos

**Campos Obligatorios:**
- ✅ Título
- ✅ Autor
- ✅ Contenido
- ✅ Dificultad

**Validaciones Adicionales:**
- Mínimo 10 palabras en el contenido
- Recomendación: 50+ palabras para análisis completo

**Ejemplos:**

✅ **VÁLIDO:**
```
Título: "Fábula de la Hormiga y la Cigarra"
Autor: "Phaedrus"
Contenido: [300 palabras en latín]
Dificultad: 2
```

❌ **INVÁLIDO:**
```
Título: "Test"
Autor: "Desconocido"
Contenido: "est" [Solo 1 palabra]
→ Error: Contenido muy corto
```

---

## 3. Sistema de Auditoría

### ¿Qué registra?

El sistema registra automáticamente cada carga con:

- **Timestamp**: Fecha y hora exacta
- **Usuario**: Quién realizó la carga (usuario autenticado)
- **Acción**: Tipo de operación (ADD, UPDATE, DELETE, etc.)
- **Datos Cargados**: Contenido completo
- **Validación**: Estado (éxito, advertencia, error)
- **Duplicados Detectados**: Si los hay
- **Puntuación de Completitud**: Porcentaje

### Estructura del Log

```json
{
  "timestamp": "2025-12-07T14:30:45.123456",
  "action": "vocabulary_add",
  "user_id": "admin_user",
  "data_type": "vocabulary",
  "data_id": 725,
  "validation_status": "success",
  "completeness_score": 0.95,
  "duplicates_found": [],
  "new_value": {
    "latin_word": "puella",
    "translation": "niña",
    "part_of_speech": "noun",
    "genitive": "puellae",
    "gender": "f",
    "declension": "1",
    "level": 1
  }
}
```

### Acceso a Auditoría

En la sección de Administración → Auditoría, puedes:

1. **Ver tabla de logs**: Resumen rápido de todas las cargas
2. **Detalles de log**: Expandir para ver exactamente qué se cargó
3. **Exportar reporte**: Descargar en JSON o CSV

---

## 4. Niveles de Validación

### 🔴 ESTRICTO

- ❌ Rechaza **cualquier duplicado** (sin excepciones)
- ❌ Requiere **completitud total** (100%)
- ✅ Ideal para: Base de datos de producción con datos críticos

**Comportamiento:**
```
Si hay duplicado → RECHAZA ("DUPLICADO DETECTADO")
Si falta campo → RECHAZA ("Campo obligatorio faltante")
Si completitud < 100% → RECHAZA
```

### 🟡 MODERADO (PREDETERMINADO)

- ⚠️ Advierte sobre duplicados pero permite continuar
- ✅ Requiere solo campos obligatorios
- ✅ Ideal para: Modo balance entre flexibilidad y calidad

**Comportamiento:**
```
Si hay duplicado → ADVERTENCIA ("Posible duplicado")
Permite cargar si hay errores → SI (con confirmación)
Completitud < 100% → OK (solo si hay obligatorios)
```

### 🟢 FLEXIBLE

- ℹ️ Solo advierte sobre todo
- ✅ Máxima flexibilidad
- ⚠️ Ideal para: Testing, datos preliminares

**Comportamiento:**
```
Si hay duplicado → INFO ("Posible duplicado")
Permite cargar siempre → SI
Sin requerimientos estrictos → SI
```

---

## 5. Ejemplos de Uso

### Flujo Típico: Cargar Palabra Completa

```
1. Usuario selecciona "Nivel: MODERADO"
2. Abre asistente de Vocabulario
3. Completa: "puella", "niña", "noun", "puellae", "f", "1"
4. Sistema valida:
   ✅ No es duplicado
   ✅ 100% completa
   ✅ Todos los campos válidos
5. Muestra: "✅ VÁLIDO - 100% Completo"
6. Usuario hace clic en "Guardar"
7. Se registra en auditoría:
   - Timestamp: 2025-12-07 14:30
   - Usuario: admin_user
   - Validación: success
   - Completitud: 100%
```

### Flujo con Advertencia: Cargar Palabra Sin Algunos Detalles

```
1. Usuario selecciona "Nivel: MODERADO"
2. Completa: "amare", "amar", "verb" [SIN partes principales]
3. Sistema valida:
   ✅ No es duplicado
   ⚠️ 60% completa (faltan partes principales)
   ✅ Campos obligatorios presentes
4. Muestra:
   ✅ VÁLIDO (pero con advertencia)
   ⚠️ "Se recomienda incluir partes principales"
5. Usuario confirma: "Entiendo, guardar de todas formas"
6. Se registra en auditoría:
   - Validación: warning
   - Completitud: 60%
   - Mensaje: "Campos recomendados faltantes"
```

### Flujo con Error: Duplicado Detectado (Modo ESTRICTO)

```
1. Usuario selecciona "Nivel: ESTRICTO"
2. Intenta cargar: "puella" (ya existe en BD)
3. Sistema valida:
   ❌ DUPLICADO DETECTADO
   Muestra lista de coincidencias exactas:
   - ID: 1, Palabra: "puella", Traducción: "niña", Nivel: 1
4. Mensaje: "❌ INVÁLIDO - Esta palabra ya existe"
5. Usuario no puede guardar
6. Se registra en auditoría:
   - Acción: VALIDATION_ERROR
   - Validación: error
   - Duplicados encontrados: 1
```

---

## 6. Interpretación de Puntuación de Completitud

| Score | Significado | Acción Recomendada |
|-------|-------------|-------------------|
| 100% | Datos perfectamente completos | ✅ Guardar sin preocupaciones |
| 80-99% | Datos muy completos | ✅ Guardar (solo faltan campos opcionales) |
| 60-79% | Datos parcialmente completos | ⚠️ Revisar, considerar si faltan campos importantes |
| < 60% | Datos incompletos | ❌ Completar antes de guardar (si nivel=ESTRICTO) |

---

## 7. Interpretación de Duplicados

### Tipos de Duplicados

#### Exact Match (Coincidencia Exacta)
```
Detectado: palabra/texto/título es idéntico
Acción: 
  - ESTRICTO: RECHAZA
  - MODERADO: ADVIERTE
  - FLEXIBLE: INFO
```

#### Similar (Similitud > 85%)
```
Detectado: palabra similar pero no idéntica
Acción: 
  - Nivel flexible: ADVIERTE si similitud > 85%
  - Niveles estrictos: IGNORA
```

#### Title Duplicate (Texto)
```
Detectado: Mismo título (puede tener diferente autor)
Acción:
  - ESTRICTO: RECHAZA
  - MODERADO: ADVIERTE
  - FLEXIBLE: INFO
```

---

## 8. Casos de Uso

### ✅ Usar ESTRICTO

- Producción: BD con datos importantes
- Datos únicos: Nunca debe haber duplicados
- Información crítica: Necesita máxima calidad

### ✅ Usar MODERADO

- Desarrollo: Balance entre calidad y velocidad
- Importación: De múltiples fuentes
- Verificación: Auditor humano revisará después

### ✅ Usar FLEXIBLE

- Testing: Datos de prueba
- Preliminar: Antes de validación final
- Investigación: Exploración de contenidos

---

## 9. Integración en el Admin Panel

Los asistentes de carga incluyen automáticamente:

1. **Selector de Nivel** (arriba de cada asistente)
2. **Validación en Tiempo Real** (después de cada campo)
3. **Resumen de Validación** (al final de cada paso)
4. **Confirmación Antes de Guardar** (con detalles)
5. **Auditoría Automática** (registra cada carga)

---

## 10. Preguntas Frecuentes

### ¿Qué pasa si hay un duplicado?

**ESTRICTO:** No te permite guardar
**MODERADO:** Te advierte, puedes ignorar
**FLEXIBLE:** Solo te informa

### ¿Puedo cargar datos incompletos?

Depende del nivel:
- **ESTRICTO:** No, a menos que sean 100% completos
- **MODERADO:** Sí, si tienen campos obligatorios
- **FLEXIBLE:** Sí, sin restricciones

### ¿Dónde puedo ver los logs de auditoría?

En el panel de Admin → Sección "Auditoría" (próxima interfaz)

### ¿Puedo descargar los logs?

Sí, en formato JSON o CSV desde la sección de Auditoría

### ¿Se puede deshacer una carga?

En esta versión se registra en auditoría. La opción de deshacer está en desarrollo.

---

## 11. Recomendaciones

✅ **HACER:**
- Usar **MODERADO** como predeterminado
- Revisar advertencias incluso si cargas igual
- Mantener auditoría para trazabilidad
- Exportar logs periódicamente
- Usar ESTRICTO para datos críticos

❌ **NO HACER:**
- Ignorar completitud en palabras importantes
- Cargar el mismo dato múltiples veces
- Confiar en UI sin revisar la auditoría
- Eliminar logs de auditoría sin backup

---

## 12. Troubleshooting

### "Se detectó un duplicado pero estoy seguro de que es diferente"

→ Revisa detenidamente el registro existente en la BD. Quizá sea una variación muy similar que cumpla una función.

### "Mi vocabulario está incompleto pero necesito guardarlo"

→ Usa nivel FLEXIBLE o MODERADO. Luego puedes editarlo desde el admin cuando tengas los datos.

### "¿Por qué me rechaza si está todo en latín?"

→ Verifica que:
- La palabra tenga traducción al español
- Esté indicado el tipo gramatical (POS)
- Para sustantivos: el genitivo (obligatorio en ESTRICTO)

---

## Resumen Técnico

```
ComprehensiveValidator
├── DuplicateValidator
│   ├── check_vocabulary_duplicate()
│   ├── check_sentence_duplicate()
│   └── check_text_duplicate()
├── CompletenessValidator
│   ├── validate_vocabulary()
│   ├── validate_sentence()
│   └── validate_text()
└── AuditManager
    ├── create_vocabulary_audit()
    ├── create_sentence_audit()
    ├── create_text_audit()
    └── export_audit_report()
```

Toda la lógica se integra en el UI mediante:
- `admin_validation_audit_ui.py` - Componentes Streamlit
- Session state para persistencia
- Feedback visual en tiempo real

---

**Última actualización:** 2025-12-07
**Versión:** 1.0
**Estado:** Completo y listo para integración
