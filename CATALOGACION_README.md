# 🎯 MÓDULO DE CATALOGACIÓN DE TEXTOS LATINOS

## ¿Qué es?

Un sistema profesional y robusto para analizar, catalogar y validar textos latinos. **Completamente independiente de Streamlit**, diseñado para ejecutarse como herramienta CLI o en procesos batch.

La idea central: **Separar la generación de contenido catalogado de la aplicación de enseñanza**.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│     MÓDULO DE CATALOGACIÓN (utils + catalog_tool.py)    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ComprehensiveLatinAnalyzer (comprehensive_analyzer)    │
│  ├─ Análisis morfológico (PyCollatinus)                │
│  ├─ Análisis sintáctico (LatinCy)                      │
│  ├─ Análisis semántico                                 │
│  └─ Validación cruzada                                 │
│                     ↓                                   │
│  VocabularyManager (vocabulary_manager)                │
│  ├─ Gestión de lemas                                  │
│  ├─ Formas inflexionadas                              │
│  ├─ Definiciones y semántica                          │
│  └─ Análisis de frecuencia                            │
│                     ↓                                   │
│  BatchTextProcessor (batch_processor)                  │
│  ├─ Procesamiento en lotes                            │
│  ├─ Control de calidad                                │
│  └─ Reportes y sincronización BD                      │
│                     ↓                                   │
│  ComprehensiveValidator (quality_validator)           │
│  ├─ Validaciones morfológicas                         │
│  ├─ Validaciones sintácticas                          │
│  ├─ Validaciones semánticas                           │
│  └─ Reportes de calidad                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Componentes

| Archivo | Descripción |
|---------|------------|
| `comprehensive_analyzer.py` | Analizador integral (morfología + sintaxis + semántica) |
| `vocabulary_manager.py` | Gestión de vocabulario con validación |
| `batch_processor.py` | Procesamiento batch de textos |
| `quality_validator.py` | Validación y control de calidad |
| `catalog_tool.py` | Interfaz CLI para todas las operaciones |

---

## 🚀 Quick Start

### Instalación

```bash
# Asegúrate de que PyCollatinus y LatinCy están instalados
pip install pycollatinus
pip install spacy
python -m spacy download la_core_web_lg
```

### Uso Básico

#### 1. Analizar un texto individual

```bash
python catalog_tool.py analyze --text "Rosa est pulchra" --translation "La rosa es hermosa"
```

**Salida:**
```json
{
  "text": "Rosa est pulchra",
  "translation": "La rosa es hermosa",
  "quality": 0.87,
  "word_count": 3,
  "status": "validated",
  "full_analysis": {
    "word_analyses": [
      {
        "word": "Rosa",
        "lemma": "rosa",
        "pos": "sustantivo",
        "case": "nominativo",
        "syntax": "sujeto",
        "confidence": 0.92
      },
      ...
    ]
  }
}
```

#### 2. Procesar lote de textos

```bash
python catalog_tool.py process \
  --input textos.jsonl \
  --source "Cicerón" \
  --output reporte.json
```

#### 3. Validar un texto

```bash
python catalog_tool.py validate --text "Rosa est pulchra"
```

#### 4. Analizar morfología

```bash
python catalog_tool.py morphology --word "rosa"
```

#### 5. Analizar sintaxis

```bash
python catalog_tool.py syntax --text "Rosa est pulchra"
```

---

## 💻 Uso Programático

### Análisis Individual

```python
from utils.comprehensive_analyzer import ComprehensiveLatinAnalyzer

analyzer = ComprehensiveLatinAnalyzer()

analysis = analyzer.analyze_text(
    text="Rosa est pulchra",
    translation="La rosa es hermosa",
    difficulty_level=1
)

print(f"Calidad: {analysis.quality_score}")
print(f"Palabras: {len(analysis.word_analyses)}")
print(f"Problemas: {analysis.issues}")
```

### Procesamiento en Batch

```python
from utils.batch_processor import BatchTextProcessor, TextSource
from utils.comprehensive_analyzer import ComprehensiveLatinAnalyzer

analyzer = ComprehensiveLatinAnalyzer()
processor = BatchTextProcessor(analyzer)

source = TextSource(name="Cicerón", author="M.T. Cicero")

# Desde archivo
report = processor.process_from_file(
    "textos.jsonl",
    source,
    format="jsonl"
)

print(f"Exitosos: {report.successfully_processed}")
print(f"Calidad promedio: {report.average_quality_score:.2f}")
```

### Gestión de Vocabulario

```python
from utils.vocabulary_manager import VocabularyManager, InMemoryVocabularyRepository

repo = InMemoryVocabularyRepository()
vocab = VocabularyManager(repo)

# Añadir palabra
vocab.add_or_update_word(
    lemma="amīcus",
    definitions=["Amigo", "Compañero"],
    pos="sustantivo",
    gender="masculino",
    declension="2ª"
)

# Validar
is_valid, issues = vocab.validate_word("amīcus")
if is_valid:
    vocab.verify_word("amīcus", verified_by="admin")
```

### Validación de Calidad

```python
from utils.quality_validator import ComprehensiveValidator, ValidationLevel

validator = ComprehensiveValidator(level=ValidationLevel.STRICT)

report = validator.validate_sentence(analysis)

print(f"Válido: {report.is_valid}")
print(f"Score general: {report.overall_score:.2f}")
print(f"Recomendaciones: {report.recommendations}")
```

---

## 📊 Flujo de Trabajo Completo

### Paso 1: Preparación de Textos

Crear archivo `textos.jsonl`:
```json
{"text": "Rosa est pulchra", "translation": "La rosa es hermosa", "difficulty_level": 1}
{"text": "Amat puella florem", "translation": "La chica ama la flor", "difficulty_level": 2}
{"text": "Agricola amat terram", "translation": "El granjero ama la tierra", "difficulty_level": 2}
```

### Paso 2: Procesar y Analizar

```bash
python catalog_tool.py process \
  --input textos.jsonl \
  --source "Exercitia" \
  --output reporte_analisis.json
```

### Paso 3: Revisar Resultados

```bash
# Ver reporte
cat reporte_analisis.json

# Identificar problemas
python catalog_tool.py quality --text "Texto problemático"
```

### Paso 4: Guardar en BD

```python
from utils.batch_processor import DatabaseSyncManager

sync = DatabaseSyncManager(db_connection)
saved_count = sync.save_batch_to_db(report)
print(f"Guardados en BD: {saved_count}")
```

---

## 🎯 Características Principales

### ✅ Análisis Integral

- **Morfología**: Lematización, paradigmas, formas inflexionadas
- **Sintaxis**: Funciones, dependencias, construcciones especiales
- **Semántica**: Definiciones, campos semánticos, frecuencia
- **Validación cruzada**: Detecta inconsistencias

### ✅ Control de Calidad

- Scores de confianza por componente
- Validaciones morfológicas, sintácticas, semánticas
- Reportes detallados de problemas
- Sugerencias automáticas de mejora

### ✅ Gestión de Vocabulario

- Almacenamiento de lemas
- Múltiples definiciones por palabra
- Formas inflexionadas
- Análisis de frecuencia
- Verificación de entrada

### ✅ Procesamiento Batch

- Procesar múltiples textos eficientemente
- Callbacks de progreso
- Reportes detallados
- Sincronización con BD

### ✅ Interfaz Flexible

- CLI con múltiples comandos
- API programática
- Salida JSON para integración

---

## 🔧 Configuración

### Threshold de Calidad

```python
# Textos por debajo de 0.7 requieren revisión manual
processor = BatchTextProcessor(analyzer, quality_threshold=0.7)
```

### Nivel de Validación

```python
# Validación exhaustiva
validator = ComprehensiveValidator(level=ValidationLevel.STRICT)
```

### Seleccionar Analizadores

```python
# Verificar disponibilidad
if analyzer.morph_analyzer:
    print("✅ Morfología disponible")
if analyzer.syntax_analyzer:
    print("✅ Sintaxis disponible")
```

---

## 📈 Ejemplos Reales

### Ejemplo 1: Procesamiento de Capítulo Completo

```python
from utils.batch_processor import BatchTextProcessor, TextSource

# Cargar capítulo
with open("ciceron_cap1.json") as f:
    texts = json.load(f)

source = TextSource(
    name="Pro Milone",
    author="Cicerón",
    period="clásico",
    genre="oración judicial"
)

processor = BatchTextProcessor(analyzer, vocab_manager)

def progress(current, total):
    print(f"Procesando... {current}/{total}")

report = processor.process_batch(
    texts,
    source,
    progress_callback=progress
)

# Análisis
print(f"Éxito: {report.successfully_processed}/{report.total_texts}")
print(f"Calidad: {report.average_quality_score:.2f}")

# Guardar
report.save_to_json("reporte_cap1.json")
```

### Ejemplo 2: Validación Manual de Textos Problemáticos

```python
# Obtener textos con baja calidad
problems = processor.identify_problematic_texts(quality_threshold=0.7)

for result in problems:
    print(f"\n❌ {result.text_id}")
    print(f"   Calidad: {result.quality_score:.2f}")
    print(f"   Problemas: {result.analysis.issues}")
    
    # Revisar manualmente y re-procesar si es necesario
```

### Ejemplo 3: Enriquecimiento de Vocabulario

```python
from utils.vocabulary_manager import DefinitionSource

# Procesar un lote
report = processor.process_batch(texts, source)

# Para cada análisis exitoso, enriquecer vocabulario
for result in report.results:
    if result.status == ProcessingStatus.COMPLETED:
        for word_analysis in result.analysis.word_analyses:
            vocab.update_word_frequency(word_analysis.word, 1)

# Exportar vocabulario actualizado
vocab.export_to_json("vocabulario_enriquecido.json")

# Estadísticas
stats = vocab.get_frequency_stats()
print(f"Total palabras únicas: {stats['total_unique_words']}")
print(f"Total ocurrencias: {stats['total_occurrences']}")
```

---

## 📋 Estructura de Datos

### ComprehensiveSentenceAnalysis

```python
{
  "original_text": "Rosa est pulchra",
  "translation": "La rosa es hermosa",
  "word_analyses": [
    {
      "word": "Rosa",
      "morphology": {
        "lemma": "rosa",
        "pos": "sustantivo",
        "case": "nominativo",
        "gender": "femenino",
        "number": "singular"
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
  "validation_status": "validated",
  "issues": []
}
```

---

## ⚠️ Troubleshooting

### PyCollatinus no carga

```bash
pip install --upgrade pycollatinus
# O reinstalar
pip uninstall pycollatinus -y && pip install pycollatinus
```

### LatinCy no disponible

```bash
pip install spacy
python -m spacy download la_core_web_lg
```

### Bajo score de calidad

1. Verificar que el texto es latino válido
2. Revisar caracteres especiales (macrones, etc.)
3. Aumentar threshold de confianza manualmente
4. Complementar definiciones faltantes

---

## 📚 Documentación Completa

Ver `CATALOGACION_GUIDE.md` para documentación exhaustiva.

---

## 🎓 Próximos Pasos

- [ ] Integración con API REST
- [ ] Dashboard web para monitoreo
- [ ] Exportación a múltiples formatos
- [ ] Detección automática de construcciones retóricas
- [ ] Análisis métrico (verso)

---

**Versión**: 1.0  
**Estado**: Producción  
**Última actualización**: 2025-12-07

¡Listo para catalogar textos latinos con confianza! 📚✨
