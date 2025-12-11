
import re

# Ruta al archivo de administración
admin_file_path = "pages/99_⚙️_Administracion.py"

# Leer el archivo actual
with open(admin_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Patrón a buscar (líneas 1716-1725)
pattern = r"(\s+if analyze_btn and latin_text and spanish_translation:\s+try:\s+with st\.spinner\("🧠 Analizando oración con Stanza... \(El primer análisis tarda ~10 segundos\)":\s+from utils\.stanza_analyzer import StanzaAnalyzer\s+if not StanzaAnalyzer\.is_available\(\):\s+st\.error\("❌ Stanza no está disponible\. Revisa la instalación\."\)\s+else:\s+analyzer = StanzaAnalyzer\(\))"

# Reemplazo
replacement = """            if analyze_btn and latin_text and spanish_translation:
                try:
                    # Inicializar Stanza con spinner si es necesario
                    analyzer, available = initialize_stanza_with_spinner()

                    if not available:
                        st.error("❌ Stanza no está disponible. Revisa la instalación.")
                    else:"""

# Realizar el reemplazo
new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

# Guardar el archivo modificado
with open(admin_file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Modificación aplicada correctamente")
