import streamlit.components.v1 as components
import uuid

def render_mermaid(diagram_code: str, height: int = 800):
    """
    Render a Mermaid diagram in Streamlit using the Mermaid.js CDN.
    
    Args:
        diagram_code: The Mermaid diagram code (without the ```mermaid wrapper)
        height: Height of the diagram container in pixels
    """
    # Generate unique ID for this diagram
    diagram_id = f"mermaid-{uuid.uuid4()}"
    
    # Escape backticks and other potential issues
    safe_code = diagram_code.replace("`", "\`")
    
    html_code = f"""
    <div id="{diagram_id}" class="mermaid" style="text-align: center; overflow: visible; width: 100%; display: flex; justify-content: center;">
    {safe_code}
    </div>
    
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        
        mermaid.initialize({{ 
            startOnLoad: false, 
            theme: 'default',
            securityLevel: 'loose',
            fontFamily: 'Cardo, serif'
        }});
        
        const element = document.getElementById('{diagram_id}');
        
        try {{
            await mermaid.run({{
                nodes: [element]
            }});
        }} catch (error) {{
            console.error('Mermaid rendering error:', error);
            element.innerHTML = '<p style="color: red;">Error rendering diagram: ' + error.message + '</p><pre>' + `{safe_code}` + '</pre>';
        }}
    </script>
    """
    
    components.html(html_code, height=height, scrolling=False)
