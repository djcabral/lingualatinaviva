"""
Script para extraer y alinear frases de textos bilingües.

Útil para preparar corpus de entrenamiento a partir de ediciones bilingües
de obras clásicas (ej: latín-español, latín-italiano).
"""

import re
from pathlib import Path
from typing import List, Tuple
import json

def split_into_sentences(text: str) -> List[str]:
    """
    Divide texto en oraciones.
    
    Heurística simple: dividir por puntos, signos de exclamación, interrogación.
    Ajusta según tus textos.
    """
    # Dividir por . ! ? seguido de mayúscula o fin de línea
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Limpiar espacios
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def align_parallel_text(
    latin_text: str,
    translation_text: str,
    language: str = "Spanish"
) -> List[dict]:
    """
    Alinea texto latino con su traducción.
    
    ASUME que ambos textos tienen el mismo número de oraciones
    y están correctamente alineadas (misma oración en misma posición).
    
    Args:
        latin_text: Texto completo en latín
        translation_text: Traducción completa
        language: "Spanish" o "Italian"
    
    Returns:
        Lista de pares {"latin": "...", "spanish/italian": "..."}
    """
    
    latin_sentences = split_into_sentences(latin_text)
    trans_sentences = split_into_sentences(translation_text)
    
    # Verificar alineación
    if len(latin_sentences) != len(trans_sentences):
        print(f"⚠️ ADVERTENCIA: Desalineación detectada")
        print(f"   Latín: {len(latin_sentences)} oraciones")
        print(f"   {language}: {len(trans_sentences)} oraciones")
        print()
        
        # Usar el mínimo para evitar errores
        min_len = min(len(latin_sentences), len(trans_sentences))
        latin_sentences = latin_sentences[:min_len]
        trans_sentences = trans_sentences[:min_len]
        
        print(f"   Usando solo las primeras {min_len} oraciones alineadas")
        print()
    
    # Crear pares
    pairs = []
    lang_key = language.lower()
    
    for lat, trans in zip(latin_sentences, trans_sentences):
        pairs.append({
            "latin": lat,
            lang_key: trans
        })
    
    return pairs

def load_parallel_files(
    latin_file: Path,
    translation_file: Path,
    language: str = "Spanish"
) -> List[dict]:
    """
    Carga textos paralelos desde archivos y los alinea.
    """
    
    print(f"📖 Procesando: {latin_file.name}")
    
    with open(latin_file, 'r', encoding='utf-8') as f:
        latin_text = f.read()
    
    with open(translation_file, 'r', encoding='utf-8') as f:
        trans_text = f.read()
    
    pairs = align_parallel_text(latin_text, trans_text, language)
    
    print(f"   ✅ Extraídos: {len(pairs)} pares")
    
    return pairs

def process_multiple_works(
    works_config: List[dict],
    output_file: Path
):
    """
    Procesa múltiples obras y las combina.
    
    Args:
        works_config: Lista de configuraciones, cada una con:
            {
                "latin_file": "path/to/latin.txt",
                "translation_file": "path/to/translation.txt",
                "language": "Spanish" o "Italian"
            }
        output_file: Archivo de salida JSON
    """
    
    all_pairs = []
    
    for work in works_config:
        pairs = load_parallel_files(
            Path(work["latin_file"]),
            Path(work["translation_file"]),
            work["language"]
        )
        all_pairs.extend(pairs)
    
    # Guardar
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_pairs, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    spanish_count = sum(1 for p in all_pairs if 'spanish' in p)
    italian_count = sum(1 for p in all_pairs if 'italian' in p)
    
    print()
    print("=" * 60)
    print("✅ RESUMEN")
    print("=" * 60)
    print(f"Total de pares: {len(all_pairs)}")
    print(f"  - Latín-Español: {spanish_count}")
    print(f"  - Latín-Italiano: {italian_count}")
    print()
    print(f"Guardado en: {output_file}")
    print()

# ============================================
# EJEMPLO DE USO
# ============================================

if __name__ == "__main__":
    
    print("=" * 60)
    print("EXTRACTOR DE TEXTOS PARALELOS")
    print("=" * 60)
    print()
    
    # OPCIÓN 1: Una sola obra
    print("OPCIÓN 1: Procesar una obra bilingüe")
    print("-" * 60)
    print()
    
    # Ejemplo: De Bello Gallico (latín-español)
    # Ajusta las rutas a tus archivos reales
    
    # pairs = load_parallel_files(
    #     latin_file=Path("data/texts/caesar_gallico_la.txt"),
    #     translation_file=Path("data/texts/caesar_gallico_es.txt"),
    #     language="Spanish"
    # )
    # 
    # with open("data/corpus/caesar_es.json", "w", encoding="utf-8") as f:
    #     json.dump(pairs, f, ensure_ascii=False, indent=2)
    
    print("Descomenta el código y ajusta las rutas")
    print()
    
    # OPCIÓN 2: Múltiples obras mezcladas
    print("OPCIÓN 2: Procesar múltiples obras")
    print("-" * 60)
    print()
    
    # Configuración de ejemplo
    works_config = [
        # Obras en español
        {
            "latin_file": "data/texts/caesar_la.txt",
            "translation_file": "data/texts/caesar_es.txt",
            "language": "Spanish"
        },
        {
            "latin_file": "data/texts/virgilio_la.txt",
            "translation_file": "data/texts/virgilio_es.txt",
            "language": "Spanish"
        },
        
        # Obras en italiano
        {
            "latin_file": "data/texts/ovidio_la.txt",
            "translation_file": "data/texts/ovidio_it.txt",
            "language": "Italian"
        },
        {
            "latin_file": "data/texts/ciceron_la.txt",
            "translation_file": "data/texts/ciceron_it.txt",
            "language": "Italian"
        }
    ]
    
    # Descomentar para usar:
    # process_multiple_works(
    #     works_config=works_config,
    #     output_file=Path("data/corpus/mixed_multilingual.json")
    # )
    
    print("Configuración de ejemplo preparada")
    print()
    print("=" * 60)
    print("📋 INSTRUCCIONES")
    print("=" * 60)
    print()
    print("1. **Organiza tus textos:**")
    print()
    print("   data/texts/")
    print("   ├── obra1_latino.txt       # César en latín")
    print("   ├── obra1_español.txt      # César en español")
    print("   ├── obra2_latino.txt       # Virgilio en latín")
    print("   ├── obra2_italiano.txt     # Virgilio en italiano")
    print("   └── ...")
    print()
    print("2. **Verifica alineación:**")
    print("   - Cada archivo debe tener UNA ORACIÓN POR PÁRRAFO")
    print("   - O bien, oraciones separadas por punto+mayúscula")
    print("   - La oración 1 del latino = oración 1 de la traducción")
    print()
    print("3. **Edita la configuración en este script:**")
    print("   - Ajusta works_config con tus archivos reales")
    print("   - Especifica el idioma de cada obra")
    print()
    print("4. **Ejecuta:**")
    print("   python scripts//home/diego/Projects/latin-python/test_debug_scripts/extract_parallel_texts.py")
    print()
    print("5. **Resultado:**")
    print("   data/corpus/mixed_multilingual.json")
    print()
    print("6. **Usa con prepare_multilingual_corpus.py:**")
    print("   El JSON generado ya está listo para convertir al")
    print("   formato de entrenamiento con prefijos.")
    print()
    
    # OPCIÓN 3: Análisis de alineación
    print()
    print("OPCIÓN 3: Verificar alineación de un texto")
    print("-" * 60)
    print()
    
    def verify_alignment(latin_file: Path, trans_file: Path):
        """Muestra primeras 5 oraciones para verificar alineación."""
        
        with open(latin_file, 'r', encoding='utf-8') as f:
            latin_text = f.read()
        
        with open(trans_file, 'r', encoding='utf-8') as f:
            trans_text = f.read()
        
        latin_sentences = split_into_sentences(latin_text)
        trans_sentences = split_into_sentences(trans_text)
        
        print(f"Archivo latino: {latin_file.name}")
        print(f"Archivo traducción: {trans_file.name}")
        print()
        print(f"Total oraciones latino: {len(latin_sentences)}")
        print(f"Total oraciones traducción: {len(trans_sentences)}")
        print()
        
        if len(latin_sentences) != len(trans_sentences):
            print("⚠️ ADVERTENCIA: Números diferentes - revisar alineación")
        else:
            print("✅ Mismo número de oraciones")
        
        print()
        print("Primeras 5 oraciones:")
        print("-" * 60)
        
        for i in range(min(5, len(latin_sentences), len(trans_sentences))):
            print(f"\n{i+1}.")
            print(f"LA: {latin_sentences[i][:80]}...")
            print(f"TR: {trans_sentences[i][:80]}...")
    
    # Descomentar para verificar un texto:
    # verify_alignment(
    #     Path("data/texts/cesar_la.txt"),
    #     Path("data/texts/cesar_es.txt")
    # )
    
    print("Usa verify_alignment() para revisar tus textos")
    print()
