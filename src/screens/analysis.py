from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label
from textual.containers import Container, Vertical, Horizontal
from sqlmodel import select
from ..database import get_session
from database.models import Word
from ..latin_logic import LatinMorphology
import random

from ..i18n import get_text

class AnalysisScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(get_text('analysis'), classes="title"),
            Container(
                Label("Forma:", classes="label"),
                Label("", id="target-form", classes="latin-word"),
                Label("", id="analysis-result", classes="hidden"),
                id="analysis-container"
            ),
            Horizontal(
                Button(get_text('reveal'), id="btn-reveal"),
                Button(get_text('new_form'), id="btn-new"),
                Button(get_text('dashboard'), id="btn-back"),
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        self.load_new_form()

    def load_new_form(self):
        self.query_one("#analysis-result").update("")
        self.query_one("#analysis-result").add_class("hidden")
        
        with get_session() as session:
            # Pick a random word
            words = session.exec(select(Word)).all()
            if not words:
                self.query_one("#target-form").update("No words found.")
                return

            word = random.choice(words)
            
            # Generate a random form to analyze
            if word.part_of_speech == "noun":
                forms = LatinMorphology.decline_noun(word.latin, word.declension, word.gender, word.genitive, word.irregular_forms)
                if forms:
                    case = random.choice(list(forms.keys()))
                    form = forms[case]
                    self.target_analysis = f"{word.latin}: {case} ({word.gender})"
                    self.query_one("#target-form").update(form)
                else:
                    self.load_new_form() # Retry
            elif word.part_of_speech == "verb":
                forms = LatinMorphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts)
                if forms:
                    key = random.choice(list(forms.keys()))
                    form = forms[key]
                    self.target_analysis = f"{word.latin}: {key}"
                    self.query_one("#target-form").update(form)
                else:
                    self.load_new_form()
            elif word.is_invariable:
                # Show invariable word information
                pos_translations = {
                    "adverb": "Adverbio",
                    "preposition": "Preposición",
                    "conjunction": "Conjunción",
                    "interjection": "Interjección"
                }
                pos_display = pos_translations.get(word.part_of_speech, word.part_of_speech)
                self.target_analysis = f"{word.latin} - {pos_display}: {word.translation} (Invariable)"
                self.query_one("#target-form").update(word.latin)
            else:
                self.load_new_form()  # Skip other non-inflected words

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.switch_screen("dashboard")
        elif event.button.id == "btn-new":
            self.load_new_form()
        elif event.button.id == "btn-reveal":
            self.query_one("#analysis-result").update(self.target_analysis)
            self.query_one("#analysis-result").remove_class("hidden")
