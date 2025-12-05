
import streamlit as st
from database.connection import get_session
from database import Challenge, UserChallengeProgress, Word
from utils.challenge_engine import ChallengeEngine
from sqlmodel import select
from datetime import datetime
import json


def render_content(caller="challenges"):
    """
    Página: 🎯 Desafío
    
    Esta página renderiza y ejecuta el desafío actual seleccionado desde el mapa.
    Muestra el UI apropiado según el tipo de desafío y verifica las respuestas.
    
    Args:
        caller: Identificador de quién llama a esta función ("challenges" o "adventure")
    
    DOCUMENTACIÓN:
    - Se accede desde 08_🗺️_Mapa.py
    - El ID del desafío se pasa vía st.session_state['current_challenge_id']
    - Tipos de desafío soportados: declension, conjugation, multiple_choice, translation, syntax
    - Al completar, actualiza UserChallengeProgress y desbloquea el siguiente desafío
    """
    
    # Configuración
    
    # Verificar que hay un desafío seleccionado o auto-cargar uno
    if 'current_challenge_id' not in st.session_state:
        # Check for Practice Context
        practice_context = st.session_state.get("practice_context")
        relevant_challenges = []
        if practice_context and practice_context.get("active"):
            relevant_challenges = practice_context.get("relevant_challenges", [])
            
        # Auto-cargar el primer desafío desbloqueado pero no completado
        with get_session() as session:
            query = select(Challenge).join(UserChallengeProgress).where(
                (UserChallengeProgress.status == 'unlocked') | 
                (UserChallengeProgress.status == 'in_progress')
            )
            
            # Filter by context if active
            if relevant_challenges:
                query = query.where(Challenge.id.in_(relevant_challenges))
                
            auto_challenge = session.exec(query.order_by(Challenge.order)).first()
            
            if auto_challenge:
                st.session_state['current_challenge_id'] = auto_challenge.id
                st.info(f"🎯 Cargando desafío: **{auto_challenge.title}**")
            else:
                if relevant_challenges:
                    st.warning("⚠️ No hay desafíos desbloqueados para esta lección.")
                    st.info("Completa los desafíos anteriores para desbloquear estos.")
                    if st.button("Ver Mapa Completo"):
                         st.session_state.active_tab = 2 # Switch to Adventure tab
                         st.rerun()
                    st.stop()
                else:
                    st.warning("⚠️ No hay desafíos desbloqueados disponibles")
                    st.info("Ve al tab '🗺️ Aventura' para ver el mapa de desafíos y desbloquear el primero")
                    st.stop()
    
    # Obtener sesión y desafío
    with get_session() as session:
        challenge_id = st.session_state['current_challenge_id']
        
        challenge = session.exec(
            select(Challenge).where(Challenge.id == challenge_id)
        ).first()
        
        if not challenge:
            st.error(f"❌ Desafío #{challenge_id} no encontrado")
            st.info("Por favor selecciona un desafío válido desde el tab '🗺️ Aventura'")
            st.stop()

        
        # Título
        st.title(f"🎯 Desafío #{challenge.order}")
        
        # Context Banner
        practice_context = st.session_state.get("practice_context")
        if practice_context and practice_context.get("active"):
            st.info(f"🎯 **Modo Práctica: {practice_context.get('description')}**")
            if st.button("❌ Salir del Contexto", key="exit_context_chal"):
                st.session_state.practice_context = None
                st.rerun()

        st.markdown(f"### {challenge.title}")
        st.caption(challenge.description)
        st.markdown("---")
        
        # Parser config
        try:
            full_config = json.loads(challenge.config_json)
        except json.JSONDecodeError:
            st.error(f"Error de configuración en desafío #{challenge.id}: JSON inválido")
            st.stop()
        except Exception as e:
            st.error(f"Error inesperado al cargar configuración: {str(e)}")
            st.stop()
        
        # Determinar etapa actual (0, 1, 2)
        if 'challenge_stage' not in st.session_state:
            # Inicializar basado en progreso actual
            progress = session.exec(
                select(UserChallengeProgress).where(
                    UserChallengeProgress.challenge_id == challenge.id
                )
            ).first()
            
            if progress and progress.stars < 3:
                st.session_state['challenge_stage'] = progress.stars
            else:
                # Si no hay progreso o ya tiene 3 estrellas (replay), empezar de 0
                st.session_state['challenge_stage'] = 0
        
        current_stage = st.session_state['challenge_stage']
        
        # Cargar configuración de la etapa actual
        if isinstance(full_config, list):
            # Asegurar que el índice no se salga de rango
            if current_stage >= len(full_config):
                current_stage = len(full_config) - 1
            config = full_config[current_stage]
        else:
            # Fallback para configs antiguos (no debería pasar con la migración)
            config = full_config
        
        # Mostrar progreso de etapa
        st.progress((current_stage) / 3)
        st.caption(f"Ejercicio {current_stage + 1} de 3 | ⭐ Estrellas actuales: {current_stage}")
        
        # Inicializar session_state para respuestas
        if 'user_answers' not in st.session_state:
            st.session_state['user_answers'] = {}
        
        # Renderizar UI según tipo de desafío
        if challenge.challenge_type == 'declension':
            st.markdown("#### 📚 Declina la siguiente palabra:")
            
            word = config.get('word')
            cases = config.get('cases', 'all')
            numbers = config.get('numbers', ['singular', 'plural'])
            
            # Buscar información de la palabra en la base de datos
            word_info = session.exec(
                select(Word).where(Word.latin == word.lower())
            ).first()
            
            # Construir display de información
            word_display = word.title()
            if word_info:
                if word_info.part_of_speech == 'noun':
                    # Para sustantivos: mostrar nominativo, genitivo, género y declinación
                    gen_sg = word_info.genitive_singular if hasattr(word_info, 'genitive_singular') and word_info.genitive_singular else "?"
                    gender_abbr = {'masculine': 'm.', 'feminine': 'f.', 'neuter': 'n.'}.get(word_info.gender, '')
                    decl_info = f" - {word_info.declension}ª decl." if word_info.declension else ""
                    word_display = f"{word.title()}, {gen_sg} ({gender_abbr}){decl_info}"
                elif word_info.part_of_speech == 'adjective':
                    # Para adjetivos: mostrar las tres formas principales si están disponibles
                    if hasattr(word_info, 'principal_parts') and word_info.principal_parts:
                        word_display = f"{word.title()} - {word_info.principal_parts}"
                    else:
                        word_display = f"{word.title()} (adj.)"
            
            st.info(f"**Palabra**: {word_display}")
            
            # Mapeo de casos
            # Mapeo de casos (Orden: Nom, Voc, Acc, Gen, Dat, Abl)
            case_names = {
                'nominative': 'Nominativo',
                'vocative': 'Vocativo',
                'accusative': 'Acusativo',
                'genitive': 'Genitivo',
                'dative': 'Dativo',
                'ablative': 'Ablativo'
            }
            
            # Definir orden explícito
            ordered_keys = ['nominative', 'vocative', 'accusative', 'genitive', 'dative', 'ablative']
            
            if cases == 'all':
                cases_list = ordered_keys
            else:
                # Ordenar los casos proporcionados según el orden estándar
                cases_list = sorted(cases, key=lambda x: ordered_keys.index(x) if x in ordered_keys else 99)
            
            case_abbr_map = {
                'nominative': 'nom', 'genitive': 'gen', 'dative': 'dat',
                'accusative': 'acc', 'ablative': 'abl', 'vocative': 'voc'
            }
            
            # Crear formulario dinámico según 'numbers'
            cols = st.columns(len(numbers))
            
            for idx, number in enumerate(numbers):
                with cols[idx]:
                    st.markdown(f"**{number.title()}**")
                    for case in cases_list:
                        suffix = "sg" if number == 'singular' else "pl"
                        key = f"{case_abbr_map[case]}_{suffix}"
                        
                        st.session_state['user_answers'][key] = st.text_input(
                            case_names[case],
                            key=f"{caller}_input_{key}",
                            placeholder=f"{word} ({number}) en {case_names[case].lower()}"
                        )
        
        elif challenge.challenge_type == 'conjugation':
            st.markdown("#### ⚔️ Conjuga el siguiente verbo:")
            
            verb = config.get('verb')
            tense = config.get('tense', 'present')
            numbers = config.get('numbers', ['singular', 'plural']) # Nuevo soporte para numbers
            
            tense_names = {
                'present': 'Presente de Indicativo',
                'imperfect': 'Imperfecto de Indicativo',
                'perfect': 'Perfecto de Indicativo'
            }
            
            # Buscar información del verbo en la base de datos
            verb_info = session.exec(
                select(Word).where(Word.latin == verb.lower(), Word.part_of_speech == 'verb')
            ).first()
            
            # Construir display de información
            verb_display = verb
            if verb_info:
                if verb_info.principal_parts:
                    verb_display = f"{verb} ({verb_info.principal_parts})"
                if verb_info.conjugation:
                    verb_display += f" - {verb_info.conjugation}ª conjugación"
            
            st.info(f"**Verbo**: {verb_display} | **Tiempo**: {tense_names.get(tense, tense)}")
            
            tense_abbr = {
                'present': 'pres',
                'imperfect': 'imp',
                'perfect': 'perf'
            }.get(tense, 'pres')
            
            # Formulario de conjugación dinámico
            cols = st.columns(len(numbers))
            
            for idx, number in enumerate(numbers):
                with cols[idx]:
                    st.markdown(f"**{number.title()}**")
                    suffix = "sg" if number == 'singular' else "pl"
                    
                    for person in [1, 2, 3]:
                        key = f"{tense_abbr}_{person}{suffix}"
                        st.session_state['user_answers'][key] = st.text_input(
                            f"{person}ª persona", 
                            key=f"{caller}_conj_{key}"
                        )
        
        elif challenge.challenge_type == 'multiple_choice':
            st.markdown("#### ❓ Responde:")
            
            questions = config.get('questions', [])
            
            for i, question in enumerate(questions):
                st.markdown(f"**{question['text']}**")
                
                selected = st.radio(
                    "Opciones",
                    options=range(len(question['options'])),
                    format_func=lambda x: question['options'][x],
                    key=f"q{i}",
                    label_visibility="collapsed"
                )
                
                st.session_state['user_answers'][f'q{i}'] = selected
                st.markdown("---")
        
        elif challenge.challenge_type == 'translation':
            st.markdown("#### 🌍 Traduce al latín:")
            
            if 'translations' in config:
                translations = config['translations']
            else:
                translations = [{'spanish': config.get('spanish')}]
            
            for i, trans in enumerate(translations):
                st.markdown(f"**{trans['spanish']}**")
                
                if len(translations) == 1:
                    key = 'translation'
                else:
                    key = f't{i}'
                
                st.session_state['user_answers'][key] = st.text_input(
                    "Latín:",
                    key=f"trans_{i}",
                    placeholder="Escribe tu traducción en latín"
                )
                
                if i < len(translations) - 1:
                    st.markdown("---")
                    
        elif challenge.challenge_type == 'syntax':
            st.markdown("#### 📐 Análisis Sintáctico:")
            sentences = config.get('sentences', [])
            
            for i, sent in enumerate(sentences):
                st.markdown(f"**Oración:** {sent['sentence']}")
                st.markdown(f"*Identifica el {sent.get('target', 'Sujeto')}*") # Simplificado para demo
                
                st.session_state['user_answers'][f's{i}'] = st.text_input(
                    "Respuesta:",
                    key=f"syntax_{i}"
                )
        
        elif challenge.challenge_type == 'sentence_order':
            st.markdown("#### 🧩 Rompecabezas: Ordena la oración")
            st.info("Haz clic en las palabras para ordenarlas correctamente.")
            
            target_sentence = config.get('target_sentence', '')
            translation = config.get('translation', '')
            
            if translation:
                st.markdown(f"**Traducción:** *{translation}*")
            
            # Inicializar estado del rompecabezas
            puzzle_key = f"puzzle_{challenge.id}_{current_stage}"
            if puzzle_key not in st.session_state:
                import random
                words = target_sentence.split()
                distractors = config.get('distractors', [])
                all_words = words + distractors
                random.shuffle(all_words)
                st.session_state[puzzle_key] = {
                    'bank': all_words,
                    'answer': []
                }
            
            state = st.session_state[puzzle_key]
            
            # Área de respuesta
            st.markdown("##### Tu Respuesta:")
            answer_cols = st.columns(max(1, len(state['answer']) + 1))
            for i, word in enumerate(state['answer']):
                if answer_cols[i].button(word, key=f"ans_{i}_{puzzle_key}"):
                    state['answer'].pop(i)
                    state['bank'].append(word)
                    st.rerun()
                    
            st.markdown("---")
            
            # Banco de palabras
            st.markdown("##### Palabras Disponibles:")
            # Organizar en filas de 4 botones
            bank_words = state['bank']
            rows = [bank_words[i:i + 4] for i in range(0, len(bank_words), 4)]
            
            for r_idx, row in enumerate(rows):
                cols = st.columns(4)
                for c_idx, word in enumerate(row):
                    if cols[c_idx].button(word, key=f"bank_{r_idx}_{c_idx}_{puzzle_key}"):
                        state['bank'].remove(word)
                        state['answer'].append(word)
                        st.rerun()
            
            # Guardar respuesta para verificación
            st.session_state['user_answers']['ordered_words'] = state['answer']
        
        elif challenge.challenge_type == 'match_pairs':
            st.markdown("#### 🔗 Parejas: Une los términos")
            st.info("Selecciona un término de la izquierda y su pareja de la derecha.")
            
            pairs = config.get('pairs', [])
            
            # Inicializar estado
            match_key = f"match_{challenge.id}_{current_stage}"
            if match_key not in st.session_state:
                import random
                left_items = [p['left'] for p in pairs]
                right_items = [p['right'] for p in pairs]
                random.shuffle(left_items)
                random.shuffle(right_items)
                
                st.session_state[match_key] = {
                    'left_items': left_items,
                    'right_items': right_items,
                    'matches': {}, # left -> right
                    'selected_left': None,
                    'completed': set() # set of left items
                }
            
            state = st.session_state[match_key]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Latín**")
                for item in state['left_items']:
                    # Estilo condicional
                    disabled = item in state['completed']
                    type_ = "primary" if state['selected_left'] == item else "secondary"
                    if item in state['matches']:
                        type_ = "primary" # Ya emparejado (aunque disabled)
                    
                    if st.button(item, key=f"left_{item}_{match_key}", disabled=disabled, type=type_, width="stretch"):
                        state['selected_left'] = item
                        st.rerun()
                        
            with col2:
                st.markdown("**Español / Gramática**")
                for item in state['right_items']:
                    # Verificar si este item ya fue emparejado
                    is_matched = False
                    matched_left = None
                    for l, r in state['matches'].items():
                        if r == item:
                            is_matched = True
                            matched_left = l
                            break
                    
                    disabled = is_matched
                    
                    if st.button(item, key=f"right_{item}_{match_key}", disabled=disabled, width="stretch"):
                        if state['selected_left']:
                            # Registrar intento de match
                            state['matches'][state['selected_left']] = item
                            state['completed'].add(state['selected_left'])
                            state['selected_left'] = None
                            st.rerun()
                        else:
                            st.warning("Primero selecciona un término de la columna izquierda.")
        
            # Guardar respuestas para verificación
            st.session_state['user_answers']['matches'] = state['matches']
        
        # Botones de acción
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("🔄 Reiniciar Desafío", width="stretch"):
                st.session_state.pop('user_answers', None)
                st.session_state.pop('challenge_stage', None)
                st.rerun()
        
        with col2:
            submit = st.button("✅ Verificar", type="primary", width="stretch")
        
        # Verificar respuestas
        if submit:
            st.markdown("---")
            st.markdown("## 📊 Resultados")
            
            # Crear instancia del motor
            engine = ChallengeEngine()
            
            # Verificar
            with st.spinner("Verificando..."):
                score, errors, feedback = engine.verify_challenge(challenge, st.session_state['user_answers'], config_override=config)
            
            # Mostrar resultado
            st.metric("Puntuación", f"{score:.0f}%")
            
            if score >= 60: # Aprobado el ejercicio actual
                st.success("✅ ¡Correcto!")
                
                # Avanzar etapa
                next_stage = current_stage + 1
                
                # Actualizar progreso en BD
                progress = session.exec(
                    select(UserChallengeProgress).where(
                        UserChallengeProgress.challenge_id == challenge.id
                    )
                ).first()
                
                if progress:
                    # Actualizar estrellas (1 estrella por ejercicio completado)
                    # Aseguramos que no baje si ya tenía más
                    if next_stage > progress.stars:
                        progress.stars = next_stage
                    
                    # Si completó las 3 etapas
                    if next_stage >= 3:
                        progress.status = 'completed'
                        progress.completed_at = datetime.now()
                        progress.best_score = 100 # Asumimos 100 si completó todo
                        
                        # Desbloquear siguiente nivel
                        next_challenge_obj = session.exec(
                            select(Challenge).where(Challenge.order == challenge.order + 1)
                        ).first()
                        
                        if next_challenge_obj:
                            next_progress = session.exec(
                                select(UserChallengeProgress).where(
                                    UserChallengeProgress.challenge_id == next_challenge_obj.id
                                )
                            ).first()
                            
                            if next_progress and next_progress.status == 'locked':
                                next_progress.status = 'unlocked'
                                next_progress.unlocked_at = datetime.now()
                                st.balloons()
                                st.success(f"🎉 ¡Desbloqueaste el nivel {next_challenge_obj.order}: {next_challenge_obj.title}!")
                    
                    session.commit()
                
                # Lógica de UI para siguiente paso
                if next_stage < 3:
                    st.success(f"✅ ¡Correcto! Has ganado la estrella #{next_stage}.")
                    st.info("🔄 Cargando siguiente ejercicio...")
                    
                    # Actualizar estado para el siguiente ejercicio
                    st.session_state['challenge_stage'] = next_stage
                    st.session_state.pop('user_answers', None)
                    
                    # Auto-avance con pequeña pausa
                    import time
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.success("🏆 ¡Nivel Completado! Has obtenido las 3 estrellas.")
                    st.balloons()
                    
                    # Auto-avance al siguiente nivel
                    next_challenge_obj = session.exec(
                        select(Challenge).where(Challenge.order == challenge.order + 1)
                    ).first()
                    
                    if next_challenge_obj:
                        st.info(f"Avanzando al nivel {next_challenge_obj.order}...")
                        import time
                        time.sleep(2)
                        st.session_state.pop('user_answers', None)
                        st.session_state.pop('challenge_stage', None)
                        st.session_state['current_challenge_id'] = next_challenge_obj.id
                        st.rerun()
                    else:
                        st.success("¡Has completado todos los niveles disponibles!")
                        st.info("Ve al tab '🗺️ Aventura' para ver tu progreso completo")
        
            else:
                st.error("❌ Incorrecto. Inténtalo de nuevo.")
                if errors:
                    with st.expander("Ver errores"):
                        for error in errors:
                            st.markdown(f"- {error}")
                
                if st.button("🔄 Reintentar"):
                    st.session_state.pop('user_answers', None)
                    st.rerun()
