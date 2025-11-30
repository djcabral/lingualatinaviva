from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, DataTable, TabbedContent, TabPane
from textual.containers import Container, Vertical, Horizontal
from sqlmodel import select
from ..database import get_session
from database import Word
from ..latin_logic import LatinMorphology
import random

from ..i18n import get_text

class ConjugationScreen(Screen):
    CSS = """
    .conjugation-content {
        height: 1fr;
    }
    
    .table-container {
        height: 1fr;
        overflow: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(get_text('conjugation'), classes="title"),
            Label("", id="conj-word", classes="latin-word"),
            
            TabbedContent(classes="conjugation-content"):
                with TabPane(get_text('indicative')):
                    Container(
                        DataTable(id="table-indicative"),
                        classes="table-container"
                    )
                with TabPane(get_text('subjunctive')):
                    Container(
                        DataTable(id="table-subjunctive"),
                        classes="table-container"
                    )
                with TabPane(get_text('other_forms')): # Imperative & Participles
                    Container(
                        Label(get_text('imperative'), classes="section-title"),
                        DataTable(id="table-imperative"),
                        Label(get_text('participles'), classes="section-title"),
                        DataTable(id="table-participles"),
                        classes="table-container"
                    )

            Horizontal(
                Button(get_text('new_word'), id="btn-new"),
                Button(get_text('dashboard'), id="btn-back"),
                classes="button-row"
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        # Setup Indicative Table
        table_ind = self.query_one("#table-indicative", DataTable)
        table_ind.add_columns(get_text('tense'), get_text('active'), get_text('passive'))
        
        # Setup Subjunctive Table
        table_sub = self.query_one("#table-subjunctive", DataTable)
        table_sub.add_columns(get_text('tense'), get_text('active'), get_text('passive'))
        
        # Setup Imperative Table
        table_imp = self.query_one("#table-imperative", DataTable)
        table_imp.add_columns(get_text('number'), get_text('active'), get_text('passive'))

        # Setup Participles Table
        table_part = self.query_one("#table-participles", DataTable)
        table_part.add_columns("Participio", "Forma", "Declinación")

        self.load_new_word()

    def load_new_word(self):
        with get_session() as session:
            # Fetch verbs only
            statement = select(Word).where(Word.part_of_speech == "verb", Word.status == "active")
            words = session.exec(statement).all()
            
            if not words:
                self.query_one("#conj-word").update(get_text('no_words'))
                return

            word = random.choice(words)
            self.query_one("#conj-word").update(f"{word.latin} ({word.principal_parts})")
            
            # Generate forms
            forms = LatinMorphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts, word.irregular_forms)
            participles = LatinMorphology.get_participles(word.latin, word.conjugation, word.principal_parts)
            
            # --- Indicative ---
            table_ind = self.query_one("#table-indicative", DataTable)
            table_ind.clear()
            
            if forms:
                # Helper to add tense block
                def add_tense_block(tense_name, prefix_act, prefix_pass):
                    table_ind.add_row(Text(tense_name, style="bold"), "", "")
                    for i, person in enumerate(["1. Sg", "2. Sg", "3. Sg", "1. Pl", "2. Pl", "3. Pl"], 1):
                        key_suffix = f"{i}sg" if i <= 3 else f"{i-3}pl"
                        if i <= 3:
                            key_suffix = f"{i}sg"
                        else:
                            key_suffix = f"{i-3}pl"
                            
                        act = forms.get(f"{prefix_act}_{key_suffix}", "-")
                        pas = forms.get(f"{prefix_pass}_{key_suffix}", "-")
                        table_ind.add_row(person, act, pas)
                    table_ind.add_row("", "", "") # Spacer

                # We need to manually construct rows because the previous structure was different
                # Present
                table_ind.add_row(get_text('present'), "", "")
                table_ind.add_row("1. Sg", forms.get("pres_1sg"), forms.get("pres_pass_1sg"))
                table_ind.add_row("2. Sg", forms.get("pres_2sg"), forms.get("pres_pass_2sg"))
                table_ind.add_row("3. Sg", forms.get("pres_3sg"), forms.get("pres_pass_3sg"))
                table_ind.add_row("1. Pl", forms.get("pres_1pl"), forms.get("pres_pass_1pl"))
                table_ind.add_row("2. Pl", forms.get("pres_2pl"), forms.get("pres_pass_2pl"))
                table_ind.add_row("3. Pl", forms.get("pres_3pl"), forms.get("pres_pass_3pl"))
                
                # Imperfect
                table_ind.add_row(get_text('imperfect'), "", "")
                table_ind.add_row("1. Sg", forms.get("imp_1sg"), forms.get("imp_pass_1sg"))
                table_ind.add_row("2. Sg", forms.get("imp_2sg"), forms.get("imp_pass_2sg"))
                table_ind.add_row("3. Sg", forms.get("imp_3sg"), forms.get("imp_pass_3sg"))
                table_ind.add_row("1. Pl", forms.get("imp_1pl"), forms.get("imp_pass_1pl"))
                table_ind.add_row("2. Pl", forms.get("imp_2pl"), forms.get("imp_pass_2pl"))
                table_ind.add_row("3. Pl", forms.get("imp_3pl"), forms.get("imp_pass_3pl"))

                # Future
                table_ind.add_row(get_text('future'), "", "")
                table_ind.add_row("1. Sg", forms.get("fut_1sg"), forms.get("fut_pass_1sg"))
                table_ind.add_row("2. Sg", forms.get("fut_2sg"), forms.get("fut_pass_2sg"))
                table_ind.add_row("3. Sg", forms.get("fut_3sg"), forms.get("fut_pass_3sg"))
                table_ind.add_row("1. Pl", forms.get("fut_1pl"), forms.get("fut_pass_1pl"))
                table_ind.add_row("2. Pl", forms.get("fut_2pl"), forms.get("fut_pass_2pl"))
                table_ind.add_row("3. Pl", forms.get("fut_3pl"), forms.get("fut_pass_3pl"))

                # Perfect
                table_ind.add_row(get_text('perfect'), "", "")
                table_ind.add_row("1. Sg", forms.get("perf_1sg"), forms.get("perf_pass_1sg"))
                table_ind.add_row("2. Sg", forms.get("perf_2sg"), forms.get("perf_pass_2sg"))
                table_ind.add_row("3. Sg", forms.get("perf_3sg"), forms.get("perf_pass_3sg"))
                table_ind.add_row("1. Pl", forms.get("perf_1pl"), forms.get("perf_pass_1pl"))
                table_ind.add_row("2. Pl", forms.get("perf_2pl"), forms.get("perf_pass_2pl"))
                table_ind.add_row("3. Pl", forms.get("perf_3pl"), forms.get("perf_pass_3pl"))

            # --- Subjunctive ---
            table_sub = self.query_one("#table-subjunctive", DataTable)
            table_sub.clear()
            if forms:
                # Present
                table_sub.add_row(get_text('present'), "", "")
                table_sub.add_row("1. Sg", forms.get("pres_subj_1sg"), forms.get("pres_subj_pass_1sg"))
                table_sub.add_row("2. Sg", forms.get("pres_subj_2sg"), forms.get("pres_subj_pass_2sg"))
                table_sub.add_row("3. Sg", forms.get("pres_subj_3sg"), forms.get("pres_subj_pass_3sg"))
                table_sub.add_row("1. Pl", forms.get("pres_subj_1pl"), forms.get("pres_subj_pass_1pl"))
                table_sub.add_row("2. Pl", forms.get("pres_subj_2pl"), forms.get("pres_subj_pass_2pl"))
                table_sub.add_row("3. Pl", forms.get("pres_subj_3pl"), forms.get("pres_subj_pass_3pl"))
                
                # Imperfect
                table_sub.add_row(get_text('imperfect'), "", "")
                table_sub.add_row("1. Sg", forms.get("imp_subj_1sg"), forms.get("imp_subj_pass_1sg"))
                table_sub.add_row("2. Sg", forms.get("imp_subj_2sg"), forms.get("imp_subj_pass_2sg"))
                table_sub.add_row("3. Sg", forms.get("imp_subj_3sg"), forms.get("imp_subj_pass_3sg"))
                table_sub.add_row("1. Pl", forms.get("imp_subj_1pl"), forms.get("imp_subj_pass_1pl"))
                table_sub.add_row("2. Pl", forms.get("imp_subj_2pl"), forms.get("imp_subj_pass_2pl"))
                table_sub.add_row("3. Pl", forms.get("imp_subj_3pl"), forms.get("imp_subj_pass_3pl"))

            # --- Imperative ---
            table_imp = self.query_one("#table-imperative", DataTable)
            table_imp.clear()
            if forms:
                table_imp.add_row("Singular", forms.get("imv_2sg"), forms.get("imv_pass_2sg"))
                table_imp.add_row("Plural", forms.get("imv_2pl"), forms.get("imv_pass_2pl"))

            # --- Participles ---
            table_part = self.query_one("#table-participles", DataTable)
            table_part.clear()
            if participles:
                # Present Active Participle (declinable like 3rd declension adjective)
                pres_act = participles.get("pres_act", "-")
                table_part.add_row(get_text('present') + " Act.", pres_act if pres_act != "-" else "—", "(3ª decl.)")
                
                # Perfect Passive Participle (declinable like 1st/2nd declension adjective)
                perf_pass = participles.get("perf_pass", "-")
                table_part.add_row(get_text('perfect') + " Pas.", perf_pass if perf_pass != "-" else "—", "(1ª/2ª decl.)")
                
                # Future Active Participle (declinable like 1st/2nd declension adjective)
                fut_act = participles.get("fut_act", "-")
                table_part.add_row(get_text('future') + " Act.", fut_act if fut_act != "-" else "—", "(1ª/2ª decl.)")
                
                # Future Passive / Gerundive (declinable like 1st/2nd declension adjective)
                fut_pass = participles.get("fut_pass", "-")
                table_part.add_row("Gerundivo", fut_pass if fut_pass != "-" else "—", "(1ª/2ª decl.)")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.switch_screen("dashboard")
        elif event.button.id == "btn-new":
            self.load_new_word()
