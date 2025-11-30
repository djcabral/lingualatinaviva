"""
Script para descargar e importar textos clásicos (Fedro y Eutropio)
Fuente: The Latin Library (Dominio Público)
"""
import requests
from pathlib import Path
import sys
import os

# Add project root to path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import get_session
from database.syntax_models import SentenceAnalysis
from utils.syntax_analyzer import LatinSyntaxAnalyzer
import re

# Textos a descargar
TEXTS = [
    {
        "author": "Phaedrus",
        "title": "Fabulae",
        "url": "https://www.thelatinlibrary.com/phaedrus/fab1.shtml",
        "base_level": 4,
        "source_prefix": "phaedrus_fab"
    },
    {
        "author": "Eutropius",
        "title": "Breviarium",
        "url": "https://www.thelatinlibrary.com/eutropius/eutropius1.shtml",
        "base_level": 5,
        "source_prefix": "eutropius_bk1"
    }
]

def download_text(url: str) -> str:
    """Descarga texto y limpia HTML básico"""
    print(f"📥 Descargando {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Limpieza muy básica de HTML para extraer texto
        text = response.text
        # Eliminar scripts y estilos
        text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
        # Extraer parrafos
        paragraphs = re.findall(r'<p>(.*?)</p>', text, flags=re.DOTALL)
        clean_text = "\n".join(paragraphs)
        # Eliminar tags HTML restantes
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        return clean_text
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        return ""

def clean_and_segment(text: str) -> list:
    """Segmenta en oraciones"""
    sentences = []
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text)
    # Dividir por puntuación
    raw = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', text)
    
    for s in raw:
        s = s.strip()
        if len(s) > 20 and not s.isdigit():
            sentences.append(s)
    return sentences

def import_classical():
    print("="*60)
    print("IMPORTANDO TEXTOS CLÁSICOS")
    print("="*60)
    
    try:
        analyzer = LatinSyntaxAnalyzer()
        print("✅ LatinCy inicializado")
    except:
        print("⚠️ LatinCy no disponible, importando sin análisis detallado")
        analyzer = None
        
    with get_session() as session:
        total_imported = 0
        
        for item in TEXTS:
            print(f"\nProcesando {item['author']} - {item['title']}...")
            raw_text = download_text(item['url'])
            if not raw_text:
                continue
                
            sentences = clean_and_segment(raw_text)
            print(f"  Encontradas {len(sentences)} oraciones candidatas")
            
            count = 0
            for i, sent in enumerate(sentences):
                # Limitar a 50 oraciones por texto para prueba inicial
                if count >= 50: break
                
                # Verificar duplicados
                exists = session.query(SentenceAnalysis).filter(
                    SentenceAnalysis.latin_text == sent
                ).first()
                
                if exists: continue
                
                try:
                    if analyzer:
                        analysis = analyzer.analyze_sentence(
                            latin_text=sent,
                            source=f"{item['source_prefix']}_{i+1}",
                            level=item['base_level']
                        )
                    else:
                        analysis = SentenceAnalysis(
                            latin_text=sent,
                            source=f"{item['source_prefix']}_{i+1}",
                            complexity_level=item['base_level'],
                            sentence_type="complex"
                        )
                    
                    session.add(analysis)
                    count += 1
                    total_imported += 1
                    print(f"  Importada: {sent[:40]}...", end='\r')
                    
                except Exception as e:
                    print(f"  Error: {e}")
            
            session.commit()
            print(f"\n  ✅ Importadas {count} oraciones de {item['author']}")

    print(f"\nTotal global importado: {total_imported}")

if __name__ == "__main__":
    import_classical()
