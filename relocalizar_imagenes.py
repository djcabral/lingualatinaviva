#!/usr/bin/env python3
"""
Script para relocalizar imágenes temporales de .gemini a static/images/curso_gramatica/
y actualizar las referencias en course_view.py
"""

import os
import shutil
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).parent
DEST_DIR = BASE_DIR / "static" / "images" / "curso_gramatica"
COURSE_VIEW = BASE_DIR / "pages" / "modules" / "course_view.py"

# Mapeo de imágenes a relocalizar
IMAGES_TO_RELOCATE = [
    {
        "origen": "/home/diego/.gemini/antigravity/brain/5349b34e-2a1c-47b0-af7d-5f05fb4d17a8/roman_empire_spiral_infographic_es_1764521116498.png",
        "destino": "leccion1_imperio_espiral.png",
        "leccion": 1,
        "descripcion": "Infografía espiral del Imperio Romano"
    },
    {
        "origen": "/home/diego/.gemini/antigravity/brain/0e47d831-cf2f-4330-af23-f3ac0d1cca8e/cultura_medidas_1764512580897.png",
        "destino": "leccion10_medidas_romanas.png",
        "leccion": 10,
        "descripcion": "Sistema de medidas romanas"
    },
    {
        "origen": "/home/diego/.gemini/antigravity/brain/0e47d831-cf2f-4330-af23-f3ac0d1cca8e/cultura_tiempo_1764512610050.png",
        "destino": "leccion10_tiempo_romano.png",
        "leccion": 10,
        "descripcion": "Sistema de tiempo romano"
    },
    {
        "origen": "/home/diego/.gemini/antigravity/brain/0e47d831-cf2f-4330-af23-f3ac0d1cca8e/cultura_geografia_militar_1764512635828.png",
        "destino": "leccion13_geografia_militar.png",
        "leccion": 13,
        "descripcion": "Geografía militar romana"
    }
]

def main():
    print("=" * 80)
    print("RELOCALIZACIÓN DE IMÁGENES TEMPORALES")
    print("=" * 80)
    print()
    
    # Crear directorio de destino si no existe
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Procesar cada imagen
    relocated = []
    for img in IMAGES_TO_RELOCATE:
        origen = Path(img["origen"])
        destino = DEST_DIR / img["destino"]
        
        print(f"📸 Procesando: {img['descripcion']}")
        print(f"   Origen: {origen}")
        print(f"   Destino: {destino}")
        
        if not origen.exists():
            print(f"   ❌ ERROR: Archivo origen no existe")
            print()
            continue
        
        # Copiar archivo
        try:
            shutil.copy2(origen, destino)
            print(f"   ✅ Copiado exitosamente")
            relocated.append({
                "old_path": str(origen),
                "new_path": f"static/images/curso_gramatica/{img['destino']}",
                "leccion": img["leccion"]
            })
        except Exception as e:
            print(f"   ❌ ERROR al copiar: {e}")
        
        print()
    
    print("=" * 80)
    print(f"RESUMEN: {len(relocated)}/{len(IMAGES_TO_RELOCATE)} imágenes relocalizadas")
    print("=" * 80)
    print()
    
    if relocated:
        print("📝 SIGUIENTE PASO:")
        print("   Actualizar las siguientes rutas en course_view.py:")
        print()
        for img in relocated:
            print(f"   Buscar: {img['old_path']}")
            print(f"   Reemplazar por: {img['new_path']}")
            print()
    
    # Mostrar archivos en destino
    print("=" * 80)
    print(f"ARCHIVOS EN {DEST_DIR.name}")
    print("=" * 80)
    if DEST_DIR.exists():
        files = sorted([f.name for f in DEST_DIR.iterdir() if f.is_file()])
        print(f"Total: {len(files)} archivos")
        print()
        for f in files:
            if f in [img["destino"] for img in IMAGES_TO_RELOCATE]:
                print(f"✨ {f} (recién agregado)")
            else:
                print(f"   {f}")

if __name__ == "__main__":
    main()
