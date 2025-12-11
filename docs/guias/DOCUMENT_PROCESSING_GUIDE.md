# Guía Completa: Procesamiento de Documentos para Corpus de Entrenamiento

## Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Workflow Completo](#workflow-completo)
3. [Paso 1: Escaneo](#paso-1-escaneo)
4. [Paso 2: Preprocesamiento con ScanTailor](#paso-2-preprocesamiento-con-scantailor)
5. [Paso 3: OCR (Reconocimiento de Texto)](#paso-3-ocr-reconocimiento-de-texto)
6. [Paso 4: Limpieza Post-OCR](#paso-4-limpieza-post-ocr)
7. [Paso 5: Alineación de Textos Paralelos](#paso-5-alineación-de-textos-paralelos)
8. [Paso 6: Generación del Corpus Final](#paso-6-generación-del-corpus-final)
9. [Casos Especiales](#casos-especiales)
10. [Scripts Disponibles](#scripts-disponibles)
11. [Checklist Final](#checklist-final)

---

## Resumen Ejecutivo

**Objetivo:** Convertir libros físicos bilingües (latín-español/italiano) en corpus de texto listo para entrenar modelos de traducción.

**Tiempo estimado:** 4-5 horas por obra de ~200 páginas  
**Herramientas principales:** ScanTailor, Tesseract OCR, scripts Python personalizados

**Input:** Libro físico escaneado  
**Output:** Archivos JSON con pares de oraciones alineadas

---

## Workflow Completo

```
Libro Físico
    ↓
[PASO 1] Escaneo (300 DPI, TIF)
    ↓
[PASO 2] ScanTailor (limpiar, deskew)
    ↓
    TIF limpios
    ↓
[PASO 3] OCR con Tesseract
    ↓
    Archivos .txt raw
    ↓
[PASO 4] Limpieza automática + manual
    ↓
    Archivos .txt limpios
    ↓
[PASO 5] Alineación de textos paralelos
    ↓
    Archivos .txt alineados
    ↓
[PASO 6] Generación de corpus JSON
    ↓
    ✅ corpus.json → Listo para entrenamiento
```

---

## Paso 1: Escaneo

### Configuración del Escáner

| Parámetro | Valor Recomendado | Notas |
|-----------|-------------------|-------|
| **Resolución** | 300 DPI (mínimo) | 600 DPI para libros antiguos |
| **Formato** | **TIF** o PNG | ✅ Sin compresión con pérdida |
| **Color** | Escala de grises (8-bit) | Suficiente para texto |
| **Profundidad** | 8 bits | Balance calidad/tamaño |

### ¿Por Qué TIF?

✅ **Ventajas:**
- Sin pérdida de calidad
- Soportado por todos los OCR
- Estándar de archivo

❌ **Evitar JPG:**
- Compresión con pérdida
- Artefactos que dificultan el OCR

### Estructura de Archivos

```
data/scans/
├── obra1/
│   ├── page_001.tif
│   ├── page_002.tif
│   └── ...
├── obra2/
│   ├── page_001.tif
│   └── ...
```

---

## Paso 2: Preprocesamiento con ScanTailor

### ¿Qué es ScanTailor?

Herramienta open-source para limpiar escaneos de libros.

**Instalar:**
```bash
# Ubuntu/Debian
sudo apt install scantailor-advanced

# Windows
# Descargar de: https://github.com/4lex4/scantailor-advanced
```

### Configuración Óptima

1. **Fix Orientation** → Auto
2. **Split Pages** → Auto (o Manual para ediciones bilingües)
3. **Deskew** → Auto
4. **Select Content** → Auto (ajustar manualmente si falla)
5. **Margins** → 10-20mm todos los lados
6. **Output:**
   - Mode: **Black & White** ← Mejor para OCR
   - DPI: **300** (mantener original)
   - Format: **TIF**

### Output Esperado

```
data/scans/obra1_processed/
├── page_001.tif  ← Limpio, sin márgenes, deskewed
├── page_002.tif
└── ...
```

---

## Paso 3: OCR (Reconocimiento de Texto)

### Opción A: Tesseract (Recomendada - Gratuita)

#### Instalación

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-lat  # Latín
sudo apt install tesseract-ocr-spa  # Español
sudo apt install tesseract-ocr-ita  # Italiano

# Verificar instalación
tesseract --version
```

#### Uso Básico

**Un archivo:**
```bash
tesseract page_001.tif output_001 -l lat
```

**Múltiples archivos:**
```bash
for file in *.tif; do
    tesseract "$file" "${file%.tif}" -l lat
done
```

#### Ediciones Bilingües

**Para columnas paralelas o párrafos alternados, usa el script automático:**

```bash
python scripts/process_bilingual_ocr.py
```

Ver [Casos Especiales](#casos-especiales) para detalles.

### Opción B: Adobe Acrobat Pro (De Pago)

1. Herramientas → Escanear y OCR → En este archivo
2. Seleccionar idioma
3. Exportar como texto

### Opción C: Google Cloud Vision API (Mejor Calidad, Cuota Limitada)

Excelente para latín clásico, pero requiere configuración de API.

### Combinar Archivos

```bash
# Unir todos los .txt en uno solo
cd data/ocr/obra1/
cat *.txt > obra1_raw.txt
```

---

## Paso 4: Limpieza Post-OCR

### Script Automático

```bash
python scripts/clean_ocr_text.py \
    --input data/ocr/obra1_raw.txt \
    --output data/cleaned/obra1_clean.txt \
    --language latin
```

### Qué Limpia Automáticamente

- ✅ Números de página
- ✅ Encabezados repetitivos
- ✅ Guiones de división silábica
- ✅ Espacios múltiples
- ✅ Errores comunes de OCR (j→i en latín, acentos en español, etc.)

### Revisión Manual Necesaria

Después de la limpieza automática, **siempre revisa:**

1. **Primeras 20-30 oraciones** - Para detectar patrones de error
2. **Nombres propios** - Suelen tener errores (Caesar → Cæsar)
3. **Abreviaturas** - Pueden confundir al OCR
4. **Números romanos** - III a veces se lee como IlI

**Herramienta recomendada:** VS Code con búsqueda/reemplazo por regex

---

## Paso 5: Alineación de Textos Paralelos

### Verificar Estructura Similar

```bash
python scripts/analyze_text_structure.py \
    --latin data/cleaned/obra1_la.txt \
    --translation data/cleaned/obra1_es.txt
```

Output:
```
📄 obra1_la.txt
   Párrafos: 45
   Oraciones: 234

📄 obra1_es.txt
   Párrafos: 45
   Oraciones: 234

✅ Estructura similar
```

### Alineación Automática

```bash
python scripts/align_parallel_texts.py \
    --latin data/cleaned/obra1_la.txt \
    --translation data/cleaned/obra1_es.txt \
    --output data/aligned/obra1
```

### Formato Final

**Cada archivo debe tener:**
- ✅ Una oración por línea
- ✅ Línea N del latín = Línea N de la traducción
- ✅ UTF-8 encoding

**Ejemplo:**

```
obra1_la.txt:
Gallia est omnis divisa in partes tres.
Quarum unam incolunt Belgae.

obra1_es.txt:
Toda la Galia está dividida en tres partes.
Una de ellas la habitan los belgas.
```

### Validación

```bash
python scripts/validate_alignment.py \
    --latin data/aligned/obra1_la.txt \
    --translation data/aligned/obra1_es.txt
```

---

## Paso 6: Generación del Corpus Final

### Para Una Sola Obra

```bash
python scripts/create_json_corpus.py \
    --latin data/aligned/obra1_la.txt \
    --translation data/aligned/obra1_es.txt \
    --output data/corpus/obra1_es.json \
    --language spanish
```

### Para Múltiples Obras (Multilingüe)

```bash
python scripts/prepare_multilingual_corpus.py
```

Edita primero el script con la configuración de tus obras.

### Corpus Final

```json
[
  {
    "latin": "Gallia est omnis divisa in partes tres.",
    "target": "Toda la Galia está dividida en tres partes.",
    "prefix": "translate Latin to Spanish: "
  },
  {
    "latin": "Alea iacta est.",
    "target": "Il dado è tratto.",
    "prefix": "translate Latin to Italian: "
  }
]
```

**¡Listo para subir a Colab y entrenar!**

---

## Casos Especiales

### Caso 1: Ediciones Bilingües - Columnas Paralelas

**Aspecto típico:**
```
┌──────────────────────────────┐
│  LATÍN       │  ESPAÑOL      │
│  Gallia est  │  Toda la      │
│  omnis...    │  Galia...     │
└──────────────────────────────┘
```

**Solución:**

```python
from scripts.process_bilingual_ocr import batch_process_bilingual
from pathlib import Path

batch_process_bilingual(
    input_dir=Path("data/scans/caesar"),
    output_dir=Path("data/ocr/caesar"),
    layout="columns",      # ← Columnas paralelas
    trans_lang="spa"       # ← Español (o "ita" para italiano)
)
```

### Caso 2: Ediciones Bilingües - Párrafos Alternados

**Aspecto típico:**
```
[LATÍN]
Gallia est omnis divisa in partes tres.

[ESPAÑOL]
Toda la Galia está dividida en tres partes.

[LATÍN]
Quarum unam incolunt Belgae.
```

**Solución:**

```python
batch_process_bilingual(
    input_dir=Path("data/scans/virgilio"),
    output_dir=Path("data/ocr/virgilio"),
    layout="alternating",  # ← Párrafos alternados
    trans_lang="spa"
)
```

### Caso 3: Columnas No Centradas

Si las columnas no están exactamente al 50%:

```python
batch_process_bilingual(
    input_dir=Path("data/scans/ovidio"),
    output_dir=Path("data/ocr/ovidio"),
    layout="columns",
    split_x=900,          # ← Píxel exacto de división
    trans_lang="ita"
)
```

---

## Scripts Disponibles

### Scripts de OCR

| Script | Propósito | Uso |
|--------|-----------|-----|
| `process_bilingual_ocr.py` | OCR de ediciones bilingües | Automático |
| `clean_ocr_text.py` | Limpieza post-OCR | Requerido |

### Scripts de Alineación

| Script | Propósito | Uso |
|--------|-----------|-----|
| `analyze_text_structure.py` | Verificar alineación | Opcional |
| `align_parallel_texts.py` | Alinear textos | Requerido |
| `validate_alignment.py` | Validar calidad | Recomendado |

### Scripts de Generación de Corpus

| Script | Propósito | Uso |
|--------|-----------|-----|
| `create_json_corpus.py` | Generar JSON de una obra | Requerido |
| `prepare_multilingual_corpus.py` | Combinar múltiples obras | Para multilingüe |
| `extract_parallel_texts.py` | Extraer de formatos especiales | Según necesidad |

---

## Checklist Final

### Antes de Entrenar

- [ ] ✅ Escaneo completo (300+ DPI, TIF)
- [ ] ✅ Preprocesado con ScanTailor
- [ ] ✅ OCR completado
- [ ] ✅ Limpieza automática aplicada
- [ ] ✅ Revisión manual de al menos 30 oraciones
- [ ] ✅ Textos alineados (misma cantidad de líneas)
- [ ] ✅ Validación automática pasada
- [ ] ✅ Corpus JSON generado
- [ ] ✅ Mínimo 500 pares de oraciones
- [ ] ✅ Copia de seguridad de archivos originales

### Calidad del Corpus

| Métrica | Mínimo | Ideal | Excelente |
|---------|--------|-------|-----------|
| **Pares totales** | 500 | 1,000 | 5,000+ |
| **Alineación** | 90% | 95% | 99% |
| **Errores OCR** | <5% | <2% | <1% |

---

## Tiempo Estimado por Obra (~200 páginas)

| Paso | Tiempo |
|------|--------|
| 1. Escaneo | 30-60 min |
| 2. ScanTailor | 45 min |
| 3. OCR (automático) | 10 min |
| 4. Limpieza manual | 2-3 horas |
| 5. Alineación | 30 min |
| 6. Validación | 30 min |
| **TOTAL** | **4-5 horas** |

---

## Troubleshooting

### Problema: OCR produce mucho ruido

**Solución:**
- Mejorar calidad de escaneo (600 DPI)
- Ajustar contraste en ScanTailor
- Usar modo "Black & White" en output

### Problema: Desalineación de textos

**Solución:**
- Verificar que ambos textos tengan misma estructura
- Revisar manualmente primeros párrafos
- Usar script de validación para detectar problemas

### Problema: Edición bilingüe no se separa bien

**Solución:**
- En ScanTailor, usar "Split Pages" manual
- Ajustar `split_x` en el script
- Como último recurso, separar manualmente con GIMP

---

## Recursos Adicionales

### Documentación Relacionada

- [`docs/OCR_TO_CORPUS_GUIDE.md`](file:///home/diego/Projects/latin-python/docs/OCR_TO_CORPUS_GUIDE.md) - Guía técnica detallada
- [`docs/COLAB_QUICKSTART.md`](file:///home/diego/Projects/latin-python/docs/COLAB_QUICKSTART.md) - Entrenar en Google Colab
- Artifact: `multilingual_training_guide.md` - Guía de entrenamiento multilingüe

### Herramientas

- **ScanTailor Advanced**: https://github.com/4lex4/scantailor-advanced
- **Tesseract OCR**: https://github.com/tesseract-ocr/tesseract
- **Google Colab**: https://colab.research.google.com

---

## Próximos Pasos

Una vez tengas el corpus JSON:

1. **Sube a Google Colab** usando `colab_training.ipynb`
2. **Entrena el modelo** (~45-60 min en GPU T4)
3. **Descarga el modelo entrenado**
4. **Integra en tu aplicación**

¡Listo! 🚀
