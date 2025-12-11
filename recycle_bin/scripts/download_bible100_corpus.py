"""
Script para descargar el corpus Bible-100 (latín-español)

Fuente: https://github.com/christos-c/bible-corpus
Corpus masivamente paralelo de la Biblia en 100 idiomas.
"""

import requests
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict
import re

# URLs del corpus Bible-100
LATIN_URL = "https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/Latin.xml"
SPANISH_URL = "https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/Spanish.xml"

OUTPUT_DIR = Path("data/training_corpus/phase1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def download_bible_xml(url: str, language: str) -> str:
    """
    Descarga el archivo XML de la Biblia.
    
    Args:
        url: URL del archivo XML
        language: Idioma ('Latin' o 'Spanish')
        
    Returns:
        Contenido XML como string
    """
    print(f"📥 Descargando Biblia en {language}...")
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        print(f"✅ {language} descargado ({len(response.text)} caracteres)")
        return response.text
    except Exception as e:
        print(f"❌ Error descargando {language}: {e}")
        return None

def parse_bible_xml(xml_content: str) -> Dict[str, str]:
    """
    Parsea el XML y extrae versículos.
    
    Args:
        xml_content: Contenido XML
        
    Returns:
        Diccionario {verse_id: text}
    """
    verses = {}
    
    try:
        root = ET.fromstring(xml_content)
        
        # Iterar sobre todos los versículos
        for verse in root.findall('.//seg'):
            verse_id = verse.get('id')
            text = verse.text or ''
            text = text.strip()
            
            if verse_id and text:
                verses[verse_id] = text
        
        print(f"   Versículos extraídos: {len(verses)}")
        return verses
        
    except Exception as e:
        print(f"❌ Error parseando XML: {e}")
        return {}

def clean_text(text: str) -> str:
    """
    Limpia el texto de caracteres especiales.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto limpio
    """
    # Eliminar múltiples espacios
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def align_verses(latin_verses: Dict[str, str], spanish_verses: Dict[str, str]) -> List[Dict]:
    """
    Alinea versículos latinos con españoles.
    
    Args:
        latin_verses: Diccionario de versículos en latín
        spanish_verses: Diccionario de versículos en español
        
    Returns:
        Lista de pares alineados
    """
    print("🔗 Alineando versículos...")
    
    aligned_pairs = []
    
    for verse_id in latin_verses:
        if verse_id not in spanish_verses:
            continue
        
        latin_text = clean_text(latin_verses[verse_id])
        spanish_text = clean_text(spanish_verses[verse_id])
        
        # Filtros de calidad
        if not latin_text or not spanish_text:
            continue
        
        if len(latin_text) < 10 or len(spanish_text) < 10:
            continue
        
        if len(latin_text) > 500 or len(spanish_text) > 500:
            continue
        
        aligned_pairs.append({
            'latin': latin_text,
            'spanish': spanish_text,
            'source': f'bible100_{verse_id}'
        })
    
    print(f"✅ {len(aligned_pairs)} pares alineados de Bible-100")
    return aligned_pairs

def load_classical_samples() -> List[Dict]:
    """
    Carga los classical samples existentes.
    
    Returns:
        Lista de pares clásicos
    """
    samples_path = Path("data/texts/classical_samples_translated.json")
    
    if not samples_path.exists():
        print("⚠️ classical_samples_translated.json no encontrado")
        return []
    
    with open(samples_path, 'r', encoding='utf-8') as f:
        samples = json.load(f)
    
    # Convertir al formato estándar
    formatted = []
    for sample in samples:
        formatted.append({
            'latin': sample['latin'],
            'spanish': sample['translation'],
            'source': sample['source']
        })
    
    print(f"✅ {len(formatted)} classical samples cargados")
    return formatted

def split_and_save(all_pairs: List[Dict], validation_ratio: float = 0.1):
    """
    Divide en train/val y guarda.
    
    Args:
        all_pairs: Lista de todos los pares
        validation_ratio: Porcentaje para validación
    """
    import random
    random.seed(42)
    
    shuffled = all_pairs.copy()
    random.shuffle(shuffled)
    
    split_idx = int(len(shuffled) * (1 - validation_ratio))
    train = shuffled[:split_idx]
    validation = shuffled[split_idx:]
    
    print(f"\n📊 División de datos:")
    print(f"   - Entrenamiento: {len(train)} pares ({(1-validation_ratio)*100:.0f}%)")
    print(f"   - Validación: {len(validation)} pares ({validation_ratio*100:.0f}%)")
    
    # Guardar
    train_path = OUTPUT_DIR / "train.json"
    val_path = OUTPUT_DIR / "validation.json"
    
    with open(train_path, 'w', encoding='utf-8') as f:
        json.dump(train, f, ensure_ascii=False, indent=2)
    
    with open(val_path, 'w', encoding='utf-8') as f:
        json.dump(validation, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    stats = {
        'total_pairs': len(all_pairs),
        'train_pairs': len(train),
        'validation_pairs': len(validation),
        'sources': {}
    }
    
    for item in all_pairs:
        source = item['source'].split('_')[0]
        stats['sources'][source] = stats['sources'].get(source, 0) + 1
    
    stats_path = OUTPUT_DIR / "stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Datasets guardados en: {OUTPUT_DIR}")
    print(f"   - {train_path.name}")
    print(f"   - {val_path.name}")
    print(f"   - {stats_path.name}")

def main():
    """
    Función principal.
    """
    print("=" * 60)
    print("DESCARGA DE CORPUS BIBLE-100")
    print("=" * 60)
    
    # 1. Descargar XMLs
    latin_xml = download_bible_xml(LATIN_URL, "Latin")
    spanish_xml = download_bible_xml(SPANISH_URL, "Spanish")
    
    if not latin_xml or not spanish_xml:
        print("\n❌ Error: No se pudieron descargar los archivos")
        return
    
    # 2. Parsear XMLs
    print("\n📖 Parseando archivos XML...")
    latin_verses = parse_bible_xml(latin_xml)
    spanish_verses = parse_bible_xml(spanish_xml)
    
    # 3. Alinear versículos
    bible_pairs = align_verses(latin_verses, spanish_verses)
    
    # 4. Agregar classical samples
    classical_pairs = load_classical_samples()
    
    # 5. Combinar
    all_pairs = bible_pairs + classical_pairs
    print(f"\n📦 Total de pares: {len(all_pairs)}")
    
    # 6. Dividir y guardar
    split_and_save(all_pairs)
    
    print("\n" + "=" * 60)
    print("✅ CORPUS PREPARADO")
    print("=" * 60)
    print(f"\n🚀 Próximos pasos:")
    print("   1. Verifica los archivos en data/training_corpus/phase1/")
    print("   2. Sube train.json y validation.json a Google Drive")
    print("   3. Ejecuta el notebook de entrenamiento en Colab")

if __name__ == "__main__":
    main()
