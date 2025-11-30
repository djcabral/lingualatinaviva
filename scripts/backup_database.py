#!/usr/bin/env python3
"""
Backup Database Script
Script para crear respaldos de la base de datos SQLite.

Uso:
    python scripts/backup_database.py
    python scripts/backup_database.py --output-dir /ruta/a/backups
    python scripts/backup_database.py --compress
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
import hashlib

# Añadir el directorio raíz al path para imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.constants import DB_PATH, BACKUP_DIR


class DatabaseBackup:
    """Maneja operaciones de respaldo de base de datos"""
    
    def __init__(self, db_path: str = None, backup_dir: str = None):
        """
        Inicializa el sistema de respaldo.
        
        Args:
            db_path: Ruta a la base de datos (por defecto: lingua_latina.db)
            backup_dir: Directorio para guardar respaldos (por defecto: backups/)
        """
        self.db_path = db_path or os.path.join(ROOT_DIR, DB_PATH)
        self.backup_dir = backup_dir or os.path.join(ROOT_DIR, BACKUP_DIR)
        
        # Crear directorio de backups si no existe
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, compress: bool = False, include_timestamp: bool = True) -> str:
        """
        Crea un respaldo completo de la base de datos.
        
        Args:
            compress: Si True, comprime el respaldo con gzip
            include_timestamp: Si True, incluye timestamp en el nombre del archivo
            
        Returns:
            Ruta al archivo de respaldo creado
            
        Raises:
            FileNotFoundError: Si la base de datos no existe
            Exception: Si hay un error durante el respaldo
        """
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Base de datos no encontrada: {self.db_path}")
        
        # Generar nombre del archivo de respaldo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if include_timestamp else "latest"
        backup_filename = f"lingua_latina_{timestamp}.db.backup"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        print(f"📦 Creando respaldo de: {self.db_path}")
        print(f"💾 Destino: {backup_path}")
        
        try:
            # Método 1: Usar el API de SQLite para respaldo online (más seguro)
            # Esto permite hacer respaldo incluso si la DB está en uso
            self._create_online_backup(backup_path)
            
            # Verificar integridad del respaldo
            if not self.verify_backup_integrity(backup_path):
                raise Exception("La verificación de integridad del respaldo falló")
            
            # Comprimir si se solicitó
            if compress:
                print("🗜️  Comprimiendo respaldo...")
                compressed_path = self._compress_backup(backup_path)
                backup_path = compressed_path
            
            # Crear archivo de metadata
            self._create_metadata(backup_path)
            
            # Obtener tamaño del respaldo
            size_mb = os.path.getsize(backup_path) / (1024 * 1024)
            
            print(f"✅ Respaldo creado exitosamente!")
            print(f"📊 Tamaño: {size_mb:.2f} MB")
            print(f"📁 Ubicación: {backup_path}")
            
            return backup_path
            
        except Exception as e:
            print(f"❌ Error al crear respaldo: {str(e)}")
            # Limpiar archivo de respaldo parcial si existe
            if os.path.exists(backup_path):
                os.remove(backup_path)
            raise
    
    def _create_online_backup(self, backup_path: str):
        """
        Crea un respaldo usando el API online de SQLite.
        
        Args:
            backup_path: Ruta donde guardar el respaldo
        """
        # Conectar a la base de datos fuente
        source_conn = sqlite3.connect(self.db_path)
        
        # Crear/conectar a la base de datos destino
        backup_conn = sqlite3.connect(backup_path)
        
        try:
            # Realizar el respaldo
            with backup_conn:
                source_conn.backup(backup_conn, pages=100, progress=self._backup_progress)
            
            print()  # Nueva línea después del progreso
            
        finally:
            source_conn.close()
            backup_conn.close()
    
    def _backup_progress(self, status, remaining, total):
        """
        Callback para mostrar progreso del respaldo.
        
        Args:
            status: Estado actual
            remaining: Páginas restantes
            total: Total de páginas
        """
        if total > 0:
            progress = ((total - remaining) / total) * 100
            print(f"\r⏳ Progreso: {progress:.1f}% ({total - remaining}/{total} páginas)", end='')
    
    def _compress_backup(self, backup_path: str) -> str:
        """
        Comprime un archivo de respaldo con gzip.
        
        Args:
            backup_path: Ruta al archivo de respaldo
            
        Returns:
            Ruta al archivo comprimido
        """
        compressed_path = f"{backup_path}.gz"
        
        with open(backup_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Eliminar archivo sin comprimir
        os.remove(backup_path)
        
        return compressed_path
    
    def verify_backup_integrity(self, backup_path: str) -> bool:
        """
        Verifica la integridad de un archivo de respaldo.
        
        Args:
            backup_path: Ruta al archivo de respaldo
            
        Returns:
            True si el respaldo es válido, False en caso contrario
        """
        try:
            # Descomprimir temporalmente si es necesario
            temp_path = backup_path
            is_compressed = backup_path.endswith('.gz')
            
            if is_compressed:
                temp_path = backup_path[:-3]
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(temp_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            
            # Verificar integridad usando PRAGMA integrity_check
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            
            # Limpiar archivo temporal si se descomprimió
            if is_compressed and os.path.exists(temp_path):
                os.remove(temp_path)
            
            return result[0] == "ok"
            
        except Exception as e:
            print(f"⚠️  Advertencia: No se pudo verificar integridad: {str(e)}")
            return False
    
    def _create_metadata(self, backup_path: str):
        """
        Crea un archivo JSON con metadata del respaldo.
        
        Args:
            backup_path: Ruta al archivo de respaldo
        """
        metadata = {
            "backup_date": datetime.now().isoformat(),
            "original_db_path": self.db_path,
            "backup_size_bytes": os.path.getsize(backup_path),
            "compressed": backup_path.endswith('.gz'),
            "checksum": self._calculate_checksum(backup_path),
            "app_version": "1.0.0"  # Podría venir de constants
        }
        
        metadata_path = f"{backup_path}.meta.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def _calculate_checksum(self, file_path: str) -> str:
        """
        Calcula el checksum SHA256 de un archivo.
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            Checksum en formato hexadecimal
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def list_backups(self) -> list:
        """
        Lista todos los respaldos disponibles.
        
        Returns:
            Lista de diccionarios con información de cada respaldo
        """
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.db.backup') or filename.endswith('.db.backup.gz'):
                filepath = os.path.join(self.backup_dir, filename)
                metadata_path = f"{filepath}.meta.json"
                
                backup_info = {
                    "filename": filename,
                    "path": filepath,
                    "size_mb": os.path.getsize(filepath) / (1024 * 1024),
                    "created_at": datetime.fromtimestamp(os.path.getctime(filepath))
                }
                
                # Cargar metadata si existe
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        backup_info["metadata"] = json.load(f)
                
                backups.append(backup_info)
        
        # Ordenar por fecha de creación (más reciente primero)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        
        return backups


def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(description="Crear respaldo de la base de datos")
    parser.add_argument(
        "--output-dir",
        help="Directorio donde guardar el respaldo (default: backups/)",
        default=None
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Comprimir el respaldo con gzip"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Listar respaldos existentes"
    )
    
    args = parser.parse_args()
    
    backup_manager = DatabaseBackup(backup_dir=args.output_dir)
    
    if args.list:
        # Listar respaldos existentes
        print("📋 Respaldos disponibles:")
        print("-" * 80)
        
        backups = backup_manager.list_backups()
        
        if not backups:
            print("No hay respaldos disponibles.")
        else:
            for backup in backups:
                print(f"\n📦 {backup['filename']}")
                print(f"   📅 Fecha: {backup['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   📊 Tamaño: {backup['size_mb']:.2f} MB")
                if "metadata" in backup and "checksum" in backup["metadata"]:
                    print(f"   🔐 Checksum: {backup['metadata']['checksum'][:16]}...")
    else:
        # Crear nuevo respaldo
        try:
            backup_path = backup_manager.create_backup(compress=args.compress)
            print("\n✨ ¡Respaldo completado con éxito!")
            
        except Exception as e:
            print(f"\n💥 Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
