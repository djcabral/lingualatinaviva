# Guía Completa: Del Escaneo al Corpus de Entrenamiento

## Tabla de Contenidos

1. [Post-OCR: Limpieza Inicial](#1-post-ocr-limpieza-inicial)
2. [Corrección de Errores Comunes](#2-corrección-de-errores-comunes)
3. [Alineación de Textos Paralelos](#3-alineación-de-textos-paralelos)
4. [Validación de Calidad](#4-validación-de-calidad)
5. [Formato Final](#5-formato-final)
6. [Herramientas Útiles](#6-herramientas-útiles)

---

## 1. Post-OCR: Limpieza Inicial

### Paso 1.1: Eliminar Encabezados y Números de Página

**Problema típico después del OCR:**
```
=====================================
LIBRO I - CAPÍTULO 3
Página 47
=====================================

Gallia est omnis divisa in partes tres.

________________
Footnote: ...
________________
Página 48
```

**Limpieza:**

```python
# scripts/clean_ocr_text.py
import re

def remove_page_numbers(text):
    """Elimina números de página y encabezados."""
    # Eliminar "Página XX"
    text = re.sub(r'Página\s+\d+', '', text)
    
    # Eliminar líneas con solo números
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Eliminar líneas de separación (===, ---, ___)
    text = re.sub(r'^[=\-_]{3,}\s*$', '', text, flags=re.MULTILINE)
    
    return text

def remove_headers_footers(text):
    """Elimina encabezados repetitivos."""
    # Eliminar "LIBRO X - CAPÍTULO Y"
    text = re.sub(r'LIBRO\s+[IVX]+\s*-\s*CAPÍTULO\s+\d+', '', text)
    
    # Eliminar "Footnote: ..."
    text = re.sub(r'Footnote:.*?(?=\n\n|\Z)', '', text, flags=re.DOTALL)
    
    return text

# Uso:
with open('data/ocr/raw/caesar_es.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

clean_text = remove_page_numbers(raw_text)
clean_text = remove_headers_footers(clean_text)

with open('data/ocr/cleaned/caesar_es.txt', 'w', encoding='utf-8') as f:
    f.write(clean_text)
```

### Paso 1.2: Normalizar Espacios en Blanco

```python
def normalize_whitespace(text):
    """Normaliza espacios, tabs y líneas vacías."""
    # Convertir tabs a espacios
    text = text.replace('\t', ' ')
    
    # Eliminar múltiples espacios
    text = re.sub(r' +', ' ', text)
    
    # Eliminar espacios al inicio/fin de línea
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    
    # Eliminar más de 2 líneas vacías consecutivas
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text
```

### Paso 1.3: Corregir Guiones de División Silábica

**Problema:**
```
Caesar in Galliam profe-
ctus est.
```

**Solución:**
```python
def fix_hyphenation(text):
    """Une palabras divididas por guiones."""
    # Patrón: letra + guión + salto de línea + letra minúscula
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    
    return text

# Resultado:
# "Caesar in Galliam profectus est."
```

---

## 2. Corrección de Errores Comunes de OCR

### Paso 2.1: Errores Típicos en Latín

```python
def fix_latin_ocr_errors(text):
    """Corrige errores comunes de OCR en latín."""
    
    # Diccionario de correcciones comunes
    corrections = {
        # ae → æ (diptongo mal interpretado)
        r'\bae\b': 'æ',
        
        # Confusiones comunes
        r'\bcum\b': 'cum',  # a veces OCR lee "cnm"
        r'quum': 'cum',     # ortografía antigua
        
        # j → i (el latín clásico no usa j)
        r'j': 'i',
        
        # Mayúsculas incorrectas
        r'\bEST\b': 'est',
        r'\bET\b': 'et',
        
        # Números romanos mal interpretados
        r'\bI[Il]I\b': 'III',  # III a veces se lee como IlI
    }
    
    for pattern, replacement in corrections.items():
        text = re.sub(pattern, replacement, text)
    
    return text
```

### Paso 2.2: Errores Típicos en Español/Italiano

```python
def fix_spanish_ocr_errors(text):
    """Corrige errores comunes en español."""
    
    corrections = {
        # Acentos mal interpretados
        r'o´': 'ó',
        r'a´': 'á',
        r'e´': 'é',
        
        # Confusiones 1/l, 0/O
        r'\bl\b': 'l',  # "l" aislada probablemente es "1"
        r'\bO\b(?=[0-9])': '0',
        
        # Ñ mal interpretada
        r'n˜': 'ñ',
        r'ñ': 'ñ',
    }
    
    for pattern, replacement in corrections.items():
        text = re.sub(pattern, replacement, text)
    
    return text
```

### Paso 2.3: Script de Limpieza Completo

```python
# scripts/clean_ocr_text.py (versión completa)

def full_ocr_cleanup(input_file, output_file, language='latin'):
    """Limpieza completa de texto OCR."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. Eliminar basura
    text = remove_page_numbers(text)
    text = remove_headers_footers(text)
    
    # 2. Normalizar
    text = normalize_whitespace(text)
    text = fix_hyphenation(text)
    
    # 3. Correcciones específicas del idioma
    if language == 'latin':
        text = fix_latin_ocr_errors(text)
    elif language == 'spanish':
        text = fix_spanish_ocr_errors(text)
    elif language == 'italian':
        text = fix_italian_ocr_errors(text)
    
    # 4. Guardar
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✅ Limpiado: {input_file} → {output_file}")

# Uso:
full_ocr_cleanup(
    'data/ocr/raw/caesar_la.txt',
    'data/ocr/cleaned/caesar_la.txt',
    language='latin'
)
```

---

## 3. Alineación de Textos Paralelos

### Paso 3.1: Verificar Estructura Similar

Antes de alinear, verifica que ambos textos tengan estructura similar:

```python
def analyze_text_structure(file_path):
    """Analiza la estructura de un texto."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Contar oraciones (aproximado)
    sentences = re.split(r'[.!?]+\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Contar párrafos
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    print(f"📄 {file_path}")
    print(f"   Párrafos: {len(paragraphs)}")
    print(f"   Oraciones aproximadas: {len(sentences)}")
    print(f"   Caracteres: {len(text)}")
    print()
    
    return paragraphs, sentences

# Comparar:
la_para, la_sent = analyze_text_structure('data/ocr/cleaned/caesar_la.txt')
es_para, es_sent = analyze_text_structure('data/ocr/cleaned/caesar_es.txt')

if abs(len(la_para) - len(es_para)) > 5:
    print("⚠️ ADVERTENCIA: Diferencia significativa en párrafos")
```

### Paso 3.2: Alineación Manual (Recomendado para Textos Cortos)

Para textos cortos (<100 oraciones), es más confiable alinear manualmente:

**Formato recomendado:**

```
# caesar_la_aligned.txt
Gallia est omnis divisa in partes tres.
Quarum unam incolunt Belgae.
Aliam Aquitani.

# caesar_es_aligned.txt
Toda la Galia está dividida en tres partes.
Una de ellas la habitan los belgas.
Otra los aquitanos.
```

**Reglas:**
- ✅ Una oración por línea
- ✅ Línea N del latín = Línea N de la traducción
- ✅ Líneas vacías deben coincidir

### Paso 3.3: Alineación Semi-Automática (Para Textos Largos)

```python
def align_by_paragraphs(latin_file, trans_file, output_dir):
    """Alinea textos por párrafos y los divide en oraciones."""
    
    with open(latin_file, 'r', encoding='utf-8') as f:
        latin_text = f.read()
    
    with open(trans_file, 'r', encoding='utf-8') as f:
        trans_text = f.read()
    
    # Dividir en párrafos
    latin_paragraphs = [p.strip() for p in latin_text.split('\n\n') if p.strip()]
    trans_paragraphs = [p.strip() for p in trans_text.split('\n\n') if p.strip()]
    
    if len(latin_paragraphs) != len(trans_paragraphs):
        print(f"⚠️ Advertencia: {len(latin_paragraphs)} vs {len(trans_paragraphs)} párrafos")
        print("   Revisar alineación manual")
    
    # Alinear y dividir en oraciones
    latin_sentences = []
    trans_sentences = []
    
    for lat_para, trans_para in zip(latin_paragraphs, trans_paragraphs):
        # Dividir párrafo en oraciones
        lat_sents = split_into_sentences(lat_para)
        trans_sents = split_into_sentences(trans_para)
        
        if len(lat_sents) != len(trans_sents):
            print(f"⚠️ Párrafo con {len(lat_sents)} vs {len(trans_sents)} oraciones")
            print(f"   LATÍN: {lat_para[:60]}...")
            print(f"   TRANS: {trans_para[:60]}...")
            print()
        
        # Tomar el mínimo para evitar desalineación
        min_len = min(len(lat_sents), len(trans_sents))
        latin_sentences.extend(lat_sents[:min_len])
        trans_sentences.extend(trans_sents[:min_len])
    
    # Guardar alineados
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'latin_aligned.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(latin_sentences))
    
    with open(output_dir / 'translation_aligned.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(trans_sentences))
    
    print(f"✅ Alineados {len(latin_sentences)} pares de oraciones")
```

---

## 4. Validación de Calidad

### Paso 4.1: Revisión Manual de Muestra

Siempre revisa manualmente las primeras 20-30 oraciones:

```python
def show_sample(latin_file, trans_file, lang="ES", n=20):
    """Muestra muestra para revisión manual."""
    
    with open(latin_file, 'r', encoding='utf-8') as f:
        latin = [line.strip() for line in f if line.strip()]
    
    with open(trans_file, 'r', encoding='utf-8') as f:
        trans = [line.strip() for line in f if line.strip()]
    
    print("=" * 80)
    print(f"MUESTRA PARA REVISIÓN (primeras {n} oraciones)")
    print("=" * 80)
    print()
    
    for i in range(min(n, len(latin), len(trans))):
        print(f"{i+1}.")
        print(f"  LA: {latin[i]}")
        print(f"  {lang}: {trans[i]}")
        print()
        
        # Pausa cada 5 para revisión
        if (i + 1) % 5 == 0:
            input("Presiona Enter para continuar...")

# Uso:
show_sample('data/aligned/latin_aligned.txt', 'data/aligned/spanish_aligned.txt')
```

### Paso 4.2: Validaciones Automáticas

```python
def validate_alignment(latin_file, trans_file):
    """Validaciones automáticas de calidad."""
    
    with open(latin_file, 'r', encoding='utf-8') as f:
        latin = [line.strip() for line in f if line.strip()]
    
    with open(trans_file, 'r', encoding='utf-8') as f:
        trans = [line.strip() for line in f if line.strip()]
    
    issues = []
    
    # 1. Mismo número de líneas
    if len(latin) != len(trans):
        issues.append(f"⚠️ Diferente número de líneas: {len(latin)} vs {len(trans)}")
    
    # 2. Líneas vacías
    empty_latin = [i for i, line in enumerate(latin) if not line]
    empty_trans = [i for i, line in enumerate(trans) if not line]
    
    if empty_latin:
        issues.append(f"⚠️ Líneas vacías en latín: {empty_latin}")
    if empty_trans:
        issues.append(f"⚠️ Líneas vacías en traducción: {empty_trans}")
    
    # 3. Longitud muy diferente (posible error)
    for i, (lat, trs) in enumerate(zip(latin, trans)):
        ratio = len(trs) / len(lat) if len(lat) > 0 else 0
        
        if ratio > 3 or ratio < 0.3:
            issues.append(f"⚠️ Línea {i+1}: Longitud muy diferente")
            issues.append(f"     LA: {lat[:60]}...")
            issues.append(f"     TR: {trs[:60]}...")
    
    # Reportar
    if issues:
        print("⚠️ PROBLEMAS DETECTADOS:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("✅ Validación pasada")
        return True
```

---

## 5. Formato Final

### Paso 5.1: Conversión a JSON

```python
def create_json_corpus(latin_file, trans_file, output_file, language='spanish'):
    """Crea corpus en formato JSON."""
    
    with open(latin_file, 'r', encoding='utf-8') as f:
        latin = [line.strip() for line in f if line.strip()]
    
    with open(trans_file, 'r', encoding='utf-8') as f:
        trans = [line.strip() for line in f if line.strip()]
    
    # Crear pares
    pairs = []
    for lat, trs in zip(latin, trans):
        pairs.append({
            "latin": lat,
            language: trs
        })
    
    # Guardar JSON
    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Creado: {output_file} ({len(pairs)} pares)")

# Uso:
create_json_corpus(
    'data/aligned/caesar_la.txt',
    'data/aligned/caesar_es.txt',
    'data/corpus/caesar_es.json',
    language='spanish'
)
```

---

## 6. Herramientas Útiles

### Herramienta Completa: Pipeline Automático

```bash
# scripts/ocr_to_corpus.sh

#!/bin/bash

# 1. Limpieza OCR
python scripts/clean_ocr_text.py \
    --input data/ocr/raw/caesar_la.txt \
    --output data/ocr/cleaned/caesar_la.txt \
    --language latin

python scripts/clean_ocr_text.py \
    --input data/ocr/raw/caesar_es.txt \
    --output data/ocr/cleaned/caesar_es.txt \
    --language spanish

# 2. Alineación
python scripts/align_parallel_texts.py \
    --latin data/ocr/cleaned/caesar_la.txt \
    --translation data/ocr/cleaned/caesar_es.txt \
    --output data/aligned/caesar

# 3. Validación
python scripts/validate_alignment.py \
    --latin data/aligned/caesar_la.txt \
    --translation data/aligned/caesar_es.txt

# 4. Conversión a JSON
python scripts/create_json_corpus.py \
    --latin data/aligned/caesar_la.txt \
    --translation data/aligned/caesar_es.txt \
    --output data/corpus/caesar_es.json \
    --language spanish

echo "✅ Pipeline completado"
```

### Checklist Final

Antes de usar el corpus para entrenamiento:

- [ ] ✅ Eliminé números de página y encabezados
- [ ] ✅ Corregí guiones de división silábica
- [ ] ✅ Normalicé espacios en blanco
- [ ] ✅ Corregí errores comunes de OCR
- [ ] ✅ Verifiqué que ambos textos tienen igual número de oraciones
- [ ] ✅ Revisé manualmente al menos 30 oraciones
- [ ] ✅ Pasé validaciones automáticas
- [ ] ✅ Convertí a formato JSON
- [ ] ✅ Tengo al menos 500 pares bien alineados

---

## Resumen del Workflow

```
OCR Raw Text
    ↓
[1. Limpieza] → Remove headers, fix hyphenation
    ↓
Cleaned Text
    ↓
[2. Corrección] → Fix OCR errors
    ↓
Corrected Text
    ↓
[3. Alineación] → Align sentences
    ↓
Aligned Text
    ↓
[4. Validación] → Manual + automatic checks
    ↓
Validated Text
    ↓
[5. JSON] → Create corpus
    ↓
Ready for Training! 🚀
```

Total de tiempo estimado: **2-4 horas por obra** (dependiendo del tamaño y calidad del OCR).
