#!/usr/bin/env python3
"""
Script para auditar las imágenes de lecciones en Lingua Latina Viva.
Identifica imágenes referenciadas en course_view.py que no existen físicamente.
"""

import os
import re
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent
COURSE_VIEW_FILE = BASE_DIR / "pages" / "modules" / "course_view.py"

def extract_image_paths(file_path):
    """Extrae todas las rutas de imágenes del archivo course_view.py"""
    image_paths = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrón para encontrar st.image()
    pattern = r'st\.image\(["\']([^"\']+)["\']'
    matches = re.findall(pattern, content)
    
    return matches

def check_image_exists(image_path, base_dir):
    """Verifica si el archivo de imagen existe"""
    # Convertir rutas absolutas que apuntan a .gemini
    if image_path.startswith("/home/diego/.gemini"):
        return os.path.exists(image_path)
    
    # Para rutas relativas
    full_path = base_dir / image_path
    return full_path.exists()

def main():
    print("=" * 80)
    print("AUDITORÍA DE IMÁGENES - LINGUA LATINA VIVA")
    print("=" * 80)
    print()
    
    # Extraer rutas de imágenes
    image_paths = extract_image_paths(COURSE_VIEW_FILE)
    print(f"Total de referencias a imágenes encontradas: {len(image_paths)}")
    print()
    
    # Clasificar imágenes
    existing = []
    missing = []
    gemini_paths = []
    
    for img_path in image_paths:
        if img_path.startswith("/home/diego/.gemini"):
            gemini_paths.append(img_path)
            if check_image_exists(img_path, BASE_DIR):
                existing.append(img_path)
            else:
                missing.append(img_path)
        else:
            if check_image_exists(img_path, BASE_DIR):
                existing.append(img_path)
            else:
                missing.append(img_path)
    
    # Reporte de resultados
    print(f"✅ Imágenes existentes: {len(existing)}")
    print(f"❌ Imágenes faltantes: {len(missing)}")
    print(f"📁 Imágenes en directorio .gemini: {len(gemini_paths)}")
    print()
    
    if missing:
        print("=" * 80)
        print("IMÁGENES FALTANTES (por lección)")
        print("=" * 80)
        print()
        
        # Agrupar por lección
        missing_by_lesson = {}
        for img in missing:
            # Extraer número de lección
            lesson_match = re.search(r'lesson[_]?(\d+)', img, re.IGNORECASE)
            if lesson_match:
                lesson_num = int(lesson_match.group(1))
            else:
                lesson_match = re.search(r'leccion(\d+)', img, re.IGNORECASE)
                if lesson_match:
                    lesson_num = int(lesson_match.group(1))
                else:
                    lesson_num = 0  # Sin lección específica
            
            if lesson_num not in missing_by_lesson:
                missing_by_lesson[lesson_num] = []
            missing_by_lesson[lesson_num].append(img)
        
        # Imprimir por lección
        for lesson_num in sorted(missing_by_lesson.keys()):
            if lesson_num == 0:
                print("📝 Imágenes generales:")
            else:
                print(f"📖 Lección {lesson_num}:")
            for img in missing_by_lesson[lesson_num]:
                print(f"   - {img}")
            print()
    
    if gemini_paths:
        print("=" * 80)
        print("IMÁGENES EN DIRECTORIO .GEMINI (temporal)")
        print("=" * 80)
        print()
        print("⚠️  Las siguientes imágenes están en el directorio .gemini temporal.")
        print("    Se recomienda moverlas a 'static/images/curso_gramatica/'")
        print()
        for img in gemini_paths:
            exists = "✅" if check_image_exists(img, BASE_DIR) else "❌"
            print(f"{exists} {img}")
        print()
    
    # Estadísticas finales
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Total de imágenes: {len(image_paths)}")
    print(f"Existentes: {len(existing)} ({len(existing)/len(image_paths)*100:.1f}%)")
    print(f"Faltantes: {len(missing)} ({len(missing)/len(image_paths)*100:.1f}%)")
    print()
    
    if missing:
        print("💡 Próximos pasos:")
        print("   1. Revisar la lista de imágenes faltantes")
        print("   2. Generar las imágenes de alta prioridad")
        print("   3. Mover imágenes de .gemini a static/images/")
        print()

if __name__ == "__main__":
    main()
