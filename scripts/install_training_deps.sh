#!/bin/bash

# Script de instalación de dependencias para entrenamiento local
# Para NVIDIA GTX 1060 con CUDA

echo "=========================================="
echo "INSTALACIÓN DE DEPENDENCIAS"
echo "=========================================="
echo ""

# Activar virtual environment
source .venv/bin/activate

echo "📦 Instalando PyTorch con soporte CUDA..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo ""
echo "📦 Instalando Transformers y dependencias..."
pip install transformers datasets sacrebleu accelerate

echo ""
echo "✅ Instalación completada"
echo ""

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA disponible: {torch.cuda.is_available()}')"

echo ""
echo "=========================================="
echo "LISTO PARA ENTRENAR"
echo "=========================================="
echo ""
echo "Para entrenar, ejecuta:"
echo "  python scripts/train_local_gpu.py"
echo ""
