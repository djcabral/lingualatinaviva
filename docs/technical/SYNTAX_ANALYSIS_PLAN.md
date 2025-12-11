# Visión y Metodología: Análisis Sintáctico Pedagógico

## 1. Introducción y Contexto
El proyecto **Lingua Latina Viva** busca trascender las herramientas tradicionales de aprendizaje de latín (flashcards simples o diccionarios estáticos) para ofrecer una experiencia inmersiva y analítica.

La faceta de **Análisis Sintáctico Pedagógico** nace de una necesidad crítica: las herramientas automáticas de NLP (como spaCy/LatinCy) son excelentes para procesar texto, pero sus etiquetas (`nsubj`, `dobj`, `abl`) son insuficientes para un estudiante. Un estudiante no necesita saber que una palabra es un "modificador nominal"; necesita entender que es un **Ablativo de Instrumento** o un **Dativo de Interés**.

## 2. Objetivos del Módulo

### Objetivo General
Crear un "Profesor Digital" capaz de explicar la estructura de cualquier oración latina con la profundidad y matiz de un gramático tradicional, pero con la interactividad de una aplicación moderna.

### Objetivos Específicos
1.  **Cerrar la brecha entre NLP y Pedagogía:** Traducir las dependencias técnicas de la IA a términos gramaticales clásicos que se enseñan en las aulas.
2.  **Explicar el "Porqué":** No solo identificar el caso (ej. Ablativo), sino su función semántica en ese contexto específico (ej. Ablativo Absoluto vs. Ablativo de Tiempo).
3.  **Visualización Intuitiva:** Permitir al estudiante "desarmar" la oración visualmente para entender cómo se relacionan las palabras entre sí.
4.  **Aprendizaje Inductivo:** Fomentar que el estudiante deduzca reglas gramaticales observando patrones reales en textos auténticos (*Familia Romana*, César, Cicerón).

## 3. Metodología Pedagógica

Nuestra metodología se basa en tres pilares:

### A. El Enfoque Estructural (Structural Approach)
Entendemos la oración latina no como una secuencia lineal de palabras, sino como una estructura jerárquica.
*   **Núcleo:** El verbo es el sol alrededor del cual giran los demás elementos.
*   **Satélites:** Argumentos (Sujeto, Objeto) y Adjuntos (Circunstanciales).
*   **Implementación:** Usamos árboles de dependencias para visualizar esta jerarquía, pero con etiquetas amigables ("¿Quién lo hace?", "¿A quién?", "¿Cómo?").

### B. La Gramática Explicada (Explanatory Grammar)
Cada anotación debe ser educativa.
*   *Incorrecto:* "puella: Nominativo"
*   *Correcto:* "puella: **Sujeto**. Está en caso Nominativo porque realiza la acción del verbo."
*   *Incorrecto:* "gladio: Ablativo"
*   *Correcto:* "gladio: **Ablativo de Instrumento**. Indica el objeto utilizado para realizar la acción ('con una espada')."

### C. Progresión Gradual (Scaffolding)
El sistema debe adaptarse al nivel del texto.
*   **Nivel 1 (Familia Romana):** Oraciones simples, orden SOV, casos básicos.
*   **Nivel 5 (César):** Oraciones compuestas, ablativo absoluto, oraciones de infinitivo.
*   **Nivel 10 (Cicerón/Virgilio):** Hipérbaton complejo, figuras retóricas, subjuntivos matizados.

## 4. ¿Qué pretendemos con este desarrollo?

Pretendemos crear el **Tesauro Sintáctico Interactivo** más completo disponible en software libre.

A diferencia de un libro de texto donde los ejemplos son estáticos y limitados, este sistema permitirá:
1.  **Búsqueda Semántica:** "¿Muéstrame todos los ejemplos de 'Ablativo Absoluto' en los textos de César?"
2.  **Análisis Comparativo:** Ver cómo diferentes autores usan las mismas construcciones.
3.  **Corrección Inteligente:** En los ejercicios de traducción, el sistema podrá decir "Usaste un acusativo, pero aquí se requiere un dativo porque el verbo indica dar/entregar".

## 5. Estrategia Técnica

Para lograr esto, no podemos depender solo de la IA. Implementamos un sistema **Híbrido (Human-in-the-loop)**:

1.  **Capa 1: NLP Automático (LatinCy):** Procesa el texto crudo y genera una estructura base (80% de precisión).
2.  **Capa 2: Reglas Heurísticas:** Scripts que detectan patrones obvios (ej. `cum` + subjuntivo = Cum Histórico).
3.  **Capa 3: Curaduría Manual (El "Gold Standard"):** Profesores/Expertos (o el usuario avanzado) refinan las etiquetas y añaden las explicaciones pedagógicas ricas. Estas correcciones retroalimentan el sistema.

Este documento sirve como norte para el desarrollo de las funcionalidades técnicas descritas en el Plan de Implementación.
