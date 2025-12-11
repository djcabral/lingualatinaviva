"""
Script para descargar y procesar textos de Maud Reed desde Internet Archive
"""
import os
import requests
from pathlib import Path

# URLs de Internet Archive
JULIA_URL = "https://archive.org/download/juliaalatinread00reeduoft/juliaalatinread00reeduoft.pdf"
CAMILLA_URL = "https://archive.org/download/camilla00reeduoft/camilla00reeduoft.pdf"

# Directorio de descarga
DOWNLOAD_DIR = Path("data/maud_reed")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url: str, filename: str) -> Path:
    """Descarga un archivo desde una URL"""
    filepath = DOWNLOAD_DIR / filename
    
    if filepath.exists():
        print(f"✓ {filename} ya existe, saltando descarga")
        return filepath
    
    print(f"📥 Descargando {filename}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"  Progress: {percent:.1f}%", end='\r')
    
    print(f"\n✅ {filename} descargado exitosamente")
    return filepath

def download_all():
    """Descarga todos los textos de Maud Reed"""
    print("=" * 60)
    print("Descargando textos de Maud Reed desde Internet Archive")
    print("=" * 60)
    
    julia_path = download_file(JULIA_URL, "julia.pdf")
    camilla_path = download_file(CAMILLA_URL, "camilla.pdf")
    
    print("\n" + "=" * 60)
    print("✅ Descarga completada")
    print("=" * 60)
    print(f"Julia: {julia_path}")
    print(f"Camilla: {camilla_path}")
    
    return julia_path, camilla_path

if __name__ == "__main__":
    download_all()
