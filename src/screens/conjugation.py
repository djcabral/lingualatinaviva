from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, DataTable
from textual.containers import Container, Vertical, Horizontal
from sqlmodel import select
from ..database import get_session
from database.models import Word
from ..latin_logic import LatinMorphology
import random

from ..i18n import get_text

class ConjugationScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(get_text('conjugation'), classes="title"),
            Label("", id="conj-word", classes="latin-word"),
            Container(
                DataTable(id="conj-table"),
                id="table-container"
            ),
            Horizontal(
                Button(get_text('new_word'), id="btn-new"),
                Button(get_text('dashboard'), id="btn-back"),
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(f"{get_text('person')}", get_text('singular'), get_text('plural'))
        self.load_new_word()

    def load_new_word(self):
        with get_session() as session:
            # Fetch verbs only
            statement = select(Word).where(Word.part_of_speech == "verb")
            words = session.exec(statement).all()
            
            if not words:
                self.query_one("#conj-word").update(get_text('no_words'))
                return

            word = random.choice(words)
            self.query_one("#conj-word").update(f"{word.latin} ({word.principal_parts})")
            
            # Generate forms
            forms = LatinMorphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts)
            
            table = self.query_one(DataTable)
            table.clear()
            
            if forms:
                # Present
                table.add_row(get_text('present'), "", "")
                table.add_row("1. ", forms.get("pres_1sg", "-"), forms.get("pres_1pl", "-"))
                table.add_row("2. ", forms.get("pres_2sg", "-"), forms.get("pres_2pl", "-"))
                table.add_row("3. ", forms.get("pres_3sg", "-"), forms.get("pres_3pl", "-"))
                
                # Imperfect
                table.add_row(get_text('imperfect'), "", "")
                table.add_row("1. ", forms.get("imp_1sg", "-"), forms.get("imp_1pl", "-"))
                table.add_row("2. ", forms.get("imp_2sg", "-"), forms.get("imp_2pl", "-"))
                table.add_row("3. ", forms.get("imp_3sg", "-"), forms.get("imp_3pl", "-"))

                # Perfect
                table.add_row(get_text('perfect'), "", "")
                table.add_row("1. ", forms.get("perf_1sg", "-"), forms.get("perf_1pl", "-"))
                table.add_row("2. ", forms.get("perf_2sg", "-"), forms.get("perf_2pl", "-"))
                table.add_row("3. ", forms.get("perf_3sg", "-"), forms.get("perf_3pl", "-"))

            else:
                table.add_row("Error", "Generating", "Forms")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.switch_screen("dashboard")
        elif event.button.id == "btn-new":
            self.load_new_word()
