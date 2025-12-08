# 📘 MANUAL DE USO COMPLETO - Lingua Latina Viva

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Estructura de la Aplicación](#estructura-de-la-aplicación)
3. [Guía de Navegación Principal](#guía-de-navegación-principal)
4. [Panel de Administración - Guía Completa](#panel-de-administración---guía-completa)
5. [Problemas de Performance y Recomendaciones](#problemas-de-performance-y-recomendaciones)
6. [Mejoras de Usabilidad Recomendadas](#mejoras-de-usabilidad-recomendadas)

---

## Descripción General

**Lingua Latina Viva** es una plataforma educativa interactiva para el aprendizaje del latín. Combina:

- 📚 **Lecciones estructuradas** (41 lecciones organizadas por nivel)
- 🧠 **Memorización con SRS** (Spaced Repetition System)
- 📐 **Análisis sintáctico visual** con Stanza NLP
- ⚔️ **Práctica interactiva** (declinaciones, conjugaciones, desafíos)
- 🎮 **Gamificación** (puntos XP, aventura, desafíos desbloqueables)
- 🗺️ **Mapa de progreso** (aventura interactiva)
- ⚙️ **Panel administrativo completo** (gestión de datos y contenido)

---

## Estructura de la Aplicación

### Arquitectura General

```
app.py (punto de entrada)
├── Splash Screen (primer acceso)
├── Sidebar global
│   ├── Configuración global (tamaño de fuente)
│   ├── Información de navegación
│   └── Enlace a admin (99_⚙️_Administracion.py)
│
└── Páginas principales (pages/)
    ├── 01_🏠_Inicio.py - Dashboard
    ├── 02_📘_Lecciones.py - Curso estructurado
    ├── 03_🧠_Memorización.py - SRS + Diccionario
    ├── 04_⚔️_Práctica.py - Declinaciones, Conjugaciones, Aventura, Desafíos
    ├── 05_🔍_Análisis.py - Sintaxis, Morfología, Scriptorium, Collatinus
    ├── 06_🎮_Ludus.py - Juego de aventura
    ├── 07_📧_Contacto.py - Contacto
    └── 99_⚙️_Administracion.py - Panel administrativo
```

### Base de Datos

- **Engine**: SQLite (lingua_latina.db)
- **ORM**: SQLModel (SQLAlchemy 2.x con type hints)
- **Datos**: 724 palabras, 40+ oraciones analizadas, 30 lecciones

---

## Guía de Navegación Principal

### 1. 🏠 Inicio (Dashboard)

**Ubicación**: Primera página al entrar (01_🏠_Inicio.py)

**Secciones**:

- **Bienvenida personalizada**: Saludo con nombre de usuario
- **Estadísticas clave**:
  - Total de palabras memorizadas
  - Puntos XP acumulados
  - Rachas de días (días consecutivos practicando)
  - Desafíos completados
  
- **Próximos pasos recomendados**: Sugerencias personalizadas basadas en progreso
  - Comenzar lección
  - Practicar vocabulario
  - Mejorar palabras débiles
  - Resolver desafíos
  
- **Progreso por módulo**: Gráficos de avance en:
  - Vocabulario
  - Sintaxis
  - Ejercicios
  - Lecturas

**Recomendación de uso**: Revisa esta página diariamente para ver tu progreso y obtener recomendaciones personalizadas.

---

### 2. 📘 Lecciones (Curso Estructurado)

**Ubicación**: 02_📘_Lecciones.py

**Tabs disponibles**:

#### Tab 1: 📘 Curso Estructurado
- **41 lecciones organizadas por nivel**:
  - **Nivel Básico** (Lecciones 1-13): Introducción a declinación y conjugación
  - **Nivel Avanzado** (Lecciones 14-30): Tiempos más complejos
  - **Nivel Experto** (Lecciones 31+): Condicionales, subjuntivo, construcciones especiales
  
- **Contenido de cada lección**:
  - Explicación gramatical
  - Vocabulario nuevas
  - Ejemplos de traducción
  - Enlaces a ejercicios relacionados
  
- **Requisitos de lección**:
  - Dominio de vocabulario (% de precisión mínima)
  - Número de traducciones correctas
  - Lecturas completadas
  - Análisis sintácticos resueltos

#### Tab 2: 📖 Lecturas Graduadas
- Textos seleccionados organizados por dificultad
- Cada lectura vinculada con el vocabulario de la lección

#### Tab 3: ⚖️ Referencia Gramatical
- Tablas de conjugación y declinación
- Referencia rápida de construcciones latinas

**Cómo usar**: 
1. Selecciona una lección
2. Lee la explicación
3. Estudia el vocabulario nuevo
4. Completa los requisitos antes de pasar a la siguiente

---

### 3. 🧠 Memorización

**Ubicación**: 03_🧠_Memorización.py

**Tabs disponibles**:

#### Tab 1: 🎴 Vocabulario (SRS)
- **Sistema de Repetición Espaciada**:
  - Palabras organizadas en intervalos (1 día, 3 días, 7 días, 30 días)
  - Cada respuesta correcta aumenta el intervalo
  - Respuesta incorrecta reinicia el contador
  
- **Opciones**:
  - Latín → Español (traducción)
  - Español → Latín (escritura)
  - Audio (si disponible)
  
- **Niveles de dificultad**: Configurable por usuario

#### Tab 2: 📚 Diccionario
- Acceso a todas las palabras en la base de datos
- Búsqueda por término, POS (Part of Speech), dificultad
- Información completa: lema, traducción, pronunciación, ejemplos

**Cómo usar**:
- Practica 10-15 minutos diarios con el SRS
- Los algoritmos ajustarán automáticamente la dificultad
- Usa el diccionario para buscar palabras cuando traducas textos

---

### 4. ⚔️ Práctica (Ejercicios Interactivos)

**Ubicación**: 04_⚔️_Práctica.py

**Tabs disponibles**:

#### Tab 1: 📜 Declinaciones
- Práctica de casos y números
- Niveles progresivos según tu avance
- Tipos de ejercicios:
  - Completar el caso faltante
  - Identificar la forma correcta
  - Traducir frase con énfasis en declinación

#### Tab 2: ⚔️ Conjugaciones
- Práctica de tiempos, modos, personas
- Tiempos introducidos progresivamente:
  - Nivel 1: Solo presente de indicativo
  - Nivel 2: Presente + Imperfecto
  - Nivel 3+: Todos los tiempos indicativos
  
- Voz activa y pasiva

#### Tab 3: 🗺️ Aventura
- **Mapa interactivo de progreso**
- Desafíos organizados en fases temáticas:
  - Fase 1: Primera Declinación
  - Fase 2: Presente de Indicativo
  - Fase 3+: Construcciones avanzadas
  
- Sistema de estrellas (1-3) basado en porcentaje de aciertos
- Desbloqueo automático del siguiente desafío

#### Tab 4: 🎯 Desafíos
- Desafíos individuales más complejos
- Tipos de desafío:
  - Declinación
  - Conjugación
  - Opción múltiple
  - Traducción
  - Análisis sintáctico
  
- Puntuación XP y logros

**Cómo usar**:
- Comienza con Declinaciones y Conjugaciones guiadas
- Progresa a la Aventura cuando sientas confianza
- Completa Desafíos para ganar XP y desbloquear contenido

---

### 5. 🔍 Análisis

**Ubicación**: 05_🔍_Análisis.py

**Tabs disponibles**:

#### Tab 1: 📐 Sintaxis Visual
- **Análisis completo de oraciones latinas**
- Muestra:
  - Árbol de dependencia sintáctica
  - Roles sintácticos (sujeto, predicado, objeto directo, etc.)
  - Información morfológica de cada palabra
  - Etiquetas POS (Part Of Speech)
  
- **Visualización interactiva**: Haz clic en palabras para ver análisis profundo
- **Herramientas**:
  - Glosario de abreviaturas
  - Explicaciones pedagógicas
  - Construcciones especiales destacadas

#### Tab 2: 🔍 Analizador Morfológico
- Análisis detallado de palabras individuales
- Información:
  - Lema (forma de diccionario)
  - Parte del discurso
  - Caso, número, género (cuando aplica)
  - Tiempo, modo, voz (para verbos)
  - Formas alternativas

#### Tab 3: ✍️ Scriptorium
- **Escritura y traducción de textos**
- Interfaz para escribir/pegar oraciones latinas
- Análisis automático y corrección

#### Tab 4: 📖 Consulta Collatinus
- **Motor de análisis morfológico avanzado**
- Basado en diccionario Collatinus
- Búsqueda de formas flexionadas
- Información etimológica

**Cómo usar**:
- Usa Sintaxis Visual para entender la estructura de textos
- Usa el Analizador Morfológico para descomponer palabras
- Practica escritura con Scriptorium
- Consulta Collatinus para información profunda

---

### 6. 🎮 Ludus (Juego de Aventura)

**Ubicación**: 06_🎮_Ludus.py

- **Experiencia de juego inmersiva**
- Progresión a través de mundo mitológico latino
- Cada desafío derrota un "enemigo" (concepto gramatical)
- Recompensas: XP, cofres, poder-ups

---

### 7. 📧 Contacto

**Ubicación**: 07_📧_Contacto.py

- Formulario para reportar bugs
- Sugerencias de mejora
- Preguntas sobre contenido

---

## Panel de Administración - Guía Completa

**Ubicación**: 99_⚙️_Administracion.py
**Acceso**: Visible en el sidebar derecho de cualquier página

### ⚠️ AVISO IMPORTANTE SOBRE PERFORMANCE

**Problema identificado**: El panel de administración puede tardar 10-30 segundos en cargar la primera vez, especialmente las secciones con muchos datos. Esto se debe a:

1. Carga de modelos de NLP (Spacy) - primeras 2 veces
2. Inicialización de bases de datos en caché
3. Multitud de operaciones de consulta

**SOLUCIÓN IMPLEMENTADA (Parcial)**: Se han agregado spinners en muchas secciones, pero NO EN TODAS.

**Recomendación del usuario**: Añadir indicadores visuales de carga en TODAS las operaciones que tarden más de 2 segundos.

---

### Navegación del Panel

**Selector de Sección** (Sidebar izquierdo):
```
Radio buttons para elegir sección:
- Vocabulario
- Textos
- Lecciones
- Ejercicios
- Sintaxis
- Usuario
- Estadísticas
- Requisitos de Lección
- Catalogación
- Configuración
```

---

### SECCIÓN 1: 📝 Vocabulario

**Tabs**:

#### Tab 1: ➕ Añadir Palabra
- **Formulario para crear palabras nuevas**:
  - Latín (requerido)
  - Español (traducción, requerido)
  - Parte del discurso (noun, verb, adjective, etc.)
  - Declination/Conjugation (para nombres y verbos)
  - Nivel de dificultad (1-10)
  - Frecuencia en corpus
  - Notas pedagógicas
  - Partes principales (para verbos): presente, infinitivo, perfecto, supino
  
- **Validación**: 
  - Chequeo de duplicados
  - Normalización de caracteres latinos
  - Verificación de formato

- **Guarde botón**: Guarda en BD y actualiza cachés

#### Tab 2: 📚 Ver Palabras
- **Tabla de todas las palabras**:
  - Búsqueda por término
  - Filtro por POS, nivel, frecuencia
  - Editor en línea para modificar
  - Botón eliminar con confirmación

- **Información mostrada**:
  - Latín, Español, POS, Nivel
  - Declination/Conjugation
  - Frecuencia
  - Última actualización

#### Tab 3: 📥 Importar Vocabulario
- **Dos modos**:
  
  **Modo 1: Carga CSV**
  - Descarga plantilla de ejemplo
  - Carga archivo CSV con palabras
  - Validación automática
  - Reporte de errores antes de guardar
  
  **Modo 2: Importación Inteligente (NLP)**
  - Pega cualquier texto en latín
  - Sistema analiza automáticamente:
    - Segmentación de palabras
    - Análisis morfológico con Spacy
    - Detección de lemas
    - Vinculación a vocabulario existente
    - Generación de vocabulario nuevo si es necesario
  - Nivel de dificultad personalizado

#### Tab 4: 📤 Exportar Vocabulario
- **Genera archivo exportable**:
  - Formato: Excel (.xlsx)
  - Incluye: Latín, Español, POS, Nivel, Frecuencia, Notas
  - Filtros opcionales por nivel, POS

#### Tab 5: 🛠️ Herramientas de Vocabulario
- **Limpieza de datos**:
  - Remover duplicados
  - Normalizar caracteres
  - Llenar vacíos en traducción
  
- **Análisis de corpus**:
  - Palabras sin traducción
  - Palabras sin nivel asignado
  - Palabras sin declination/conjugation (para verbs)
  
- **Validación**:
  - Palabras duplicadas
  - Formato incorrecto
  - Caracteres inválidos

---

### SECCIÓN 2: 📜 Gestión de Textos

**Tabs**:

#### Tab 1: ➕ Añadir Texto
- **Formulario de nuevo texto**:
  - Título (requerido)
  - Autor
  - Contenido en latín (requerido, large textarea)
  - Nivel de dificultad
  - Número de libro (opcional)
  - Número de capítulo (opcional)

- **Proceso automático**:
  - Tokeniza el texto
  - Vincula con vocabulario existente
  - Crea registros TextWordLink
  - Reporta cuántas palabras se vincularon

#### Tab 2: 📚 Ver Textos
- **Lista de textos importados**:
  - Expandible para ver contenido completo
  - Muestra: Título, Nivel, Autor
  - Primeras 200 caracteres en preview
  
- **Cacheo**: Utiliza caché en session_state para evitar recargas

#### Tab 3: 📥 Importar Textos
- **Dos modos**:
  
  **Modo 1: CSV Estructurado**
  - Descarga plantilla
  - Columnas: latin_text, spanish_translation, complexity, source
  - Validación antes de importar
  
  **Modo 2: Importación NLP**
  - Pega cualquier texto latino
  - Título automático o manual
  - Nivel de dificultad personalizado
  - Análisis completo y vinculación automática

#### Tab 4: 📤 Exportar Textos
- **Genera CSV exportable**:
  - Incluye todos los textos
  - Formato: título, autor, dificultad, contenido

#### Tab 5: 🛠️ Herramientas de Análisis
- **Re-analizar todos los textos**:
  - Executa análisis morfológico profundo con Stanza
  - Barra de progreso actualizada
  - Reporta total de palabras analizadas
  - Reporta errores si ocurren

⚠️ **NOTA DE PERFORMANCE**: Esta opción puede tardar 5-10 minutos si hay muchos textos

---

### SECCIÓN 3: 📚 Gestión de Lecciones

**Tabs**:

#### Tab 1: ➕ Añadir Lección
- **Formulario de nueva lección**:
  - Número de lección (1-100)
  - Título
  - Contenido en Markdown
  - Ruta de imagen (opcional)
  - Nivel (auto-detectado según número)
  - Vocabulario asociado (multiselect)

- **Validación**: 
  - Número de lección único
  - Contenido requerido

#### Tab 2: 📖 Ver Lecciones
- **Tabla de lecciones**:
  - Búsqueda por número o título
  - Vista expandible del contenido
  - Editor en línea
  - Botón eliminar

- **Información**:
  - Número, Título, Nivel
  - Vocabulario asociado
  - Fechas

---

### SECCIÓN 4: 🎯 Gestión de Ejercicios

**Tabs**:

#### Tab 1: ➕ Crear Ejercicio
- **Editor visual para crear ejercicios**:
  - Tipo de ejercicio (múltiple opción, llenar vacío, traducción, etc.)
  - Enunciado
  - Opciones de respuesta
  - Respuesta correcta
  - Puntuación XP
  - Lección asociada

#### Tab 2: 📂 Ver Ejercicios
- **Listado de ejercicios creados**
- Filtro por tipo, lección
- Editor en línea
- Eliminar

#### Tab 3: 📤 Exportar Ejercicios
- **Descarga JSON de configuración**
- Respaldo de datos

---

### SECCIÓN 5: 📐 Gestión de Sintaxis

**Tabs**:

#### Tab 1: ➕ Nueva Oración
- **Análisis y anotación de oraciones**:
  - Input: Oración en latín (requerido)
  - Input: Traducción al español (requerido)
  - Nivel de complejidad (1-10)
  - Fuente (opcional, ej: "familia_romana_cap1")
  
- **Análisis automático con Stanza**:
  - Ejecuta análisis morfosintáctico
  - Genera árbol de dependencia
  - Extrae información de cada token

- **Editor de anotaciones**:
  - Tabla editable con columnas:
    - ID: Número de palabra
    - Palabra: Forma en el texto
    - Lema: Forma de diccionario
    - POS: Parte del discurso
    - Dep: Función sintáctica
    - Head: Palabra de la que depende
    - **Rol Pedagógico** (EDITABLE): Sujeto, Predicado, Obj. Directo, etc.
    - **Función Caso** (EDITABLE): Información de caso si aplica
    - **Explicación** (EDITABLE): Notas pedagógicas
  
- **Metadatos de oración**:
  - Tipo: simple, compound, complex
  - Construcciones especiales: ablativo absoluto, acusativo + infinitivo, etc.
  - Notas generales

- **Guardado**:
  - Crea registro SentenceAnalysis
  - Crea registros TokenAnnotation para cada palabra anotada
  - Crea registro SentenceStructure si hay notas

⚠️ **NOTA DE PERFORMANCE**: El análisis con Stanza tarda 5-15 segundos la primera vez, 2-3 segundos después

#### Tab 2: 📚 Ver Oraciones
- **Lista de oraciones analizadas**
- Vista de análisis completo
- Opciones de edición, eliminación

#### Tab 3: 📥 Importar Oraciones
- **Importación masiva CSV**:
  - Columnas: latin_text, spanish_translation, complexity, source
  - Validación automática
  - Reporte de éxito/errores

#### Tab 4: 📤 Exportar Oraciones
- **Descarga JSON o CSV**
- Incluye análisis completo

#### Tab 5: ❓ Ayuda
- Guía de cómo usar el análisis sintáctico

---

### SECCIÓN 6: 👤 Gestión de Usuario

**Tabs**:

#### Tab 1: 👤 Mi Perfil
- **Información del usuario**:
  - Nombre
  - Email
  - Nivel actual
  - Total XP
  - Fecha de creación
  
- **Edición de preferencias**:
  - Nivel de dificultad preferido
  - Idioma de interfaz
  - Notificaciones

#### Tab 2: 📊 Actividad
- **Historial de actividades**:
  - Últimas lecciones completadas
  - Últimos ejercicios resueltos
  - Rachas
  - Desafíos completados

#### Tab 3: 🔐 Seguridad
- **Cambio de contraseña** (si aplicable)
- **Historial de sesiones**

---

### SECCIÓN 7: 📋 Estadísticas del Corpus

**Contenido**:

- **Métricas clave**:
  - Total de palabras en base de datos
  - Total de textos
  - Total de oraciones analizadas
  
- **Distribución por tipo**:
  - Gráfico de barras: Cantidad de palabras por POS (noun, verb, adjective, etc.)
  - Desglose por nivel de dificultad

- **Análisis de cobertura**:
  - Porcentaje de palabras con traducción completa
  - Porcentaje de verbos con partes principales
  - Palabras "huérfanas" (sin relacionar a textos)

---

### SECCIÓN 8: 📋 Gestión de Requisitos de Lección

**Contenido**:

- **Selector de lección** (dropdown de 1-41)
- **Requisitos configurables por lección**:
  - Tipo de requisito:
    - vocabulary_mastery: % mínimo de dominio de palabras
    - exercises: Número mínimo de ejercicios completados
    - translations: Número mínimo de traducciones correctas
    - readings: Número mínimo de lecturas
    - analysis: Número mínimo de análisis sintácticos
  
  - Descripción del requisito
  - ¿Es obligatorio? (sí/no)
  - Peso/Importancia (1-10)
  - Criterios especiales en JSON

- **Herramientas**:
  - Editor en línea
  - Botón agregar requisito
  - Botón eliminar
  - Validación de requisitos

---

### SECCIÓN 9: 🏷️ Catalogación

**Contenido**:

- **Catalogación de contenido**:
  - Etiquetado automático de palabras, textos, oraciones
  - Categorización temática
  - Vinculación de contenido relacionado

---

### SECCIÓN 10: ⚙️ Configuración General

**Contenido**:

- **Configuración de aplicación**:
  - Modo de mantenimiento (activa/desactiva)
  - Nivel máximo permitido
  - Ajustes de gamificación (XP por actividad)
  - Temas de UI
  - Idioma de base de datos

---

## Problemas de Performance y Recomendaciones

### Problemas Identificados

#### 1. ❌ CRÍTICO: Demora en carga de panel administrativo

**Síntomas**: 
- Panel tarda 10-30 segundos en cargar la primera vez
- No hay indicador visual de que algo está cargando

**Causas raíz**:
- Carga inicial de modelos Spacy/Stanza (5-10 segundos)
- Múltiples queries a base de datos
- Cachés no completamente implementados

**Impacto**: 
- Usuario piensa que la app "está rota"
- Experiencia frustrante

**RECOMENDACIÓN**: Agregar `st.spinner("Cargando administración...")` al inicio de la página

---

#### 2. ⚠️ ALTO: Sin indicadores de carga en algunas operaciones

**Secciones afectadas**:
- Importación inteligente de textos (NLP)
- Re-análisis de todos los textos
- Análisis sintáctico con Stanza
- Carga de estadísticas del corpus

**RECOMENDACIÓN**: 
```python
# Agregar antes de operaciones lentas:
with st.spinner("⏳ Procesando... Esto puede tomar unos momentos"):
    # operación lenta
```

---

#### 3. ⚠️ MEDIO: Caché inconsistente

**Problema**: 
- Algunas secciones usan `st.session_state` para cachear
- Otras cargan datos cada vez
- Puede haber datos desincronizados

**RECOMENDACIÓN**: 
- Estandarizar patrón de cacheo
- Agregar botón "🔄 Recargar" en cada sección
- Limpiar caché automáticamente después de cambios

---

#### 4. ⚠️ MEDIO: Falta de validación en formularios

**Afectadas**:
- Formulario de nueva oración (sintaxis)
- Formulario de nuevo texto
- Formulario de nueva lección

**RECOMENDACIÓN**:
- Validar campos requeridos ANTES de procesar
- Mostrar errores específicos en rojo
- Deshabilitar botón guardarcimiento hasta que sea válido

---

#### 5. ⚠️ MEDIO: Poca información sobre capacidad del sistema

**Problema**: 
- Usuario no sabe cuántos datos hay en BD
- No sabe si la app está cerca del límite

**RECOMENDACIÓN**:
- Mostrar en Estadísticas: Total de registros, tamaño BD, % utilización
- Advertencia si se acerca a límites

---

### Mejoras de Usabilidad Recomendadas

#### 1. 🎯 CRITICIDAD ALTA

**Agregar spinner global de carga en admin**
```python
# Al inicio de pages/99_⚙️_Administracion.py
if 'admin_loaded' not in st.session_state:
    st.session_state.admin_loaded = False
    with st.spinner("⏳ Inicializando panel de administración..."):
        # cargar configuración inicial
        st.session_state.admin_loaded = True
```

**Agregar botón "Actualizar caché" en cada sección**
```python
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🔄 Recargar"):
        st.session_state[f'{section}_cache'] = []
        st.rerun()
```

---

#### 2. 🎯 CRITICIDAD ALTA

**Mejorar diseño del formulario de nueva oración**
- Agregar guía paso a paso: "1. Escribe oración → 2. Escribe traducción → 3. Clic en Analizar"
- Mostrar vista previa del análisis ANTES de guardar
- Resaltar en rojo si falta información

---

#### 3. 🎯 CRITICIDAD ALTA

**Agregar búsqueda y filtros globales**

En Tab "Ver Palabras":
- Búsqueda por latín Y español simultáneamente
- Filtro por rango de nivel
- Filtro por "incompleto" (sin traducción, sin conjugación, etc.)

---

#### 4. 🎯 CRITICIDAD MEDIA

**Mejorar feedback después de acciones**
- Cuando se guarda: mostrar `st.success()` con detalles
- Cuando falla: mostrar `st.error()` con sugerencia de solución
- Cuando se completa importación: mostrar resumen (X palabras importadas, Y con errores, etc.)

---

#### 5. 🎯 CRITICIDAD MEDIA

**Agregar tooltips y ayuda contextual**
- Hover sobre etiquetas de campos complejos
- Iconos ℹ️ para expandir información
- Ejemplos inline

---

#### 6. 🎯 CRITICIDAD MEDIA

**Estandarizar estructura de tabs**
- Todos los tabs debe tener estructura:
  - 📊 Ver/Listar (siempre primero)
  - ➕ Crear/Añadir
  - 📥 Importar
  - 📤 Exportar
  - 🛠️ Herramientas

- O mejor aún: Mover "Ver" al principio SIEMPRE

**Propuesta de orden estándar**:
```
["📚 Ver Items", "➕ Añadir Item", "📥 Importar", "📤 Exportar", "🛠️ Herramientas"]
```

---

#### 7. 🎯 CRITICIDAD MEDIA

**Agregar historial de cambios**

Para cada sección importante (vocabulario, textos, oraciones):
- Tabla de últimas 10 modificaciones
- Quién modificó, cuándo, qué cambió
- Botón de "deshacer" (si es posible)

---

#### 8. 🎯 CRITICIDAD BAJA

**Mejorar visualización de datos en estadísticas**

En "Estadísticas del Corpus":
- Añadir más gráficos:
  - Pastel: % incompleto vs completo
  - Línea: Crecimiento de vocabulario en el tiempo
  - Mapa de calor: Palabras por frecuencia

---

#### 9. 🎯 CRITICIDAD BAJA

**Agregar confirmación antes de acciones destructivas**

- Eliminar palabra: "¿Estás seguro? Esto eliminará también las referencias."
- Eliminar lección: "¿Estás seguro? Se perderá todo el contenido."
- Limpiar BD: "Esta acción no se puede deshacer."

```python
if st.button("🗑️ Eliminar"):
    confirm = st.checkbox("Confirmar eliminación")
    if confirm and st.button("Sí, eliminar permanentemente"):
        # eliminar
```

---

#### 10. 🎯 CRITICIDAD BAJA

**Agregar dark mode toggle**
- Opción en sidebar
- Persistir en session_state

---

## Resumen de Estado Actual

### ✅ Lo que funciona bien

1. ✅ Navegación principal clara e intuitiva
2. ✅ Módulos educativos bien estructurados
3. ✅ Panel administrativo completo con 10+ secciones
4. ✅ Análisis sintáctico funcionando con Stanza
5. ✅ Sistema de cacheo parcialmente implementado
6. ✅ Importación NLP inteligente funcional
7. ✅ Validación de datos implementada

### ⚠️ Lo que necesita mejora

1. ⚠️ **Indicadores de carga visuales** - CRÍTICO
2. ⚠️ **Performance de admin panel** - CRÍTICO
3. ⚠️ **Feedback del usuario incompleto** - ALTO
4. ⚠️ **Cachés inconsistentes** - ALTO
5. ⚠️ **Formularios sin validación visual** - MEDIO
6. ⚠️ **Documentación en interfaz** - MEDIO

### 📊 Recomendación de Próximas Acciones

**Prioridad 1** (Esta semana):
- [ ] Agregar spinners globales en admin
- [ ] Mejorar feedback de guardado
- [ ] Reemplazar orden de tabs (Ver primero)

**Prioridad 2** (Próximas dos semanas):
- [ ] Estandarizar cachés
- [ ] Agregar confirmaciones destructivas
- [ ] Mejorar buscadores y filtros

**Prioridad 3** (Mes siguiente):
- [ ] Agregar dark mode
- [ ] Historial de cambios
- [ ] Más gráficos en estadísticas

---

**Documento generado**: 8 de Diciembre de 2025  
**Versión**: 1.0  
**Estado de la app**: 85% completada - Funcional
