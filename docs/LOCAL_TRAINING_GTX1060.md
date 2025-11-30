# 🖥️ Entrenamiento Local con GTX 1060 (6GB)

## ✅ Sí, puedes entrenar localmente

Tu NVIDIA GTX 1060 de 6GB es **suficiente** para entrenar mT5-small, con algunas optimizaciones.

---

## 📋 Requisitos Previos

### 1. Verificar CUDA

```bash
# Verificar que CUDA esté instalado
nvidia-smi

# Deberías ver algo como:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 535.xx       Driver Version: 535.xx       CUDA Version: 12.x    |
# +-----------------------------------------------------------------------------+
```

### 2. Instalar PyTorch con CUDA

```bash
# En tu virtual environment
./.venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verificar instalación
./.venv/bin/python -c "import torch; print(f'CUDA disponible: {torch.cuda.is_available()}')"
```

### 3. Instalar Dependencias de Entrenamiento

```bash
./.venv/bin/pip install transformers datasets sacrebleu accelerate
```

---

## 🚀 Entrenar (1 comando)

```bash
# Asegúrate de tener los datos preparados primero
./.venv/bin/python scripts/download_training_corpus.py

# Luego entrena
./.venv/bin/python scripts/train_local_gpu.py
```

**¡Eso es todo!** El script hace todo automáticamente.

---

## ⚙️ Optimizaciones Aplicadas

El script `train_local_gpu.py` está optimizado para 6GB VRAM:

| Parámetro | Valor | Razón |
|-----------|-------|-------|
| `batch_size` | 4 | Reducido para caber en memoria |
| `gradient_accumulation` | 4 | Simula batch_size=16 |
| `fp16` | True | Usa menos memoria (precisión mixta) |
| `gradient_checkpointing` | True | Ahorra ~30% de memoria |
| `optim` | adafactor | Optimizador más eficiente |

**Resultado**: Usa ~5.5GB de los 6GB disponibles.

---

## ⏱️ Tiempos Esperados

| Corpus | Tiempo en GTX 1060 |
|--------|-------------------|
| 1,000 pares (ejemplo) | ~2-3 horas |
| 10,000 pares | ~8-10 horas |
| 30,000 pares | ~24-30 horas |

**Comparación con Colab (T4)**:
- Colab T4: ~8-12 horas para 30,000 pares
- GTX 1060: ~24-30 horas para 30,000 pares

**Ventaja local**: No hay límite de tiempo, puedes pausar y reanudar.

---

## 🔄 Sistema de Checkpoints

El script guarda progreso cada 500 pasos:

```
models/checkpoints_local/
├── checkpoint-500/
├── checkpoint-1000/
├── checkpoint-1500/
└── ...
```

**Si se interrumpe**:
- Simplemente vuelve a ejecutar el script
- Detecta automáticamente el último checkpoint
- Continúa desde ahí

---

## 📊 Monitorear Progreso

### Durante el Entrenamiento

Verás logs en tiempo real:

```
Step 50:  loss=2.456, eval_loss=2.123
Step 100: loss=2.234, eval_loss=2.001
Step 500: loss=1.987, eval_loss=1.856, bleu=18.4
```

### Uso de GPU

En otra terminal:

```bash
# Ver uso de GPU en tiempo real
watch -n 1 nvidia-smi

# Deberías ver ~5.5GB / 6GB usados
```

---

## 🆘 Solución de Problemas

### "CUDA out of memory"

**Solución 1**: Reduce batch size

```python
# En train_local_gpu.py, línea ~150
per_device_train_batch_size=2,  # Cambiar de 4 a 2
gradient_accumulation_steps=8,   # Cambiar de 4 a 8
```

**Solución 2**: Reduce longitud máxima

```python
# En train_local_gpu.py, línea ~100
max_length=64,  # Cambiar de 128 a 64
```

**Solución 3**: Cierra otros programas

```bash
# Cerrar navegador, Streamlit, etc.
# La GPU necesita estar dedicada al entrenamiento
```

### "CUDA not available"

```bash
# Reinstalar PyTorch con CUDA
./.venv/bin/pip uninstall torch torchvision torchaudio
./.venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Entrenamiento muy lento

- ✅ Normal: GTX 1060 es ~2-3x más lenta que T4
- ⚠️ Verifica que esté usando GPU: `nvidia-smi` debe mostrar uso
- ⚠️ Si usa CPU: Verifica instalación de CUDA

---

## 💡 Consejos

### 1. Entrenar de Noche

```bash
# Iniciar entrenamiento y dejar corriendo
nohup ./.venv/bin/python scripts/train_local_gpu.py > training.log 2>&1 &

# Ver progreso
tail -f training.log

# Detener si es necesario
pkill -f train_local_gpu.py
```

### 2. Pausar y Reanudar

```bash
# Pausar: Ctrl+C
# El último checkpoint se guarda automáticamente

# Reanudar: Ejecutar de nuevo
./.venv/bin/python scripts/train_local_gpu.py
```

### 3. Comparar con Colab

**Usa local si**:
- ✅ Tienes tiempo (24-30 horas está bien)
- ✅ No quieres depender de límites de Colab
- ✅ Quieres control total

**Usa Colab si**:
- ✅ Necesitas resultados rápidos (8-12 horas)
- ✅ No tienes GPU local
- ✅ Quieres GPU más potente (T4 o A100)

---

## 📦 Después del Entrenamiento

El modelo final estará en:

```
models/latin_translator_v1.0_local/
├── config.json
├── pytorch_model.bin
├── tokenizer_config.json
└── ...
```

**Usar en tu aplicación**:

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("models/latin_translator_v1.0_local")
tokenizer = AutoTokenizer.from_pretrained("models/latin_translator_v1.0_local")

# Traducir
input_text = "translate Latin to Spanish: Gallia est omnis divisa in partes tres."
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=128, num_beams=4)
translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(translation)
```

---

## 🎯 Resumen

**Comando único**:
```bash
./.venv/bin/python scripts/train_local_gpu.py
```

**Tiempo**: ~2-3 horas (corpus actual) o ~24-30 horas (corpus completo)

**Memoria GPU**: ~5.5GB / 6GB

**Resultado**: Modelo de traducción latín→español listo para usar

---

**¿Listo para entrenar?** 🚀

Ejecuta el script y deja que tu GPU haga el trabajo.
