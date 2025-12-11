
# ✅ Solución para el Spinner de Stanza

## Problema
El módulo de análisis de sintaxis tarda ~20 segundos en cargar sin mostrar un indicador visual, lo que hace que los usuarios piensen que la aplicación está colgada.

## Solución Implementada

### 1. Nuevo Archivo: `utils/stanza_spinner.py`
Se ha creado un nuevo módulo que proporciona una función para inicializar Stanza con un spinner visible.

### 2. Modificación Necesaria en `pages/99_⚙️_Administracion.py`

Para implementar esta solución, necesitas hacer los siguientes cambios en el archivo de administración:

#### Paso 1: Añadir la importación
Al principio del archivo (cerca de las otras importaciones), añade:
```python
from utils.stanza_spinner import initialize_stanza_with_spinner
```

#### Paso 2: Modificar la sección de Sintaxis
Reemplaza las líneas 1716-1724:

```python
if analyze_btn and latin_text and spanish_translation:
    try:
        with st.spinner("🧠 Analizando oración con Stanza... (El primer análisis tarda ~10 segundos)"):
            from utils.stanza_analyzer import StanzaAnalyzer

        if not StanzaAnalyzer.is_available():
            st.error("❌ Stanza no está disponible. Revisa la instalación.")
        else:
            analyzer = StanzaAnalyzer()
```

Por:

```python
if analyze_btn and latin_text and spanish_translation:
    try:
        # Inicializar Stanza con spinner si es necesario
        analyzer, available = initialize_stanza_with_spinner()

        if not available:
            st.error("❌ Stanza no está disponible. Revisa la instalación.")
        else:
```

## Cómo Funciona

1. La primera vez que se accede a la función de análisis, se muestra un spinner con el mensaje:
   "🧠 **Inicializando analizador de Stanza...**\n\nEste proceso tarda ~20 segundos solo la primera vez."

2. El analizador se inicializa en segundo plano mientras el spinner está visible.

3. Una vez inicializado, el analizador se guarda en `st.session_state` para no tener que reiniciarlo en cada uso.

4. Las siguientes veces que se utiliza el analizador, se carga directamente desde la sesión sin mostrar el spinner.

## Ventajas

- ✅ El usuario sabe que la aplicación está trabajando
- ✅ Se informa sobre el tiempo estimado de espera
- ✅ El analizador se inicializa solo una vez por sesión
- ✅ No afecta al rendimiento después de la inicialización

## Notas Adicionales

- Si Stanza no está disponible, se mostrará un mensaje de advertencia claro.
- Si hay un error durante la inicialización, se mostrará un mensaje de error específico.
- El spinner solo aparece durante la inicialización, no durante cada análisis.
