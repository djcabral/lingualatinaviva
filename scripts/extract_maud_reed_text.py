"""
Script para extraer texto de PDFs de Maud Reed y procesarlos
Requiere: pip install PyPDF2 o pdfplumber
"""
import re
from pathlib import Path
from typing import List, Tuple

try:
    import pdfplumber
    PDF_LIBRARY = "pdfplumber"
except ImportError:
    try:
        import PyPDF2
        PDF_LIBRARY = "PyPDF2"
    except ImportError:
        print("ERROR: Necesitas instalar pdfplumber o PyPDF2")
        print("Ejecuta: pip install pdfplumber")
        exit(1)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrae texto de un PDF"""
    print(f"📄 Extrayendo texto de {pdf_path.name}...")
    
    text = ""
    
    if PDF_LIBRARY == "pdfplumber":
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                print(f"  Página {i+1}/{len(pdf.pages)}", end='\r')
    else:  # PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                print(f"  Página {i+1}/{len(pdf_reader.pages)}", end='\r')
    
    print(f"\n✅ Texto extraído: {len(text)} caracteres")
    return text


def clean_latin_text(text: str) -> str:
    """Limpia el texto extraído del PDF"""
    # Remover números de página
    text = re.sub(r'\n\d+\n', '\n', text)
    
    # Remover headers/footers comunes
    text = re.sub(r'(JULIA|CAMILLA|Maud Reed).*\n', '', text, flags=re.IGNORECASE)
    
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text)
    
    # Normalizar saltos de línea
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()


def is_latin_sentence(text: str) -> bool:
    """
    Verifica si una oración parece ser latín basándose en terminaciones comunes.
    Retorna True si pasa el umbral de 'densidad latina'.
    """
    # Palabras comunes en inglés que indican que no es texto latino
    english_indicators = {
        "the", "and", "of", "to", "in", "is", "that", "it", "was", "for", 
        "on", "are", "as", "with", "his", "they", "at", "be", "this", "have",
        "from", "or", "one", "had", "by", "word", "but", "not", "what", "all",
        "were", "we", "when", "your", "can", "said", "there", "use", "an",
        "each", "which", "she", "do", "how", "their", "if", "will", "up", "other",
        "about", "out", "many", "then", "them", "these", "so", "some", "her",
        "would", "make", "like", "him", "into", "time", "has", "look", "two",
        "more", "write", "go", "see", "number", "no", "way", "could", "people",
        "my", "than", "first", "water", "been", "call", "who", "oil", "its", "now",
        "find", "long", "down", "day", "did", "get", "come", "made", "may", "part"
    }
    
    # Terminaciones latinas comunes
    latin_endings = (
        "us", "a", "um", "ae", "i", "o", "is", "as", "os", "es", "ibus", "iem",
        "rum", "uum", "tur", "nt", "at", "et", "it", "mus", "tis", "ntur", "ris",
        "re", "m", "s", "t"
    )
    
    words = text.lower().split()
    if not words:
        return False
        
    # 1. Check for English indicators
    english_count = sum(1 for w in words if w in english_indicators)
    if english_count / len(words) > 0.2: # Si más del 20% son palabras inglesas comunes
        return False
        
    # 2. Check for Latin density
    latin_matches = 0
    for w in words:
        # Limpiar puntuación
        w_clean = re.sub(r'[^\w]', '', w)
        if len(w_clean) < 2: continue
        
        if w_clean.endswith(latin_endings) or w_clean in ["et", "in", "ad", "non", "sed", "si"]:
            latin_matches += 1
            
    density = latin_matches / len(words)
    return density > 0.5 # Al menos 50% de palabras con apariencia latina


def extract_sentences(text: str) -> List[Tuple[str, int]]:
    """
    Extrae oraciones latinas del texto
    Retorna: [(sentence, chapter_number), ...]
    """
    sentences = []
    
    # Roman numeral regex (strict)
    roman_regex = re.compile(r'^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
    
    def from_roman(s):
        """Convierte romano a entero"""
        if not s: return 0
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0
        for char in reversed(s):
            value = roman_map.get(char, 0)
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        return result

    # Split por líneas para procesar estructura
    lines = text.split('\n')
    
    current_chapter = 1 # Default
    current_block = ""
    
    # Filtros de secciones no deseadas
    skip_sections = ["PREFACE", "INTRODUCTION", "VOCABULARY", "INDEX"]
    skipping = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Check for section headers to skip
        if any(section in line.upper() for section in skip_sections):
            skipping = True
            continue
            
        # Detectar capítulo (re-enable processing if we were skipping)
        words = line.split()
        last_word = words[-1] if words else ""
        is_chapter_header = False
        new_chapter = 0
        
        if len(words) == 1 and roman_regex.match(line) and from_roman(line) < 100:
            new_chapter = from_roman(line)
            is_chapter_header = True
            skipping = False # New chapter likely means back to text
        elif len(words) < 6 and roman_regex.match(last_word) and from_roman(last_word) < 100:
             if line.isupper() or len(line) < 20:
                new_chapter = from_roman(last_word)
                is_chapter_header = True
                skipping = False
        
        if skipping:
            continue
            
        if is_chapter_header:
            # Procesar bloque anterior
            if current_block:
                # Dividir por puntuación final, pero cuidando abreviaturas comunes si las hubiera
                block_sentences = re.split(r'(?<=[.?!])\s+', current_block)
                for s in block_sentences:
                    s = s.strip()
                    # Filtros de calidad
                    if len(s) > 10 and re.search(r'[a-zA-Z]', s):
                        if not re.search(r'^(Page|PAGE|Chapter|CHAPTER|Exercise|Vocabulary)', s):
                            if is_latin_sentence(s):
                                sentences.append((s, current_chapter))
            
            current_chapter = new_chapter
            current_block = ""
        else:
            current_block += " " + line
            
    # Procesar último bloque
    if current_block and not skipping:
        block_sentences = re.split(r'(?<=[.?!])\s+', current_block)
        for s in block_sentences:
            s = s.strip()
            if len(s) > 10:
                 if not re.search(r'^(Page|PAGE|Chapter|CHAPTER|Exercise|Vocabulary)', s):
                    if is_latin_sentence(s):
                        sentences.append((s, current_chapter))

    return sentences


def process_book(pdf_path: Path, book_name: str) -> List[Tuple[str, int]]:
    """Procesa un libro completo"""
    print(f"\n{'='*60}")
    print(f"Procesando: {book_name}")
    print(f"{'='*60}")
    
    # Extraer texto del PDF
    raw_text = extract_text_from_pdf(pdf_path)
    
    # Limpiar
    clean_text = clean_latin_text(raw_text)
    
    # Guardar texto limpio
    output_dir = Path("data/maud_reed/extracted")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    text_file = output_dir / f"{book_name.lower()}_clean.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(clean_text)
    print(f"✅ Texto limpio guardado: {text_file}")
    
    # Extraer oraciones
    sentences = extract_sentences(clean_text)
    
    # Guardar oraciones
    sentences_file = output_dir / f"{book_name.lower()}_sentences.txt"
    with open(sentences_file, 'w', encoding='utf-8') as f:
        for sent, chapter in sentences:
            f.write(f"[Cap. {chapter}] {sent}\n")
    
    print(f"✅ {len(sentences)} oraciones extraídas")
    print(f"✅ Oraciones guardadas: {sentences_file}")
    
    return sentences


def main():
    """Procesa todos los libros de Maud Reed"""
    pdf_dir = Path("data/maud_reed")
    
    # Verificar que los PDFs existen
    julia_pdf = pdf_dir / "julia.pdf"
    camilla_pdf = pdf_dir / "camilla.pdf"
    
    if not julia_pdf.exists():
        print(f"❌ No se encontró {julia_pdf}")
        print("Ejecuta primero: python scripts/download_maud_reed.py")
        return
    
    # Procesar Julia
    julia_sentences = process_book(julia_pdf, "Julia")
    
    # Procesar Camilla (si existe)
    if camilla_pdf.exists():
        camilla_sentences = process_book(camilla_pdf, "Camilla")
    
    print(f"\n{'='*60}")
    print("✅ PROCESAMIENTO COMPLETO")
    print(f"{'='*60}")
    print(f"Total oraciones extraídas: {len(julia_sentences)}")
    if camilla_pdf.exists():
        print(f"  - Julia: {len(julia_sentences)} oraciones")
        print(f"  - Camilla: {len(camilla_sentences)} oraciones")


if __name__ == "__main__":
    main()
