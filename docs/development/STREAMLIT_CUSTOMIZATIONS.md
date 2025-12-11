# Personalizaciones de Streamlit

Este documento describe todas las personalizaciones realizadas en la interfaz de Streamlit para la aplicación Lingua Latina Viva.

## Archivo de Configuración

**Ubicación:** `.streamlit/config.toml`

### Configuraciones Aplicadas

```toml
[theme]
primaryColor = "#8B4513"        # Color marrón clásico
backgroundColor = "#F5F5DC"      # Beige suave (fondo)
secondaryBackgroundColor = "#E8E8D0"  # Beige más oscuro (sidebar, bloques)
textColor = "#2C2416"            # Marrón oscuro (texto)
font = "serif"                   # Tipografía serif para estética clásica

[server]
headless = true
port = 8502

[browser]
gatherUsageStats = false         # No enviar estadísticas a Streamlit

[runner]
fastReruns = true                # Habilitar reruns más rápidos

[client]
showErrorDetails = true          # Mostrar detalles de errores
toolbarMode = "minimal"          # Toolbar minimalista
```

## Estilos CSS Personalizados

**Ubicación:** `assets/style.css`

### 1. Tipografías

Se importan dos fuentes de Google Fonts para dar un aspecto clásico:

- **Cinzel**: Para títulos y encabezados (estilo romano/clásico)
- **Cardo**: Para el texto del cuerpo (serif legible)

```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cardo:ital,wght@0,400;0,700;1,400&display=swap');
```

### 2. Traducción de Elementos UI

**Problema:** Streamlit muestra textos en inglés como "View less" y "View more" en los botones de expansión.

**Limitación:** Estos textos son generados internamente por Streamlit y no pueden ser traducidos fácilmente:
- CSS no puede modificar el contenido de texto directamente
- JavaScript inyectado a través de `st.markdown()` no se ejecuta debido a restricciones de seguridad de Streamlit
- No hay configuración oficial para cambiar el idioma de la UI de Streamlit

**Alternativas posibles:**
1. Esperar a que Streamlit añada soporte oficial de i18n
2. Usar componentes personalizados en lugar de los nativos de Streamlit
3. Contribuir al proyecto Streamlit para añadir soporte multiidioma

**Estado actual:** Los botones "View less" y "View more" permanecen en inglés

### 3. Componentes Personalizados

#### Stat Boxes
Cajas estadísticas con bordes y sombras para mostrar métricas (XP, nivel, etc.)

```css
.stat-box { border: 2px solid; border-radius: 15px; padding: 25px; }
.stat-value { font-size: 2.5em; font-family: 'Cinzel', serif; }
.stat-label { text-transform: uppercase; letter-spacing: 2px; }
```

#### Vocabulary Cards
Tarjetas grandes para mostrar palabras latinas durante la práctica.

```css
.vocab-card { border: 3px solid; padding: 50px; max-width: 600px; }
.vocab-latin { font-size: 3.5em; font-family: 'Cinzel', serif; }
.vocab-translation { font-size: 1.8em; font-family: 'Cardo', serif; }
```

## Carga del CSS

El archivo CSS se carga en cada página mediante la función `load_css()` definida en `utils/ui_helpers.py`:

```python
def load_css():
    """Carga el archivo CSS personalizado"""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
```

**Uso en páginas:**
```python
from utils.ui_helpers import load_css
load_css()
```

## Notas de Mantenimiento

### Añadir Nuevas Traducciones de UI

Si necesitas traducir otros elementos de Streamlit:

1. Inspecciona el elemento en el navegador (F12) para encontrar su selector CSS
2. Identifica el atributo `data-testid` o la estructura del elemento
3. Agrega reglas CSS similares en `assets/style.css`:
   ```css
   [data-testid="elemento"]:has-text("English text")::before {
       content: "Texto en español" !important;
   }
   [data-testid="elemento"]:has-text("English text") {
       font-size: 0 !important;
   }
   ```

### Limitaciones

- **CSS no puede traducir todo**: Algunos textos están generados dinámicamente por JavaScript y no se pueden modificar con CSS puro.
- **Selectores `:has-text()`**: No están soportados en todos los navegadores (principalmente funciona en Chrome/Edge moderno).
- **Versiones de Streamlit**: Los selectores pueden cambiar entre versiones. Si actualizas Streamlit, revisa que las traducciones sigan funcionando.

### Alternativa (JavaScript)

Si CSS no es suficiente, puedes usar JavaScript inyectado:

```python
st.markdown("""
<script>
    // Esperar a que el DOM se cargue
    setTimeout(() => {
        document.querySelectorAll('button').forEach(btn => {
            if (btn.textContent.includes('View less')) {
                btn.textContent = btn.textContent.replace('View less', 'Ver menos');
            }
            if (btn.textContent.includes('View more')) {
                btn.textContent = btn.textContent.replace('View more', 'Ver más');
            }
        });
    }, 500);
</script>
""", unsafe_allow_html=True)
```

## Recursos

- [Streamlit Theme Configuration](https://docs.streamlit.io/library/advanced-features/theming)
- [Streamlit CSS Customization](https://docs.streamlit.io/library/advanced-features/custom-components)
- [Google Fonts](https://fonts.google.com/)

---

**Última actualización:** 2025-11-24
