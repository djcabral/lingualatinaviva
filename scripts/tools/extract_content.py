import re
import os

def extract_lessons():
    source_file = "pages/modules/course_view.py"
    output_file = "full_course_content.md"
    
    with open(source_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all render_lesson_X functions
    # Pattern looks for def render_lesson_(\d+): ... st.markdown("""(.*?)""")
    # This is a simplified regex approach. A full AST parse would be safer but maybe overkill for this structure.
    # Given the file structure, lessons are usually distinct.
    
    # We'll split by "def render_lesson_" to get chunks
    chunks = content.split("def render_lesson_")
    
    lessons = []
    
    print(f"Found {len(chunks)} potential chunks")

    for chunk in chunks[1:]: # Skip the pre-first split
        # Extract ID
        match_id = re.match(r"(\d+)\(\):", chunk)
        if not match_id:
            continue
            
        lesson_id = int(match_id.group(1))
        
        # Extract Markdown content
        # We look for st.markdown(""" ... """)
        # We need to be careful about matching the correct closing quotes
        # We will look for content between st.markdown(""" and """)
        
        markdown_matches = re.findall(r'st\.markdown\("""(.*?)"""\)', chunk, re.DOTALL)
        
        lesson_text = ""
        for md_content in markdown_matches:
            # Clean up indentation
            cleaned_lines = []
            for line in md_content.split('\n'):
                cleaned_lines.append(line.strip()) # Aggressive strip for now, or maybe just lstrip?
            
            # Simple dedent
            import textwrap
            dedented_text = textwrap.dedent(md_content)
            lesson_text += dedented_text + "\n\n"
            
        if lesson_text:
            lessons.append((lesson_id, lesson_text))

    # Sort by Lesson ID
    lessons.sort(key=lambda x: x[0])
    
    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("% Lingua Latina Viva - Contenido Completo del Curso\n")
        f.write("% Generado Automáticamente\n")
        f.write(f"% {os.popen('date').read().strip()}\n\n")
        
        for lesson_id, text in lessons:
            f.write(f"\\newpage\n\n") # Page break for PDF
            f.write(f"# Lección {lesson_id}\n\n")
            f.write(text)
            f.write("\n\n---\n\n")

    print(f"Extracted {len(lessons)} lessons to {output_file}")

if __name__ == "__main__":
    extract_lessons()
