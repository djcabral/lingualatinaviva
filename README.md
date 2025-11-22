# 🏛️ Lingua Latina Viva

**Una aplicación moderna para revivir una lengua eterna.**

**Lingua Latina Viva** es una plataforma interactiva diseñada para el aprendizaje del latín clásico con rigor académico y tecnología moderna. Combina la metodología tradicional con la interactividad de Streamlit y Python.

![Lingua Latina Viva](https://img.shields.io/badge/Status-Beta-orange) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

## 🌟 Características Principales

*   🧠 **Vocabulario Inteligente (SRS):** Sistema de repetición espaciada para maximizar la retención de palabras.
*   ⚔️ **Entrenamiento Gramatical:** Módulos intensivos de **Declinatio** (declinaciones) y **Conjugatio** (verbos) con corrección instantánea.
*   📖 **Lectura Asistida (Lectio):** Textos clásicos (César, Fedro) con análisis morfológico interactivo y diccionario contextual.
*   🏛️ **Rigor Histórico:** Base de datos curada con miles de palabras y formas gramaticales auténticas.
*   🔍 **Análisis Morfológico:** Herramientas para analizar cualquier palabra latina.

## 🚀 Instalación Local

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/djcabral/lingualatinaviva.git
    cd lingualatinaviva
    ```

2.  **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app.py
    ```

## ☁️ Despliegue

Esta aplicación está optimizada para **Streamlit Cloud**.

### Configuración Básica
1.  Haz un fork de este repositorio.
2.  Conecta tu cuenta de GitHub en [share.streamlit.io](https://share.streamlit.io).
3.  Selecciona el repositorio y el archivo principal `app.py`.

### Crear Token Personal de GitHub (Opcional)

Si necesitas que Streamlit Cloud acceda a repositorios privados o recursos protegidos, debes crear un **Personal Access Token (PAT)**:

1.  **Acceder a configuración de tokens:**
    - Ve a tu perfil de GitHub → **Settings** (Configuración)
    - En el menú lateral izquierdo, baja hasta **Developer settings** (Configuración de desarrollador)
    - Selecciona **Personal access tokens** → **Tokens (classic)**

2.  **Generar nuevo token:**
    - Haz clic en **Generate new token** → **Generate new token (classic)**
    - GitHub te pedirá tu contraseña para confirmar

3.  **Configurar el token:**
    - **Note** (Nombre): Dale un nombre descriptivo, ej: `streamlit-cloud-deployment`
    - **Expiration** (Expiración): Selecciona la duración deseada (recomendado: 90 días o más)
    - **Scopes** (Permisos): Marca las siguientes casillas:
      - ✅ `repo` (acceso completo a repositorios privados)
      - ✅ `workflow` (si usas GitHub Actions)
      - ✅ `read:org` (si el repo está en una organización)

4.  **Generar y copiar:**
    - Haz clic en **Generate token** al final de la página
    - ⚠️ **IMPORTANTE**: Copia el token inmediatamente y guárdalo en un lugar seguro
    - No podrás volver a verlo después de salir de la página

5.  **Configurar en Streamlit Cloud:**
    - En el dashboard de Streamlit Cloud, ve a tu aplicación
    - Accede a **Settings** → **Secrets**
    - Agrega el token como secret si tu aplicación lo requiere
    - O úsalo durante el proceso de conexión con GitHub cuando se te solicite

## 📜 Licencia

Este proyecto está licenciado bajo **GNU GPL v3** - consulta el archivo [LICENSE](LICENSE) para más detalles.

### Atribuciones
- **Collatinus**: Morfología y formas latinas © Yves Ouvrard & Philippe Verkerk (GPL v3)
- **Diccionario Valbuena (1819)**: Dominio público
- **Código original**: © 2025 Diego J. Cabral (GPL v3)

---
*Non scholae, sed vitae discimus.*
