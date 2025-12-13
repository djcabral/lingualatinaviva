"""
Seed lessons table with basic lesson metadata
Run with: python -m database.seed_lessons
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import create_db_and_tables, get_session
from database import Lesson
from sqlmodel import select

def seed_lessons():
    """Create all 40 lessons with basic metadata"""
    
    # Define basic lesson structure
    lessons_data = [
        # Básico (1-13)
        {"lesson_number": 1, "title": "Primeros Pasos", "level": "basico", "description": "Salutaciones y primeras palabras en latín"},
        {"lesson_number": 2, "title": "El Sistema Nominal", "level": "basico", "description": "Introducción a las declinaciones"},
        {"lesson_number": 3, "title": "Primera Declinación", "level": "basico", "description": "Sustantivos femeninos en -a"},
        {"lesson_number": 4, "title": "Segunda Declinación", "level": "basico", "description": "Sustantivos masculinos y neutros en -us, -um"},
        {"lesson_number": 5, "title": "El Verbo Sum", "level": "basico", "description": "El verbo ser/estar"},
        {"lesson_number": 6, "title": "Primera Conjugación", "level": "basico", "description": "Verbos en -āre"},
        {"lesson_number": 7, "title": "Segunda Conjugación", "level": "basico", "description": "Verbos en -ēre"},
        {"lesson_number": 8, "title": "Tercera Declinación", "level": "basico", "description": "Sustantivos consonánticos"},
        {"lesson_number": 9, "title": "Tercera Conjugación", "level": "basico", "description": "Verbos en -ĕre"},
        {"lesson_number": 10, "title": "Cuarta y Quinta Declinación", "level": "basico", "description": "Sustantivos en -us, -ū y -ēs"},
        {"lesson_number": 11, "title": "Cuarta Conjugación", "level": "basico", "description": "Verbos en -īre"},
        {"lesson_number": 12, "title": "Adjetivos de Primera Clase", "level": "basico", "description": "Adjetivos 2-1-2"},
        {"lesson_number": 13, "title": "Pronombres Personales", "level": "basico", "description": "Ego, tu, nos, vos"},
        
        # Avanzado (14-30)
        {"lesson_number": 14, "title": "El Sistema Perfectum", "level": "avanzado", "description": "Tiempos del perfecto"},
        {"lesson_number": 15, "title": "Verbos Deponentes", "level": "avanzado", "description": "Forma pasiva, significado activo"},
        {"lesson_number": 16, "title": "Participios", "level": "avanzado", "description": "Formas nominales del verbo"},
        {"lesson_number": 17, "title": "Ablativo Absoluto", "level": "avanzado", "description": "Construcción característica del latín"},
        {"lesson_number": 18, "title": "Modo Subjuntivo", "level": "avanzado", "description": "Presente e Imperfecto"},
        {"lesson_number": 19, "title": "Subjuntivo Perfecto y Pluscuamperfecto", "level": "avanzado", "description": "Consecutio Temporum"},
        {"lesson_number": 20, "title": "Infinitivos y AcI", "level": "avanzado", "description": "Acusativo con Infinitivo"},
        {"lesson_number": 21, "title": "Oraciones Finales", "level": "avanzado", "description": "Ut + subjuntivo"},
        {"lesson_number": 22, "title": "Oraciones Consecutivas", "level": "avanzado", "description": "Ut/ut non + subjuntivo"},
        {"lesson_number": 23, "title": "Oraciones Temporales", "level": "avanzado", "description": "Cum, dum, postquam"},
        {"lesson_number": 24, "title": "Oraciones Causales", "level": "avanzado", "description": "Quod, quia, cum"},
        {"lesson_number": 25, "title": "Oraciones Condicionales", "level": "avanzado", "description": "Si, nisi, ni"},
        {"lesson_number": 26, "title": "Gerundio y Gerundivo", "level": "avanzado", "description": "Formas verbales especiales"},
        {"lesson_number": 27, "title": "Supino", "level": "avanzado", "description": "Forma verbal de finalidad"},
        {"lesson_number": 28, "title": "Adjetivos de Segunda Clase", "level": "avanzado", "description": "Adjetivos de 3ª declinación"},
        {"lesson_number": 29, "title": "Comparativo y Superlativo", "level": "avanzado", "description": "Grados del adjetivo"},
        {"lesson_number": 30, "title": "Pronombres Demostrativos", "level": "avanzado", "description": "Hic, ille, iste"},
        
        # Experto (31-40)
        {"lesson_number": 31, "title": "Pronombres Relativos", "level": "experto", "description": "Qui, quae, quod"},
        {"lesson_number": 32, "title": "Oraciones de Relativo", "level": "experto", "description": "Usos especiales del relativo"},
        {"lesson_number": 33, "title": "Interrogativas", "level": "experto", "description": "Directas e indirectas"},
        {"lesson_number": 34, "title": "Estilo Indirecto", "level": "experto", "description": "Oratio obliqua"},
        {"lesson_number": 35, "title": "Perifásticas", "level": "experto", "description": "Activa y pasiva"},
        {"lesson_number": 36, "title": "Verbos Irregulares", "level": "experto", "description": "Eo, fero, volo"},
        {"lesson_number": 37, "title": "Numerales", "level": "experto", "description": "Cardinales y ordinales"},
        {"lesson_number": 38, "title": "Sintaxis Avanzada", "level": "experto", "description": "Construcciones complejas"},
        {"lesson_number": 39, "title": "Métrica Latina", "level": "experto", "description": "Hexámetro y otros metros"},
        {"lesson_number": 40, "title": "Lectura Avanzada", "level": "experto", "description": "Textos clásicos"},
    ]
    
    with get_session() as session:
        # Check if lessons already exist
        existing = session.exec(select(Lesson)).first()
        if existing:
            print("⚠️  Database already contains lessons. Skipping seed.")
            print(f"   Found {len(session.exec(select(Lesson)).all())} existing lessons.")
            return
        
        print(f"📚 Creating {len(lessons_data)} lessons...")
        count = 0
        
        for lesson_data in lessons_data:
            lesson = Lesson(
                lesson_number=lesson_data["lesson_number"],
                title=lesson_data["title"],
                level=lesson_data["level"],
                description=lesson_data.get("description"),
                content_markdown=f"## Lección {lesson_data['lesson_number']}: {lesson_data['title']}\n\nContenido pendiente.",
                is_published=True,
                order_in_level=lesson_data["lesson_number"]
            )
            session.add(lesson)
            count += 1
        
        session.commit()
        print(f"✅ Successfully created {count} lessons")

if __name__ == "__main__":
    print("🔧 Initializing database schema...")
    create_db_and_tables()
    
    print("\n📖 Seeding lessons...")
    seed_lessons()
    
    print("\n✨ Lesson seeding complete!")
