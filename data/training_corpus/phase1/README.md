# 📦 Archivos de Entrenamiento Preparados

## ✅ Lo que ya tienes

He generado los archivos de entrenamiento en:
```
data/training_corpus/phase1/
├── train.json          (916 pares)
├── validation.json     (102 pares)
└── stats.json          (estadísticas)
```

**Total: 1,018 pares latín-español**

---

## 📊 Contenido Actual

### Fuentes:
- **Vulgata**: 1,000 versículos (datos de ejemplo)
- **Classical samples**: 18 pares (Caesar, Phaedrus, Eutropius)

### Formato:
```json
[
  {
    "latin": "In principio creavit Deus caelum et terram.",
    "spanish": "En el principio creó Dios los cielos y la tierra.",
    "source": "vulgata_gen_1_1",
    "difficulty": 3
  },
  ...
]
```

---

## 🚀 Cómo Usar en Google Colab

### Opción 1: Subir Archivos Manualmente

1. Abre el notebook en Colab
2. En la sección "SECCIÓN 4: DESCARGA DE CORPUS"
3. Click en el ícono de carpeta (📁) en el panel izquierdo
4. Crea carpeta `data/`
5. Sube `train.json` y `validation.json`

### Opción 2: Subir desde Google Drive

1. Copia la carpeta `data/training_corpus/phase1/` a tu Google Drive
2. En Colab, después de montar Drive:
   ```python
   # Copiar archivos desde Drive
   !cp /content/drive/MyDrive/phase1/train.json data/
   !cp /content/drive/MyDrive/phase1/validation.json data/
   ```

### Opción 3: Usar Directamente desde Drive

En el notebook, modifica la función `load_data()`:
```python
def load_data():
    train_path = '/content/drive/MyDrive/latin_translator_phase1/train.json'
    val_path = '/content/drive/MyDrive/latin_translator_phase1/validation.json'
    # ... resto del código
```

---

## ⚠️ Importante: Calidad de los Datos

Los datos actuales son **de ejemplo** (1,000 pares repetidos).

### Para Entrenamiento Real:

Necesitas **20,000-30,000 pares únicos**. Opciones:

#### A. Descargar Vulgata Completa

1. Ve a: https://www.sacred-texts.com/bib/vul/
2. Descarga el texto completo
3. Busca traducción española (Reina-Valera, Nácar-Colunga)
4. Usa un script de alineación

#### B. Usar OPUS Corpus

1. Ve a: https://opus.nlpl.eu/
2. Busca "Latin-Spanish"
3. Descarga formato Moses o TMX
4. Convierte a JSON

#### C. Perseus Digital Library

1. Ve a: https://www.perseus.tufts.edu/hopper/
2. Descarga textos clásicos con traducciones
3. Extrae pares manualmente o con script

---

## 🎯 Recomendación

### Para Probar el Sistema (AHORA):
✅ Usa los archivos actuales (1,018 pares)
- Tiempo de entrenamiento: ~30 minutos
- BLEU esperado: ~15-20 (bajo, pero funcional para prueba)
- **Objetivo**: Verificar que todo funciona

### Para Modelo Real (DESPUÉS):
📥 Consigue corpus de 20,000-30,000 pares
- Tiempo de entrenamiento: ~8-12 horas
- BLEU esperado: ~30-35 (bueno)
- **Objetivo**: Modelo útil para producción

---

## 📝 Próximos Pasos

1. **Ahora**: Prueba el entrenamiento con datos actuales
   - Sube archivos a Colab
   - Ejecuta notebook
   - Verifica que funciona

2. **Luego**: Consigue corpus más grande
   - Descarga Vulgata completa
   - Re-ejecuta script de preparación
   - Re-entrena modelo

---

## 🆘 Si Necesitas Ayuda

- **Ver datos**: `cat data/training_corpus/phase1/train.json | head -20`
- **Contar pares**: `wc -l data/training_corpus/phase1/train.json`
- **Estadísticas**: `cat data/training_corpus/phase1/stats.json`

---

**¿Listo para entrenar?** 🚀

Los archivos están en `data/training_corpus/phase1/`. Súbelos a Colab y ejecuta el notebook.
