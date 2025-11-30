#!/usr/bin/env python3
"""
Restore Database Script
Script para restaurar la base de datos desde un respaldo.

Uso:
    python scripts/restore_database.py respaldo.db.backup
    python scripts/restore_database.py respaldo.db.backup.gz --force
    python scripts/restore_database.py --list
    python scripts/restore_database.py --preview respaldo.db.backup
"""

import os
import sys
import shutil
import sqlite3
import gzip
import json
from datetime import datetime
from pathlib import Path
import argparse

# Añadir el directorio raíz al path para imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.constants import DB_PATH, BACKUP_DIR


class DatabaseRestore:
    """Maneja operaciones de restauración de base de datos"""
    
    def __init__(self, db_path: str = None, backup_dir: str = None):
        """
        Inicializa el sistema de restauración.
        
        Args:
            db_path: Ruta a la base de datos (por defecto: lingua_latina.db)
            backup_dir: Directorio de respaldos (por defecto: backups/)
        """
        self.db_path = db_path or os.path.join(ROOT_DIR, DB_PATH)
        self.backup_dir = backup_dir or os.path.join(ROOT_DIR, BACKUP_DIR)
    
    def restore_from_backup(self, backup_path: str, confirm: bool = True, create_safety_backup: bool = True) -> bool:
        """
        Restaura la base de datos desde un archivo de respaldo.
        
        Args:
            backup_path: Ruta al archivo de respaldo
            confirm: Si True, solicita confirmación antes de restaurar
            create_safety_backup: Si True, crea un respaldo de seguridad antes de restaurar
            
        Returns:
            True si la restauración fue exitosa
            
        Raises:
            FileNotFoundError: Si el archivo de respaldo no existe
            Exception: Si hay un error durante la restauración
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Archivo de respaldo no encontrado: {backup_path}")
        
        # Mostrar información del respaldo
        self._show_backup_info(backup_path)
        
        # Solicitar confirmación
        if confirm:
            print("\n⚠️  ADVERTENCIA: Esta operación sobrescribirá la base de datos actual.")
            response = input("¿Estás seguro de que quieres continuar? (sí/no): ")
            if response.lower() not in ['sí', 'si', 'yes', 's', 'y']:
                print("❌ Restauración cancelada.")
                return False
        
        try:
            # Crear respaldo de seguridad de la DB actual
            safety_backup_path = None
            if create_safety_backup and os.path.exists(self.db_path):
                print("\n🛡️  Creando respaldo de seguridad de la base de datos actual...")
                safety_backup_path = self._create_safety_backup()
                print(f"✅ Respaldo de seguridad creado: {safety_backup_path}")
            
            # Descomprimir si es necesario
            temp_backup_path = backup_path
            is_compressed = backup_path.endswith('.gz')
            
            if is_compressed:
                print("\n📦 Descomprimiendo respaldo...")
                temp_backup_path = self._decompress_backup(backup_path)
            
            # Verificar integridad del respaldo
            print("\n🔍 Verificando integridad del respaldo...")
            if not self._verify_integrity(temp_backup_path):
                raise Exception("La verificación de integridad falló. El respaldo puede estar corrupto.")
            print("✅ Integridad verificada")
            
            # Restaurar la base de datos
            print(f"\n♻️  Restaurando base de datos...")
            print(f"   Desde: {backup_path}")
            print(f"   Hacia: {self.db_path}")
            
            # Cerrar cualquier conexión abierta (importante en Streamlit)
            # Nota: En producción, debería asegurarse que la app no esté corriendo
            
            # Copiar el archivo de respaldo sobre la DB actual
            shutil.copy2(temp_backup_path, self.db_path)
            
            # Limpiar archivo temporal si se descomprimió
            if is_compressed and temp_backup_path != backup_path:
                os.remove(temp_backup_path)
            
            # Validar la restauración
            print("\n🔍 Validando restauración...")
            if not self._validate_restore():
                raise Exception("La validación de la restauración falló")
            
            print("\n✅ ¡Base de datos restaurada exitosamente!")
            
            if safety_backup_path:
                print(f"\n💡 Respaldo de seguridad guardado en: {safety_backup_path}")
                print("   Puedes eliminarlo si todo funciona correctamente.")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante la restauración: {str(e)}")
            
            # Si hubo error y se creó un respaldo de seguridad, ofrecer restaurarlo
            if safety_backup_path and os.path.exists(safety_backup_path):
                print("\n⚠️  ¿Quieres restaurar el respaldo de seguridad?")
                response = input("(sí/no): ")
                if response.lower() in ['sí', 'si', 'yes', 's', 'y']:
                    shutil.copy2(safety_backup_path, self.db_path)
                    print("✅ Respaldo de seguridad restaurado")
            
            raise
    
    def _create_safety_backup(self) -> str:
        """
        Crea un respaldo de seguridad antes de restaurar.
        
        Returns:
            Ruta al respaldo de seguridad creado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safety_backup_filename = f"safety_backup_{timestamp}.db.backup"
        safety_backup_path = os.path.join(self.backup_dir, safety_backup_filename)
        
        # Asegurar que el directorio existe
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        
        # Copiar la DB actual
        shutil.copy2(self.db_path, safety_backup_path)
        
        return safety_backup_path
    
    def _decompress_backup(self, compressed_path: str) -> str:
        """
        Descomprime un archivo de respaldo gzip.
        
        Args:
            compressed_path: Ruta al archivo comprimido
            
        Returns:
            Ruta al archivo descomprimido
        """
        decompressed_path = compressed_path[:-3]  # Remover .gz
        
        with gzip.open(compressed_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return decompressed_path
    
    def _verify_integrity(self, backup_path: str) -> bool:
        """
        Verifica la integridad de un archivo de respaldo.
        
        Args:
            backup_path: Ruta al archivo de respaldo
            
        Returns:
            True si el respaldo es válido
        """
        try:
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            
            return result[0] == "ok"
            
        except Exception as e:
            print(f"⚠️  Error al verificar integridad: {str(e)}")
            return False
    
    def _validate_restore(self) -> bool:
        """
        Valida que la restauración fue exitosa.
        
        Returns:
            True si la validación pasa
        """
        try:
            # Intentar conectar y hacer una consulta básica
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar integridad
            cursor.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()
            
            if integrity_result[0] != "ok":
                return False
            
            # Verificar que existen tablas esperadas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            conn.close()
            
            # Debería haber al menos algunas tablas
            return len(tables) > 0
            
        except Exception as e:
            print(f"⚠️  Error en validación: {str(e)}")
            return False
    
    def preview_backup_content(self, backup_path: str):
        """
        Muestra el contenido de un respaldo antes de restaurar.
        
        Args:
            backup_path: Ruta al archivo de respaldo
        """
        if not os.path.exists(backup_path):
            print(f"❌ Archivo no encontrado: {backup_path}")
            return
        
        print(f"\n📋 Vista previa del respaldo: {os.path.basename(backup_path)}")
        print("=" * 80)
        
        # Descomprimir si es necesario
        temp_path = backup_path
        is_compressed = backup_path.endswith('.gz')
        
        if is_compressed:
            temp_path = self._decompress_backup(backup_path)
        
        try:
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            
            # Listar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()
            
            print(f"\n📊 Tablas encontradas: {len(tables)}")
            print("-" * 80)
            
            for (table_name,) in tables:
                # Contar registros en cada tabla
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                
                # Obtener esquema de la tabla
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                print(f"\n📋 {table_name}")
                print(f"   Registros: {count}")
                print(f"   Columnas: {len(columns)}")
                
                # Mostrar algunas columnas
                if columns:
                    print(f"   Estructura:")
                    for col in columns[:5]:  # Mostrar solo las primeras 5 columnas
                        print(f"      - {col[1]} ({col[2]})")
                    if len(columns) > 5:
                        print(f"      ... y {len(columns) - 5} columnas más")
            
            conn.close()
            
            # Limpiar archivo temporal
            if is_compressed and temp_path != backup_path:
                os.remove(temp_path)
            
            print("\n" + "=" * 80)
            
        except Exception as e:
            print(f"❌ Error al leer respaldo: {str(e)}")
            
            # Limpiar archivo temporal en caso de error
            if is_compressed and temp_path != backup_path and os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _show_backup_info(self, backup_path: str):
        """
        Muestra información sobre el respaldo.
        
        Args:
            backup_path: Ruta al archivo de respaldo
        """
        print(f"\n📦 Información del respaldo:")
        print("-" * 80)
        print(f"Archivo: {os.path.basename(backup_path)}")
        print(f"Ruta: {backup_path}")
        print(f"Tamaño: {os.path.getsize(backup_path) / (1024 * 1024):.2f} MB")
        print(f"Fecha de creación: {datetime.fromtimestamp(os.path.getctime(backup_path))}")
        
        # Mostrar metadata si existe
        metadata_path = f"{backup_path}.meta.json"
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            print(f"\n📄 Metadata:")
            print(f"   Fecha de respaldo: {metadata.get('backup_date', 'N/A')}")
            print(f"   Comprimido: {'Sí' if metadata.get('compressed', False) else 'No'}")
            if 'checksum' in metadata:
                print(f"   Checksum: {metadata['checksum'][:16]}...")
        
        print("-" * 80)
    
    def list_backups(self) -> list:
        """
        Lista todos los respaldos disponibles.
        
        Returns:
            Lista de rutas a archivos de respaldo
        """
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.db.backup') or filename.endswith('.db.backup.gz'):
                filepath = os.path.join(self.backup_dir, filename)
                backups.append({
                    "filename": filename,
                    "path": filepath,
                    "size_mb": os.path.getsize(filepath) / (1024 * 1024),
                    "created_at": datetime.fromtimestamp(os.path.getctime(filepath))
                })
        
        # Ordenar por fecha (más reciente primero)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        
        return backups


def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(description="Restaurar base de datos desde respaldo")
    parser.add_argument(
        "backup_file",
        nargs="?",
        help="Archivo de respaldo a restaurar"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="No solicitar confirmación"
    )
    parser.add_argument(
        "--no-safety-backup",
        action="store_true",
        help="No crear respaldo de seguridad antes de restaurar"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Listar respaldos disponibles"
    )
    parser.add_argument(
        "--preview",
        metavar="FILE",
        help="Previsualizar contenido de un respaldo"
    )
    
    args = parser.parse_args()
    
    restore_manager = DatabaseRestore()
    
    if args.list:
        # Listar respaldos
        print("📋 Respaldos disponibles:")
        print("=" * 80)
        
        backups = restore_manager.list_backups()
        
        if not backups:
            print("No hay respaldos disponibles.")
        else:
            for i, backup in enumerate(backups, 1):
                print(f"\n{i}. {backup['filename']}")
                print(f"   📅 {backup['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   📊 {backup['size_mb']:.2f} MB")
    
    elif args.preview:
        # Previsualizar respaldo
        restore_manager.preview_backup_content(args.preview)
    
    elif args.backup_file:
        # Restaurar desde respaldo
        try:
            success = restore_manager.restore_from_backup(
                args.backup_file,
                confirm=not args.force,
                create_safety_backup=not args.no_safety_backup
            )
            
            if success:
                sys.exit(0)
            else:
                sys.exit(1)
                
        except Exception as e:
            print(f"\n💥 Error: {str(e)}")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
