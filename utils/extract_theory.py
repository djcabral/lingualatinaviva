import ast
import json
import os
import re

def extract_lesson_content(file_path):
    with open(file_path, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())

    lessons = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("render_lesson_"):
            try:
                lesson_id = node.name.replace("render_lesson_", "")
                if not lesson_id.isdigit():
                    continue
                lesson_num = int(lesson_id)
                
                # Find inner function 'theory_content'
                theory_func = None
                for inner in node.body:
                    if isinstance(inner, ast.FunctionDef) and inner.name == "theory_content":
                        theory_func = inner
                        break
                
                sections = []
                if theory_func:
                    for stmt in theory_func.body:
                        # Check for st.markdown calls
                        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                            call = stmt.value
                            if isinstance(call.func, ast.Attribute) and call.func.attr == "markdown":
                                # Extract string content
                                if call.args and isinstance(call.args[0], ast.Constant): # Python 3.8+
                                    content = call.args[0].value
                                    sections.append({"type": "markdown", "content": content})
                                elif call.args and isinstance(call.args[0], ast.Str): # Python < 3.8
                                    content = call.args[0].s
                                    sections.append({"type": "markdown", "content": content})
                            
                            # Check for st.image calls
                            elif isinstance(call.func, ast.Attribute) and call.func.attr == "image":
                                img_path = ""
                                caption = ""
                                if call.args and isinstance(call.args[0], ast.Constant):
                                    img_path = call.args[0].value
                                
                                # Find caption in keywords
                                for kw in call.keywords:
                                    if kw.arg == "caption" and isinstance(kw.value, ast.Constant):
                                        caption = kw.value.value
                                
                                sections.append({"type": "image", "path": img_path, "caption": caption})

                            # Check for render_styled_table calls
                            elif isinstance(call.func, ast.Name) and call.func.id == "render_styled_table":
                                headers = []
                                rows = []
                                # Arg 0: headers list
                                if len(call.args) > 0 and isinstance(call.args[0], ast.List):
                                    headers = [elt.value for elt in call.args[0].elts if isinstance(elt, ast.Constant)]
                                
                                # Arg 1: rows list of lists
                                if len(call.args) > 1 and isinstance(call.args[1], ast.List):
                                    for row_node in call.args[1].elts:
                                        if isinstance(row_node, ast.List):
                                            row_data = [elt.value for elt in row_node.elts if isinstance(elt, ast.Constant)]
                                            rows.append(row_data)
                                
                                sections.append({"type": "table", "headers": headers, "rows": rows})

                lessons[lesson_num] = {
                    "id": lesson_num,
                    "sections": sections
                }
            except Exception as e:
                print(f"Error parsing lesson {node.name}: {e}")

    return lessons

def main():
    source_file = "pages/modules/course_view.py"
    output_dir = "portability/lessons"
    
    print(f"Parsing {source_file}...")
    lessons = extract_lesson_content(source_file)
    
    print(f"Found {len(lessons)} lessons.")
    
    for lesson_num, content in lessons.items():
        output_file = os.path.join(output_dir, f"lesson_{lesson_num}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        print(f"Exported lesson {lesson_num} to {output_file}")

if __name__ == "__main__":
    main()
