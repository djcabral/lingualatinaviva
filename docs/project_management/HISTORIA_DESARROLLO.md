# Historia del Desarrollo de Lingua Latina Viva

## Documentación Completa del Proceso de Creación

---

## Fase 0: Concepción y Planificación Inicial

### Objetivo Original
Crear una aplicación educativa interactiva para el aprendizaje del latín clásico, combinando:
- Gramática estructurada por lecciones
- Sistema de memorización espaciada (SRS)
- Práctica interactiva
- Análisis sintáctico
- Gamificación

### Stack Tecnológico Elegido
- **Framework**: Streamlit (Python) - Por su rapidez de desarrollo y componentes UI nativos
- **Base de Datos**: SQLite + SQLModel - Simplicidad y portabilidad
- **NLP Latino**: CLTK (Classical Language Toolkit) - Análisis morfológico
- **Estilo**: CSS personalizado - Control total sobre la estética

---

## Fase 1: Estructura Básica y Modelos de Datos

### 1.1 Arquitectura Inicial (Semanas 1-2)

**Decisiones Arquitectónicas:**
- Estructura modular con páginas Streamlit separadas
- Sistema de navegación basado en `st.switch_page()`
- Módulos reutilizables en `pages/modules/`

**Modelos de Datos Creados:**
```python
# database/models.py - Primera versión
- Word: Vocabulario latino con morfología
- Author: Autores clásicos
- Text: Textos para lectura
- ReviewLog: Sistema SRS
- UserProfile: Perfil del usuario
- Challenge: Sistema de desafíos gamificados
```

**Problema Encontrado:**
- Duplicación de modelos causaba errores de registro en SQLAlchemy
- **Solución**: Implementación de `models_loader.py` con caché de Streamlit

### 1.2 Sistema de Lecciones (Semana 3)

**Enfoque Inicial: Hardcoded**
- Lecciones 1-40 como funciones Python en `course_view.py`
- Contenido en markdown renderizado con `st.markdown()`
- Imágenes estáticas en `static/images/curso_gramatica/`

**Ventajas:**
- Desarrollo rápido
- Control total del contenido
- Fácil de iterar

**Desventajas:**
- Difícil de mantener a escala
- No editable sin código
- Archivo `course_view.py` creció a +180KB

---

## Fase 2: Sistemas de Práctica y Memorización

### 2.1 Módulo de Vocabulario (Semanas 4-5)

**Características Implementadas:**
- Sistema SRS basado en algoritmo SM-2
- Tarjetas de repaso con análisis morfológico
- Estadísticas de progreso
- Filtros por nivel y parte del discurso

**Archivo:** `pages/modules/vocab_view.py`

**Desafío Técnico:**
- Sincronización entre `ReviewLog` y `UserVocabularyProgress`
- **Solución**: Tabla `UserVocabularyProgress` como fuente de verdad

### 2.2 Práctica de Declinaciones (Semana 6)

**Implementación:**
- Generador automático de formas declinadas
- Sistema de validación con normalización de macrones
- Modos: Guiado, Libre, Desafío
- Integración con sistema de XP

**Archivo:** `pages/modules/declensions_view.py`

**Lógica Morfológica:**
- `utils/latin_logic.py`: Clase `LatinMorphology`
- Soporte para 5 declinaciones
- Manejo de excepciones (vis, bos, sus, etc.)
- Neutros, pluralia tantum, singularia tantum

### 2.3 Práctica de Conjugaciones (Semana 7)

**Características:**
- 4 conjugaciones + mixta
- Todos los tiempos y modos
- Voz activa y pasiva
- Verbos irregulares (sum, possum, eo, fero, volo, nolo, malo)

**Archivo:** `pages/modules/conjugations_view.py`

**Problema Crítico Resuelto:**
- Conjugaciones no cargaban por datos "sucios" en vocabulario
- Palabras con sufijos `_1242`, `_363`, etc.
- **Solución**: Script `vocabulary_cleanup.py` + migración de datos

---

## Fase 3: Análisis Sintáctico y Lecturas

### 3.1 Sistema de Análisis (Semanas 8-9)

**Componentes:**
- `SentenceAnalysis`: Oraciones analizadas con LatinCy
- `TokenAnnotation`: Anotaciones pedagógicas por palabra
- `SyntaxCategory`: Categorización jerárquica
- `SentenceStructure`: Identificación de cláusulas

**Archivos:**
- `database/syntax_models.py`
- `pages/modules/syntax_view.py`
- `utils/text_analyzer.py`

**Integración CLTK:**
- Análisis morfológico automático
- Generación de árboles de dependencias
- Caché de análisis para performance

### 3.2 Lecturas Interactivas (Semana 10)

**Innovación Principal:**
- Texto latino con tooltips hover
- Análisis morfológico instantáneo
- Código de colores por maestría:
  - Verde: ≥70% (bien aprendida)
  - Naranja: 40-70% (en progreso)
  - Púrpura: <40% (con dificultades)
  - Gris: Sin estudiar

**Archivo:** `pages/modules/readings_view.py`

**CSS Personalizado:**
- Tooltips con gradientes
- Posicionamiento inteligente (evita bordes)
- Responsive design

---

## Fase 4: Gamificación y Desafíos

### 4.1 Sistema de Desafíos (Semanas 11-12)

**Arquitectura:**
- `Challenge`: Configuración del desafío (JSON)
- `UserChallengeProgress`: Progreso individual
- Sistema de estrellas (0-3)
- Desbloqueo progresivo

**Tipos de Desafíos:**
1. Declinación
2. Conjugación
3. Opción múltiple
4. Traducción
5. Sintaxis

**Archivo:** `pages/modules/challenges_view.py`

### 4.2 Módulo Ludus - Juegos Educativos (Semana 13)

**Juegos Implementados:**

1. **Clasificador de Palabras**
   - Arrastrar palabras a categorías
   - Validación en tiempo real
   - Animaciones con confetti

2. **Sopa de Letras**
   - Generación algorítmica de tablero
   - Selección interactiva
   - Palabras en todas direcciones

3. **Crucigrama Latino**
   - Grid dinámico
   - Pistas en español
   - Validación letra por letra

**Archivo:** `pages/06_🎮_Ludus.py`

**Desafío Técnico:**
- Estado del juego no se reseteaba correctamente
- **Solución**: Gestión explícita de `st.session_state` con claves únicas

---

## Fase 5: Administración y Gestión de Contenido

### 5.1 Panel de Administración (Semanas 14-15)

**Secciones Implementadas:**

1. **Gestión de Vocabulario**
   - CRUD completo
   - Importación masiva CSV
   - Validación de datos

2. **Gestión de Textos**
   - Editor de textos clásicos
   - Vinculación con autores
   - Análisis automático

3. **Gestión de Lecciones**
   - Editor markdown
   - Carga de imágenes
   - Preview en vivo

4. **Gestión de Sintaxis**
   - Categorización de oraciones
   - Anotaciones pedagógicas

5. **Gestión de Usuarios**
   - Progreso actual
   - Reset de progreso (gamificación/aprendizaje/total)
   - Configuración de perfil

6. **Estadísticas**
   - Métricas del corpus
   - Distribución por tipo
   - Gráficos interactivos

**Archivo:** `pages/99_⚙️_Administracion.py` (101KB)

### 5.2 Requisitos de Lección (Semana 16)

**Sistema Implementado:**
- `LessonRequirement`: Requisitos configurables por lección
- `UserLessonProgress`: Seguimiento de cumplimiento
- Filosofía: 100% requisitos obligatorios (strict mode)

**Tipos de Requisitos:**
- `vocabulary_mastery`: Dominio de vocabulario
- `challenge_completion`: Completar desafíos
- `analysis_practice`: Práctica de análisis
- `reading_completion`: Lecturas completadas
- `exercise_completion`: Ejercicios completados

**Criterios JSON Flexibles:**
```json
{
  "min_words": 20,
  "min_accuracy": 0.8
}
```

---

## Fase 6: Refactorización y Estabilización

### 6.1 Limpieza de Vocabulario (Semana 17)

**Problema:**
- CSV con 1879 palabras "sucias": `syllaba_1242`, `puella_363`
- Duplicados masivos
- Módulos de práctica fallaban

**Solución Implementada:**

1. **Script de Limpieza:** `vocabulary_cleanup.py`
   - Remover sufijos `_número`
   - Eliminar duplicados
   - Backup automático

2. **Script de Aplicación:** `apply_vocabulary_fix.py`
   - Limpiar tabla `Word`
   - Reimportar vocabulario limpio
   - Re-aplicar migraciones

3. **Verificación:** `diagnose_conjugation.py`
   - 0 palabras sucias después de limpieza
   - 28 verbos funcionando correctamente

**Resultado:**
- Vocabulario 100% limpio
- Conjugaciones cargando correctamente
- Base de datos consistente

### 6.2 Protección contra Duplicación de Modelos (Semana 18)

**Problema:**
- Error: "Multiple classes found for path 'UserLessonProgress'"
- Streamlit recargaba módulos causando doble registro

**Solución:**
- Singleton guards en todos los archivos de modelos:
  ```python
  if '__INTEGRATION_MODELS_MODULE_LOADED__' in globals():
      logger.warning("⚠️ WARNING: Reloading detected!")
  else:
      globals()['__INTEGRATION_MODELS_MODULE_LOADED__'] = True
  ```

**Archivos Protegidos:**
- `database/models.py`
- `database/integration_models.py`
- `database/syntax_models.py`

### 6.3 Mejoras de UI/UX (Semana 19)

**Tablas Estilizadas:**
- Función `render_styled_table()` en lecciones
- Reemplazo de tablas markdown por HTML estilizado
- Headers con gradientes
- Responsive design

**Diagramas Mermaid:**
- Corrección de sintaxis (quotes en labels)
- Full-width rendering
- Fallback a infografías cuando falla

**Paradigm Generator:**
- Refactorización de tablas
- Participios como tablas de declinación
- Filtros persistentes

---

## Fase 7: Contenido Visual y Educativo

### 7.1 Generación de Imágenes (Semanas 20-22)

**Estrategia:**
- Imagen AI con prompts en español
- Estilo coherente (tonos cálidos, históricamente preciso)
- 3 imágenes por lección básica/intermedia
- 1 imagen por lección experta

**Imágenes Generadas:**

**Lecciones Básicas (1-10):**
- Lección 1: Mapa Imperio Romano + Alfabeto
- Lección 2: Foro Romano
- Lección 3: Diagrama declinaciones
- Lección 4: Vida cotidiana
- Lección 5: Diagrama del neutro
- Lección 6: Arquitectura + Conjugaciones
- Lección 7: 3ª Declinación
- Lección 8: Pretérito Perfecto
- Lección 9: 5ª Declinación
- Lección 10: Adjetivos 2ª Clase

**Lecciones Intermedias (11-20):**
- Lección 11: Grados del adjetivo
- Lección 12: Pronombres demostrativos
- Lección 13: Voz pasiva
- Lección 14: Pluscuamperfecto
- Lección 15-17: Voz pasiva y deponentes
- Lección 18-19: Subjuntivo

**Lecciones Avanzadas (20-30):**
- Infografías de infinitivos, participios
- Subordinadas (finales, consecutivas, causales, temporales)
- Ablativo absoluto, gerundio/gerundivo, perifrásticas
- Condicionales, relativas, estilo indirecto
- Métrica latina

**Lecciones Expertas (31-40):**
- Retratos de autores clásicos
- Mapas históricos
- Manuscritos y símbolos

### 7.2 Infografías Culturales (Semana 23)

**Creadas:**
- Medidas romanas
- Calendario y tiempo
- Geografía militar
- Numeración romana

**Integración:**
- Embebidas en lecciones relevantes
- Carruseles para múltiples imágenes
- Captions descriptivos

---

## Fase 8: Arquitectura Lección-Céntrica (Semana 24)

### 8.1 Modelos de Integración

**Nuevos Modelos:**
```python
# database/integration_models.py
- LessonProgress: Progreso por lección
- LessonVocabulary: Vocabulario esencial por lección
- UserVocabularyProgress: Progreso individual de palabras
- ExerciseAttempt: Registro de intentos
- ReadingProgress: Progreso en lecturas
- SyntaxAnalysisProgress: Oraciones analizadas
- UserProgressSummary: Resumen global
- UnlockCondition: Sistema de desbloqueo
- Recommendation: Motor de recomendaciones
- LessonRequirement: Requisitos por lección
- UserLessonProgress: Cumplimiento de requisitos
```

### 8.2 Migración de Datos

**Scripts Creados:**
- `database/migrate_phase2.py`: Agregar `usage_type` a `SentenceAnalysis`
- `database/migrate_phase3.py`: Crear tablas de integración
- `scripts/migrate_integration_tables.py`: Poblar datos iniciales

---

## Fase 9: Características Avanzadas (Semanas 25-26)

### 9.1 Generador de Paradigmas

**Funcionalidad:**
- Generación automática de paradigmas completos
- Sustantivos: Todas las declinaciones
- Adjetivos: 1ª/2ª clase, comparativos
- Verbos: Todos los tiempos, modos, voces
- Pronombres: Personales, demostrativos, relativos

**Archivo:** `pages/modules/paradigm_generator_view.py`

**Mejoras:**
- Tablas estilizadas consistentes
- Participios como tablas de declinación
- Filtros persistentes en session_state

### 9.2 Diccionario Interactivo

**Características:**
- Búsqueda por latín o español
- Filtros por parte del discurso
- Edición rápida desde resultados
- Navegación a panel admin

**Archivo:** `pages/modules/dictionary_view.py`

### 9.3 Scriptorium - Práctica Libre

**Concepto:**
- Espacio de escritura libre en latín
- Análisis morfológico en tiempo real
- Sin evaluación, solo exploración

**Archivo:** `pages/modules/scriptorium_view.py`

---

## Fase 10: Optimizaciones y Performance (Semana 27)

### 10.1 Caché de Análisis de Texto

**Problema:**
- Análisis CLTK muy lento (5-10s por texto)
- Re-análisis en cada carga de página

**Solución:**
```python
# utils/text_cache.py
- Caché en base de datos
- Serialización JSON de análisis
- Invalidación inteligente
```

**Resultado:**
- Carga de textos: 5s → 0.1s
- Experiencia de usuario fluida

### 10.2 Lazy Loading de Módulos

**Implementación:**
- Importación condicional de CLTK
- Carga diferida de modelos pesados
- Reducción de tiempo de inicio

### 10.3 Optimización de Queries

**Mejoras:**
- Índices en columnas frecuentes
- Eager loading de relaciones
- Reducción de N+1 queries

---

## Fase 11: Preferencias de Usuario (Semana 28 - ACTUAL)

### 11.1 Tamaño de Letra Configurable

**Implementación:**
- Campo `preferences_json` en `UserProfile`
- Slider en sidebar (1.0x - 3.0x)
- CSS dinámico con f-strings
- Persistencia automática

**Migración:**
```python
# database/add_preferences_column.py
ALTER TABLE userprofile ADD COLUMN preferences_json TEXT
```

**Archivos Modificados:**
- `database/models.py`: Nuevo campo
- `pages/modules/readings_view.py`: Slider + CSS dinámico

---

## Arquitectura Final

### Estructura de Directorios

```
latin-python/
├── app.py                          # Punto de entrada
├── pages/
│   ├── 01_🏠_Inicio.py
│   ├── 02_📘_Lecciones.py
│   ├── 03_🧠_Memorización.py
│   ├── 04_⚔️_Práctica.py
│   ├── 05_🔍_Análisis.py
│   ├── 06_🎮_Ludus.py
│   ├── 07_📧_Contacto.py
│   ├── 99_⚙️_Administracion.py
│   └── modules/
│       ├── course_view.py          # 40 lecciones hardcoded
│       ├── vocab_view.py           # SRS
│       ├── declensions_view.py     # Práctica declinaciones
│       ├── conjugations_view.py    # Práctica conjugaciones
│       ├── readings_view.py        # Lecturas interactivas
│       ├── syntax_view.py          # Análisis sintáctico
│       ├── challenges_view.py      # Desafíos gamificados
│       ├── paradigm_generator_view.py
│       ├── dictionary_view.py
│       └── scriptorium_view.py
├── database/
│   ├── models.py                   # Modelos core
│   ├── integration_models.py      # Modelos de integración
│   ├── syntax_models.py            # Modelos de sintaxis
│   ├── models_loader.py            # Caché de modelos
│   ├── connection.py               # Gestión de sesiones
│   ├── seed.py                     # Datos iniciales
│   └── migrate_*.py                # Scripts de migración
├── utils/
│   ├── latin_logic.py              # Lógica morfológica
│   ├── text_analyzer.py            # Análisis CLTK
│   ├── text_cache.py               # Caché de análisis
│   ├── srs.py                      # Algoritmo SM-2
│   ├── ui_helpers.py               # Helpers de UI
│   └── i18n.py                     # Internacionalización
├── static/
│   ├── images/
│   │   ├── curso_gramatica/        # 61 imágenes de lecciones
│   │   └── infografias/            # Infografías culturales
│   └── css/
│       └── styles.css              # Estilos globales
└── data/
    ├── vocabulary.csv              # Vocabulario limpio
    └── texts/                      # Textos clásicos
```

### Stack Tecnológico Completo

**Backend:**
- Python 3.11
- Streamlit 1.32+
- SQLModel (SQLAlchemy + Pydantic)
- SQLite

**NLP:**
- CLTK (Classical Language Toolkit)
- LatinCy (spaCy para latín)

**Frontend:**
- Streamlit Components
- Custom CSS
- HTML/JavaScript embebido

**Utilidades:**
- Pandas (manipulación de datos)
- JSON (configuración y caché)

---

## Métricas del Proyecto

### Código
- **Líneas de código**: ~15,000
- **Archivos Python**: 45+
- **Modelos de datos**: 25
- **Páginas Streamlit**: 8

### Contenido
- **Lecciones**: 40
- **Palabras en vocabulario**: ~2,500 (limpiadas)
- **Imágenes generadas**: 70+
- **Textos clásicos**: 10+
- **Oraciones analizadas**: 100+

### Base de Datos
- **Tablas**: 30
- **Tamaño**: ~50MB
- **Migraciones**: 8

---

## Lecciones Aprendidas

### 1. Arquitectura
- ✅ **Modularización temprana** evitó refactorizaciones masivas
- ✅ **Separación de concerns** (models, views, utils) facilitó mantenimiento
- ⚠️ **Hardcoded lessons** funcionó para MVP pero no escala
- ⚠️ **Session state** de Streamlit requiere gestión cuidadosa

### 2. Base de Datos
- ✅ **SQLModel** excelente balance entre ORM y validación
- ✅ **Migraciones incrementales** permitieron evolución gradual
- ⚠️ **Duplicación de modelos** causó problemas sutiles
- ✅ **Singleton pattern** resolvió problemas de registro

### 3. Performance
- ✅ **Caché agresivo** crítico para análisis NLP
- ✅ **Lazy loading** mejoró tiempo de inicio
- ⚠️ **CLTK** muy lento, considerar alternativas

### 4. UX/UI
- ✅ **Tooltips hover** mejor que modales para análisis
- ✅ **Código de colores** intuitivo para maestría
- ✅ **Gamificación** aumenta engagement
- ⚠️ **Navegación** podría ser más fluida

### 5. Contenido
- ✅ **Imágenes AI** aceleró creación de contenido visual
- ✅ **Markdown** flexible para lecciones
- ⚠️ **40 lecciones hardcoded** difícil de mantener
- ✅ **Infografías** mejor que diagramas Mermaid

---

## Próximos Pasos (Plan Maestro)

### Corto Plazo
1. ✅ Control de tamaño de letra (COMPLETADO)
2. 🔄 Verificar integración de imágenes pendientes
3. 📋 Continuar con Stage 2 del Plan Maestro
4. 🎨 Completar tríadas visuales (3 imágenes/lección)

### Mediano Plazo
- Migrar lecciones a base de datos
- Sistema de hints contextuales
- Generación de ejercicios automáticos
- Exportación de progreso

### Largo Plazo
- App móvil (React Native + API)
- Modo offline
- Comunidad de usuarios
- Contenido generado por usuarios

---

## Conclusión

El desarrollo de **Lingua Latina Viva** ha sido un proceso iterativo y evolutivo, pasando de un MVP simple a una plataforma educativa completa con:

- ✅ 40 lecciones estructuradas
- ✅ Sistema SRS completo
- ✅ Práctica interactiva (declinaciones, conjugaciones)
- ✅ Análisis sintáctico automático
- ✅ Lecturas con tooltips morfológicos
- ✅ Gamificación (desafíos, juegos)
- ✅ Panel de administración robusto
- ✅ 70+ imágenes educativas
- ✅ Preferencias de usuario persistentes

La aplicación demuestra que es posible crear herramientas educativas sofisticadas con tecnologías modernas, manteniendo un enfoque en la experiencia del usuario y la calidad del contenido pedagógico.

---

**Fecha de Documentación**: 30 de Noviembre, 2024  
**Versión de la Aplicación**: 2.0  
**Estado**: En desarrollo activo
