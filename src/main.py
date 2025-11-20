from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from textual.screen import Screen

from .database import init_db
from .screens.dashboard import Dashboard
from .screens.vocabulary import VocabularyScreen
from .screens.declension import DeclensionScreen
from .screens.conjugation import ConjugationScreen
from .screens.analysis import AnalysisScreen
from .screens.reading import ReadingScreen

class LinguaLatinaApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Scriptorium Mode"),
        ("q", "quit", "Quit"),
        ("1", "switch_screen('dashboard')", "Dashboard"),
        ("2", "switch_screen('vocabulary')", "Vocabularium"),
        ("3", "switch_screen('declension')", "Declinatio"),
        ("4", "switch_screen('conjugation')", "Conjugatio"),
        ("5", "switch_screen('analysis')", "Analysis"),
        ("6", "switch_screen('reading')", "Lectio"),
    ]
    
    SCREENS = {
        "dashboard": Dashboard,
        "vocabulary": VocabularyScreen,
        "declension": DeclensionScreen,
        "conjugation": ConjugationScreen,
        "analysis": AnalysisScreen,
        "reading": ReadingScreen,
    }

    dark = reactive(False)

    def on_mount(self) -> None:
        init_db()
        self.push_screen("dashboard")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
        if self.dark:
            self.screen.add_class("scriptorium")
        else:
            self.screen.remove_class("scriptorium")

if __name__ == "__main__":
    app = LinguaLatinaApp()
    app.run()
