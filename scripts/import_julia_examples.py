"""
Script para importar oraciones de ejemplo del libro Julia de Maud Reed
Estas son oraciones manualmente seleccionadas de los primeros capítulos
"""
from database.connection import get_session
from database.syntax_models import SentenceAnalysis, SyntaxCategory, SentenceCategoryLink
from utils.syntax_analyzer import LatinSyntaxAnalyzer

# Oraciones de ejemplo de Julia (Capítulos 1-3)
# Formato: (latin, spanish, chapter, level)
JULIA_SENTENCES = [
    # Capítulo 1 - Oraciones muy simples
    ("Rōma in Italiā est.", "Roma está en Italia.", 1, 1),
    ("Itālia in Eurōpā est.", "Italia está en Europa.", 1, 1),
    ("Graecia in Eurōpā est.", "Grecia está en Europa.", 1, 1),
    ("Īnsulae in Oceānō sunt.", "Las islas están en el océano.", 1, 1),
    ("Oppidum in īnsulā est.", "La ciudad está en la isla.", 1, 1),
    ("Sicilia īnsula est.", "Sicilia es una isla.", 1, 1),
    ("Britanniae īnsulae sunt.", "Las Bretañas son islas.", 1, 1),
    
    # Capítulo 2 - Sujeto + Verbo + Complemento
    ("Aqua in fluviīs est.", "El agua está en los ríos.", 2, 1),
    ("Silva magna est.", "El bosque es grande.", 2, 2),
    ("Puella pulchra est.", "La niña es hermosa.", 2, 2),
    ("Fēminae in viā ambulant.", "Las mujeres caminan en el camino.", 2, 2),
    ("Puer parvus est.", "El niño es pequeño.", 2, 1),
    ("Iūlia fīlia est.", "Julia es hija.", 2, 1),
    ("Mārcus fīlius est.", "Marco es hijo.", 2, 1),
    
    # Capítulo 3 - Objetos directos
    ("Iūlia rosam habet.", "Julia tiene una rosa.", 3, 2),
    ("Mārcus lībrum legit.", "Marco lee un libro.", 3, 2),
    ("Puella aquam portat.", "La niña lleva agua.", 3, 2),
    ("Fēminae puerōs vocant.", "Las mujeres llaman a los niños.", 3, 3),
    ("Agricola terram arat.", "El agricultor ara la tierra.", 3, 2),
    ("Antōnius gladium habet.", "Antonio tiene una espada.", 3, 2),
    ("Puellae rosās amant.", "Las niñas aman las rosas.", 3, 2),
    
    # Capítulo 4 - Dativos y más complejidad
    ("Iūlia mātrī rosam dat.", "Julia da una rosa a su madre.", 4, 3),
    ("Mārcus amīcō lībrum dat.", "Marco da un libro al amigo.", 4, 3),
    ("Pater fīliō pecūniam dat.", "El padre da dinero al hijo.", 4, 3),
    ("Agricola servīs cibum dat.", "El agricultor da comida a los esclavos.", 4, 3),
    
    # Capítulo 5 - Genitivos
    ("Domus Iūliae magna est.", "La casa de Julia es grande.", 5, 3),
    ("Lībri Mārcī novī sunt.", "Los libros de Marco son nuevos.", 5, 3),
    ("Fīlia agricolae pulchra est.", "La hija del agricultor es hermosa.", 5, 3),
    ("Rosa hortī rubra est.", "La rosa del jardín es roja.", 5, 3),
    
    # Capítulo 6 - Ablativos
    ("Iūlia cum mātre ambulat.", "Julia camina con su madre.", 6, 3),
    ("Mārcus in hortō lūdit.", "Marco juega en el jardín.", 6, 2),
    ("Puer gladiō pūgnat.", "El niño lucha con la espada.", 6, 3),
    ("Agricola ā silvā venit.", "El agricultor viene del bosque.", 6, 3),
]


def create_basic_categories():
    """Crea categorías sintácticas básicas"""
    categories = [
        ("Oraciones Simples", None, 1, "Oración con sujeto y verbo solamente"),
        ("Sujeto + Verbo + Complemento", None, 2, "Oración con complementos circunstanciales"),
        ("Objeto Directo", None, 2, "Oraciones con acusativo"),
        ("Objeto Indirecto", None, 3, "Oraciones con dativo"),
        ("Genitivo", None, 3, "Uso del genitivo posesivo"),
        ("Ablativo", None, 3, "Uso del ablativo (instrumento, compañía, lugar)"),
    ]
    
    with get_session() as session:
        created_cats = []
        for name, parent_id, level, desc in categories:
            # Verificar si ya existe
            existing = session.query(SyntaxCategory).filter(
                SyntaxCategory.name == name
            ).first()
            
            if not existing:
                cat = SyntaxCategory(
                    name=name,
                    parent_id=parent_id,
                    complexity_level=level,
                    description=desc
                )
                session.add(cat)
                created_cats.append(name)
        
        session.commit()
        print(f"✅ {len(created_cats)} categorías creadas")
        return created_cats


def import_julia_sentences():
    """Importa oraciones de ejemplo de Julia con análisis LatinCy"""
    print("="*60)
    print("Importando oraciones de Julia (Maud Reed)")
    print("="*60)
    
    try:
        # Crear analizador LatinCy
        print("\n📊 Inicializando LatinCy...")
        analyzer = LatinSyntaxAnalyzer()
        print("✅ LatinCy inicializado")
    except Exception as e:
        print(f"⚠️  LatinCy no disponible: {e}")
        print("Las oraciones se importarán sin análisis automático")
        analyzer = None
    
    # Crear categorías
    print("\n📁 Creando categorías sintácticas...")
    create_basic_categories()
    
    # Importar oraciones
    print(f"\n📝 Importando {len(JULIA_SENTENCES)} oraciones...")
    
    with get_session() as session:
        imported = 0
        for latin, spanish, chapter, level in JULIA_SENTENCES:
            # Verificar si ya existe
            existing = session.query(SentenceAnalysis).filter(
                SentenceAnalysis.latin_text == latin
            ).first()
            
            if existing:
                print(f"  ⏭️  Ya existe: {latin[:50]}...")
                continue
            
            if analyzer:
                # Analizar con LatinCy
                try:
                    analysis = analyzer.analyze_sentence(
                        latin_text=latin,
                        translation=spanish,
                        source=f"julia_cap{chapter}",
                        level=level,
                        lesson_number=chapter
                    )
                    session.add(analysis)
                    print(f"  ✅ Analizado: {latin[:50]}...")
                    imported += 1
                except Exception as e:
                    print(f"  ❌ Error analizando '{latin[:30]}...': {e}")
            else:
                # Sin análisis automático
                analysis = SentenceAnalysis(
                    latin_text=latin,
                    spanish_translation=spanish,
                    complexity_level=level,
                    source=f"julia_cap{chapter}",
                    lesson_number=chapter,
                    sentence_type="simple"
                )
                session.add(analysis)
                print(f"  ✅ Importado (sin análisis): {latin[:50]}...")
                imported += 1
        
        session.commit()
    
    print(f"\n{'='*60}")
    print(f"✅ IMPORTACIÓN COMPLETA")
    print(f"{'='*60}")
    print(f"Total: {imported} oraciones nuevas importadas")
    print(f"Fuente: Julia (Maud Reed) - Capítulos 1-6")


if __name__ == "__main__":
    import_julia_sentences()
