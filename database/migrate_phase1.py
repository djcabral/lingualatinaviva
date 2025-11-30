"""
Script de migración - Fase 1: Base de Datos Mejorada

Este script:
1. Crea autores iniciales
2. Marca palabras invariables
3. Asigna ranking de frecuencia a palabras existentes
4. Marca palabras fundamentales
"""

from database.connection import get_session
from database import Author, Word, WordFrequency
from sqlmodel import select

# Datos de autores iniciales
AUTHORS_DATA = [
    {
        "name": "Caesar",
        "full_name": "Gaius Julius Caesar",
        "difficulty_level": 1,
        "period": "Republican",
        "description": "General y estadista romano. Prosa militar clara y directa. Ideal para principiantes."
    },
    {
        "name": "Nepos",
        "full_name": "Cornelius Nepos",
        "difficulty_level": 1,
        "period": "Republican",
        "description": "Biógrafo romano. Estilo simple y narrativo."
    },
    {
        "name": "Cicero",
        "full_name": "Marcus Tullius Cicero",
        "difficulty_level": 2,
        "period": "Republican",
        "description": "Máximo orador romano. Prosa elegante pero compleja."
    },
    {
        "name": "Ovid",
        "full_name": "Publius Ovidius Naso",
        "difficulty_level": 2,
        "period": "Imperial",
        "description": "Poeta de las Metamorfosis. Narrativa poética accesible."
    },
    {
        "name": "Virgil",
        "full_name": "Publius Vergilius Maro",
        "difficulty_level": 3,
        "period": "Imperial",
        "description": "Autor de la Eneida. Poesía épica de alto nivel."
    },
    {
        "name": "Livy",
        "full_name": "Titus Livius",
        "difficulty_level": 3,
        "period": "Imperial",
        "description": "Historiador romano. Prosa narrativa elaborada."
    },
    {
        "name": "Horace",
        "full_name": "Quintus Horatius Flaccus",
        "difficulty_level": 4,
        "period": "Imperial",
        "description": "Poeta lírico. Estilo denso y alusivo."
    },
    {
        "name": "Tacitus",
        "full_name": "Publius Cornelius Tacitus",
        "difficulty_level": 4,
        "period": "Imperial",
        "description": "Historiador. Prosa concisa y compleja."
    },
]

# Top 100 palabras más frecuentes del latín clásico
# Basado en Dickinson College Core Vocabulary y análisis de corpus
TOP_100_WORDS = [
    # Conjunciones y partículas (extremadamente frecuentes)
    "et", "que", "sed", "aut", "nam", "enim", "atque", "ac", "non", "ne",
    # Preposiciones
    "in", "ad", "ab", "ex", "de", "cum", "per", "pro", "sine", "super",
    # Pronombres y adjetivos demostrativos
    "qui", "quae", "quod", "hic", "haec", "hoc", "ille", "illa", "illud",
    "is", "ea", "id", "ipse", "ipsa", "ipsum",
    # Verbos más frecuentes
    "sum", "facio", "dico", "video", "habeo", "venio", "do", "possum",
    "fero", "capio", "peto", "volo", "pono", "teneo", "mitto", "ago",
    # Sustantivos comunes
    "homo", "res", "dies", "manus", "tempus", "locus", "pars", "corpus",
    "bellum", "rex", "civis", "urbs", "animus", "mors", "vita", "nomen",
    # Adjetivos frecuentes
    "magnus", "multus", "bonus", "malus", "parvus", "primus", "summus",
    "totus", "omnis", "alius", "alter", "tantus", "quantus",
    # Adverbios frecuentes
    "iam", "nunc", "tunc", "semper", "numquam", "saepe", "bene", "male",
    "sic", "ita", "tam", "quam", "etiam", "tamen", "autem"
]

# Palabras invariables que deben marcarse
PREPOSITIONS = [
    "ab", "a", "abs", "ad", "ante", "apud", "circa", "citra", "contra",
    "cum", "de", "ex", "e", "erga", "extra", "in", "infra", "inter",
    "intra", "iuxta", "ob", "per", "post", "praeter", "prope", "propter",
    "pro", "secundum", "sine", "sub", "super", "supra", "trans", "ultra"
]

ADVERBS = [
    "iam", "nunc", "tunc", "mox", "statim", "semper", "numquam", "saepe",
    "raro", "olim", "modo", "diu", "bene", "male", "non", "ne", "haud",
    "vix", "paene", "sic", "ita", "tam", "quam", "satis", "nimis", "plus",
    "magis", "minus", "maxime", "minime", "etiam", "quoque", "quam",
    "tantum", "solum", "certe", "plane", "prope", "fere", "ubi", "quo",
    "unde", "qua", "hic", "illic", "ibi", "alibi", "ubique", "nusquam"
]

CONJUNCTIONS = [
    "et", "atque", "ac", "que", "sed", "autem", "tamen", "vero", "at",
    "aut", "vel", "sive", "seu", "nam", "namque", "enim", "etenim",
    "quod", "quia", "quoniam", "quando", "cum", "ut", "ne", "an", "num",
    "si", "nisi", "ni", "sin"
]

def migrate_phase1():
    """Ejecuta la migración de Fase 1"""
    
    print("=== Migración Fase 1: Base de Datos Mejorada ===\n")
    
    with get_session() as session:
        # 1. Crear autores
        print("1. Creando autores...")
        for author_data in AUTHORS_DATA:
            # Verificar si ya existe
            existing = session.exec(
                select(Author).where(Author.name == author_data["name"])
            ).first()
            
            if not existing:
                author = Author(**author_data)
                session.add(author)
                print(f"   ✓ Creado: {author.name}")
            else:
                print(f"   - Ya existe: {author_data['name']}")
        
        session.commit()
        print()
        
        # 2. Marcar palabras invariables
        print("2. Marcando palabras invariables...")
        
        # Preposiciones
        for prep in PREPOSITIONS:
            word = session.exec(select(Word).where(Word.latin == prep)).first()
            if word:
                word.is_invariable = True
                word.is_fundamental = True
                word.category = "preposition"
                word.part_of_speech = "preposition"
                session.add(word)
                print(f"   ✓ Preposición: {prep}")
        
        # Adverbios
        for adv in ADVERBS:
            word = session.exec(select(Word).where(Word.latin == adv)).first()
            if word:
                word.is_invariable = True
                word.is_fundamental = True
                word.category = "adverb"
                if word.part_of_speech != "adverb":
                    word.part_of_speech = "adverb"
                session.add(word)
                print(f"   ✓ Adverbio: {adv}")
        
        # Conjunciones
        for conj in CONJUNCTIONS:
            word = session.exec(select(Word).where(Word.latin == conj)).first()
            if word:
                word.is_invariable = True
                word.is_fundamental = True
                word.category = "conjunction"
                word.part_of_speech = "conjunction"
                session.add(word)
                print(f"   ✓ Conjunción: {conj}")
        
        session.commit()
        print()
        
        # 3. Marcar palabras del top 100
        print("3. Marcando palabras del top 100...")
        for rank, word_latin in enumerate(TOP_100_WORDS, start=1):
            word = session.exec(select(Word).where(Word.latin == word_latin)).first()
            if word:
                word.frequency_rank_global = rank
                word.is_fundamental = True
                session.add(word)
                print(f"   ✓ #{rank}: {word_latin}")
        
        session.commit()
        print()
        
        # 4. Estadísticas finales
        print("=== Estadísticas ===")
        total_authors = session.exec(select(Author)).all()
        total_words = session.exec(select(Word)).all()
        invariable_words = session.exec(
            select(Word).where(Word.is_invariable == True)
        ).all()
        fundamental_words = session.exec(
            select(Word).where(Word.is_fundamental == True)
        ).all()
        
        print(f"Autores creados: {len(total_authors)}")
        print(f"Total palabras: {len(total_words)}")
        print(f"Palabras invariables: {len(invariable_words)}")
        print(f"Palabras fundamentales: {len(fundamental_words)}")
        print()
        print("✅ Migración completada exitosamente!")

if __name__ == "__main__":
    migrate_phase1()
