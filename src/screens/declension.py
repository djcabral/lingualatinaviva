from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, Input, DataTable
from textual.containers import Container, Vertical, Horizontal, Grid
from sqlmodel import select
from ..database import get_session
from database.models import Word
from ..latin_logic import LatinMorphology
import random

from ..i18n import get_text

class DeclensionScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(get_text('declension'), classes="title"),
            Label("", id="decl-word", classes="latin-word"),
            Container(
                DataTable(id="decl-table"),
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
        table.add_columns(get_text('case'), get_text('singular'), get_text('plural'))
        self.load_new_word()

    def load_new_word(self):
        with get_session() as session:
            # Fetch nouns only
            statement = select(Word).where(Word.part_of_speech == "noun")
            words = session.exec(statement).all()
            
            if not words:
                self.query_one("#decl-word").update(get_text('no_words'))
                return

            word = random.choice(words)
            self.query_one("#decl-word").update(f"{word.latin} ({word.genitive}, {word.gender})")
            
            # Generate forms
            forms = LatinMorphology.decline_noun(word.latin, word.declension, word.gender, word.genitive, word.irregular_forms)
            
            table = self.query_one(DataTable)
            table.clear()
            
            if forms:
                rows = [
                    (get_text('nominative'), forms.get("nom_sg", "-"), forms.get("nom_pl", "-")),
                    (get_text('genitive'), forms.get("gen_sg", "-"), forms.get("gen_pl", "-")),
                    (get_text('dative'), forms.get("dat_sg", "-"), forms.get("dat_pl", "-")),
                    (get_text('accusative'), forms.get("acc_sg", "-"), forms.get("acc_pl", "-")),
                    (get_text('ablative'), forms.get("abl_sg", "-"), forms.get("abl_pl", "-")),
                ]
                table.add_rows(rows)
            else:
                table.add_row("Error", "Generating", "Forms")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.switch_screen("dashboard")
        elif event.button.id == "btn-new":
            self.load_new_word()
