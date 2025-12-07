# 📚 MÓDULO DE CATALOGACIÓN INTEGRAL - Lingua Latina Viva

## Visión General

El **Módulo de Catalogación Integral** es un sistema independiente y robusto diseñado para proporcionar análisis profundos de textos latinos. Separa completamente la **generación de contenido catalogado** de la **aplicación de enseñanza**, permitiendo:

- 📖 **Distribución ligera**: Solo lecciones, ejercicios y BD compilada
- 🔧 **Procesamiento offline**: Análisis sin dependencias de Streamlit
- ✅ **Control de calidad**: Validación y revisión antes de integrar
- 📊 **Análisis exhaustivo**: Morfología, sintaxis, semántica integradas

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                 MÓDULO DE CATALOGACIÓN                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ComprehensiveLatinAnalyzer (comprehensive_analyzer.py)  │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Análisis morfológico (PyCollatinus)                   │  │
│  │ • Análisis sintáctico (LatinCy)                         │  │
│  │ • Análisis semántico                                    │  │
│  │ • Validación cruzada de resultados                      │  │
│  │ • Cálculo de scores de confianza                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  VocabularyManager (vocabulary_manager.py)               │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Almacenamiento de lemas                               │  │
│  │ • Gestión de formas inflexionadas                       │  │
│  │ • Enriquecimiento de definiciones                       │  │
│  │ • Análisis de frecuencia y dificultad                   │  │
│  │ • Validación de coherencia                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  BatchTextProcessor (batch_processor.py)                 │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Procesamiento en lotes                                │  │
│  │ • Control de calidad                                    │  │
│  │ • Generación de reportes                                │  │
│  │ • Sincronización con BD                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  catalog_tool.py - Interfaz CLI                          │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Comandos de análisis individual                       │  │
│  │ • Procesamiento de lotes                                │  │
│  │ • Validación de textos                                  │  │
│  │ • Reportes de calidad                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Componentes Principales

### 1. ComprehensiveLatinAnalyzer

**Archivo**: `utils/comprehensive_analyzer.py`

Analizador integral que combina múltiples fuentes:

```python
from utils.comprehensive_analyzer import ComprehensiveLatinAnalyzer

analyzer = ComprehensiveLatinAnalyzer()

# Analizar texto
analysis = analyzer.analyze_text(
    text="Rosa est pulchra",
    translation="La rosa es hermosa",
    source="ejemplo",
    difficulty_level=1
)

# Resultado: ComprehensiveSentenceAnalysis
print(f"Calidad: {analysis.quality_score}")
print(f"Palabras analizadas: {len(analysis.word_analyses)}")
print(f"Problemas encontrados: {analysis.issues}")
```

**Salida**:
```json
{
  "word_analyses": [
    {
      "word": "Rosa",
      "morphology": {
        "lemma": "rosa",
        "pos": "sustantivo",
        "case": "nominativo",
        "number": "singular",
        "gender": "femenino"
      },
      "syntax": {
        "function": "sujeto",
        "dependency_relation": "nsubj"
      },
      "semantics": {
        "definitions": ["Flor del rosal"],
        "frequency_score": 0.9
      }
    }
  ],
  "quality_score": 0.85,
  "validation_status": "validated"
}
```

### 2. VocabularyManager

**Archivo**: `utils/vocabulary_manager.py`

Gestión exhaustiva del vocabulario:

```python
from utils.vocabulary_manager import VocabularyManager, InMemoryVocabularyRepository

# Crear gestor
repo = InMemoryVocabularyRepository()
vocab = VocabularyManager(repo)

# Añadir palabra
vocab.add_or_update_word(
    lemma="rosa",
    definitions=["Flor del rosal", "Símbolo de belleza"],
    pos="sustantivo",
    gender="femenino",
    declension="1ª",
    difficulty_level=2
)

# Añadir formas inflexionadas
vocab.add_inflected_form(
    lemma="rosa",
    form="rosae",
    case="genitivo",
    number="singular"
)

# Búsquedas
results = vocab.search_by_definition("flor")
unverified = vocab.get_unverified_words()
stats = vocab.get_frequency_stats()
```

### 3. BatchTextProcessor

**Archivo**: `utils/batch_processor.py`

Procesamiento eficiente de múltiples textos:

```python
from utils.batch_processor import BatchTextProcessor, TextSource

processor = BatchTextProcessor(analyzer, vocab_manager)

# Procesar textos desde archivo
source = TextSource(
    name="Cicerón",
    author="Marcus Tullius Cicero",
    period="clásico",
    genre="oración"
)

report = processor.process_from_file(
    "textos.jsonl",
    source,
    format="jsonl"
)

# Obtener resultados
print(f"Exitosos: {report.successfully_processed}/{report.total_texts}")
print(f"Calidad promedio: {report.average_quality_score:.2f}")
print(f"Tiempo total: {report.total_processing_time:.2f}s")
print(f"Recomendaciones: {report.recommendations}")
```

### 4. Herramienta CLI (catalog_tool.py)

**Archivo**: `catalog_tool.py`

Interfaz de línea de comandos para todas las operaciones:

```bash
# Analizar texto individual
python catalog_tool.py analyze --text "Salve, munde!"

# Procesar lote de textos
python catalog_tool.py process --input textos.json --source "Cicerón" --output reporte.json

# Validar texto
python catalog_tool.py validate --text "Rosa est pulchra"

# Análisis de calidad
python catalog_tool.py quality --text "Rosa est pulchra"

# Análisis morfológico
python catalog_tool.py morphology --word "rosa"

# Análisis sintáctico
python catalog_tool.py syntax --text "Rosa est pulchra"

# Estadísticas de vocabulario
python catalog_tool.py vocabulary --stats
```

---

## Flujo de Trabajo Típico

### Fase 1: Preparación de Textos

```
Textos originales (libros, inscripciones)
        ↓
Extracción y limpieza
        ↓
Archivo JSON/JSONL con textos
        ↓
    {
      "text": "Rosa est pulchra",
      "translation": "La rosa es hermosa",
      "source": "Cicerón",
      "lesson_number": 1,
      "difficulty_level": 2
    }
```

### Fase 2: Análisis y Catalogación

```
Archivo de textos
        ↓
BatchTextProcessor.process_from_file()
        ↓
Para cada texto:
  1. ComprehensiveLatinAnalyzer analiza
  2. VocabularyManager actualiza léxico
  3. Validación cruzada
  4. Cálculo de calidad
        ↓
BatchProcessingReport con resultados
        ↓
    {
      "successful": 95,
      "failed": 2,
      "requires_review": 3,
      "average_quality": 0.87
    }
```

### Fase 3: Revisión y Refinamiento

```
Análisis de problemas
        ↓
¿Calidad > umbral?
  ├─ Sí → Listo para BD
  └─ No → Revisión manual
        ↓
Mejoras y correcciones
        ↓
Re-procesamiento si es necesario
```

### Fase 4: Almacenamiento en BD

```
Análisis validados
        ↓
DatabaseSyncManager.save_batch_to_db()
        ↓
BD compilada (lingua_latina.db)
        ↓
Distribución con aplicación Streamlit
```

---

## Estructura de Datos Clave

### ComprehensiveSentenceAnalysis

```python
@dataclass
class ComprehensiveSentenceAnalysis:
    original_text: str                          # Texto latino
    translation: Optional[str]                  # Traducción
    word_analyses: List[ComprehensiveWordAnalysis]  # Análisis de cada palabra
    
    sentence_type: str                          # declarativa, interrogativa, etc.
    main_verb_index: Optional[int]              # Índice del verbo principal
    special_constructions: List[str]            # ablativo absoluto, etc.
    
    overall_confidence: float                   # Confianza 0-1
    quality_score: float                        # Score de calidad
    validation_status: str                      # validated, needs_review, error
    issues: List[str]                           # Problemas encontrados
```

### ComprehensiveWordAnalysis

```python
@dataclass
class ComprehensiveWordAnalysis:
    word: str                                   # Forma en el texto
    position_in_sentence: int                   # Posición 0-based
    
    morphology: MorphologicalData               # {lemma, pos, case, number, etc.}
    semantics: SemanticData                     # {definitions, etymology, etc.}
    syntax: SyntacticAnalysis                   # {function, head_word, etc.}
    
    overall_confidence: float                   # Promedio de confianzas
    validation_status: str                      # pending, validated, needs_review
```

### LatinWord (Entrada de Vocabulario)

```python
@dataclass
class LatinWord:
    lemma: str                                  # Forma de diccionario
    definitions: List[Definition]               # Múltiples definiciones
    inflected_forms: List[InflectedForm]        # Formas conjugadas/declinadas
    
    pos: str                                    # Categoría gramatical
    declension: Optional[str]                   # 1ª, 2ª, 3ª, etc.
    conjugation: Optional[str]                  # 1ª, 2ª, 3ª, etc.
    gender: Optional[str]                       # m, f, n
    
    frequency: int                              # Ocurrencias encontradas
    difficulty_level: int                       # 1-10
    
    is_verified: bool                           # Ha sido verificada
    etymology: Optional[str]                    # Origen de la palabra
    relations: List[WordRelation]               # Sinónimos, derivados, etc.
```

---

## Ejemplos de Uso

### Ejemplo 1: Análisis Simple

```python
from utils.comprehensive_analyzer import ComprehensiveLatinAnalyzer

analyzer = ComprehensiveLatinAnalyzer()

text = "Amare et sapere vix deo conceditur"
analysis = analyzer.analyze_text(text)

for word in analysis.word_analyses:
    print(f"{word.word:12} → {word.morphology.lemma:12} ({word.morphology.pos.value})")
    print(f"   Sintaxis: {word.syntax.function.value}")
    print()
```

**Salida**:
```
Amare        → amare           (verbo)
   Sintaxis: sujeto

et           → et              (conjunción)
   Sintaxis: conjunción

sapere       → sapere          (verbo)
   Sintaxis: predicado

vix          → vix             (adverbio)
   Sintaxis: adverbial

deo          → deus            (sustantivo)
   Sintaxis: objeto indirecto

conceditur   → concedo         (verbo)
   Sintaxis: predicado
```

### Ejemplo 2: Procesamiento en Batch

```python
from utils.batch_processor import BatchTextProcessor, TextSource

# Preparar datos
texts = [
    {"text": "Rosa est pulchra", "translation": "La rosa es hermosa"},
    {"text": "Amat puella florem", "translation": "La chica ama la flor"},
    {"text": "Agricola amat terram", "translation": "El granjero ama la tierra"},
]

source = TextSource(
    name="Exercitia Latina",
    author="Desconocido",
    genre="ejercicio"
)

# Procesar
processor = BatchTextProcessor(analyzer, vocab_manager)
report = processor.process_batch(texts, source)

# Analizar resultados
print(f"✅ Exitosos: {report.successfully_processed}")
print(f"⚠️ Requieren revisión: {report.requires_review}")
print(f"❌ Fallos: {report.failed}")
print(f"📊 Calidad promedio: {report.average_quality_score:.2f}")

# Guardar reporte
report.save_to_json("reporte_batch.json")
```

### Ejemplo 3: Gestión de Vocabulario

```python
from utils.vocabulary_manager import VocabularyManager, InMemoryVocabularyRepository

repo = InMemoryVocabularyRepository()
vocab = VocabularyManager(repo)

# Crear entrada
vocab.add_or_update_word(
    lemma="amīcus",
    definitions=["Amigo", "Persona allegada"],
    pos="sustantivo",
    gender="masculino",
    declension="2ª",
    difficulty_level=1
)

# Validar
is_valid, issues = vocab.validate_word("amīcus")
if is_valid:
    vocab.verify_word("amīcus", verified_by="admin")

# Estadísticas
stats = vocab.get_frequency_stats()
print(f"Palabras totales: {stats['total_unique_words']}")
print(f"Verificadas: {stats['verified_words']}")
```

---

## Mejores Prácticas

### ✅ Hacer

1. **Validar siempre antes de guardar en BD**
   ```python
   is_valid, issues = vocab.validate_word(lemma)
   if is_valid:
       # Guardar en BD
   ```

2. **Usar análisis con calidad threshold**
   ```python
   processor = BatchTextProcessor(analyzer, quality_threshold=0.75)
   ```

3. **Revisar reportes de problemas**
   ```python
   problems = processor.identify_problematic_texts()
   ```

4. **Mantener vocabulario actualizado**
   ```python
   vocab.update_word_frequency(lemma, count)
   ```

### ❌ No Hacer

1. **No confiar ciegamente en confianza automática**
   - Siempre revisar manualmente textos complejos

2. **No procesar lotes enormes de una vez**
   - Dividir en lotes de 100-500 textos

3. **No ignorar issues de validación**
   - Revisar y corregir antes de integrar en BD

---

## Configuración y Ajustes

### Control de Calidad

```python
# Threshold de calidad (0-1)
processor = BatchTextProcessor(
    analyzer,
    quality_threshold=0.7  # 70% mínimo
)
```

### Analizadores Disponibles

```python
# Asegurar que tenemos analizadores
if analyzer.morph_analyzer:
    print("✅ PyCollatinus disponible")
if analyzer.syntax_analyzer:
    print("✅ LatinCy disponible")
if analyzer.logic_engine:
    print("✅ Motor de lógica disponible")
```

---

## Troubleshooting

### PyCollatinus no carga

```bash
pip install pycollatinus
python -c "from pycollatinus import Lemmatiseur; print('OK')"
```

### LatinCy no disponible

```bash
pip install spacy
python -m spacy download la_core_web_lg
```

### Bajo score de calidad

1. Verificar que el texto es válido latino
2. Revisar si hay caracteres especiales
3. Considerar compilación manual de definiciones

---

## Próximos Pasos

### Mejoras Planeadas

- [ ] Integración con LILA (Linked Latin)
- [ ] Mejora de análisis sintáctico con reglas personalizadas
- [ ] API REST para procesos remotos
- [ ] Dashboard de monitoreo web
- [ ] Exportación a múltiples formatos (CSV, XML)

### Extensiones Posibles

- [ ] Soporte para textos medievales
- [ ] Análisis métrico (verso)
- [ ] Detección automática de construcciones retóricas
- [ ] Generación de mapas conceptuales

---

## Referencia de Comandos CLI

```bash
# Análisis individual
python catalog_tool.py analyze --text "Salve, amice!" --translation "¡Hola, amigo!"

# Procesamiento batch
python catalog_tool.py process \
  --input textos.jsonl \
  --source "Cicerón" \
  --author "M.T. Cicero" \
  --period "clásico" \
  --output reporte.json

# Validación
python catalog_tool.py validate --text "Rosa est pulchra"

# Análisis de calidad
python catalog_tool.py quality --text "Rosa est pulchra" --json

# Morfología
python catalog_tool.py morphology --word "rosa"

# Sintaxis
python catalog_tool.py syntax --text "Rosa est pulchra"

# Vocabulario
python catalog_tool.py vocabulary --stats --json
```

---

**Versión**: 1.0  
**Última actualización**: 2025-12-07  
**Estado**: Producción
