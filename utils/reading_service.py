"""
Servicio de Lecturas (Reading Service)
Este módulo gestiona la recuperación de lecturas y el enriquecimiento de textos con tooltips.

Funciones principales:
- get_reading_for_lesson: Obtiene la lectura asignada a una lección
- enrich_reading_with_tooltips: Añade tooltips HTML interactivos a las palabras difíciles
"""

from typing import Optional, Dict, List, Tuple
from sqlmodel import Session, select
from database import Text, TextWordLink, Word, ReadingProgress

class ReadingService:
    def __init__(self, session: Session):
        self.session = session

    def get_reading_for_lesson(self, lesson_number: int) -> Optional[Text]:
        """
        Obtiene la lectura principal asociada a una lección.
        Por ahora, usamos una convención simple o un mapeo manual.
        En el futuro, esto podría estar en la base de datos (Lesson.reading_id).
        """
        # Mapeo temporal de lección a ID de texto (simulado)
        # Asumimos que los textos están creados en orden de dificultad
        # Lección 5 -> Texto 1, Lección 10 -> Texto 2, etc.
        
        # Lógica provisional: buscar texto con dificultad similar a la lección / 2
        target_difficulty = max(1, lesson_number // 2)
        
        statement = select(Text).where(Text.difficulty == target_difficulty).order_by(Text.id)
        text = self.session.exec(statement).first()
        
        return text

    def enrich_reading_with_tooltips(self, text_id: int) -> str:
        """
        Toma el contenido de un texto y envuelve las palabras difíciles en spans con tooltips.
        Retorna el HTML procesado.
        """
        text = self.session.get(Text, text_id)
        if not text:
            return ""
            
        content = text.content
        
        # Obtener enlaces de palabras para este texto
        links = self.session.exec(
            select(TextWordLink, Word)
            .join(Word, TextWordLink.word_id == Word.id)
            .where(TextWordLink.text_id == text_id)
        ).all()
        
        # Crear un mapa de reemplazos: posición -> (palabra, definición)
        # Nota: Esto es complejo porque requiere saber la posición exacta en el string.
        # Simplificación: Reemplazar palabras clave usando búsqueda de texto, 
        # teniendo cuidado de no reemplazar dentro de etiquetas HTML ya creadas.
        
        # Mejor enfoque: Tokenizar el contenido y reconstruirlo.
        # Por ahora, haremos una sustitución simple de las palabras conocidas.
        
        enriched_content = content
        
        # Ordenar por longitud descendente para evitar reemplazar subcadenas primero
        # (ej: reemplazar 'ama' dentro de 'amat')
        links_sorted = sorted(links, key=lambda x: len(x[1].latin), reverse=True)
        
        for link, word in links_sorted:
            # Crear el HTML del tooltip
            # Usamos un estilo simple compatible con Streamlit (title attribute)
            # O un componente custom si fuera necesario.
            
            latin_form = link.form or word.latin
            definition = word.definition_es or word.translation
            pos = word.part_of_speech
            
            tooltip_html = f"""<span class="word-tooltip" title="{definition} ({pos})">{latin_form}</span>"""
            
            # Reemplazo seguro (solo palabras completas)
            # Esto es frágil con regex simple, pero servirá para el prototipo.
            # En producción usaríamos un tokenizador real.
            import re
            pattern = re.compile(r'\b' + re.escape(latin_form) + r'\b', re.IGNORECASE)
            enriched_content = pattern.sub(tooltip_html, enriched_content)
            
        return enriched_content

    def mark_reading_as_completed(self, user_id: int, text_id: int):
        """Registra que el usuario ha completado la lectura."""
        from datetime import datetime
        
        progress = self.session.exec(
            select(ReadingProgress).where(
                ReadingProgress.user_id == user_id,
                ReadingProgress.text_id == text_id
            )
        ).first()
        
        if not progress:
            progress = ReadingProgress(
                user_id=user_id,
                text_id=text_id,
                status="completed",
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow()
            )
            self.session.add(progress)
        else:
            progress.status = "completed"
            progress.completed_at = datetime.utcnow()
            self.session.add(progress)
            
        self.session.commit()
