"""
Script de Entrenamiento Local para GPU NVIDIA GTX 1060 (6GB VRAM)

Este script está optimizado para entrenar mT5-small en una GPU con memoria limitada.

Optimizaciones aplicadas:
- Batch size reducido (4 en lugar de 8)
- Gradient accumulation (simula batch más grande)
- Precisión mixta (fp16) para ahorrar memoria
- Gradient checkpointing (reduce uso de memoria)
- Evaluación menos frecuente

Requisitos:
- NVIDIA GTX 1060 (6GB VRAM)
- CUDA instalado
- PyTorch con soporte CUDA
"""

import os
import json
import torch
from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    TrainingArguments,
    Trainer
)
from datasets import Dataset, DatasetDict
import evaluate
import numpy as np

# Verificar GPU
print("=" * 60)
print("VERIFICACIÓN DE HARDWARE")
print("=" * 60)

if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"✅ GPU detectada: {gpu_name}")
    print(f"💾 Memoria GPU: {gpu_memory:.1f} GB")
    
    # Limpiar caché de GPU
    torch.cuda.empty_cache()
    print("🧹 Caché de GPU limpiada")
else:
    print("❌ GPU no detectada")
    print("⚠️ El entrenamiento será MUY lento en CPU")
    response = input("¿Continuar de todos modos? (y/n): ")
    if response.lower() != 'y':
        exit()

print()

# Configuración
DATA_DIR = Path("data/training_corpus/phase1")
OUTPUT_DIR = Path("models/checkpoints_local")
FINAL_MODEL_DIR = Path("models/latin_translator_v1.0_local")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FINAL_MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "google/mt5-small"

# ============================================
# CARGAR DATOS
# ============================================

print("=" * 60)
print("CARGANDO DATOS")
print("=" * 60)

def load_data():
    """Carga datos de entrenamiento."""
    train_path = DATA_DIR / "train.json"
    val_path = DATA_DIR / "validation.json"
    
    if not train_path.exists() or not val_path.exists():
        print(f"❌ Error: No se encontraron los archivos de datos")
        print(f"   Esperado en: {DATA_DIR}")
        print(f"   Ejecuta primero: python scripts/download_training_corpus.py")
        exit()
    
    with open(train_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    
    with open(val_path, 'r', encoding='utf-8') as f:
        val_data = json.load(f)
    
    train_dataset = Dataset.from_dict({
        'latin': [item['latin'] for item in train_data],
        'spanish': [item['spanish'] for item in train_data]
    })
    
    val_dataset = Dataset.from_dict({
        'latin': [item['latin'] for item in val_data],
        'spanish': [item['spanish'] for item in val_data]
    })
    
    return DatasetDict({
        'train': train_dataset,
        'validation': val_dataset
    })

dataset = load_data()

print(f"✅ Datos cargados:")
print(f"   - Entrenamiento: {len(dataset['train'])} pares")
print(f"   - Validación: {len(dataset['validation'])} pares")
print()

# ============================================
# CARGAR MODELO
# ============================================

print("=" * 60)
print("CARGANDO MODELO")
print("=" * 60)

print(f"📥 Descargando {MODEL_NAME}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Habilitar gradient checkpointing para ahorrar memoria
model.gradient_checkpointing_enable()
model.config.use_cache = False  # Incompatible con gradient checkpointing

print(f"✅ Modelo cargado")
print(f"📊 Parámetros: {model.num_parameters():,}")
print()

# ============================================
# PREPROCESAMIENTO
# ============================================

print("=" * 60)
print("PREPROCESANDO DATOS")
print("=" * 60)

def preprocess_function(examples):
    """Preprocesa los datos para mT5."""
    inputs = ["translate Latin to Spanish: " + text for text in examples['latin']]
    targets = examples['spanish']
    
    model_inputs = tokenizer(
        inputs,
        max_length=48,
        truncation=True,
        padding='max_length'
    )
    
    labels = tokenizer(
        targets,
        max_length=48,
        truncation=True,
        padding='max_length'
    )
    
    model_inputs['labels'] = labels['input_ids']
    
    return model_inputs

tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset['train'].column_names
)

print("✅ Datos preprocesados")
print()

# ============================================
# CONFIGURACIÓN DE ENTRENAMIENTO
# ============================================

print("=" * 60)
print("CONFIGURACIÓN DE ENTRENAMIENTO")
print("=" * 60)

# Configuración optimizada para GTX 1060 (6GB)
training_args = TrainingArguments(
    # Directorios
    output_dir=str(OUTPUT_DIR),
    logging_dir=str(OUTPUT_DIR / "logs"),
    
    # Guardado de checkpoints
    save_strategy="steps",
    save_steps=500,
    save_total_limit=2,  # Solo mantener últimos 2 checkpoints
    
    # Evaluación
    eval_strategy="steps",
    eval_steps=500,
    
    # Hiperparámetros optimizados para 6GB VRAM (ajustado por OOM)
    learning_rate=5e-5,
    per_device_train_batch_size=1,      # Reducido de 2 a 1
    per_device_eval_batch_size=1,       # Reducido de 2 a 1
    gradient_accumulation_steps=16,     # Aumentado a 16 (simula batch_size=16)
    num_train_epochs=20,
    
    # Optimizaciones de memoria
    fp16=True,                           # Precisión mixta
    gradient_checkpointing=True,         # Ahorra memoria
    optim="adafactor",                   # Optimizador que usa menos memoria
    eval_accumulation_steps=1,           # Mover a CPU frecuentemente para evitar OOM
    
    # Logging
    logging_steps=50,
    
    # Otros
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    report_to="none",
    
    # Desactivar features que usan memoria extra
    dataloader_pin_memory=False,
    dataloader_num_workers=0,
)

print("✅ Configuración lista")
print(f"\n📊 Parámetros:")
print(f"   - Batch size efectivo: {training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps}")
print(f"   - Épocas: {training_args.num_train_epochs}")
print(f"   - Learning rate: {training_args.learning_rate}")
print(f"   - FP16: {training_args.fp16}")
print(f"   - Gradient checkpointing: {training_args.gradient_checkpointing}")
print()

# ============================================
# MÉTRICAS
# ============================================

metric = evaluate.load("sacrebleu")

def compute_metrics(eval_preds):
    """Calcula BLEU score."""
    preds, labels = eval_preds
    
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    result = metric.compute(
        predictions=decoded_preds,
        references=[[label] for label in decoded_labels]
    )
    
    return {"bleu": result["score"]}

# ============================================
# ENTRENAMIENTO
# ============================================

print("=" * 60)
print("INICIANDO ENTRENAMIENTO")
print("=" * 60)

# Verificar checkpoints existentes
checkpoints = [d for d in OUTPUT_DIR.iterdir() if d.is_dir() and d.name.startswith("checkpoint-")]

if checkpoints:
    latest = sorted(checkpoints, key=lambda x: int(x.name.split("-")[1]))[-1]
    print(f"🔄 Reanudando desde: {latest}")
    resume_from = str(latest)
else:
    print("🆕 Iniciando desde cero")
    resume_from = None

# Crear Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['validation'],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

print()
print("🚀 Entrenamiento iniciado...")
print(f"⏱️ Tiempo estimado: ~2-3 horas (para 1,000 pares)")
print(f"💾 Checkpoints en: {OUTPUT_DIR}")
print(f"📊 Puedes monitorear en: {OUTPUT_DIR / 'logs'}")
print()
print("=" * 60)
print()

# ENTRENAR
try:
    trainer.train(resume_from_checkpoint=resume_from)
    
    print()
    print("=" * 60)
    print("✅ ENTRENAMIENTO COMPLETADO")
    print("=" * 60)
    
except KeyboardInterrupt:
    print()
    print("=" * 60)
    print("⚠️ ENTRENAMIENTO INTERRUMPIDO")
    print("=" * 60)
    print("💾 El progreso se guardó en el último checkpoint")
    print("🔄 Puedes reanudar ejecutando este script nuevamente")
    exit()

except RuntimeError as e:
    if "out of memory" in str(e).lower():
        print()
        print("=" * 60)
        print("❌ ERROR: MEMORIA GPU INSUFICIENTE")
        print("=" * 60)
        print("💡 Soluciones:")
        print("   1. Reduce per_device_train_batch_size a 2")
        print("   2. Aumenta gradient_accumulation_steps a 8")
        print("   3. Reduce max_length de 128 a 64")
        print("   4. Cierra otros programas que usen la GPU")
        exit()
    else:
        raise

# ============================================
# GUARDAR MODELO FINAL
# ============================================

print()
print("=" * 60)
print("GUARDANDO MODELO FINAL")
print("=" * 60)

trainer.save_model(str(FINAL_MODEL_DIR))
tokenizer.save_pretrained(str(FINAL_MODEL_DIR))

print(f"✅ Modelo guardado en: {FINAL_MODEL_DIR}")
print()

# ============================================
# EVALUACIÓN FINAL
# ============================================

print("=" * 60)
print("EVALUACIÓN FINAL")
print("=" * 60)

eval_results = trainer.evaluate()

print(f"📊 Resultados:")
print(f"   - Loss: {eval_results['eval_loss']:.4f}")
print(f"   - BLEU: {eval_results['eval_bleu']:.2f}")
print()

if eval_results['eval_bleu'] > 30:
    print("🎉 ¡Excelente calidad!")
elif eval_results['eval_bleu'] > 20:
    print("✅ Buena calidad")
elif eval_results['eval_bleu'] > 10:
    print("⚠️ Calidad aceptable - considera más datos")
else:
    print("❌ Calidad baja - necesitas corpus más grande")

print()
print("=" * 60)
print("🎉 ¡ENTRENAMIENTO FINALIZADO!")
print("=" * 60)
print()
print(f"📁 Modelo final: {FINAL_MODEL_DIR}")
print()
print("🚀 Para usar el modelo:")
print(f"   from transformers import AutoModelForSeq2SeqLM, AutoTokenizer")
print(f"   model = AutoModelForSeq2SeqLM.from_pretrained('{FINAL_MODEL_DIR}')")
print(f"   tokenizer = AutoTokenizer.from_pretrained('{FINAL_MODEL_DIR}')")
print()
