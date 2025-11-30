#!/usr/bin/env python3
"""
Script para regenerar todos los diagramas SVG de las oraciones con las nuevas traducciones

IMPORTANTE: Ejecutar desde el entorno virtual activado:
    source .venv/bin/activate  # o: . .venv/bin/activate
    python3 scripts/regenerate_syntax_svgs.py
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database.syntax_models import SentenceAnalysis
from sqlmodel import select
from utils.syntax_analyzer import LatinSyntaxAnalyzer

def regenerate_all_svgs():
    """Regenera los SVG de todas las oraciones en la base de datos"""
    
    print("🔄 Inicializando analizador sintáctico...")
    analyzer = LatinSyntaxAnalyzer("la_core_web_lg")
    
    with get_session() as session:
        # Obtener todas las oraciones
        query = select(SentenceAnalysis)
        sentences = session.exec(query).all()
        
        total = len(sentences)
        print(f"\n📊 Total de oraciones a procesar: {total}\n")
        
        updated = 0
        errors = 0
        
        for i, sentence in enumerate(sentences, 1):
            try:
                # Regenerar el SVG usando el código actualizado
                doc = analyzer.nlp(sentence.latin_text)
                new_svg = analyzer._generate_tree_diagram(doc)
                
                if new_svg:
                    sentence.tree_diagram_svg = new_svg
                    updated += 1
                    print(f"✅ [{i}/{total}] {sentence.latin_text[:50]}...")
                else:
                    print(f"⚠️  [{i}/{total}] No se pudo generar SVG para: {sentence.latin_text[:50]}")
                    errors += 1
                    
            except Exception as e:
                print(f"❌ [{i}/{total}] Error procesando '{sentence.latin_text[:50]}': {e}")
                errors += 1
        
        # Guardar cambios
        print(f"\n💾 Guardando cambios en la base de datos...")
        session.commit()
        
        print(f"\n✨ Proceso completado:")
        print(f"   - SVG actualizados: {updated}")
        print(f"   - Errores: {errors}")
        print(f"   - Total: {total}")
        
        if updated > 0:
            print(f"\n✅ Los árboles de dependencias ahora muestran términos en español con arcos rectos.")

if __name__ == "__main__":
    try:
        regenerate_all_svgs()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
