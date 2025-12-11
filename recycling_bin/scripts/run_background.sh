#!/bin/bash

# Directorio base
BASE_DIR="/home/diego/Projects/latin-python"
cd "$BASE_DIR"

# Archivo de log
LOG_FILE="training.log"

echo "🚀 Iniciando entrenamiento en segundo plano..."
echo "📄 Log: $LOG_FILE"
echo "🆔 PID: $$"

# Ejecutar con nohup
nohup /home/diego/Projects/latin-python/.venv/bin/python scripts/train_local_gpu.py > "$LOG_FILE" 2>&1 &

PID=$!
echo "✅ Proceso iniciado con PID: $PID"
echo "📊 Para ver el progreso: tail -f $LOG_FILE"
