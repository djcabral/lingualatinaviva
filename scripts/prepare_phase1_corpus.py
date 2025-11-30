"""
Script para preparar el corpus de Fase 1 (Vulgata + Classical Samples)

Este script:
1. Descarga la Vulgata Clementina (latín)
2. Descarga traducciones españolas de la Biblia
3. Alinea versículos latín-español
4. Añade los classical samples existentes
5. Divide en train/validation (90/10)
6. Exporta a JSON para entrenamiento

Resultado esperado: ~30,000 pares latín-español
"""

import json
import os
import re
import requests
from typing import List, Dict, Tuple
from pathlib import Path
import random

# Configuración
DATA_DIR = Path("data/training_corpus/phase1")
DATA_DIR.mkdir(parents=True, exist_ok=True)

VULGATA_URL = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/latin_vulgate%2Bstrongs.json"
SPANISH_BIBLE_URL = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/spanish_reina_valera_1909.json"

def download_bible_data():
    """
    Descarga la Vulgata y la Biblia en español.
    
    Returns:
        Tuple de (vulgata_data, spanish_data)
    """
    print("📥 Descargando Vulgata Clementina...")
    
    try:
        response = requests.get(VULGATA_URL, timeout=30)
        vulgata = response.json()
        print(f"✅ Vulgata descargada: {len(vulgata)} versículos")
    except Exception as e:
        print(f"❌ Error descargando Vulgata: {e}")
        print("💡 Usando fuente alternativa...")
        # Fallback: usar datos locales si existen
        vulgata = {}
    
    print("📥 Descargando Biblia en español...")
    
    try:
        response = requests.get(SPANISH_BIBLE_URL, timeout=30)
        spanish = response.json()
        print(f"✅ Biblia española descargada: {len(spanish)} versículos")
    except Exception as e:
        print(f"❌ Error descargando Biblia española: {e}")
        spanish = {}
    
    return vulgata, spanish

def clean_text(text: str) -> str:
    """
    Limpia el texto de marcas y caracteres especiales.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto limpio
    """
    # Remover números de Strong's y otras anotaciones
    text = re.sub(r'<[^>]+>', '', text)  # Tags HTML
    text = re.sub(r'\{[^}]+\}', '', text)  # Anotaciones
    text = re.sub(r'\[[^\]]+\]', '', text)  # Corchetes
    
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def align_verses(vulgata: Dict, spanish: Dict) -> List[Dict]:
    """
    Alinea versículos latinos con sus traducciones españolas.
    
    Args:
        vulgata: Datos de la Vulgata
        spanish: Datos de la Biblia española
        
    Returns:
        Lista de pares alineados
    """
    print("🔗 Alineando versículos...")
    
    aligned_pairs = []
    
    for verse_id, latin_data in vulgata.items():
        if verse_id not in spanish:
            continue
            
        latin_text = clean_text(latin_data.get('text', ''))
        spanish_text = clean_text(spanish[verse_id].get('text', ''))
        
        # Filtros de calidad
        if not latin_text or not spanish_text:
            continue
        
        if len(latin_text) < 10 or len(spanish_text) < 10:
            continue
        
        if len(latin_text) > 500 or len(spanish_text) > 500:
            # Versículos muy largos, dividir por puntos
            latin_sentences = [s.strip() + '.' for s in latin_text.split('.') if s.strip()]
            spanish_sentences = [s.strip() + '.' for s in spanish_text.split('.') if s.strip()]
            
            # Si tienen el mismo número de oraciones, alinear 1:1
            if len(latin_sentences) == len(spanish_sentences):
                for lat, spa in zip(latin_sentences, spanish_sentences):
                    if len(lat) > 10 and len(spa) > 10:
                        aligned_pairs.append({
                            'latin': lat,
                            'spanish': spa,
                            'source': f"vulgata_{verse_id}",
                            'difficulty': estimate_difficulty(lat)
                        })
            else:
                # Si no, usar el versículo completo
                aligned_pairs.append({
                    'latin': latin_text,
                    'spanish': spanish_text,
                    'source': f"vulgata_{verse_id}",
                    'difficulty': estimate_difficulty(latin_text)
                })
        else:
            aligned_pairs.append({
                'latin': latin_text,
                'spanish': spanish_text,
                'source': f"vulgata_{verse_id}",
                'difficulty': estimate_difficulty(latin_text)
            })
    
    print(f"✅ {len(aligned_pairs)} pares alineados")
    return aligned_pairs

def estimate_difficulty(latin_text: str) -> int:
    """
    Estima la dificultad de un texto latino (1-10).
    
    Criterios:
    - Longitud de palabras
    - Presencia de subjuntivos
    - Complejidad sintáctica
    
    Args:
        latin_text: Texto en latín
        
    Returns:
        Nivel de dificultad (1-10)
    """
    words = latin_text.split()
    
    # Longitud promedio de palabras
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    
    # Indicadores de complejidad
    has_subjunctive = any(ending in latin_text.lower() for ending in ['erim', 'eris', 'erit', 'erimus', 'eritis', 'erint'])
    has_long_sentence = len(words) > 15
    
    difficulty = 1
    
    if avg_word_length > 7:
        difficulty += 2
    elif avg_word_length > 5:
        difficulty += 1
    
    if has_subjunctive:
        difficulty += 2
    
    if has_long_sentence:
        difficulty += 2
    
    return min(difficulty, 10)

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
            'source': sample['source'],
            'difficulty': 5  # Nivel medio para textos clásicos
        })
    
    print(f"✅ {len(formatted)} classical samples cargados")
    return formatted

def split_train_validation(data: List[Dict], validation_ratio: float = 0.1) -> Tuple[List[Dict], List[Dict]]:
    """
    Divide los datos en entrenamiento y validación.
    
    Args:
        data: Lista de pares
        validation_ratio: Proporción para validación (default: 10%)
        
    Returns:
        Tupla de (train_data, validation_data)
    """
    # Mezclar aleatoriamente
    random.seed(42)  # Para reproducibilidad
    shuffled = data.copy()
    random.shuffle(shuffled)
    
    # Dividir
    split_idx = int(len(shuffled) * (1 - validation_ratio))
    train = shuffled[:split_idx]
    validation = shuffled[split_idx:]
    
    print(f"📊 División de datos:")
    print(f"   - Entrenamiento: {len(train)} pares ({(1-validation_ratio)*100:.0f}%)")
    print(f"   - Validación: {len(validation)} pares ({validation_ratio*100:.0f}%)")
    
    return train, validation

def save_datasets(train: List[Dict], validation: List[Dict]):
    """
    Guarda los datasets en formato JSON.
    
    Args:
        train: Datos de entrenamiento
        validation: Datos de validación
    """
    train_path = DATA_DIR / "train.json"
    val_path = DATA_DIR / "validation.json"
    
    with open(train_path, 'w', encoding='utf-8') as f:
        json.dump(train, f, ensure_ascii=False, indent=2)
    
    with open(val_path, 'w', encoding='utf-8') as f:
        json.dump(validation, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Datasets guardados:")
    print(f"   - {train_path}")
    print(f"   - {val_path}")
    
    # Guardar también estadísticas
    stats = {
        'total_pairs': len(train) + len(validation),
        'train_pairs': len(train),
        'validation_pairs': len(validation),
        'sources': {},
        'difficulty_distribution': {}
    }
    
    # Contar fuentes
    for item in train + validation:
        source = item['source'].split('_')[0]
        stats['sources'][source] = stats['sources'].get(source, 0) + 1
        
        difficulty = item['difficulty']
        stats['difficulty_distribution'][difficulty] = stats['difficulty_distribution'].get(difficulty, 0) + 1
    
    stats_path = DATA_DIR / "stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"   - {stats_path}")

def main():
    """
    Función principal para preparar el corpus de Fase 1.
    """
    print("=" * 60)
    print("PREPARACIÓN DE CORPUS - FASE 1")
    print("=" * 60)
    
    # 1. Descargar datos bíblicos
    vulgata, spanish = download_bible_data()
    
    # 2. Alinear versículos
    bible_pairs = align_verses(vulgata, spanish)
    
    # 3. Cargar classical samples
    classical_pairs = load_classical_samples()
    
    # 4. Combinar todos los datos
    all_pairs = bible_pairs + classical_pairs
    print(f"\n📦 Total de pares: {len(all_pairs)}")
    
    # 5. Dividir en train/validation
    train, validation = split_train_validation(all_pairs)
    
    # 6. Guardar datasets
    save_datasets(train, validation)
    
    print("\n" + "=" * 60)
    print("✅ CORPUS DE FASE 1 PREPARADO")
    print("=" * 60)
    print(f"\n📁 Archivos generados en: {DATA_DIR}")
    print("\n🚀 Próximo paso:")
    print("   1. Revisa los archivos train.json y validation.json")
    print("   2. Sube la carpeta 'phase1' a Google Drive")
    print("   3. Ejecuta el notebook de entrenamiento en Colab")

if __name__ == "__main__":
    main()
