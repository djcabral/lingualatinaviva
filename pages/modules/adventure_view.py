
import streamlit as st
from database.connection import get_session
from database import Challenge, UserChallengeProgress, UserProfile
from sqlmodel import select
from datetime import datetime


def render_content():
    """
    Página: 🗺️ Mapa de Desafíos
    
    Esta página muestra el mapa visual de desafíos progresivos tipo Duolingo.
    El usuario puede ver su progreso y acceder a desafíos desbloqueados.
    
    DOCUMENTACIÓN:
    - Los desafíos se muestran en orden vertical (scroll hacia abajo)
    - Estados: 🔒 Bloqueado, 🔓 Desbloqueado, ▶️ En progreso, ⭐⭐⭐ Completado
    - Solo se puede acceder a desafíos desbloqueados o completados
    - El progreso se guarda automáticamente en UserChallengeProgress
    """
    
    # Si hay un desafío seleccionado, renderizar el desafío en lugar del mapa
    if 'current_challenge_id' in st.session_state:
        # Botón para volver al mapa
        if st.button("← Volver al Mapa", key="back_to_map"):
            st.session_state.pop('current_challenge_id', None)
            st.session_state.pop('user_answers', None)
            st.session_state.pop('challenge_stage', None)
            st.rerun()
        
        # Renderizar el desafío usando challenges_view
        import pages.modules.challenges_view as challenges_view
        challenges_view.render_content(caller="adventure")
        return  # Salir temprano, no mostrar el mapa
    
    # Configuración de la página

    
    # Título principal
    st.title("🗺️ Mapa de Desafíos")
    
    # Check for Practice Context
    practice_context = st.session_state.get("practice_context")
    relevant_challenges = []
    if practice_context and practice_context.get("active"):
        st.info(f"🎯 **Modo Aventura: {practice_context.get('description')}**")
        relevant_challenges = practice_context.get("relevant_challenges", [])
        if st.button("❌ Salir del Modo Aventura", key="exit_context_adv"):
            st.session_state.practice_context = None
            st.rerun()
    else:
        st.markdown("Progresa desbloqueando desafíos en orden. **¡No puedes saltar niveles!**")
    
    st.markdown("---")
    
    # Obtener sesión de BD y cargar datos
    with get_session() as session:
        # Cargar todos los desafíos
        challenges = session.exec(select(Challenge).order_by(Challenge.order)).all()
        
        # Cargar progreso del usuario
        progress_list = session.exec(select(UserChallengeProgress).where(UserChallengeProgress.user_id == 1)).all()
        
        # Verificar si faltan registros de progreso (para nuevos desafíos agregados)
        existing_challenge_ids = {p.challenge_id for p in progress_list}
        missing_challenges = [ch for ch in challenges if ch.id not in existing_challenge_ids]
        
        if missing_challenges:
            # Si es la primera vez absoluta (no hay ningún progreso)
            if not progress_list:
                st.info("Inicializando tu mapa de desafíos...")
                
                # El primero desbloqueado
                first = True
                for ch in challenges:
                    status = 'unlocked' if first else 'locked'
                    new_progress = UserChallengeProgress(
                        user_id=1,
                        challenge_id=ch.id,
                        status=status,
                        unlocked_at=datetime.now() if first else None
                    )
                    session.add(new_progress)
                    first = False
            else:
                # Si ya hay progreso pero faltan nuevos desafíos, agregarlos como bloqueados
                for ch in missing_challenges:
                    new_progress = UserChallengeProgress(
                        user_id=1,
                        challenge_id=ch.id,
                        status='locked'
                    )
                    session.add(new_progress)
            
            session.commit()
            # Recargar progreso actualizado
            progress_list = session.exec(select(UserChallengeProgress).where(UserChallengeProgress.user_id == 1)).all()
        
        # Crear diccionario para acceso rápido
        progress_dict = {p.challenge_id: p for p in progress_list}
        
        # Sidebar: Estadísticas del usuario
        st.sidebar.title("📊 Tu Progreso")
        
        total_stars = sum(p.stars for p in progress_list)
        completed_count = sum(1 for p in progress_list if p.status == 'completed')
        total_challenges = len(challenges)
        
        st.sidebar.metric("⭐ Estrellas Totales", total_stars)
        st.sidebar.metric("✅ Desafíos Completados", f"{completed_count}/{total_challenges}")
        
        if total_challenges > 0:
            progress_pct = (completed_count / total_challenges) * 100
            st.sidebar.metric("📈 Progreso Global", f"{progress_pct:.0f}%")
            st.sidebar.progress(progress_pct / 100)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🏆 Sistema de Estrellas")
        st.sidebar.markdown("""
        - ⭐⭐⭐ = 100% correcto
        - ⭐⭐ = 80-99% correcto
        - ⭐ = 60-79% correcto (mínimo aprobado)
        - Sin estrellas = <60% (debes reintentar)
        """)
        
        # Mostrar mapa de desafíos
        st.markdown("## 🎮 Tus Desafíos")
        
        # Agrupar por fases (cada 10 desafíos)
        phases = {
            'Fase 1: Primera Declinación': list(range(1, 11)),
            'Fase 2: Presente de Indicativo': list(range(11, 21)),
        }
        
        for phase_name, phase_range in phases.items():
            with st.expander(phase_name, expanded=True):
                phase_challenges = [ch for ch in challenges if ch.order in phase_range]
                
                for challenge in phase_challenges:
                    progress = progress_dict.get(challenge.id)
                    
                    # Si por alguna razón extraña aún no hay progreso (no debería pasar con la lógica de arriba),
                    # mostramos un estado por defecto sin escribir en BD para evitar duplicados
                    if not progress:
                        continue # Saltamos para evitar errores, o podríamos mostrar un placeholder
                    
                    # Mostrar desafío según su estado
                    col1, col2, col3 = st.columns([1, 7, 2])
                    
                    with col1:
                        # Icono según estado
                        if progress.status == 'locked':
                            st.markdown("🔒")
                        elif progress.status == 'unlocked':
                            st.markdown("🔓")
                        elif progress.status == 'in_progress':
                            st.markdown("▶️")
                        elif progress.status == 'completed':
                            stars_display = "⭐" * progress.stars
                            st.markdown(f"✅")
                    
                    with col2:
                        # Título y descripción
                        title_prefix = ""
                        if challenge.id in relevant_challenges:
                            title_prefix = "🎯 "
                            
                        if progress.status == 'completed':
                            stars_display = "⭐" * progress.stars
                            st.markdown(f"**{title_prefix}{challenge.order}. {challenge.title}** {stars_display}")
                        else:
                            st.markdown(f"**{title_prefix}{challenge.order}. {challenge.title}**")
                        
                        if challenge.id in relevant_challenges:
                            st.caption(f"🔥 ¡Recomendado para esta lección!")
                        
                        st.caption(challenge.description)
                        
                        # Mostrar stats si está completado
                        if progress.status == 'completed':
                            st.caption(
                                f"📊 Score: {progress.best_score:.0f}% | "
                                f"🔁 Intentos: {progress.attempts}"
                            )
                    
                    with col3:
                        # Botón de acción
                        if progress.status == 'locked':
                            st.button(
                                "🔒 Bloqueado",
                                key=f"btn_locked_{challenge.id}",
                                disabled=True,
                                help="Completa el desafío anterior para desbloquear"
                            )
                        
                        elif progress.status in ['unlocked', 'in_progress']:
                            if st.button(
                                "▶️ Jugar",
                                key=f"btn_play_{challenge.id}",
                                type="primary"
                            ):
                                # Guardar ID del desafío actual en session_state
                                st.session_state['current_challenge_id'] = challenge.id
                                # Limpiar estado previo
                                st.session_state.pop('user_answers', None)
                                st.session_state.pop('challenge_stage', None)
                                # Forzar cambio de tab
                                st.rerun()
                        
                        elif progress.status == 'completed':
                            if st.button(
                                "🔄 Repetir",
                                key=f"btn_replay_{challenge.id}",
                                help="Mejora tu puntuación"
                            ):
                                st.session_state['current_challenge_id'] = challenge.id
                                # Limpiar estado previo para reiniciar
                                st.session_state.pop('user_answers', None)
                                st.session_state.pop('challenge_stage', None)
                                st.rerun()
                    
                    st.markdown("---")
    
    # Footer
    st.markdown("### 💡 Consejo")
    st.info("""
    **Cómo usar el mapa**:
    1. Haz clic en "▶️ Jugar" en el primer desafío desbloqueado
    2. Completa el desafío con al menos 60% de aciertos para aprobarlo
    3. El siguiente desafío se desbloqueará automáticamente
    4. ¡Intenta obtener 3 estrellas en cada desafío!
    """)

