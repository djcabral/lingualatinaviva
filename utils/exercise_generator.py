"""
Generador de Ejercicios (Exercise Generator)
Este módulo genera ejercicios dinámicos basados en el contenido de la lección.

Funciones principales:
- generate_vocabulary_match: Genera ejercicios de emparejamiento
- generate_declension_choice: Genera preguntas de opción múltiple para declinaciones
- generate_conjugation_choice: Genera preguntas de opción múltiple para conjugaciones
- generate_sentence_completion: Genera ejercicios de completar oraciones
"""

import random
from typing import List, Dict, Any, Optional, Tuple
from sqlmodel import Session, select
from database import Word, LessonVocabulary, SentenceAnalysis

class ExerciseGenerator:
    def __init__(self, session: Session):
        self.session = session

    def generate_vocabulary_match(self, lesson_number: int, num_pairs: int = 5) -> List[Dict[str, str]]:
        """
        Genera pares de vocabulario para ejercicios de emparejamiento.
        Retorna una lista de diccionarios con 'latin' y 'spanish'.
        """
        statement = (
            select(Word)
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .where(LessonVocabulary.lesson_number == lesson_number)
        )
        words = self.session.exec(statement).all()
        
        if len(words) < num_pairs:
            # Si no hay suficientes palabras, usar todas las disponibles
            selected_words = words
        else:
            selected_words = random.sample(words, num_pairs)
            
        return [
            {
                "id": str(w.id),
                "latin": w.latin,
                "spanish": w.translation
            }
            for w in selected_words
        ]

    def generate_declension_choice(self, lesson_number: int, num_questions: int = 3) -> List[Dict[str, Any]]:
        """
        Genera preguntas de opción múltiple para identificar casos/números de sustantivos.
        """
        # Obtener sustantivos de la lección
        statement = (
            select(Word)
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .where(LessonVocabulary.lesson_number == lesson_number)
            .where(Word.part_of_speech == 'noun')
        )
        nouns = self.session.exec(statement).all()
        
        if not nouns:
            return []
            
        questions = []
        # Casos y números posibles (simplificado por ahora)
        cases = ["Nominativo", "Genitivo", "Dativo", "Acusativo", "Ablativo"]
        numbers = ["Singular", "Plural"]
        
        # En una implementación real, usaríamos un generador de formas (paradigm generator)
        # para crear la forma declinada correcta. Por ahora, simulamos la lógica
        # preguntando por propiedades teóricas o usando formas si estuvieran en BD.
        
        # Como fallback, generamos preguntas sobre el género o declinación que sí tenemos en BD
        for _ in range(min(len(nouns), num_questions)):
            noun = random.choice(nouns)
            
            q_type = random.choice(["declension", "gender"])
            
            if q_type == "declension" and noun.declension:
                # Normalize declension to "Xª" format (e.g., "3" -> "3ª")
                raw_decl = noun.declension.strip()
                if raw_decl.isdigit():
                    correct = f"{raw_decl}ª"
                elif raw_decl.endswith("ª"):
                    correct = raw_decl
                else:
                    correct = f"{raw_decl}ª"  # Fallback
                
                # Use consistent format for all options
                all_options = ["1ª", "2ª", "3ª", "4ª", "5ª"]
                # Remove correct answer and sample distractors
                distractors = [opt for opt in all_options if opt != correct]
                options = [correct] + random.sample(distractors, min(3, len(distractors)))
                random.shuffle(options)
                
                questions.append({
                    "type": "multiple_choice",
                    "question": f"¿A qué declinación pertenece el sustantivo **{noun.latin}**?",
                    "options": options,
                    "correct_answer": correct,
                    "explanation": f"'{noun.latin}' pertenece a la {correct} declinación."
                })
                
            elif q_type == "gender" and noun.gender:
                # Normalize gender from database (m, f, n) to display labels
                gender_map = {
                    "m": "Masculino", "masculino": "Masculino", "M": "Masculino",
                    "f": "Femenino", "femenino": "Femenino", "F": "Femenino", 
                    "n": "Neutro", "neutro": "Neutro", "N": "Neutro"
                }
                raw_gender = noun.gender.strip().lower()
                correct = gender_map.get(raw_gender, noun.gender)
                
                options = ["Masculino", "Femenino", "Neutro"]
                random.shuffle(options)
                
                questions.append({
                    "type": "multiple_choice",
                    "question": f"¿Cuál es el género de **{noun.latin}**?",
                    "options": options,
                    "correct_answer": correct,
                    "explanation": f"'{noun.latin}' es un sustantivo {correct.lower()}."
                })
                
        return questions

    def generate_conjugation_choice(self, lesson_number: int, num_questions: int = 3) -> List[Dict[str, Any]]:
        """
        Genera preguntas de opción múltiple para verbos.
        """
        statement = (
            select(Word)
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .where(LessonVocabulary.lesson_number == lesson_number)
            .where(Word.part_of_speech == 'verb')
        )
        verbs = self.session.exec(statement).all()
        
        if not verbs:
            return []
            
        questions = []
        
        for _ in range(min(len(verbs), num_questions)):
            verb = random.choice(verbs)
            
            if verb.conjugation:
                # Normalize conjugation to "Xª" format (e.g., "1" -> "1ª")
                raw_conj = verb.conjugation.strip()
                if raw_conj.isdigit():
                    correct = f"{raw_conj}ª"
                elif raw_conj.lower() == "mixta":
                    correct = "Mixta"
                elif raw_conj.endswith("ª"):
                    correct = raw_conj
                else:
                    correct = f"{raw_conj}ª"  # Fallback
                
                # Use consistent format for all options
                all_options = ["1ª", "2ª", "3ª", "4ª", "Mixta"]
                # Remove correct answer and sample distractors
                distractors = [opt for opt in all_options if opt != correct]
                options = [correct] + random.sample(distractors, min(3, len(distractors)))
                random.shuffle(options)
                
                questions.append({
                    "type": "multiple_choice",
                    "question": f"¿A qué conjugación pertenece el verbo **{verb.latin}**?",
                    "options": options,
                    "correct_answer": correct,
                    "explanation": f"'{verb.latin}' pertenece a la {correct} conjugación."
                })
                
        return questions

    def generate_sentence_completion(self, lesson_number: int, num_questions: int = 3) -> List[Dict[str, Any]]:
        """
        Genera ejercicios de completar oraciones ocultando una palabra clave.
        """
        statement = (
            select(SentenceAnalysis)
            .where(SentenceAnalysis.lesson_number == lesson_number)
        )
        sentences = self.session.exec(statement).all()
        
        if not sentences:
            return []
            
        questions = []
        
        for _ in range(min(len(sentences), num_questions)):
            sentence = random.choice(sentences)
            words = sentence.latin_text.split()
            
            if len(words) < 3:
                continue
                
            # Elegir una palabra para ocultar (evitar palabras muy cortas si es posible)
            candidates = [i for i, w in enumerate(words) if len(w) > 2]
            if not candidates:
                candidates = range(len(words))
                
            hide_idx = random.choice(candidates)
            correct_word = words[hide_idx].strip(".,?!")
            
            # Crear la oración con el hueco
            words_display = words.copy()
            words_display[hide_idx] = "_______"
            display_text = " ".join(words_display)
            
            # Generar distractores (palabras aleatorias de la misma lección o genéricas)
            # Por simplicidad, usamos distractores fijos o de la misma oración por ahora
            distractors = ["et", "non", "est", "sunt"] # Placeholder
            options = [correct_word] + distractors[:3]
            random.shuffle(options)
            
            questions.append({
                "type": "fill_blank",
                "question": f"Completa la oración: <br>_{display_text}_",
                "options": options,
                "correct_answer": correct_word,
                "explanation": f"La palabra correcta es '{correct_word}'. Traducción: {sentence.spanish_translation}"
            })
            
        return questions
