#!/usr/bin/env python3
"""
Script para redistribuir vocabulario a través de las lecciones L1-L30.

Problema actual: 84% del vocabulario está en L1
Objetivo: 15-30 palabras por lección, distribuidas según contenido gramatical

Uso:
    python scripts/redistribute_vocabulary.py --dry-run  # Simular cambios
    python scripts/redistribute_vocabulary.py --execute  # Aplicar cambios
"""

import argparse
import pandas as pd
import sys
from pathlib import Path
from typing import Dict, List
from sqlalchemy import create_engine, text
from database.connection import get_session
from database.models import Word

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))


VOCABULARY_MAPPING_CSV = "data/vocabulary_by_lesson.csv"


def load_vocabulary_mapping(csv_path: str) -> pd.DataFrame:
    """Carga el CSV con la nueva asignación de vocabulario"""
    try:
        df = pd.read_csv(csv_path)
        required_columns = ['latin', 'new_lesson', 'reason']
        
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
        
        return df
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {csv_path}")
        print("   Ejecuta primero: análisis de lecciones para generar el CSV")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer CSV: {e}")
        sys.exit(1)


def validate_distribution(df: pd.DataFrame) -> bool:
    """Valida que la distribución sea equitativa (15-30 palablas/lección)"""
    lesson_counts = df['new_lesson'].value_counts().sort_index()
    
    print("\n📊 Distribución de palabras por lección:")
    print("="*50)
    
    all_valid = True
    for lesson, count in lesson_counts.items():
        status = "✅" if 15 <= count <= 30 else "⚠️"
        print(f"  Lección {lesson:2d}: {count:3d} palabras {status}")
        
        if count < 15:
            print(f"    ⚠️  AVISO: Menos de 15 palabras")
            all_valid = False
        elif count > 30:
            print(f"    ⚠️  AVISO: Más de 30 palabras")
            all_valid = False
    
    print("="*50)
    print(f"Total: {len(df)} palabras redistribuidas")
    
    # Verificar que todas las lecciones L1-30 tengan palabras
    missing_lessons = set(range(1, 31)) - set(lesson_counts.index)
    if missing_lessons:
        print(f"\n⚠️  Lecciones sin vocabulario: {sorted(missing_lessons)}")
        all_valid = False
    
    return all_valid


def apply_redistribution(df: pd.DataFrame, dry_run: bool = True) -> None:
    """Aplica la redistribución de vocabulario en la base de datos"""
    
    if dry_run:
        print("\n🔍 MODO DRY-RUN: Simulando cambios (sin modificar DB)")
    else:
        print("\n⚡ MODO EJECUCIÓN: Aplicando cambios a la base de datos")
        response = input("¿Estás seguro de continuar? (sí/no): ")
        if response.lower() not in ['sí', 'si', 'yes']:
            print("❌ Operación cancelada")
            return
    
    with get_session() as session:
        changes_applied = 0
        words_notFound = []
        
        for _, row in df.iterrows():
            latin_word = row['latin']
            new_lesson = int(row['new_lesson'])
            reason = row['reason']
            
            # Buscar palabra en DB
            word = session.query(Word).filter(Word.latin == latin_word).first()
            
            if not word:
                words_not_found.append(latin_word)
                continue
            
            old_lesson = word.level
            
            if dry_run:
                print(f"  [{changes_applied+1:3d}] '{latin_word}' (L{old_lesson} → L{new_lesson}) - {reason}")
            else:
                word.level = new_lesson
                session.add(word)
                print(f"  ✅ [{changes_applied+1:3d}] '{latin_word}' actualizada (L{old_lesson} → L{new_lesson})")
            
            changes_applied += 1
        
        if not dry_run:
            session.commit()
            print(f"\n✅ {changes_applied} palabras redistribuidas exitosamente")
        else:
            print(f"\n🔍 {changes_applied} cambios serían aplicados")
        
        if words_not_found:
            print(f"\n⚠️  Palabras no encontradas en DB: {len(words_not_found)}")
            for word in words_not_found[:10]:
                print(f"    - {word}")
            if len(words_not_found) > 10:
                print(f"    ... y {len(words_not_found) - 10} más")


def create_backup(db_path: str = "lingua_latina.db") -> str:
    """Crea un backup de la base de datos antes de modificarla"""
    from datetime import datetime
    import shutil
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/lingua_latina_backup_{timestamp}.db"
    
    Path("backups").mkdir(exist_ok=True)
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        sys.exit(1)


def verify_current_distribution() -> None:
    """Muestra la distribución actual de vocabulario"""
    with get_session() as session:
        result = session.execute(text("""
            SELECT level, COUNT(*) as count
            FROM word
            GROUP BY level
            ORDER BY level
        """))
        
        print("\n📊 Distribución ACTUAL de vocabulario:")
        print("="*50)
        
        total = 0
        for row in result:
            level, count = row
            percentage = 0
            total += count
            print(f"  Lección {level:2d}: {count:4d} palabras ({percentage:.1f}%)")
        
        # Calculate percentages in second pass
        result = session.execute(text("""
            SELECT level, COUNT(*) as count
            FROM word
            GROUP BY level
            ORDER BY level
        """))
        
        print("\n📊 Distribución ACTUAL de vocabulario:")
        print("="*50)
        
        for row in result:
            level, count = row
            percentage = (count / total * 100) if total > 0 else 0
            print(f"  Lección {level:2d}: {count:4d} palabras ({percentage:.1f}%)")
        
        print("="*50)
        print(f"Total: {total} palabras")


def main():
    parser = argparse.ArgumentParser(
        description="Redistribuir vocabulario a través de lecciones L1-L30"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Simular cambios sin modificar la base de datos"
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help="Ejecutar redistribución (requiere confirmación)"
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help="Solo validar el CSV sin hacer cambios"
    )
    parser.add_argument(
        '--current',
        action='store_true',
        help="Mostrar distribución actual y salir"
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help="No crear backup (solo para dry-run)"
    )
    
    args = parser.parse_args()
    
    # Mostrar distribución actual
    if args.current:
        verify_current_distribution()
        return
    
    # Validar que se especificó al menos una opción
    if not (args.dry_run or args.execute or args.validate):
        print("❌ Debes especificar --dry-run, --execute, o --validate")
        parser.print_help()
        sys.exit(1)
    
    # Cargar mapping
    print(f"\n📂 Cargando mapping desde {VOCABULARY_MAPPING_CSV}...")
    df = load_vocabulary_mapping(VOCABULARY_MAPPING_CSV)
    print(f"✅ {len(df)} palabras en el mapping")
    
    # Validar distribución
    print("\n🔍 Validando distribución...")
    is_valid = validate_distribution(df)
    
    if not is_valid:
        print("\n⚠️  La distribución tiene advertencias (ver arriba)")
        if args.execute:
            response = input("¿Continuar de todas formas? (sí/no): ")
            if response.lower() not in ['sí', 'si', 'yes']:
                print("❌ Operación cancelada")
                return
    else:
        print("\n✅ Distribución válida: todas las lecciones tienen 15-30 palabras")
    
    # Si solo validar, salir
    if args.validate:
        return
    
    # Crear backup si se va a ejecutar
    if args.execute and not args.no_backup:
        create_backup()
    
    # Aplicar redistribución
    verify_current_distribution()
    apply_redistribution(df, dry_run=args.dry_run)
    
    if args.execute:
        print("\n📊 Nueva distribución:")
        verify_current_distribution()


if __name__ == "__main__":
    main()
