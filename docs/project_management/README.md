# Lingua Latina Viva

Una plataforma integral para el aprendizaje del latín con análisis lingüístico avanzado.

## Características

- Análisis morfológico usando PyCollatinus
- Análisis sintáctico usando LatinCy (basado en Universal Dependencies)
- Sistema de repetición espaciada (SRS) para vocabulario
- Ejercicios interactivos y lecciones estructuradas
- Interfaz web moderna basada en Streamlit

## Requisitos

- Python 3.9+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
   ```
   git clone <repository-url>
   cd lingua-latina-viva
   ```

2. Crear un entorno virtual:
   ```
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Ejecutar la aplicación:
   ```
   streamlit run app.py
   ```

## Componentes Clave

### Análisis Lingüístico

El sistema utiliza dos motores principales para el análisis lingüístico:

1. **PyCollatinus**: Para análisis morfológico detallado
2. **LatinCy**: Modelo de spaCy para latín basado en Universal Dependencies

### Integración con Universal Dependencies

El proyecto incluye herramientas para integrar y validar análisis contra el corpus de Universal Dependencies:

- `utils/ud_enhancer.py`: Mejora los análisis existentes con datos de UD
- `scripts/integrate_ud_corpus.py`: Scripts para integración masiva con corpus UD

### Estructura del Proyecto

```
lingua-latina-viva/
├── app/                 # Aplicación principal
├── database/            # Modelos y conexión a base de datos
├── pages/               # Páginas de la interfaz Streamlit
├── scripts/             # Scripts de utilidad y procesamiento
├── utils/               # Funciones auxiliares
├── data/                # Datos y corpus
└── requirements.txt     # Dependencias del proyecto
```

## Uso

Después de iniciar la aplicación con `streamlit run app.py`, puedes:

1. Navegar por las lecciones de latín
2. Practicar vocabulario con el sistema SRS
3. Analizar textos latinos con herramientas lingüísticas avanzadas
4. Realizar ejercicios interactivos

## Desarrollo

Para contribuir al desarrollo:

1. Haz un fork del repositorio
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. Realiza tus cambios
4. Confirma tus cambios (`git commit -am 'Añadir nueva función'`)
5. Empuja la rama (`git push origin feature/nueva-funcion`)
6. Crea un nuevo Pull Request

## Licencia

Este proyecto está licenciado bajo GPL-3.0. Ver el archivo `LICENSE` para más detalles.

