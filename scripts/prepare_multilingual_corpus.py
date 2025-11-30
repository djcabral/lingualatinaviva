"""
Script para preparar corpus multilingüe (Latín → Español/Italiano)

Este script combina textos bilingües latín-español y latín-italiano
en un formato compatible con mT5 para entrenamiento multilingüe.
"""

import json
from pathlib import Path
from typing import List, Dict

def prepare_multilingual_corpus(
    latin_spanish_pairs: List[Dict[str, str]],
    latin_italian_pairs: List[Dict[str, str]],
    output_dir: Path,
    train_split: float = 0.9
):
    """
    Prepara corpus multilingüe para entrenamiento.
    
    Args:
        latin_spanish_pairs: Lista de {"latin": "...", "spanish": "..."}
        latin_italian_pairs: Lista de {"latin": "...", "italian": "..."}
        output_dir: Directorio de salida
        train_split: Proporción para entrenamiento (0.9 = 90%)
    """
    
    all_pairs = []
    
    # Agregar pares latín-español
    for pair in latin_spanish_pairs:
        all_pairs.append({
            "latin": pair["latin"],
            "target": pair["spanish"],
            "language": "Spanish"
        })
    
    # Agregar pares latín-italiano
    for pair in latin_italian_pairs:
        all_pairs.append({
            "latin": pair["latin"],
            "target": pair["italian"],
            "language": "Italian"
        })
    
    print(f"📊 Total de pares:")
    print(f"   - Latín-Español: {len(latin_spanish_pairs)}")
    print(f"   - Latín-Italiano: {len(latin_italian_pairs)}")
    print(f"   - Total: {len(all_pairs)}")
    
    # Mezclar y dividir
    import random
    random.seed(42)
    random.shuffle(all_pairs)
    
    split_idx = int(len(all_pairs) * train_split)
    train_pairs = all_pairs[:split_idx]
    val_pairs = all_pairs[split_idx:]
    
    # Formatear para mT5
    def format_pairs(pairs):
        formatted = []
        for pair in pairs:
            formatted.append({
                "latin": pair["latin"],
                "target": pair["target"],
                "prefix": f"translate Latin to {pair['language']}: "
            })
        return formatted
    
    train_data = format_pairs(train_pairs)
    val_data = format_pairs(val_pairs)
    
    # Guardar
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "train.json", "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / "validation.json", "w", encoding="utf-8") as f:
        json.dump(val_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Corpus guardado en: {output_dir}")
    print(f"   - Entrenamiento: {len(train_data)} pares")
    print(f"   - Validación: {len(val_data)} pares")
    
    # Estadísticas por idioma
    train_es = sum(1 for p in train_pairs if p["language"] == "Spanish")
    train_it = sum(1 for p in train_pairs if p["language"] == "Italian")
    
    print(f"\n📈 Distribución en entrenamiento:")
    print(f"   - Español: {train_es} ({train_es/len(train_data)*100:.1f}%)")
    print(f"   - Italiano: {train_it} ({train_it/len(train_data)*100:.1f}%)")

# ============================================
# EJEMPLO DE USO
# ============================================

if __name__ == "__main__":
    
    # Ejemplo 1: Cargar desde archivos JSON separados
    print("=" * 60)
    print("OPCIÓN 1: Cargar desde archivos existentes")
    print("=" * 60)
    
    # Tus archivos actuales
    with open("data/training_corpus/phase1/train.json", "r", encoding="utf-8") as f:
        current_spanish = json.load(f)
    
    # Supongamos que tienes un archivo para italiano
    # Ajusta la ruta según tu estructura
    try:
        with open("data/training_corpus/latin_italian.json", "r", encoding="utf-8") as f:
            italian_pairs = json.load(f)
    except FileNotFoundError:
        print("⚠️ Archivo latin_italian.json no encontrado")
        print("Creando datos de ejemplo...")
        
        # Datos de ejemplo (reemplaza con tus textos reales)
        italian_pairs = [
            {"latin": "Alea iacta est", "italian": "Il dado è tratto"},
            {"latin": "Veni vidi vici", "italian": "Venni, vidi, vinsi"},
            {"latin": "Carpe diem", "italian": "Cogli l'attimo"},
            {"latin": "In vino veritas", "italian": "Nel vino la verità"},
        ]
    
    # Convertir formato actual a formato esperado
    spanish_pairs = [
        {"latin": item["latin"], "spanish": item["spanish"]}
        for item in current_spanish
    ]
    
    # Preparar corpus multilingüe
    prepare_multilingual_corpus(
        latin_spanish_pairs=spanish_pairs,
        latin_italian_pairs=italian_pairs,
        output_dir=Path("data/training_corpus/multilingual"),
        train_split=0.9
    )
    
    print("\n" + "=" * 60)
    print("OPCIÓN 2: Cargar desde archivos de texto paralelos")
    print("=" * 60)
    print()
    
    def load_parallel_texts(latin_file: str, target_file: str, language: str):
        """
        Carga textos paralelos de archivos separados.
        
        Formato esperado:
        - latin_file: Una frase latina por línea
        - target_file: Traducción correspondiente por línea
        """
        with open(latin_file, "r", encoding="utf-8") as f:
            latin_lines = [line.strip() for line in f if line.strip()]
        
        with open(target_file, "r", encoding="utf-8") as f:
            target_lines = [line.strip() for line in f if line.strip()]
        
        assert len(latin_lines) == len(target_lines), \
            f"Archivos desalineados: {len(latin_lines)} vs {len(target_lines)}"
        
        pairs = [
            {"latin": lat, language.lower(): tgt}
            for lat, tgt in zip(latin_lines, target_lines)
        ]
        
        print(f"✅ Cargados {len(pairs)} pares de {latin_file}")
        return pairs
    
    # Ejemplo de uso (descomenta y ajusta rutas):
    # spanish_pairs = load_parallel_texts(
    #     "data/texts/latin_corpus.txt",
    #     "data/texts/spanish_corpus.txt",
    #     "Spanish"
    # )
    # 
    # italian_pairs = load_parallel_texts(
    #     "data/texts/latin_corpus_it.txt",
    #     "data/texts/italian_corpus.txt",
    #     "Italian"
    # )
    # 
    # prepare_multilingual_corpus(
    #     latin_spanish_pairs=spanish_pairs,
    #     latin_italian_pairs=italian_pairs,
    #     output_dir=Path("data/training_corpus/multilingual")
    # )
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES")
    print("=" * 60)
    print()
    print("1. Organiza tus textos bilingües en alguno de estos formatos:")
    print()
    print("   Formato JSON:")
    print("   [{\"latin\": \"...\", \"spanish\": \"...\"}, ...]")
    print("   [{\"latin\": \"...\", \"italian\": \"...\"}, ...]")
    print()
    print("   Formato TXT (archivos paralelos):")
    print("   latin.txt  →  Una frase por línea")
    print("   spanish.txt → Traducción correspondiente")
    print("   italian.txt → Traducción correspondiente")
    print()
    print("2. Ejecuta este script con tus datos")
    print()
    print("3. Usa el corpus generado en:")
    print("   data/training_corpus/multilingual/")
    print()
    print("4. Sube a Colab y entrena normalmente")
    print("   (el notebook ya soporta el formato con prefix)")
