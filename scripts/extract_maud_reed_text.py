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


def extract_sentences(text: str) -> List[Tuple[str, int]]:
    """
    Extrae oraciones latinas del texto
    Retorna: [(sentence, chapter_number), ...]
    """
    sentences = []
    current_chapter = 1
    
    # Split por párrafos
    paragraphs = text.split('\n\n')
    
    for para in paragraphs:
        # Detectar cambio de capítulo
        chapter_match = re.search(r'(?:Chapter|Capitulum|Cap\.?)\s+(\d+|[IVX]+)', para, re.IGNORECASE)
        if chapter_match:
            # Convertir romano a arábigo si es necesario
            chapter_num = chapter_match.group(1)
            if chapter_num.isdigit():
                current_chapter = int(chapter_num)
            else:
                # Conversión básica de romanos
                roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
                current_chapter = sum(roman_map.get(c, 0) for c in chapter_num)
            continue
        
        # Extraer oraciones (termina en . ! ? ; o :)
        para_sentences = re.split(r'([.!?;:])\s+', para)
        
        for i in range(0, len(para_sentences)-1, 2):
            if i+1 < len(para_sentences):
                sentence = para_sentences[i] + para_sentences[i+1]
                sentence = sentence.strip()
                
                # Filtrar oraciones muy cortas o que no parezcan latín
                if len(sentence) > 10 and re.search(r'[a-zA-Z]', sentence):
                    # Verificar que tiene características de latín (no es solo números o inglés)
                    if not re.match(r'^(The|And|Exercise|Vocabulary|Notes)', sentence):
                        sentences.append((sentence, current_chapter))
    
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
