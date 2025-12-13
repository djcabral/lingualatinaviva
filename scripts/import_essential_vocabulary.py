#!/usr/bin/env python3
"""
Script SIMPLIFICADO para importar vocabulario esencial y pool general.

Enfoque pragmático:
1. Importar vocabulario esencial (CSV manual) → asignado a lecciones específicas
2. Importar pool general de 1500 palabras frecuentes → nivel 0 (general practice)

El vocabulariio esencial se usa en ejercicios estáticos.
El pool general se usa en práctica de SRS/flashcards.

Uso:
    # Importar esencial
    python scripts/import_essential_vocabulary.py --essential data/essential_vocabulary_l1_l5.csv
    
    # Importar pool general (DCC Core 1000)
    python scripts/import_essential_vocabulary.py --general data/dcc_core_1000.csv
"""

import argparse
import csv
import sys
import sqlite3
from pathlib import Path
from typing import List, Dict


def import_essential_vocabulary(csv_path: str, dry_run: bool = False):
    """
    Importa vocabulario esencial desde CSV y lo asigna a lecciones.
    
    CSV format: latin,lesson,pos,translation,reason
    """
    print(f"\n📂 Importando vocabulario esencial desde {csv_path}...")
    
    words_to_import = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words_to_import.append({
                'latin': row['latin'].strip(),
                'lesson': int(row['lesson']),
                'pos': row['pos'].strip(),
                'translation': row['translation'].strip(),
                'reason': row.get('reason', '').strip()
            })
    
    print(f"✅ {len(words_to_import)} palabras en el CSV")
    
    if dry_run:
        print("\n🔍 MODO DRY-RUN: Mostrando primeras 10 palabras...")
        for word in words_to_import[:10]:
            print(f"  L{word['lesson']:2d}: {word['latin']:15s} ({word['pos']}) = {word['translation']}")
        return
    
    # Importar a base de datos
    db_path = Path(__file__).parent.parent / "lingua_latina.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    imported = 0
    updated = 0
    
    for word_data in words_to_import:
        # Buscar si ya existe
        cursor.execute(
            "SELECT id FROM word WHERE latin = ?",
            (word_data['latin'],)
        )
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar nivel/lección
            cursor.execute("""
                UPDATE word 
                SET level = ?, translation = ?, part_of_speech = ?
                WHERE latin = ?
            """, (
                word_data['lesson'],
                word_data['translation'],
                word_data['pos'],
                word_data['latin']
            ))
            updated += 1
            print(f"  ✓ Actualizada: {word_data['latin']} → L{word_data['lesson']}")
        else:
            # Crear nueva
            cursor.execute("""
                INSERT INTO word (
                    latin, translation, part_of_speech, level,
                    is_plurale_tantum, is_singulare_tantum,
                    is_invariable, is_fundamental, status
                )
                VALUES (?, ?, ?, ?, 0, 0, 0, 1, 'active')
            """, (
                word_data['latin'],
                word_data['translation'],
                word_data['pos'],
                word_data['lesson']
            ))
            imported += 1
            print(f"  + Nueva: {word_data['latin']} → L{word_data['lesson']}")
    
    conn.commit()
    conn.close()
    print(f"\n✅ Importadas: {imported} | Actualizadas: {updated}")


def import_general_pool(csv_path: str, dry_run: bool = False):
    """
    Importa pool general de vocabulario frecuente (nivel 0).
    Estas palabras no están asignadas a una lección específica, son para práctica general.
    
    CSV format: latin,english,pos,frequency_rank
    """
    print(f"\n📂 Importando pool general desde {csv_path}...")
    
    words_to_import = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words_to_import.append({
                'latin': row.get('latin', row.get('Latin', '')).strip(),
                'translation': row.get('english', row.get('English', '')).strip(),
                'pos': row.get('pos', row.get('POS', 'noun')).strip(),
                'frequency_rank': int(row.get('frequency_rank', row.get('Rank', 999)))
            })
    
    print(f"✅ {len(words_to_import)} palabras en el pool")
    
    if dry_run:
        print("\n🔍 MODO DRY-RUN: Mostrando primeras 10 palabras...")
        for word in words_to_import[:10]:
            print(f"  #{word['frequency_rank']:4d}: {word['latin']:15s} = {word['translation']}")
        return
    
    # Importar a base de datos
    db_path = Path(__file__).parent.parent / "lingua_latina.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    for word_data in words_to_import:
        # Buscar si ya existe
        cursor.execute(
            "SELECT id, level FROM word WHERE latin = ?",
            (word_data['latin'],)
        )
        existing = cursor.fetchone()
        
        if existing:
            # Si ya está asignada a una lección, no la sobreescribir
            skipped += 1
            continue
        else:
            # Crear nueva en pool general (level=0)
            is_fundamental = 1 if word_data['frequency_rank'] <= 100 else 0
            cursor.execute("""
                INSERT INTO word (
                    latin, translation, part_of_speech, level,
                    frequency_rank_global, is_fundamental,
                    is_plurale_tantum, is_singulare_tantum,
                    is_invariable, status
                )
                VALUES (?, ?, ?, 0, ?, ?, 0, 0, 0, 'active')
            """, (
                word_data['latin'],
                word_data['translation'],
                word_data['pos'],
                word_data['frequency_rank'],
                is_fundamental
            ))
            imported += 1
            
            if imported % 100 == 0:
                print(f"  Importadas: {imported}...")
    
    conn.commit()
    conn.close()
    print(f"\n✅ Importadas al pool: {imported} | Ya existían: {skipped}")


def main():
    parser = argparse.ArgumentParser(
        description="Importar vocabulario esencial y pool general"
    )
    parser.add_argument('--essential', help="CSV con vocabulario esencial por lección")
    parser.add_argument('--general', help="CSV con pool general de frecuencia")
    parser.add_argument('--dry-run', action='store_true', help="Simular sin modificar DB")
    
    args = parser.parse_args()
    
    if not args.essential and not args.general:
        print("❌ Debes especificar --essential o --general (o ambos)")
        parser.print_help()
        sys.exit(1)
    
    if args.essential:
        import_essential_vocabulary(args.essential, dry_run=args.dry_run)
    
    if args.general:
        import_general_pool(args.general, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
