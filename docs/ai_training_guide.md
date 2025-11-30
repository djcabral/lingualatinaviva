# Guía Completa: Entrenamiento de IA para Traducción Latín→Español

## Índice
1. [Introducción](#introducción)
2. [Preparación de Datos](#preparación-de-datos)
3. [Configuración de Google Colab](#configuración-de-google-colab)
4. [Entrenamiento por Sesiones](#entrenamiento-por-sesiones)
5. [Integración con la Aplicación](#integración-con-la-aplicación)

---

## Introducción

### Objetivo
Entrenar un modelo de IA especializado que:
- Traduzca latín clásico a español
- Sea relativamente compacto (~500MB)
- Tenga alta calidad en textos clásicos (Caesar, Cicero, Virgilio, etc.)

### Arquitectura Elegida
**mT5-small** (Google's multilingual T5)
- **Tamaño**: ~300MB
- **Ventajas**: 
  - Pre-entrenado en 101 idiomas (incluye conocimiento de estructuras latinas)
  - Arquitectura encoder-decoder ideal para traducción
  - Fácil de afinar (fine-tune)
- **Desventajas**: 
  - Necesita corpus de entrenamiento de calidad
  - Requiere ~8-12 horas de entrenamiento en GPU

### Sistema de Checkpoints
El entrenamiento se guardará cada 500 pasos en Google Drive, permitiendo:
- Pausar y reanudar en cualquier momento
- No perder progreso si se desconecta Colab
- Evaluar modelos intermedios

---

## Preparación de Datos

### Fase 1: Recopilación de Corpus

#### Fuentes Recomendadas

**1. Vulgata (Biblia Latina)**
- **Ventaja**: Texto completo con múltiples traducciones españolas
- **Tamaño**: ~800,000 palabras
- **Descarga**: [Sacred Texts](https://sacred-texts.com/bib/vul/)

**2. Perseus Digital Library**
- **Textos**: Caesar, Cicero, Virgilio, Ovidio
- **Formato**: XML con traducciones
- **URL**: https://www.perseus.tufts.edu/hopper/

**3. Tus Datos Existentes**
- `data/texts/classical_samples_translated.json` (18 pares)
- Textos de Maud Reed (cuando los traduzcas)

#### Estructura de Datos Objetivo

```json
[
  {
    "latin": "Gallia est omnis divisa in partes tres.",
    "spanish": "Toda la Galia está dividida en tres partes.",
    "source": "caesar_bg_1_1",
    "difficulty": 3
  },
  ...
]
```

### Fase 2: Script de Preparación

Crearemos un script local para:
1. Descargar corpus
2. Limpiar y normalizar textos
3. Crear splits de entrenamiento/validación (90/10)
4. Exportar en formato compatible con Hugging Face

**Tamaño objetivo**: 20,000-50,000 pares latín-español

---

## Configuración de Google Colab

### Paso 1: Crear Notebook

1. Ve a [Google Colab](https://colab.research.google.com/)
2. Crea un nuevo notebook: `Latin_Spanish_Translator_Training.ipynb`
3. Conecta a Google Drive para persistencia

### Paso 2: Configuración Inicial

```python
# ============================================
# SECCIÓN 1: CONFIGURACIÓN Y CONEXIÓN
# ============================================
# ¿Por qué? Necesitamos acceso a Google Drive para guardar checkpoints

from google.colab import drive
drive.mount('/content/drive')

# Crear directorio de trabajo
!mkdir -p /content/drive/MyDrive/latin_translator
%cd /content/drive/MyDrive/latin_translator

print("✅ Google Drive conectado")
print("📁 Directorio de trabajo: /content/drive/MyDrive/latin_translator")
```

### Paso 3: Instalación de Dependencias

```python
# ============================================
# SECCIÓN 2: INSTALACIÓN DE LIBRERÍAS
# ============================================
# ¿Por qué cada una?
# - transformers: Framework de Hugging Face para modelos de lenguaje
# - datasets: Manejo eficiente de datos de entrenamiento
# - sentencepiece: Tokenización requerida por mT5
# - sacrebleu: Métrica de evaluación de traducción (BLEU score)

!pip install -q transformers datasets sentencepiece sacrebleu

print("✅ Dependencias instaladas")
```

### Paso 4: Verificar GPU

```python
# ============================================
# SECCIÓN 3: VERIFICACIÓN DE HARDWARE
# ============================================
# ¿Por qué? Asegurarnos de tener GPU disponible

import torch

if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"✅ GPU disponible: {gpu_name}")
    print(f"💾 Memoria GPU: {gpu_memory:.1f} GB")
else:
    print("❌ GPU no disponible. Ve a Runtime > Change runtime type > GPU")
```

---

## Entrenamiento por Sesiones

### Arquitectura del Sistema de Checkpoints

```
/content/drive/MyDrive/latin_translator/
├── data/
│   ├── train.json          # Datos de entrenamiento
│   ├── validation.json     # Datos de validación
│   └── test.json           # Datos de prueba
├── checkpoints/
│   ├── checkpoint-500/     # Guardado cada 500 pasos
│   ├── checkpoint-1000/
│   └── ...
├── final_model/            # Modelo final entrenado
└── training_log.txt        # Registro de progreso
```

### Paso 5: Cargar o Preparar Datos

```python
# ============================================
# SECCIÓN 4: CARGA DE DATOS
# ============================================
# ¿Por qué este formato?
# - JSON es fácil de editar y verificar manualmente
# - Hugging Face Datasets puede cargarlo directamente
# - Permite añadir metadatos (source, difficulty)

import json
from datasets import Dataset, DatasetDict

# Opción A: Cargar datos existentes
def load_training_data():
    """
    Carga los datos de entrenamiento desde archivos JSON.
    
    Estructura esperada:
    [
      {"latin": "...", "spanish": "..."},
      ...
    ]
    """
    with open('data/train.json', 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    
    with open('data/validation.json', 'r', encoding='utf-8') as f:
        val_data = json.load(f)
    
    # Convertir a formato Hugging Face Dataset
    train_dataset = Dataset.from_dict({
        'latin': [item['latin'] for item in train_data],
        'spanish': [item['spanish'] for item in train_data]
    })
    
    val_dataset = Dataset.from_dict({
        'latin': [item['latin'] for item in val_data],
        'spanish': [item['spanish'] for item in val_data]
    })
    
    dataset = DatasetDict({
        'train': train_dataset,
        'validation': val_dataset
    })
    
    return dataset

# Cargar datos
dataset = load_training_data()

print(f"✅ Datos cargados:")
print(f"   - Entrenamiento: {len(dataset['train'])} pares")
print(f"   - Validación: {len(dataset['validation'])} pares")
print(f"\n📝 Ejemplo:")
print(f"   Latin: {dataset['train'][0]['latin']}")
print(f"   Spanish: {dataset['train'][0]['spanish']}")
```

### Paso 6: Preparar Modelo y Tokenizer

```python
# ============================================
# SECCIÓN 5: INICIALIZACIÓN DEL MODELO
# ============================================
# ¿Por qué mT5-small?
# - Tamaño manejable (~300MB)
# - Pre-entrenado en múltiples idiomas
# - Arquitectura probada para traducción

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/mt5-small"

# Cargar tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Cargar modelo
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print(f"✅ Modelo cargado: {MODEL_NAME}")
print(f"📊 Parámetros: {model.num_parameters():,}")
```

### Paso 7: Preprocesamiento de Datos

```python
# ============================================
# SECCIÓN 6: PREPROCESAMIENTO
# ============================================
# ¿Por qué este preprocesamiento?
# - mT5 necesita prefijos de tarea ("translate Latin to Spanish: ")
# - Tokenización convierte texto a IDs numéricos
# - Padding asegura que todos los ejemplos tengan la misma longitud

def preprocess_function(examples):
    """
    Preprocesa los datos para el modelo mT5.
    
    Args:
        examples: Batch de ejemplos con 'latin' y 'spanish'
    
    Returns:
        Dict con input_ids, attention_mask, labels
    """
    # Añadir prefijo de tarea
    inputs = ["translate Latin to Spanish: " + text for text in examples['latin']]
    targets = examples['spanish']
    
    # Tokenizar inputs
    model_inputs = tokenizer(
        inputs,
        max_length=128,      # Longitud máxima de entrada
        truncation=True,     # Truncar si es muy largo
        padding='max_length' # Rellenar si es muy corto
    )
    
    # Tokenizar targets
    labels = tokenizer(
        targets,
        max_length=128,
        truncation=True,
        padding='max_length'
    )
    
    model_inputs['labels'] = labels['input_ids']
    
    return model_inputs

# Aplicar preprocesamiento
tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset['train'].column_names
)

print("✅ Datos preprocesados")
```

### Paso 8: Configurar Entrenamiento con Checkpoints

```python
# ============================================
# SECCIÓN 7: CONFIGURACIÓN DE ENTRENAMIENTO
# ============================================
# ¿Por qué estos parámetros?
# - output_dir: Dónde guardar checkpoints (en Google Drive)
# - save_steps: Guardar cada 500 pasos (cada ~30 min)
# - evaluation_strategy: Evaluar cada 500 pasos
# - learning_rate: Tasa de aprendizaje conservadora
# - num_train_epochs: 3 épocas completas (~8-12 horas)

from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    # Directorio de salida (en Google Drive para persistencia)
    output_dir="./checkpoints",
    
    # Estrategia de guardado
    save_strategy="steps",
    save_steps=500,                    # Guardar cada 500 pasos
    save_total_limit=5,                # Mantener solo últimos 5 checkpoints
    
    # Estrategia de evaluación
    evaluation_strategy="steps",
    eval_steps=500,                    # Evaluar cada 500 pasos
    
    # Hiperparámetros
    learning_rate=5e-5,                # Tasa de aprendizaje
    per_device_train_batch_size=8,    # Tamaño de batch (ajustar según GPU)
    per_device_eval_batch_size=8,
    num_train_epochs=3,                # Número de épocas
    
    # Optimizaciones
    fp16=True,                         # Precisión mixta (más rápido)
    gradient_accumulation_steps=2,     # Acumular gradientes
    
    # Logging
    logging_dir="./logs",
    logging_steps=100,
    
    # Otros
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    report_to="none"                   # No usar wandb/tensorboard
)

print("✅ Configuración de entrenamiento lista")
print(f"📊 Pasos totales estimados: {len(tokenized_dataset['train']) // 8 * 3}")
print(f"💾 Checkpoints se guardarán en: ./checkpoints")
```

### Paso 9: Función de Métricas

```python
# ============================================
# SECCIÓN 8: MÉTRICAS DE EVALUACIÓN
# ============================================
# ¿Por qué BLEU?
# - Métrica estándar para traducción automática
# - Compara traducción generada vs. referencia
# - Rango 0-100 (más alto = mejor)

import numpy as np
from datasets import load_metric

metric = load_metric("sacrebleu")

def compute_metrics(eval_preds):
    """
    Calcula métricas de evaluación (BLEU score).
    
    Args:
        eval_preds: Tupla de (predictions, labels)
    
    Returns:
        Dict con métricas
    """
    preds, labels = eval_preds
    
    # Decodificar predicciones
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    
    # Decodificar labels (reemplazar -100 con pad_token_id)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    # Calcular BLEU
    result = metric.compute(
        predictions=decoded_preds,
        references=[[label] for label in decoded_labels]
    )
    
    return {"bleu": result["score"]}

print("✅ Función de métricas configurada")
```

### Paso 10: Iniciar/Reanudar Entrenamiento

```python
# ============================================
# SECCIÓN 9: ENTRENAMIENTO
# ============================================
# ¿Cómo funciona la reanudación?
# - Si existe un checkpoint, Trainer lo carga automáticamente
# - El entrenamiento continúa desde el último paso guardado
# - No se pierde progreso entre sesiones

import os

# Verificar si hay checkpoints existentes
checkpoints = [d for d in os.listdir("./checkpoints") if d.startswith("checkpoint-")]

if checkpoints:
    # Ordenar por número de paso
    latest_checkpoint = sorted(checkpoints, key=lambda x: int(x.split("-")[1]))[-1]
    checkpoint_path = f"./checkpoints/{latest_checkpoint}"
    print(f"🔄 Reanudando desde: {checkpoint_path}")
    resume_from_checkpoint = checkpoint_path
else:
    print("🆕 Iniciando entrenamiento desde cero")
    resume_from_checkpoint = None

# Crear Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['validation'],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Iniciar entrenamiento
print("🚀 Iniciando entrenamiento...")
print("⏱️ Tiempo estimado: 8-12 horas")
print("💡 Puedes cerrar esta pestaña. El progreso se guarda en Google Drive.")

trainer.train(resume_from_checkpoint=resume_from_checkpoint)

print("✅ Entrenamiento completado!")
```

### Paso 11: Guardar Modelo Final

```python
# ============================================
# SECCIÓN 10: GUARDAR MODELO FINAL
# ============================================

# Guardar modelo final
trainer.save_model("./final_model")
tokenizer.save_pretrained("./final_model")

print("✅ Modelo final guardado en: ./final_model")
print("📦 Tamaño aproximado: ~300MB")
print("\n📥 Para usar en tu aplicación:")
print("   1. Descarga la carpeta 'final_model' de Google Drive")
print("   2. Colócala en: /home/diego/Projects/latin-python/models/")
print("   3. Carga con: AutoModelForSeq2SeqLM.from_pretrained('models/final_model')")
```

---

## Integración con la Aplicación

### Paso 12: Script de Integración Local

Crearemos un script en tu proyecto para usar el modelo entrenado:

```python
# utils/latin_translator.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class LatinTranslator:
    """
    Traductor latín→español usando modelo entrenado.
    """
    
    def __init__(self, model_path="models/final_model"):
        """
        Inicializa el traductor.
        
        Args:
            model_path: Ruta al modelo entrenado
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        
    def translate(self, latin_text: str) -> str:
        """
        Traduce texto latino a español.
        
        Args:
            latin_text: Texto en latín
            
        Returns:
            Traducción en español
        """
        # Preparar input
        input_text = f"translate Latin to Spanish: {latin_text}"
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            max_length=128,
            truncation=True
        ).to(self.device)
        
        # Generar traducción
        outputs = self.model.generate(
            **inputs,
            max_length=128,
            num_beams=4,           # Beam search para mejor calidad
            early_stopping=True
        )
        
        # Decodificar
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return translation
```

### Uso en la Aplicación

```python
# En analyze_and_import_maud_reed.py o similar

from utils.latin_translator import LatinTranslator

# Inicializar traductor
translator = LatinTranslator()

# Usar en análisis
for sentence in sentences:
    # Análisis sintáctico (LatinCy)
    analysis = analyzer.analyze_sentence(sentence)
    
    # Traducción (modelo entrenado)
    translation = translator.translate(sentence)
    analysis.spanish_translation = translation
    
    # Guardar
    session.add(analysis)
```

---

## Monitoreo del Progreso

### Durante el Entrenamiento

El entrenamiento imprimirá logs cada 100 pasos:

```
Step 100: loss=2.456, eval_loss=2.123, bleu=12.3
Step 200: loss=2.234, eval_loss=2.001, bleu=15.7
...
```

**Interpretación**:
- `loss`: Error en datos de entrenamiento (debe bajar)
- `eval_loss`: Error en datos de validación (debe bajar)
- `bleu`: Calidad de traducción (debe subir, objetivo: >30)

### Entre Sesiones

Para verificar progreso sin entrenar:

```python
# Ver último checkpoint
!ls -lh checkpoints/

# Cargar y probar modelo intermedio
from transformers import pipeline

translator = pipeline(
    "translation",
    model="./checkpoints/checkpoint-1000",
    device=0
)

test_sentence = "Gallia est omnis divisa in partes tres."
result = translator(f"translate Latin to Spanish: {test_sentence}")
print(result[0]['translation_text'])
```

---

## Próximos Pasos

1. **Preparar datos**: Crear `train.json` y `validation.json`
2. **Ejecutar notebook**: Seguir secciones 1-11
3. **Monitorear**: Revisar cada 2-3 horas
4. **Descargar modelo**: Cuando termine, descargar de Google Drive
5. **Integrar**: Usar `LatinTranslator` en tu aplicación

¿Listo para empezar? Puedo ayudarte con:
- Script para preparar datos desde tus fuentes
- Notebook de Colab completo y listo para ejecutar
- Debugging durante el entrenamiento
