# Estado del Proyecto - Lingua Latina Viva
**Última actualización:** 23 de noviembre de 2025

---

## 📋 Tabla de Contenidos
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura y Stack Tecnológico](#arquitectura-y-stack-tecnológico)
3. [Módulos Implementados](#módulos-implementados)
4. [Sistema de Base de Datos](#sistema-de-base-de-datos)
5. [Funcionalidades Completadas](#funcionalidades-completadas)
6. [Trabajo Pendiente](#trabajo-pendiente)
7. [Hoja de Ruta Futura](#hoja-de-ruta-futura)

---

## 🎯 Resumen Ejecutivo

**Lingua Latina Viva** es una aplicación de aprendizaje de latín clásico con enfoque académico riguroso y gamificación educativa. El proyecto ha alcanzado un estado funcional con múltiples módulos interactivos implementados.

### Estado Actual
- **Fase:** Producción Beta
- **Líneas de código:** ~23,192 archivos Python
- **Módulos activos:** 11 páginas funcionales
- **Base de datos:** SQLite con 15+ tablas relacionales
- **UI Framework:** Streamlit con CSS personalizado

### Principios Fundamentales
1. **Autenticidad:** Todo el vocabulario proviene de textos clásicos reales
2. **Pedagogía Tradicional:** Inspirado en métodos europeos clásicos (Ørberg, etc.)
3. **Gamificación Seria:** Sistema de progresión estricta con XP y niveles
4. **100% Offline:** Sin dependencias externas, completamente portable

---

## 🏗️ Arquitectura y Stack Tecnológico

### Backend
- **Python 3.11+**: Lenguaje principal
- **SQLite**: Base de datos local
- **SQLModel**: ORM para manejo de datos
- **SQLAlchemy**: Motor de base de datos

### Frontend
- **Streamlit**: Framework web interactivo
- **CSS personalizado**: Estética clásica romana con tema oscuro

### Procesamiento de Lenguaje Natural
- **LatinCy**: Pipeline de NLP para latín (tokenización, POS tagging, dependency parsing)
- **spaCy**: Motor subyacente para análisis sintáctico

### Estructura de Directorios
```
latin-python/
├── app.py                      # Punto de entrada principal
├── requirements.txt            # Dependencias
├── lingua_latina.db           # Base de datos SQLite
│
├── pages/                     # Módulos de Streamlit (11 páginas)
│   ├── 01_🏠_Home.py         # Dashboard principal
│   ├── 02_🎴_Vocabularium.py  # Flashcards con SRS
│   ├── 03_📜_Declinatio.py    # Práctica de declinaciones
│   ├── 04_⚔️_Conjugatio.py    # Práctica de conjugaciones
│   ├── 05_🔍_Analysis.py      # Análisis morfológico
│   ├── 06_📖_Diccionario.py   # Diccionario completo
│   ├── 06_📖_Lectio.py        # Lecturas anotadas
│   ├── 07_⚙️_Admin.py         # Panel de administración
│   ├── 07_📜_Scriptorium.py   # Editor de textos
│   ├── 08_📖_Gramática.py     # Referencia gramatical
│   ├── 08_🗺️_Mapa.py         # Mapa de desafíos gamificados
│   ├── 09_🎯_Desafio.py       # Ejecución de desafíos
│   └── 09_📐_Syntaxis.py      # Tesauro sintáctico
│
├── database/                  # Capa de datos
│   ├── models.py             # Modelos principales (Word, ReviewLog, etc.)
│   ├── syntax_models.py      # Modelos de análisis sintáctico
│   ├── connection.py         # Gestión de sesiones
│   └── seed.py               # Datos iniciales
│
├── utils/                     # Lógica de negocio
│   ├── latin_logic.py        # Morfología latina (declinaciones/conjugaciones)
│   ├── srs.py                # Algoritmo SM-2 para repetición espaciada
│   ├── challenge_engine.py   # Motor de verificación de desafíos
│   └── validators.py         # (Futuro)
│
├── scripts/                   # Scripts de utilidad
│   ├── create_puzzle_challenges.py  # Generador de desafíos interactivos
│   └── ...
│
├── data/                      # Corpus y datos
│   ├── texts/                # Textos latinos (.txt)
│   ├── vocabulary/           # CSVs de vocabulario
│   └── corpus/               # (Futuro) Corpus por autor
│
├── assets/                    # Recursos estáticos
│   └── style.css             # Estilos personalizados
│
└── docs/                      # Documentación
    ├── ARCHITECTURE.md       # Arquitectura del sistema
    ├── PROJECT_STATUS.md     # Este archivo
    ├── AI_PROMPTS.md         # Prompts para IA
    └── CONTRIBUTING.md       # Guía de contribución
```

---

## 📚 Módulos Implementados

### 1. 🏠 Home (Dashboard)
**Estado:** ✅ Completo

- Estadísticas de progreso del usuario
- Visualización de XP y nivel actual
- Contador de racha (streak days)
- Acceso rápido a todos los módulos
- Gráficos de progreso diario/semanal

### 2. 🎴 Vocabularium (Flashcards SRS)
**Estado:** ✅ Completo

- Algoritmo SM-2 (SuperMemo 2) implementado
- Sistema de calidad 0-5 (nuevamente, difícil, bien, fácil)
- Priorización automática de palabras frecuentes
- Intervalo óptimo de revisión
- Filtros por nivel y categoría gramatical
- Estadísticas de retención

**Características técnicas:**
- Manejo de sincretismo (múltiples formas idénticas)
- Normalización de texto (ignora macrones)
- Tracking de mejores/peores palabras

### 3. 📜 Declinatio (Declinaciones)
**Estado:** ✅ Completo

- 5 declinaciones completas (1ª a 5ª)
- 3 géneros (masculino, femenino, neutro)
- 6 casos × 2 números = 12 formas por sustantivo
- Distinción parisílabos/imparisílabos (3ª decl.)
- Adjetivos de 1ª-2ª clase y 3ª clase
- Pronombres (personales, demostrativos, relativos)
- UI con columnas simétricas
- Verificación precisa con retroalimentación

**Sustantivos implementados:**
- 1ª Declinación: rosa, puella, via, etc.
- 2ª Declinación: dominus, puer, templum, etc.
- 3ª Declinación: rex, pater, nomen, mare, etc.
- 4ª Declinación: manus, cornu
- 5ª Declinación: res, dies

### 4. ⚔️ Conjugatio (Conjugaciones)
**Estado:** ✅ Completo

- 4 conjugaciones regulares + mixtas
- **Modos:** Indicativo, Subjuntivo, Imperativo
- **Tiempos (Indicativo):** Presente, Imperfecto, Futuro, Perfecto, Pluscuamperfecto, Futuro Perfecto
- **Tiempos (Subjuntivo):** Presente, Imperfecto, Perfecto, Pluscuamperfecto
- **Voces:** Activa y Pasiva (completas)
- Formas no finitas: Infinitivos (presente, perfecto, futuro), Participios, Supinos
- UI organizada por voz, modo y tiempo
- Traducción completa de todos los términos al español

**Verbos modelo:**
- 1ª: amo (amar)
- 2ª: moneo (advertir)
- 3ª: duco (conducir)
- 3ª mixta: capio (tomar)
- 4ª: audio (oír)
- Irregular: sum (ser/estar)

### 5. 🔍 Analysis (Análisis Morfológico)
**Estado:** ✅ Completo

- Selección aleatoria de palabras del corpus
- Identificación de caso/número (sustantivos)
- Identificación de persona/número/tiempo (verbos)
- **Manejo de sincretismo:** Acepta múltiples respuestas correctas
- Sistema de puntuación por aciertos
- Retroalimentación inmediata
- Normalización de input (ignora macrones y capitalización)

**Ejemplo de sincretismo:**
- "puella" puede ser: Nominativo sing., Vocativo sing., o Ablativo sing.
- Todas las opciones se aceptan como correctas

### 6. 📖 Diccionario
**Estado:** ✅ Completo

- Búsqueda por palabra latina o traducción española
- Filtros por parte del discurso y nivel
- Visualización completa de información morfológica
- Estadísticas del diccionario:
  - Total de palabras
  - Palabras por nivel
  - Distribución por categoría gramatical
  - Palabras invariables
  - Palabras fundamentales

### 7. 📖 Lectio (Lecturas Anotadas)
**Estado:** ✅ Completo

- Textos latinos importados desde archivos `.txt`
- Sistema de anotaciones interactivas:
  - Click en palabra → traducción instantánea
  - Información morfológica completa
  - Lematización automática
- Textos organizados por autor y dificultad
- Procesamiento con LatinCy
- Caché de traducciones para rendimiento

**Textos incluidos:**
- *Familia Romana* (Ørberg) - Capítulos 1-N
- *Hyginus: De Chaos* (mitología)
- (Otros textos pendientes de importar)

### 8. 📖 Gramática (Referencia)
**Estado:** ✅ Completo

- Guía completa de declinaciones (1ª-5ª)
- Guía completa de conjugaciones (1ª-4ª)
- Tablas de paradigmas completos
- Explicaciones de casos especiales
- Todo en español
- Navegación por pestañas

### 9. 🗺️ Mapa de Desafíos (Gamificación)
**Estado:** ✅ Completo

- Sistema de progresión estricta
- Desafíos organizados por nivel (1-10)
- Visualización de requisitos previos
- Sistema de estrellas (0-3):
  - ⭐⭐⭐: 100% en primer intento
  - ⭐⭐: 80-99% correcto
  - ⭐: 60-79% correcto (aprobado mínimo)
- Filtros por nivel y tipo
- Tracking de progreso por usuario

### 10. 🎯 Desafío (Ejecución)
**Estado:** ✅ Completo con 6 tipos

**Tipos de desafío implementados:**

1. **`declension`** - Declinación de sustantivos
   - Configuración: palabra, casos (all o lista), números (sg/pl o ambos)
   - Verificación automática contra formas generadas

2. **`conjugation`** - Conjugación de verbos
   - Configuración: verbo, tiempo, voz, números
   - Verificación automática

3. **`multiple_choice`** - Opción múltiple
   - Preguntas sobre gramática, casos, formas
   - Verificación de respuesta correcta

4. **`translation`** - Traducción español → latín
   - **NOTA:** Verificación básica por coincidencia de palabras
   - Requiere modelo de traducción entrenado para precisión total

5. **`syntax`** - Análisis sintáctico
   - Identificación de sujeto, predicado, objeto, etc.
   - Verificación flexible (normalización de respuestas)

6. **`sentence_order`** - Rompecabezas de ordenamiento ✨ NUEVO
   - Usuario ordena palabras para formar oración correcta
   - Opción de palabras distractoras
   - UI interactiva con banco de palabras y área de respuesta

7. **`match_pairs`** - Parejas coincidentes ✨ NUEVO
   - Emparejar términos latinos con traducciones/definiciones
   - UI de dos columnas con selección interactiva
   - Feedback visual inmediato

**Sistema de etapas:**
- Cada desafío tiene 3 etapas (ejercicios)
- Progresión automática al completar cada etapa
- Recompensa de estrellas acumulativa

**Limitación actual:** El análisis es automático pero no incluye las anotaciones pedagógicas tradicionales que los profesores de latín suelen hacer (ver sección de "Trabajo Pendiente").

### 11. 📐 Syntaxis (Tesauro Sintáctico)
**Estado:** ✅ Completo (Fase 1 Pedagógica)

**Estado:** ✅ Completo (Fase 1 Pedagógica - Estricta)

- **Modo "Corpus Verificado":** Muestra solo oraciones con análisis pedagógico 100% manual y revisado.
  - Actualmente incluye ejemplos básicos y fábulas de Fedro (Nivel 1).
- **Modo "Zona de Espera":** Repositorio de oraciones con análisis automático preliminar, ocultas al público general hasta su curación.
- **Pestaña "Análisis Pedagógico":**
  - Estructura de oración (Principal/Subordinada).
  - Anotaciones palabra por palabra (Sujeto, Objeto, etc.).
  - Explicaciones gramaticales detalladas y profesionales.
- **Visualización:**
  - Análisis Visual (colores por función).
  - Árbol de Dependencias (SVG).
  - Detalles Gramaticales (tabla morfológica).

### 12. ⚙️ Admin (Panel de Administración)
**Estado:** ✅ Completo

- Importación masiva de vocabulario desde CSV
- Gestión de palabras (CRUD completo)
- Estadísticas detalladas
- Importación de textos desde archivos
- Gestión de autores
- Herramientas de migración de datos

---

## 🗄️ Sistema de Base de Datos

### Modelos Principales

#### Word (Palabra)
```python
- id: int (PK)
- latin: str                    # Forma canónica
- translation: str              # Traducción española
- part_of_speech: str          # noun, verb, adjective, pronoun, etc.
- declension: Optional[str]    # 1, 2, 3, 4, 5 (para sustantivos/adjetivos)
- gender: Optional[str]        # m, f, n
- genitive: Optional[str]      # Genitivo singular
- conjugation: Optional[str]   # 1, 2, 3, 4, irregular (para verbos)
- principal_parts: Optional[str] # Partes principales de verbos
- level: int                   # Nivel de dificultad (1-10)
- frequency_rank_global: Optional[int]  # Ranking de frecuencia
- is_invariable: bool          # Preposiciones, adverbios, etc.
- is_fundamental: bool         # Palabra de alta prioridad
- category: Optional[str]      # Subcategoría (preposition, adverb, etc.)
- author_id: Optional[int]     # FK a Author
```

#### ReviewLog (Historial SRS)
```python
- id: int (PK)
- word_id: int (FK → Word)
- user_id: int (FK → UserProfile)
- review_date: datetime
- quality: int                 # 0-5 (algoritmo SM-2)
- ease_factor: float           # Factor de facilidad (≥1.3)
- interval: int                # Días hasta próxima revisión
- repetitions: int             # Repeticiones exitosas consecutivas
```

#### UserProfile (Perfil de Usuario)
```python
- id: int (PK)
- name: str
- level: int                   # Nivel actual (1-10)
- xp: int                      # Puntos de experiencia totales
- streak: int                  # Días consecutivos de práctica
- last_activity: datetime
- total_challenges_completed: int
- total_stars_earned: int
```

#### Challenge (Desafío Gamificado)
```python
- id: int (PK)
- level: int                   # Nivel requerido
- challenge_type: str          # declension, conjugation, syntax, etc.
- title: str
- description: str
- xp_reward: int
- config: str (JSON)           # Configuración específica del desafío
- prerequisites: str (JSON)    # Lista de challenge IDs requeridos
```

#### UserChallengeProgress (Progreso del Usuario)
```python
- id: int (PK)
- user_id: int (FK)
- challenge_id: int (FK)
- current_stage: int           # Etapa actual (0-2)
- stars_earned: int            # Estrellas totales (0-3)
- attempts: int
- completed: bool
- completion_date: datetime
```

#### SentenceAnalysis (Análisis Sintáctico)
```python
- id: int (PK)
- latin_text: str              # Oración latina
- spanish_translation: str     # Traducción
- complexity_level: int        # 1-10
- sentence_type: str           # simple, compound, complex
- source: str                  # familia_romana_cap1, etc.
- lesson_number: Optional[int]
- dependency_json: str (JSON)  # Árbol de dependencias LatinCy
- syntax_roles: str (JSON)     # {subject: [1,2], predicate: [3], ...}
- constructions: str (JSON)    # [ablative_absolute, ...]
- tree_diagram_svg: str        # Diagrama SVG pre-renderizado
- verified: bool               # Revisión manual completada
```

#### Author, Text, WordFrequency, SyntaxCategory
Modelos auxiliares para organización y metadatos.

### Relaciones Clave
```
Author 1──N Word
Author 1──N Text
Word 1──N ReviewLog
Word N──N Text (via TextWordLink)
UserProfile 1──N ReviewLog
UserProfile 1──N UserChallengeProgress
Challenge 1──N UserChallengeProgress
SentenceAnalysis N──N SyntaxCategory (via SentenceCategoryLink)
```

---

## ✅ Funcionalidades Completadas

### Morfología Latina
- [x] 5 declinaciones completas (sustantivos y adjetivos)
- [x] Distinción parisílabos/imparisílabos (3ª declinación)
- [x] 4 conjugaciones regulares + mixtas
- [x] Verbo irregular `sum`
- [x] Todos los modos: Indicativo, Subjuntivo, Imperativo
- [x] Todos los tiempos (12 del indicativo, 8 del subjuntivo)
- [x] Voz activa y pasiva completas
- [x] Formas no finitas: infinitivos, participios, supinos, gerundios
- [x] Pronombres: personales, demostrativos, relativos
- [x] Normalización de texto (macrones opcionales)

### Sistema de Repetición Espaciada (SRS)
- [x] Algoritmo SM-2 implementado
- [x] Tracking de calidad de respuesta (0-5)
- [x] Cálculo de intervalo óptimo
- [x] Priorización de palabras frecuentes
- [x] Historial completo de revisiones
- [x] Estadísticas de retención

### Análisis Sintáctico (LatinCy)
- [x] Tokenización automática
- [x] POS tagging (categorías gramaticales)
- [x] Dependency parsing (árboles sintácticos)
- [x] Lematización
- [x] Análisis morfológico automático
- [x] Generación de diagramas SVG
- [x] Almacenamiento en base de datos

### Sistema de Gamificación
- [x] Niveles (1-10)
- [x] Sistema de XP
- [x] Progresión estricta con requisitos previos
- [x] Sistema de estrellas (0-3)
- [x] Racha de días consecutivos
- [x] 6 tipos de desafíos interactivos
- [x] Tracking de progreso por usuario
- [x] Desbloqueo progresivo de contenido

### UI/UX
- [x] Tema clásico romano con modo oscuro
- [x] CSS personalizado con estética "scriptorium"
- [x] Todas las interfaces en español
- [x] Iconos emoji consistentes
- [x] Feedback visual inmediato
- [x] Navegación intuitiva
- [x] Responsividad básica

### Gestión de Contenido
- [x] Importación de vocabulario desde CSV
- [x] Importación de textos desde archivos .txt
- [x] Panel de administración completo
- [x] Editor de textos (Scriptorium)
- [x] Sistema de autores y fuentes
- [x] Categorización automática

---

## ⚠️ Trabajo Pendiente

### 1. Análisis Sintáctico Pedagógico (ALTA PRIORIDAD)

**Problema actual:** El módulo Syntaxis usa análisis automático de LatinCy pero carece de las anotaciones pedagógicas tradicionales que los profesores de latín utilizan en sus cursos.

**Se necesita:**
- Análisis de casos (función sintáctica de cada sustantivo)
- Identificación explícita de complementos (directo, indirecto, circunstancial)
- Anotación de construcciones clásicas:
  - Ablativo absoluto
  - Acusativo con infinitivo
  - Dativo posesivo/agente
  - Genitivo objetivo/subjetivo
  - Subordinadas (temporal, causal, final, consecutiva, etc.)
- Sistema de "parsing" tradicional (sujeto + predicado + complementos)
- Diagramas Reed-Kellogg (opcional, pero pedagógicamente valioso)
- Explicaciones en lenguaje natural de estructuras complejas

**Ver sección "SYNTAX_ANALYSIS_PLAN.md" para detalles completos.**

### 2. Modelo de Traducción AI

**Estado:** Entrenamiento pendiente

- [x] Corpus bilingüe preparado (Latin-Español, Latin-Italiano)
- [x] Script de entrenamiento creado (`scripts/train_local_gpu.py`)
- [ ] Entrenamiento completado en GPU
- [ ] Modelo exportado e integrado
- [ ] Verificación mejorada para desafíos de tipo `translation`

**Notas:** Actualmente la verificación de traducciones es básica (coincidencia de palabras). Con el modelo entrenado se podrá evaluar calidad semántica.

### 3. Desafíos de Tipo Puzzle

**Estado:** Implementado pero sin contenido

- [x] Tipos `sentence_order` y `match_pairs` implementados en UI
- [x] Motor de verificación completado
- [x] Script de creación de ejemplos escrito (`scripts/create_puzzle_challenges.py`)
- [ ] Script ejecutado (pendiente de aprobación del usuario)
- [ ] Desafíos de ejemplo insertados en BD
- [ ] Testing de interactividad

**Acción requerida:** Ejecutar `python scripts/create_puzzle_challenges.py`

### 4. Validación de Contenido

**Propósito:** Asegurar que todo el contenido de desafíos sea consistente con el motor gramatical de la aplicación.

- [ ] Crear script `scripts/validate_content.py`
- [ ] Validar preguntas `multiple_choice` (parsing de casos/formas)
- [ ] Validar configuración de resos `declension` y `conjugation`
- [ ] Reportar discrepancias
- [ ] Documentar workflow de creación de contenido en `CONTRIBUTING.md`

### 5. Expansión del Corpus

- [ ] Importar más capítulos de *Familia Romana*
- [ ] Importar textos de autores clásicos:
  - [ ] Caesar: *De Bello Gallico*
  - [ ] Cicero: *In Catilinam*
  - [ ] Virgilio: *Eneida* (selecciones)
  - [ ] Ovidio: *Metamorfosis* (selecciones)
- [ ] Anotar textos con construcciones sintácticas especiales
- [ ] Crear ejercicios específicos por texto

### 6. Testing y Calidad de Código

- [ ] Unit tests para `latin_logic.py`
- [ ] Integration tests para modelos de BD
- [ ] UI tests para flujos críticos (Cypress/Selenium)
- [ ] Documentación de funciones (docstrings completos)
- [ ] Type hints consistentes
- [ ] Linting con Ruff/Black

### 7. Mejoras de UI/UX

- [ ] Animaciones suaves (micro-interactions)
- [ ] Sonidos opcionales (feedback auditivo)
- [ ] Gráficos de progreso más ricos (charts.js o plotly)
- [ ] Modo claro/oscuro toggle manual
- [ ] Exportación de estadísticas (PDF/CSV)
- [ ] Impresión de paradigmas (flashcards físicas)

### 8. Multiusuario (Opcional)

- [ ] Migración a base de datos en nube (PostgreSQL)
- [ ] Sistema de autenticación
- [ ] Perfiles de usuario persistentes
- [ ] Leaderboards (opcional, según filosofía educativa)
- [ ] Compartir progreso (redes sociales)

### 9. Deployment

- [ ] Optimización de rendimiento (caching, índices BD)
- [ ] Empaquetado con PyInstaller (distribución standalone)
- [ ] Documentación de instalación para usuarios finales
- [ ] Video tutoriales
- [ ] Página de landing web

---

## 🚀 Hoja de Ruta Futura

### Fase 1: Refinamiento del Análisis Sintáctico (INMEDIATO)
**Estimado:** 2-3 semanas

1. Implementar sistema de anotaciones pedagógicas
2. Crear herramienta de anotación manual para profesores
3. Generar dataset anotado de oraciones modelo
4. Entrenar clasificador de construcciones sintácticas (opcional, ML)
5. Integrar explicaciones en lenguaje natural
6. Añadir diagramas Reed-Kellogg

**Ver:** `SYNTAX_ANALYSIS_PLAN.md`

### Fase 2: Completar Gamificación (1-2 semanas)
1. Ejecutar script de desafíos puzzle
2. Crear 50+ desafíos variados (todos los tipos)
3. Balancear curva de dificultad
4. Implementar sistema de achievements/badges
5. Testing completo de progresión

### Fase 3: Entrenar Modelo de Traducción (Variable)
1. Preparar corpus final (verificación de calidad)
2. Entrenamiento en GPU (Google Colab o local)
3. Evaluación de métricas (BLEU, perplexity)
4. Fine-tuning iterativo
5. Integración en la aplicación
6. Mejora de verificación de desafíos de traducción

### Fase 4: Expansión de Corpus (Continuo)
1. Digitalizar/importar textos clásicos
2. Anotación sintáctica manual/semi-automática
3. Creación de ejercicios por texto
4. Organización pedagógica por nivel

### Fase 5: Polishing y Release (1-2 meses)
1. Testing exhaustivo (QA)
2. Optimización de rendimiento
3. Documentación completa
4. Empaquetado standalone
5. Release público (GitHub, sitio web)
6. Marketing educativo (profesores de latín, universidades)

---

## 📊 Métricas Actuales del Proyecto

### Código
- **Lenguaje principal:** Python
- **Líneas de código:** ~23,000 (estimado)
- **Archivos Python:** 30+
- **Módulos de Streamlit:** 11 páginas

### Base de Datos
- **Tablas:** 15+
- **Palabras únicas:** ~1,500+ (depende del corpus importado)
- **Oraciones analizadas:** ~200+ (depende de textos procesados)
- **Autores:** 5-10
- **Textos:** 10-15

### Gamificación
- **Niveles:** 10
- **Tipos de desafíos:** 6 (implementados) + 2 (por poblar con contenido)
- **Sistema de XP:** ✅
- **Sistema de estrellas:** ✅
- **Progresión estricta:** ✅

---

## 🔧 Consideraciones Técnicas

### Rendimiento
- **Base de datos:** Índices en `word.latin`, `word.level`, `reviewlog.word_id`
- **Caching:** Uso de `@st.cache_data` en queries frecuentes
- **Sesiones:** Context managers (`with get_session()`)
- **Optimización pendiente:** Lazy loading de textos grandes

### Seguridad
- 100% local, sin envío de datos externos
- Sin autenticación requerida (single-user app)
- Base de datos sin encriptación (no hay datos sensibles)

### Compatibilidad
- Python 3.11+
- Streamlit 1.28+
- SQLModel 0.0.14+
- LatinCy (última versión compatible con spaCy)

---

## 📝 Notas para Continuidad del Proyecto

### Para Desarrolladores Futuros (o IA Asistente)
1. **Leer primero:** `docs/ARCHITECTURE.md` - Entiende la estructura antes de modificar
2. **Convenciones:**
   - Todos los términos gramaticales en español en la UI
   - Nombres de variables/funciones en inglés (código)
   - Docstrings en español
3. **Testing:** Siempre probar cambios en morfología con palabrases conocidas (rosa, puella, amo, sum)
4. **Base de datos:** Usar migraciones para cambios de esquema (futuro: Alembic)
5. **Git:** Commits descriptivos en español

### Archivos Clave a Revisar
- [`database/models.py`](file:///home/diego/Projects/latin-python/database/models.py): Modelos de datos principales
- [`utils/latin_logic.py`](file:///home/diego/Projects/latin-python/utils/latin_logic.py): Lógica de morfología
- [`utils/srs.py`](file:///home/diego/Projects/latin-python/utils/srs.py): Algoritmo de repetición espaciada
- [`utils/challenge_engine.py`](file:///home/diego/Projects/latin-python/utils/challenge_engine.py): Verificación de desafíos
- [`pages/09_📐_Syntaxis.py`](file:///home/diego/Projects/latin-python/pages/09_📐_Syntaxis.py): Análisis sintáctico

### Comandos Útiles
```bash
# Iniciar aplicación
streamlit run app.py

# Ejecutar script de seed
python database/seed.py

# Importar vocabulario
python scripts/import_vocabulary.py

# Crear desafíos puzzle
python scripts/create_puzzle_challenges.py

# Verificar base de datos
python test_database_phase1.py
```

---

## 🎓 Filosofía Pedagógica

Este proyecto sigue principios de enseñanza clásica de lenguas:

1. **Input Comprensible:** Textos auténticos graduados por dificultad
2. **Repetición Espaciada:** Consolidación a largo plazo mediante SRS
3. **Aprendizaje Activo:** Práctica constante de producción (declinaciones/conjugaciones)
4. **Contexto Auténtico:** Todo vocabulario proviene de textos reales
5. **Progresión Natural:** De lo simple a lo complejo, sin saltos bruscos
6. **Gamificación Seria:** Motivación mediante progreso medible, no recompensas superficiales

**Inspiraciones:**
- Método Ørberg (*Lingua Latina Per Se Illustrata*)
- Método Cambridge Latin Course
- Tradición europea de enseñanza del latín

---

## 🙏 Agradecimientos

- **LatinCy:** Pipeline de NLP específico para latín
- **spaCy:** Framework de procesamiento de lenguaje natural
- **Streamlit:** Framework de aplicaciones web interactivas
- **SQLModel:** ORM elegante y type-safe
- **Ørberg:** Inspiración pedagógica fundamental

---

## 📧 Contacto y Contribuciones

*(Pendiente: añadir información de contacto y guías de contribución)*

---

**Última revisión:** 23 de noviembre de 2025  
**Versión del documento:** 1.0  
**Próxima revisión programada:** Al completar Fase 1 del Roadmap
