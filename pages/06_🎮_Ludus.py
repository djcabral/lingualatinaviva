import streamlit as st
import random
from database.connection import get_session
from database import Word, UserVocabularyProgress, LessonVocabulary
from sqlmodel import select, and_, or_
from utils.ui_helpers import load_css

st.set_page_config(
    page_title="Ludus - Juegos",
    page_icon="🎮",
    layout="wide"
)

load_css()
from utils.ui_helpers import render_sidebar_config
render_sidebar_config()

# Custom CSS for premium look
st.markdown("""
<style>
    .word-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        margin: 8px;
        display: inline-block;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-size: 18px;
        font-weight: 600;
        user-select: none;
    }
    .word-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    .word-selected {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
        transform: scale(1.1);
    }
    .urn {
        border-radius: 20px;
        padding: 30px;
        min-height: 200px;
        margin: 15px 0;
        transition: all 0.3s ease;
        border: 3px dashed rgba(255,255,255,0.3);
    }
    .urn-red {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .urn-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .urn-green {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    .urn:hover {
        transform: scale(1.02);
        border-color: rgba(255,255,255,0.6);
    }
    .score-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎮 Ludus - Juegos Didácticos")

# Helper function for word search (module level)
def get_path_between_cells(start, end):
    """Get all cells in a straight line from start to end"""
    r1, c1 = start
    r2, c2 = end
    
    path = []
    
    # Calculate direction
    dr = 0 if r2 == r1 else (1 if r2 > r1 else -1)
    dc = 0 if c2 == c1 else (1 if c2 > c1 else -1)
    
    # Check if it's a valid straight line
    if dr == 0 and dc == 0:
        return [start]
    
    # Check if diagonal is valid
    if dr != 0 and dc != 0:
        if abs(r2 - r1) != abs(c2 - c1):
            return []  # Not a valid diagonal
    
    # Build path
    r, c = r1, c1
    while True:
        path.append((r, c))
        if r == r2 and c == c2:
            break
        r += dr
        c += dc
    
    return path

# Tabs for different games
tabs = st.tabs(["🏺 Clasificador de Palabras", "🔍 Sopa de Letras", "🧩 Crucigramas"])

with tabs[0]:
    st.markdown("### 🏺 Clasifica las Palabras")
    
    # Game configuration
    config_col1, config_col2 = st.columns([2, 1])
    
    with config_col1:
        game_type = st.selectbox(
            "Tipo de Clasificación",
            ["parisyllabic", "gender", "declension"],
            format_func=lambda x: {
                "parisyllabic": "📏 Parisílabas vs Imparisílabas",
                "gender": "⚧ Género (M/F/N)",
                "declension": "📚 Declinación (1ª/2ª/3ª)"
            }[x]
        )
    
    with config_col2:
        difficulty = st.selectbox("Dificultad", ["Fácil (5)", "Normal (8)", "Difícil (12)"])
        word_count = int(difficulty.split("(")[1].split(")")[0])
    
    # Initialize game state
    if st.button("🔄 Nuevo Juego", key="new_game_btn"):
        # Clear all game state
        for key in ['ludus_words', 'ludus_selected', 'ludus_score', 'ludus_attempts']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    if 'ludus_words' not in st.session_state:
        with get_session() as session:
            # Get practice context if exists
            practice_context = st.session_state.get("practice_context")
            lesson_id = practice_context.get("lesson_id") if practice_context and practice_context.get("active") else None
            
            # Build base query based on game type
            if game_type == "parisyllabic":
                base_query = select(Word).where(
                    Word.part_of_speech == "noun",
                    Word.declension == "3"
                )
            elif game_type == "gender":
                base_query = select(Word).where(Word.part_of_speech == "noun")
            else:  # declension
                base_query = select(Word).where(Word.part_of_speech == "noun")
            
            # SMART FILTERING: Prioritize words user has seen
            user_vocab = session.exec(
                select(UserVocabularyProgress).where(UserVocabularyProgress.user_id == 1)
            ).all()
            seen_word_ids = {v.word_id for v in user_vocab if v.times_seen > 0}
            
            # If in lesson context, get lesson vocabulary
            lesson_word_ids = set()
            if lesson_id:
                lesson_vocab = session.exec(
                    select(LessonVocabulary).where(LessonVocabulary.lesson_id == lesson_id)
                ).all()
                lesson_word_ids = {lv.word_id for lv in lesson_vocab}
            
            # Get all candidate words
            all_words = session.exec(base_query).all()
            
            # Prioritize: 1) Lesson vocab, 2) Seen vocab, 3) Frequent words, 4) Random
            priority_words = []
            
            # Priority 1: Lesson vocabulary
            if lesson_word_ids:
                priority_words.extend([w for w in all_words if w.id in lesson_word_ids])
            
            # Priority 2: Words user has seen
            seen_words = [w for w in all_words if w.id in seen_word_ids and w.id not in lesson_word_ids]
            priority_words.extend(seen_words[:word_count // 2])  # Take half from seen
            
            # Priority 3: Fill remaining with any words (preferring frequent ones if available)
            remaining = [w for w in all_words if w not in priority_words]
            random.shuffle(remaining)
            
            # Combine and sample
            candidate_pool = priority_words + remaining
            selected_words = candidate_pool[:word_count] if len(candidate_pool) >= word_count else candidate_pool
            
            st.session_state.ludus_words = {w.latin: {
                'id': w.id,
                'gender': w.gender,
                'declension': w.declension,
                'parisyllabic': w.parisyllabic,
                'translation': w.translation,
                'placed': False,
                'urn': None
            } for w in selected_words}
            
        st.session_state.ludus_selected = None
        st.session_state.ludus_score = 0
        st.session_state.ludus_attempts = 0
    
    # Score display
    if 'ludus_score' in st.session_state:
        placed_count = sum(1 for w in st.session_state.ludus_words.values() if w['placed'])
        total_count = len(st.session_state.ludus_words)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='score-badge'>⭐ {st.session_state.ludus_score} pts</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='score-badge'>📊 {placed_count}/{total_count}</div>", unsafe_allow_html=True)
        with col3:
            accuracy = (st.session_state.ludus_score / max(st.session_state.ludus_attempts, 1)) * 100 if st.session_state.ludus_attempts > 0 else 0
            st.markdown(f"<div class='score-badge'>🎯 {accuracy:.0f}%</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Define urns based on game type
    if game_type == "parisyllabic":
        urns = {
            "red": {"label": "🔴 Parisílabas", "check": lambda w: w['parisyllabic']},
            "blue": {"label": "🔵 Imparisílabas", "check": lambda w: not w['parisyllabic']}
        }
    elif game_type == "gender":
        urns = {
            "red": {"label": "🔴 Masculino", "check": lambda w: w['gender'] == 'm'},
            "blue": {"label": "🔵 Femenino", "check": lambda w: w['gender'] == 'f'},
            "green": {"label": "🟢 Neutro", "check": lambda w: w['gender'] == 'n'}
        }
    else:  # declension
        urns = {
            "red": {"label": "🔴 1ª Declinación", "check": lambda w: w['declension'] == '1'},
            "blue": {"label": "🔵 2ª Declinación", "check": lambda w: w['declension'] == '2'},
            "green": {"label": "🟢 3ª Declinación", "check": lambda w: w['declension'] == '3'}
        }
    
    # Display urns
    urn_cols = st.columns(len(urns))
    
    for idx, (urn_id, urn_data) in enumerate(urns.items()):
        with urn_cols[idx]:
            st.markdown(f"<div class='urn urn-{urn_id}'><h3 style='color:white;'>{urn_data['label']}</h3>", unsafe_allow_html=True)
            
            # Show words in this urn
            for word, data in st.session_state.ludus_words.items():
                if data['urn'] == urn_id:
                    st.markdown(f"**{word}** ({data['translation']})")
            
            # Button to place selected word
            if st.button(f"Colocar aquí ⬇️", key=f"place_{urn_id}", width="stretch"):
                if st.session_state.ludus_selected:
                    word_data = st.session_state.ludus_words[st.session_state.ludus_selected]
                    
                    # Check if correct
                    is_correct = urn_data['check'](word_data)
                    
                    st.session_state.ludus_attempts += 1
                    
                    if is_correct:
                        word_data['placed'] = True
                        word_data['urn'] = urn_id
                        st.session_state.ludus_score += 10
                        st.success(f"✅ ¡Correcto! +10 pts")
                        st.balloons()
                    else:
                        st.session_state.ludus_score = max(0, st.session_state.ludus_score - 5)
                        st.error(f"❌ Incorrecto. -5 pts")
                    
                    st.session_state.ludus_selected = None
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Banco de Palabras")
    st.caption("Haz clic en una palabra y luego en la urna correspondiente")
    
    # Display word bank
    bank_cols = st.columns(4)
    col_idx = 0
    
    for word, data in st.session_state.ludus_words.items():
        if not data['placed']:
            with bank_cols[col_idx % 4]:
                selected_class = "word-selected" if st.session_state.ludus_selected == word else ""
                
                if st.button(
                    f"{word}",
                    key=f"word_{word}",
                    help=data['translation'],
                    width="stretch"
                ):
                    st.session_state.ludus_selected = word
                    st.rerun()
            
            col_idx += 1
    
    # Check for completion
    if all(w['placed'] for w in st.session_state.ludus_words.values()):
        st.success("🎉 ¡Juego Completado!")
        st.balloons()
        
        final_score = st.session_state.ludus_score
        if final_score >= 80:
            st.markdown("### ⭐⭐⭐ ¡Perfecto!")
        elif final_score >= 60:
            st.markdown("### ⭐⭐ ¡Muy Bien!")
        else:
            st.markdown("### ⭐ ¡Bien!")

with tabs[1]:
    st.markdown("### 🔍 Sopa de Letras")
    st.caption("Encuentra las palabras latinas escondidas en el grid")
    
    # Configuration
    ws_col1, ws_col2 = st.columns([2, 1])
    
    with ws_col1:
        ws_difficulty = st.selectbox(
            "Tamaño del Grid",
            ["Pequeño (8x8)", "Mediano (10x10)", "Grande (12x12)"],
            key="ws_diff"
        )
        grid_size = int(ws_difficulty.split("(")[1].split("x")[0])
    
    with ws_col2:
        ws_word_count = st.selectbox("Palabras", [3, 5, 7, 10], key="ws_words")
    
    # Initialize word search
    if st.button("🔄 Nuevo Puzzle", key="new_ws") or 'ws_grid' not in st.session_state:
        # Clear state
        for key in ['ws_grid', 'ws_positions', 'ws_words_list', 'ws_found', 'ws_selection']:
            if key in st.session_state:
                del st.session_state[key]
        
        # Get words
        with get_session() as session:
            practice_context = st.session_state.get("practice_context")
            lesson_id = practice_context.get("lesson_id") if practice_context and practice_context.get("active") else None
            
            # Get vocabulary
            query = select(Word).where(Word.part_of_speech.in_(["noun", "verb", "adjective"]))
            
            # Smart filtering (same as classifier)
            user_vocab = session.exec(
                select(UserVocabularyProgress).where(UserVocabularyProgress.user_id == 1)
            ).all()
            seen_word_ids = {v.word_id for v in user_vocab if v.times_seen > 0}
            
            lesson_word_ids = set()
            if lesson_id:
                lesson_vocab = session.exec(
                    select(LessonVocabulary).where(LessonVocabulary.lesson_id == lesson_id)
                ).all()
                lesson_word_ids = {lv.word_id for lv in lesson_vocab}
            
            all_words = session.exec(query).all()
            
            # Prioritize lesson/seen words
            priority_words = [w for w in all_words if w.id in lesson_word_ids or w.id in seen_word_ids]
            remaining = [w for w in all_words if w not in priority_words]
            
            candidate_pool = priority_words + remaining
            selected_words = candidate_pool[:ws_word_count]
            
            word_list = [w.latin.lower() for w in selected_words]
            
            # Generate grid
            from pages.modules.ludus_generator import generate_word_search
            grid, positions = generate_word_search(word_list, grid_size)
            
            st.session_state.ws_grid = grid
            st.session_state.ws_positions = positions
            st.session_state.ws_words_list = word_list
            st.session_state.ws_found = set()
            st.session_state.ws_selection = []
            st.session_state.ws_words_info = {w.latin.lower(): w.translation for w in selected_words}
        
        st.rerun()
    
    # Display score
    if 'ws_found' in st.session_state:
        found_count = len(st.session_state.ws_found)
        total_count = len(st.session_state.ws_words_list)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='score-badge'>📊 {found_count}/{total_count} Encontradas</div>", unsafe_allow_html=True)
        with col2:
            progress_pct = (found_count / total_count) * 100 if total_count > 0 else 0
            st.markdown(f"<div class='score-badge'>🎯 {progress_pct:.0f}%</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display grid
    if 'ws_grid' in st.session_state:
        grid = st.session_state.ws_grid
        
        # Custom CSS for grid cells
        st.markdown("""
        <style>
            .ws-cell {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 18px;
                font-weight: bold;
                margin: 2px;
            }
            .ws-cell-found {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Selection instructions
        st.info("🎯 **Cómo jugar**: Haz clic en la primera letra de una palabra, luego en la última letra. El sistema verificará si encontraste una palabra.")
        
        # Display grid with buttons
        for i, row in enumerate(grid):
            cols = st.columns(len(row))
            for j, cell in enumerate(row):
                with cols[j]:
                    # Check states
                    is_found = any(
                        (i, j) in st.session_state.ws_positions.get(word, [])
                        for word in st.session_state.ws_found
                    )
                    
                    is_selected = (i, j) in st.session_state.ws_selection
                    
                    # Button styling
                    if is_found:
                        button_type = "primary"
                        label = f"✅ {cell}"
                    elif is_selected:
                        button_type = "secondary"
                        label = f"👉 {cell}"
                    else:
                        button_type = "secondary"
                        label = cell
                    
                    if st.button(
                        label,
                        key=f"ws_cell_{i}_{j}",
                        width="stretch",
                        type=button_type,
                        disabled=is_found
                    ):
                        # Toggle selection
                        if (i, j) in st.session_state.ws_selection:
                            st.session_state.ws_selection.remove((i, j))
                        else:
                            st.session_state.ws_selection.append((i, j))
                        
                        # If we have 2+ cells selected, try to validate
                        if len(st.session_state.ws_selection) >= 2:
                            start = st.session_state.ws_selection[0]
                            end = st.session_state.ws_selection[-1]
                            
                            # Get path between cells
                            path = get_path_between_cells(start, end)
                            
                            # Check if path matches any word
                            word_from_path = ''.join([grid[r][c] for r, c in path]).lower()
                            
                            found_word = None
                            for word in st.session_state.ws_words_list:
                                if word not in st.session_state.ws_found:
                                    # Check forward and backward
                                    if word_from_path == word or word_from_path[::-1] == word:
                                        found_word = word
                                        break
                            
                            if found_word:
                                st.session_state.ws_found.add(found_word)
                                st.success(f"✅ ¡Encontraste: {found_word.upper()}!")
                                st.session_state.ws_selection = []
                                st.balloons()
                            else:
                                if len(st.session_state.ws_selection) > 2:
                                    # Clear if too many wrong selections
                                    st.session_state.ws_selection = []
                                    st.error("❌ Esa no es una palabra válida")
                        
                        st.rerun()
        
        st.markdown("---")
        
        # Words to find
        st.markdown("### 📝 Palabras a Encontrar")
        
        word_cols = st.columns(3)
        for idx, word in enumerate(st.session_state.ws_words_list):
            with word_cols[idx % 3]:
                translation = st.session_state.ws_words_info.get(word, "")
                if word in st.session_state.ws_found:
                    st.success(f"✅ **{word.upper()}** ({translation})")
                else:
                    st.info(f"❌ **{word.upper()}** ({translation})")
        
        # Auto-check for words (simplified - in real implementation would need selection mechanism)
        if st.button("🔍 Buscar Automáticamente", key="auto_find"):
            st.session_state.ws_found = set(st.session_state.ws_words_list)
            st.rerun()

with tabs[2]:
    st.markdown("### 🧩 Crucigrama Latino")
    st.caption("Completa el crucigrama con vocabulario latino")
    
    # Configuration
    cw_difficulty = st.selectbox(
        "Dificultad",
        ["Fácil (3 palabras)", "Normal (5 palabras)", "Difícil (7 palabras)"],
        key="cw_diff"
    )
    cw_word_count = int(cw_difficulty.split("(")[1].split()[0])
    
    # Initialize crossword
    if st.button("🔄 Nuevo Crucigrama", key="new_cw"):
        # Clear state
        for key in ['cw_words', 'cw_answers', 'cw_grid_size']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    if 'cw_words' not in st.session_state:
        with get_session() as session:
            practice_context = st.session_state.get("practice_context")
            lesson_id = practice_context.get("lesson_id") if practice_context and practice_context.get("active") else None
            
            # Get vocabulary with translations
            query = select(Word).where(
                Word.part_of_speech.in_(["noun", "verb", "adjective"]),
                Word.translation != None
            )
            
            # Smart filtering
            user_vocab = session.exec(
                select(UserVocabularyProgress).where(UserVocabularyProgress.user_id == 1)
            ).all()
            seen_word_ids = {v.word_id for v in user_vocab if v.times_seen > 0}
            
            lesson_word_ids = set()
            if lesson_id:
                lesson_vocab = session.exec(
                    select(LessonVocabulary).where(LessonVocabulary.lesson_id == lesson_id)
                ).all()
                lesson_word_ids = {lv.word_id for lv in lesson_vocab}
            
            all_words = session.exec(query).all()
            
            # Prioritize
            priority_words = [w for w in all_words if w.id in lesson_word_ids or w.id in seen_word_ids]
            remaining = [w for w in all_words if w not in priority_words]
            
            candidate_pool = priority_words + remaining
            selected_words = candidate_pool[:cw_word_count]
            
            # Simplified crossword layout (horizontal and vertical)
            st.session_state.cw_words = [
                {
                    'word': w.latin.lower(),
                    'clue': w.translation,
                    'direction': 'horizontal' if i % 2 == 0 else 'vertical',
                    'row': i * 2,
                    'col': i if i % 2 == 0 else 0,
                    'number': i + 1
                }
                for i, w in enumerate(selected_words)
            ]
            st.session_state.cw_answers = {}
            st.session_state.cw_grid_size = max(8, cw_word_count * 2)
        
        st.rerun()
    
    # Display clues and inputs
    if 'cw_words' in st.session_state:
        # Score
        if 'cw_answers' in st.session_state:
            correct_count = sum(
                1 for entry in st.session_state.cw_words
                if st.session_state.cw_answers.get(entry['number'], '').lower() == entry['word']
            )
            total_count = len(st.session_state.cw_words)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div class='score-badge'>✅ {correct_count}/{total_count} Correctas</div>", unsafe_allow_html=True)
            with col2:
                progress_pct = (correct_count / total_count) * 100 if total_count > 0 else 0
                st.markdown(f"<div class='score-badge'>🎯 {progress_pct:.0f}%</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display clues and input fields
        st.markdown("### 📝 Pistas")
        
        horizontal = [w for w in st.session_state.cw_words if w['direction'] == 'horizontal']
        vertical = [w for w in st.session_state.cw_words if w['direction'] == 'vertical']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ➡️ Horizontal")
            for entry in horizontal:
                num = entry['number']
                clue = entry['clue']
                word_len = len(entry['word'])
                
                user_answer = st.text_input(
                    f"{num}. {clue} ({word_len} letras)",
                    key=f"cw_answer_{num}",
                    max_chars=word_len
                )
                st.session_state.cw_answers[num] = user_answer
                
                # Show feedback if complete
                if len(user_answer) == word_len:
                    if user_answer.lower() == entry['word']:
                        st.success("✅ ¡Correcto!")
                    elif user_answer:
                        st.error("❌ Incorrecto")
        
        with col2:
            st.markdown("#### ⬇️ Vertical")
            for entry in vertical:
                num = entry['number']
                clue = entry['clue']
                word_len = len(entry['word'])
                
                user_answer = st.text_input(
                    f"{num}. {clue} ({word_len} letras)",
                    key=f"cw_answer_{num}",
                    max_chars=word_len
                )
                st.session_state.cw_answers[num] = user_answer
                
                # Show feedback if complete
                if len(user_answer) == word_len:
                    if user_answer.lower() == entry['word']:
                        st.success("✅ ¡Correcto!")
                    elif user_answer:
                        st.error("❌ Incorrecto")
        
        st.markdown("---")
        
        # Check completion
        all_correct = all(
            st.session_state.cw_answers.get(entry['number'], '').lower() == entry['word']
            for entry in st.session_state.cw_words
        )
        
        if all_correct and len(st.session_state.cw_answers) == len(st.session_state.cw_words):
            st.success("🎉 ¡Crucigrama Completado!")
            st.balloons()
            
            if st.button("🏆 Ver Soluciones", key="show_solutions"):
                st.markdown("### ✨ Soluciones")
                for entry in st.session_state.cw_words:
                    st.markdown(f"**{entry['number']}. {entry['clue']}** → `{entry['word'].upper()}`")
