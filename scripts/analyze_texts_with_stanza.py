"""
Script para analizar todos los textos existentes con Stanza
Solo necesario ejecutar UNA VEZ en la máquina del administrador
"""

import sys
import os

# Add project root to path
if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

from database.connection import get_session
from database.models import Text
from sqlmodel import select
from utils.stanza_analyzer import StanzaAnalyzer, analyze_and_save_text


def main():
    """Analiza todos los textos con Stanza y guarda los resultados"""
    
    # Verificar disponibilidad de Stanza
    if not StanzaAnalyzer.is_available():
        print("❌ Stanza no está disponible")
        print(StanzaAnalyzer.install_instructions())
        print("\nPara instalar Stanza:")
        print("  pip install stanza")
        print("  python -c \"import stanza; stanza.download('la')\"")
        return
    
    print("🔬 Iniciando análisis de todos los textos con Stanza...")
    print("=" * 60)
    
    with get_session() as session:
        # Obtener todos los textos
        texts = session.exec(select(Text)).all()
        
        print(f"📚 Textos encontrados: {len(texts)}")
        print()
        
        total_analyzed = 0
        total_saved = 0
        errors = []
        
        for i, text in enumerate(texts, 1):
            print(f"\n[{i}/{len(texts)}] Analizando: {text.title}")
            print(f"  Autor: {text.author_id if text.author_id else 'Desconocido'}")
            print(f"  Longitud: {len(text.content)} caracteres")
            
            try:
                analyzed, saved = analyze_and_save_text(
                    text.id,
                    text.content,
                    session
                )
                
                total_analyzed += analyzed
                total_saved += saved
                
                print(f"  ✅ {analyzed} palabras analizadas, {saved} guardadas")
                
            except Exception as e:
                error_msg = f"Error en '{text.title}': {str(e)}"
                errors.append(error_msg)
                print(f"  ❌ {error_msg}")
                continue
        
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL")
        print("=" * 60)
        print(f"Textos procesados: {len(texts)}")
        print(f"Palabras analizadas: {total_analyzed}")
        print(f"Análisis guardados: {total_saved}")
        
        if errors:
            print(f"\n⚠️  Errores encontrados: {len(errors)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print("\n✅ Todos los textos analizados exitosamente!")
        
        print("\n💾 Análisis guardados en base de datos")
        print("Los usuarios ahora pueden ver análisis mejorados en Lectio")


if __name__ == "__main__":
    main()
