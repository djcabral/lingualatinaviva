"""
Componentes UI Reutilizables (UI Components)
Componentes comunes para mantener la cohesión visual a través de todos los módulos.
"""

import streamlit as st
from typing import List, Dict, Optional


def render_breadcrumbs(path: List[Dict[str, str]]):
    """
    Renderiza breadcrumbs de navegación.
    
    Args:
        path: Lista de dict con 'label' y 'url'
              Ej: [{'label': '🏠 Inicio', 'url': None}, {'label': '📘 Lección 3', 'url': '/Curso'}]
    """
    breadcrumb_html = " \u003e ".join([
        f"\u003ca href='{item['url']}' style='text-decoration: none; color: #8b4513;'\u003e{item['label']}\u003c/a\u003e"
        if item.get('url') else
        f"\u003cspan style='color: #666;'\u003e{item['label']}\u003c/span\u003e"
        for item in path
    ])
    
    st.markdown(
        f"\u003cdiv style='padding: 10px 0; font-size: 0.9em; color: #666;'\u003e{breadcrumb_html}\u003c/div\u003e",
        unsafe_allow_html=True
    )


def render_lesson_context(lesson_number: int, lesson_title: str, progress_percentage: float):
    """
    Renderiza un widget de contexto de lección en el sidebar.
    
    Args:
        lesson_number: Número de lección (1-40)
        lesson_title: Título de la lección
        progress_percentage: Porcentaje de progreso (0.0-1.0)
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        \u003cdiv style='background: linear-gradient(135deg, rgba(139,69,19,0.1), rgba(210,180,140,0.1)); 
                    padding: 15px; border-radius: 10px; border-left: 4px solid #8b4513;'\u003e
            \u003ch4 style='margin: 0 0 10px 0; color: #8b4513;'\u003e📍 Estás en:\u003c/h4\u003e
            \u003cp style='margin: 5px 0; font-size: 1.1em; font-weight: bold;'\u003e
                Lección {lesson_number}: {lesson_title}
            \u003c/p\u003e
            \u003cp style='margin: 5px 0; font-size: 0.9em; color: #666;'\u003e
                Progreso: {progress_percentage:.0%}
            \u003c/p\u003e
        \u003c/div\u003e
        """,
        unsafe_allow_html=True
    )
    
    # Barra de progreso
    st.sidebar.progress(progress_percentage)


def render_quick_links(lesson_number: int, links: Dict[str, str]):
    """
    Renderiza enlaces rápidos contextuales.
    
    Args:
        lesson_number: Número de lección
        links: Dict con formato {'label': 'status'}
               status puede ser: 'available', 'locked', 'completed'
               Ej: {'📘 Teoría': 'completed', '🎴 Vocabulario': 'available', '📖 Lectura': 'locked'}
    """
    st.sidebar.markdown(f"### Lección {lesson_number}:")
    
    for label, status in links.items():
        if status == 'completed':
            icon = "✅"
            color = "#28a745"
        elif status == 'available':
            icon = "▶"
            color = "#8b4513"
        elif status == 'locked':
            icon = "🔒"
            color = "#999"
        else:
            icon = "⏸"
            color = "#666"
        
        st.sidebar.markdown(
            f"\u003cspan style='color: {color};'\u003e{icon} {label}\u003c/span\u003e",
            unsafe_allow_html=True
        )


def render_progress_bar(current: int, total: int, label: str, show_percentage: bool = True):
    """
    Renderiza una barra de progreso personalizada.
    
    Args:
        current: Valor actual
        total: Valor total
        label: Etiqueta descriptiva
        show_percentage: Si mostrar el porcentaje
    """
    percentage = current / total if total > 0 else 0
    
    progress_html = f"""
    \u003cdiv style='margin: 10px 0;'\u003e
        \u003cdiv style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'\u003e
            \u003cspan style='font-weight: bold; color: #8b4513;'\u003e{label}\u003c/span\u003e
            \u003cspan style='color: #666; font-size: 0.9em;'\u003e{current}/{total}"""
    
    if show_percentage:
        progress_html += f" ({percentage:.0%})"
    
    progress_html += f"""\u003c/span\u003e
        \u003c/div\u003e
        \u003cdiv style='background: #f0f0f0; border-radius: 10px; overflow: hidden; height: 20px;'\u003e
            \u003cdiv style='background: linear-gradient(90deg, #8b4513, #d2b48c); 
                         width: {percentage*100}%; height: 100%; transition: width 0.3s ease;'\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/div\u003e
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)


def render_recommendation_card(recommendation: Dict[str, str], index: int = 0):
    """
    Renderiza una tarjeta de recomendación.
    
    Args:
        recommendation: Dict con 'priority', 'message', 'action_label', 'action_url'
        index: Índice único para identificar esta recomendación (default: 0)
    """
    priority = recommendation.get('priority', 'medium')
    
    if priority == 'high':
        border_color = "#dc3545"
        icon = "🔴"
    elif priority == 'medium':
        border_color = "#ffc107"
        icon = "🟡"
    else:
        border_color = "#6c757d"
        icon = "⚪"
    
    card_html = f"""
    \u003cdiv style='background: white; border-left: 5px solid {border_color}; 
                padding: 15px; margin: 10px 0; border-radius: 5px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'\u003e
        \u003cdiv style='display: flex; align-items: center; gap: 10px;'\u003e
            \u003cspan style='font-size: 1.5em;'\u003e{icon}\u003c/span\u003e
            \u003cspan style='flex: 1;'\u003e{recommendation['message']}\u003c/span\u003e
        \u003c/div\u003e
    \u003c/div\u003e
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Botón de acción si existe
    if recommendation.get('action_label'):
        # Usar hash del mensaje + índice para garantizar unicidad
        unique_key = f"rec_{hash(recommendation['message'])}_{index}"
        if st.button(recommendation['action_label'], key=unique_key):
            st.switch_page(recommendation.get('action_url', 'pages/01_🏠_Inicio.py'))


def render_stat_box(value: str, label: str, icon: str = ""):
    """
    Renderiza una caja de estadística.
    
    Args:
        value: Valor principal a mostrar
        label: Etiqueta descriptiva
        icon: Emoji o icono opcional
    """
    st.markdown(
        f"""
        \u003cdiv style='background: linear-gradient(135deg, rgba(139,69,19,0.05), rgba(210,180,140,0.05)); 
                    padding: 20px; border-radius: 10px; text-align: center; 
                    border: 2px solid rgba(139,69,19,0.2); min-height: 120px;
                    display: flex; flex-direction: column; justify-content: center;'\u003e
            \u003cdiv style='font-size: 2.5em; font-weight: bold; color: #8b4513; margin-bottom: 5px;'\u003e
                {icon} {value}
            \u003c/div\u003e
            \u003cdiv style='font-size: 0.9em; color: #666; text-transform: uppercase; letter-spacing: 1px;'\u003e
                {label}
            \u003c/div\u003e
        \u003c/div\u003e
        """,
        unsafe_allow_html=True
    )


def render_unlock_message(content_type: str, content_name: str, requirements: List[str]):
    """
    Renderiza un mensaje de contenido bloqueado con requisitos.
    
    Args:
        content_type: Tipo de contenido ("Lectura", "Ejercicios", "Desafío")
        content_name: Nombre específico
        requirements: Lista de requisitos no cumplidos
    """
    st.markdown(
        f"""
        \u003cdiv style='background: #fff3cd; border: 2px solid #ffc107; 
                    padding: 20px; border-radius: 10px; margin: 20px 0;'\u003e
            \u003ch4 style='color: #856404; margin-top: 0;'\u003e🔒 {content_type} Bloqueado: {content_name}\u003c/h4\u003e
            \u003cp style='color: #856404; margin-bottom: 10px;'\u003e
                \u003cstrong\u003eRequisitos pendientes:\u003c/strong\u003e
            \u003c/p\u003e
            \u003cul style='color: #856404; margin: 0; padding-left: 20px;'\u003e
        """,
        unsafe_allow_html=True
    )
    
    for req in requirements:
        st.markdown(f"\u003cli\u003e{req}\u003c/li\u003e", unsafe_allow_html=True)
    
    st.markdown("\u003c/ul\u003e\u003c/div\u003e", unsafe_allow_html=True)


def render_success_message(title: str, message: str, rewards: Optional[List[str]] = None):
    """
    Renderiza un mensaje de éxito con recompensas opcionales.
    
    Args:
        title: Título del mensaje
        message: Mensaje principal
        rewards: Lista de recompensas obtenidas (opcional)
    """
    st.markdown(
        f"""
        \u003cdiv style='background: #d4edda; border: 2px solid #28a745; 
                    padding: 20px; border-radius: 10px; margin: 20px 0;'\u003e
            \u003ch3 style='color: #155724; margin-top: 0;'\u003e✅ {title}\u003c/h3\u003e
            \u003cp style='color: #155724; font-size: 1.1em;'\u003e{message}\u003c/p\u003e
        """,
        unsafe_allow_html=True
    )
    
    if rewards:
        st.markdown(
            "\u003cp style='color: #155724; margin-bottom: 5px;'\u003e\u003cstrong\u003eRecompensas:\u003c/strong\u003e\u003c/p\u003e",
            unsafe_allow_html=True
        )
        for reward in rewards:
            st.markdown(f"- {reward}", unsafe_allow_html=False)
    
    st.markdown("\u003c/div\u003e", unsafe_allow_html=True)


def render_lesson_practice_section(lesson_number: int, unlocked_items: Dict[str, bool]):
    """
    Renderiza la sección "Practica esta Lección" al final de una lección de gramática.
    
    Args:
        lesson_number: Número de lección
        unlocked_items: Dict indicando qué está desbloqueado
                       {'vocab': True, 'exercises': False, 'reading': False, 'challenge': False}
    """
    st.markdown("---")
    st.markdown(f"## 🎯 Practica esta Lección")
    st.markdown(f"Has completado la teoría de **Lección {lesson_number}**. Ahora es momento de aplicar lo aprendido:")
    
    # Vocabulario
    if unlocked_items.get('vocab', True):
        st.markdown(
            """
            ### 📚 Vocabulario Esencial
            Las palabras clave para dominar esta lección.
            """)
        if st.button(f"Ver Vocabulario de Lección {lesson_number}", key="btn_vocab"):
            st.switch_page("pages/03_🧠_Memorización.py")
    else:
        st.markdown("### 🔒 Vocabulario Esencial\nSe desbloqueará al completar la lección.")
    
    st.markdown("")
    
    # Ejercicios
    if unlocked_items.get('exercises', False):
        st.markdown(
            """
            ### 📜 Ejercicios de Práctica
            Practica con ejercicios específicos de esta lección.
            """)
        if st.button(f"Ir a Ejercicios", key="btn_exercises"):
            st.switch_page("pages/04_⚔️_Práctica.py")
    else:
        st.markdown("### 🔒 Ejercicios de Práctica\n*Se desbloqueará cuando domines 50% del vocabulario*")
    
    st.markdown("")
    
    # Lectura
    if unlocked_items.get('reading', False):
        st.markdown(
            """
            ### 📖 Lectura Aplicada
            Lee textos que usan el vocabulario y gramática de esta lección.
            """)
        if st.button("Ver Lecturas", key="btn_reading"):
            st.switch_page("pages/02_📘_Lecciones.py")
    else:
        st.markdown("### 🔒 Lectura Aplicada\n*Se desbloqueará al completar 5 ejercicios con 70%+ de precisión*")
    
    st.markdown("")
    
    # Desafío
    if unlocked_items.get('challenge', False):
        st.markdown(
            """
            ### 🎯 Desafío Final
            Demuestra tu dominio completo de esta lección.
            """)
        if st.button("Tomar Desafío", key="btn_challenge"):
            st.switch_page("pages/04_⚔️_Práctica.py")
    else:
        st.markdown("### 🔒 Desafío Final\n*Se desbloqueará al completar: Vocabulario 80% + Ejercicios + Lectura + Análisis sintáctico*")
