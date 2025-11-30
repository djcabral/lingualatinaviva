"""
Script para procesar ediciones bilingües escaneadas.

Maneja dos casos:
1. Columnas paralelas (latín | español)
2. Párrafos alternados (latín, español, latín, español...)
"""

import os
import subprocess
from pathlib import Path
from PIL import Image
import pytesseract

def process_parallel_columns(
    input_tif: Path,
    output_dir: Path,
    split_x: int = None,  # Posición X donde dividir (mid-point si None)
    latin_lang: str = "lat",
    trans_lang: str = "spa"
):
    """
    Procesa una página con columnas paralelas.
    
    Args:
        input_tif: Archivo TIF de entrada
        output_dir: Directorio de salida
        split_x: Posición X donde dividir (None = mitad)
        latin_lang: Código de idioma para latín (lat/la)
        trans_lang: Código de idioma para traducción (spa/ita)
    """
    
    img = Image.open(input_tif)
    width, height = img.size
    
    # Calcular punto de división
    if split_x is None:
        split_x = width // 2
    
    # Columna izquierda (latín)
    left_column = img.crop((0, 0, split_x, height))
    
    # Columna derecha (traducción)
    right_column = img.crop((split_x, 0, width, height))
    
    # OCR en cada columna
    latin_text = pytesseract.image_to_string(left_column, lang=latin_lang)
    trans_text = pytesseract.image_to_string(right_column, lang=trans_lang)
    
    # Guardar
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = input_tif.stem
    
    with open(output_dir / f"{base_name}_latin.txt", 'w', encoding='utf-8') as f:
        f.write(latin_text)
    
    with open(output_dir / f"{base_name}_translation.txt", 'w', encoding='utf-8') as f:
        f.write(trans_text)
    
    print(f"✅ Procesado: {input_tif.name}")
    
    return latin_text, trans_text

def process_alternating_paragraphs(
    input_tif: Path,
    output_dir: Path,
    latin_lang: str = "lat",
    trans_lang: str = "spa"
):
    """
    Procesa una página con párrafos alternados.
    
    Primero hace OCR completo, luego separa heurísticamente.
    """
    
    img = Image.open(input_tif)
    
    # OCR completo (usa latín como idioma base)
    full_text = pytesseract.image_to_string(img, lang=latin_lang)
    
    # Separar párrafos
    paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    
    latin = []
    translation = []
    
    for i, para in enumerate(paragraphs):
        if i % 2 == 0:
            latin.append(para)
        else:
            translation.append(para)
    
    latin_text = '\n\n'.join(latin)
    trans_text = '\n\n'.join(translation)
    
    # Guardar
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = input_tif.stem
    
    with open(output_dir / f"{base_name}_latin.txt", 'w', encoding='utf-8') as f:
        f.write(latin_text)
    
    with open(output_dir / f"{base_name}_translation.txt", 'w', encoding='utf-8') as f:
        f.write(trans_text)
    
    print(f"✅ Procesado: {input_tif.name}")
    
    return latin_text, trans_text

def batch_process_bilingual(
    input_dir: Path,
    output_dir: Path,
    layout: str = "columns",  # "columns" o "alternating"
    **kwargs
):
    """
    Procesa múltiples páginas bilingües.
    
    Args:
        input_dir: Carpeta con archivos TIF
        output_dir: Carpeta de salida
        layout: "columns" para paralelas, "alternating" para alternados
    """
    
    tif_files = sorted(input_dir.glob("*.tif"))
    
    if not tif_files:
        print(f"❌ No se encontraron archivos TIF en {input_dir}")
        return
    
    print(f"📚 Encontrados {len(tif_files)} archivos TIF")
    print(f"📐 Layout: {layout}")
    print()
    
    latin_texts = []
    trans_texts = []
    
    for tif_file in tif_files:
        if layout == "columns":
            lat, trans = process_parallel_columns(tif_file, output_dir, **kwargs)
        elif layout == "alternating":
            lat, trans = process_alternating_paragraphs(tif_file, output_dir, **kwargs)
        else:
            raise ValueError(f"Layout desconocido: {layout}")
        
        latin_texts.append(lat)
        trans_texts.append(trans)
    
    # Combinar todos los textos
    combined_latin = '\n\n'.join(latin_texts)
    combined_trans = '\n\n'.join(trans_texts)
    
    with open(output_dir / "combined_latin.txt", 'w', encoding='utf-8') as f:
        f.write(combined_latin)
    
    with open(output_dir / "combined_translation.txt", 'w', encoding='utf-8') as f:
        f.write(combined_trans)
    
    print()
    print("=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print(f"Total de páginas: {len(tif_files)}")
    print(f"Archivos generados:")
    print(f"  - combined_latin.txt")
    print(f"  - combined_translation.txt")
    print()

# ============================================
# EJEMPLO DE USO
# ============================================

if __name__ == "__main__":
    
    print("=" * 60)
    print("PROCESADOR DE EDICIONES BILINGÜES")
    print("=" * 60)
    print()
    
    # OPCIÓN 1: Columnas paralelas
    print("OPCIÓN 1: Columnas paralelas (Latín | Español)")
    print("-" * 60)
    
    # batch_process_bilingual(
    #     input_dir=Path("data/scans/caesar_bilingual"),
    #     output_dir=Path("data/ocr/caesar"),
    #     layout="columns",
    #     trans_lang="spa"  # o "ita" para italiano
    # )
    
    print("Descomenta el código y ajusta las rutas")
    print()
    
    # OPCIÓN 2: Párrafos alternados
    print("OPCIÓN 2: Párrafos alternados")
    print("-" * 60)
    
    # batch_process_bilingual(
    #     input_dir=Path("data/scans/virgilio_bilingual"),
    #     output_dir=Path("data/ocr/virgilio"),
    #     layout="alternating",
    #     trans_lang="spa"
    # )
    
    print("Descomenta el código y ajusta las rutas")
    print()
    
    # OPCIÓN 3: División personalizada (columnas no centradas)
    print("OPCIÓN 3: Columnas con división personalizada")
    print("-" * 60)
    print("Si tus columnas no están exactamente al 50%:")
    print()
    
    # batch_process_bilingual(
    #     input_dir=Path("data/scans/ovidio_bilingual"),
    #     output_dir=Path("data/ocr/ovidio"),
    #     layout="columns",
    #     split_x=900,  # Dividir en píxel 900 en vez de la mitad
    #     trans_lang="ita"
    # )
    
    print("Usa split_x para especificar el punto exacto de división")
    print()
    
    print("=" * 60)
    print("📋 INSTRUCCIONES")
    print("=" * 60)
    print()
    print("1. **Prepara tus escaneos con ScanTailor:**")
    print("   - Deskew, crop, clean")
    print("   - NO dividas páginas manualmente")
    print("   - Guarda como TIF en una carpeta")
    print()
    print("2. **Identifica el layout:**")
    print("   - 'columns' si latín e italiano están lado a lado")
    print("   - 'alternating' si alternan por párrafo")
    print()
    print("3. **Ejecuta este script:**")
    print("   python scripts/process_bilingual_ocr.py")
    print()
    print("4. **Resultado:**")
    print("   data/ocr/obra/")
    print("   ├── combined_latin.txt")
    print("   └── combined_translation.txt")
    print()
    print("5. **Continúa con la guía de limpieza:**")
    print("   Sigue OCR_TO_CORPUS_GUIDE.md desde el Paso 2")
    print()
