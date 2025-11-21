from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label
from textual.containers import Container, Vertical, Horizontal
from sqlmodel import select
from database.connection import get_session
from database.models import Word, ReviewLog, UserProfile
from utils.srs import calculate_next_review
import random
from datetime import datetime

from i18n import get_text

class VocabularyScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(get_text('vocabulary'), classes="title"),
            Container(
                Label("", id="card-front", classes="latin-word"),
                Label("", id="card-back"),
                id="card-container"
            ),
            Horizontal(
                Button(get_text('show_answer'), id="btn-show"),
                id="action-bar"
            ),
            Horizontal(
                Button(f"{get_text('again')} (1)", id="btn-1", classes="rating-btn"),
                Button(f"{get_text('hard')} (2)", id="btn-2", classes="rating-btn"),
                Button(f"{get_text('good')} (3)", id="btn-3", classes="rating-btn"),
                Button(f"{get_text('easy')} (4)", id="btn-4", classes="rating-btn"),
                id="rating-bar",
                classes="hidden"
            ),
            Button(get_text('dashboard'), id="btn-back"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.current_word = None
        self.load_next_card()

    def load_next_card(self):
        self.query_one("#rating-bar").add_class("hidden")
        self.query_one("#action-bar").remove_class("hidden")
        self.query_one("#card-back").update("")
        
        with get_session() as session:
            # Simple logic: pick a word that needs review or a new word
            # In a real app, this would be a complex query based on next_review_date
            # For now, random selection for demo
            words = session.exec(select(Word).where(Word.status == 'active')).all()
            if words:
                self.current_word = random.choice(words)
                self.query_one("#card-front").update(self.current_word.latin)
            else:
                self.query_one("#card-front").update("No words found!")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.switch_screen("dashboard")
        elif event.button.id == "btn-show":
            if self.current_word:
                self.query_one("#card-back").update(f"{self.current_word.translation} ({self.current_word.part_of_speech})")
                self.query_one("#action-bar").add_class("hidden")
                self.query_one("#rating-bar").remove_class("hidden")
        elif event.button.id in ["btn-1", "btn-2", "btn-3", "btn-4"]:
            quality = int(event.button.id.split("-")[1]) + 1 # 1-indexed for SM-2 roughly
            self.process_review(quality)
            self.load_next_card()

    def process_review(self, quality: int):
        if not self.current_word:
            return
            
        with get_session() as session:
            # Find previous review
            # For simplicity in this demo, we just create a new log and don't track history deeply
            # In production, we'd fetch the last log for this word
            
            srs_data = calculate_next_review(quality)
            
            log = ReviewLog(
                word_id=self.current_word.id,
                quality=quality,
                ease_factor=srs_data["ease_factor"],
                interval=srs_data["interval"],
                repetitions=srs_data["repetitions"]
            )
            session.add(log)
            
            # Update user XP
            user = session.exec(select(UserProfile)).first()
            if user:
                user.xp += 10
                session.add(user)
                
            session.commit()
