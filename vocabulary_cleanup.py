"""
Script para limpiar vocabulary.csv
- Remueve índices numéricos de las palabras latinas (ej: syllaba_1242 → syllaba)
- Elimina duplicados manteniendo solo entradas únicas
- Crea backup del archivo original
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime
import re

def extract_word_and_id(latin_field):
    """
    Extrae la palabra latina limpia y el ID si existe.
    
    Ejemplos:
        'syllaba_1242' → ('syllaba', 1242)
        'puella' → ('puella', None)
    """
    match = re.match(r'^(.+?)_(\d+)$', latin_field)
    if match:
        word = match.group(1)
        word_id = int(match.group(2))
        return word, word_id
    return latin_field, None

def clean_translation(translation):
    """
    Limpia el campo translation removiendo referencias a variantes.
    
    Ejemplo: 'syllable (var. 1242)' → 'syllable'
    """
    # Remover pattern " (var. ###)"
    cleaned = re.sub(r'\s*\(var\.\s*\d+\)', '', translation)
    return cleaned.strip()

def clean_vocabulary_csv(input_path, output_path=None, create_backup=True):
    """
    Limpia el archivo vocabulary.csv.
    
    Args:
        input_path: Ruta al CSV original
        output_path: Ruta al CSV limpio (default: sobrescribe el original)
        create_backup: Si True, crea backup antes de modificar
    """
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path
    else:
        output_path = Path(output_path)
    
    # Crear backup si se solicita
    if create_backup:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = input_path.parent / f"{input_path.stem}_backup_{timestamp}{input_path.suffix}"
        shutil.copy2(input_path, backup_path)
        print(f"✓ Backup creado: {backup_path}")
    
    # Leer CSV original
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    print(f"📊 Filas originales: {len(rows)}")
    
    # Limpiar datos
    cleaned_rows = []
    seen_words = set()
    duplicates_removed = 0
    cleaned_count = 0
    
    for row in rows:
        latin_original = row['latin']
        latin_clean, word_id = extract_word_and_id(latin_original)
        
        # Si la palabra ya existe, skip (eliminar duplicado)
        if latin_clean in seen_words:
            duplicates_removed += 1
            continue
        
        seen_words.add(latin_clean)
        
        # Limpiar campos
        if latin_original != latin_clean:
            cleaned_count += 1
        
        row['latin'] = latin_clean
        row['translation'] = clean_translation(row['translation'])
        
        cleaned_rows.append(row)
    
    print(f"✓ Palabras limpias: {cleaned_count}")
    print(f"✓ Duplicados eliminados: {duplicates_removed}")
    print(f"✓ Filas finales: {len(cleaned_rows)}")
    
    # Escribir CSV limpio
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    print(f"✅ Archivo limpio guardado: {output_path}")
    
    return {
        'original_rows': len(rows),
        'final_rows': len(cleaned_rows),
        'cleaned': cleaned_count,
        'duplicates_removed': duplicates_removed
    }

if __name__ == '__main__':
    csv_path = Path(__file__).parent / 'data' / 'vocabulary.csv'
    
    print("=" * 60)
    print("🧹 Limpieza de Vocabulary CSV")
    print("=" * 60)
    
    stats = clean_vocabulary_csv(csv_path)
    
    print("\n" + "=" * 60)
    print("📈 Resumen")
    print("=" * 60)
    print(f"  Filas originales:      {stats['original_rows']}")
    print(f"  Filas finales:         {stats['final_rows']}")
    print(f"  Palabras limpiadas:    {stats['cleaned']}")
    print(f"  Duplicados removidos:  {stats['duplicates_removed']}")
    print("=" * 60)
