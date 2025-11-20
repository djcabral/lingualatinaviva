from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label
from textual.containers import Container, Vertical, Horizontal, Grid
from sqlmodel import select
from ..database import get_session
from database.models import UserProfile

from ..i18n import get_text

class Dashboard(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(f"🏛️ {get_text('app_title')}", classes="title"),
            Label("*Per aspera ad astra*", classes="subtitle"),
            
            # Stats Row
            Horizontal(
                Container(
                    Label("1", id="level-val", classes="stat-val"),
                    Label(get_text('level'), classes="stat-label"),
                    classes="stat-box"
                ),
                Container(
                    Label("0", id="streak-val", classes="stat-val"),
                    Label(f"{get_text('days')} (Racha)", classes="stat-label"),
                    classes="stat-box"
                ),
                Container(
                    Label("0", id="xp-val", classes="stat-val"),
                    Label(get_text('xp'), classes="stat-label"),
                    classes="stat-box"
                ),
                id="stats-container"
            ),
            
            Label(get_text('today_tasks'), classes="section-title"),
            
            # Tasks Grid
            Grid(
                Button(f"🎴 {get_text('vocabulary')}", id="btn-vocab", classes="task-btn"),
                Button(f"📜 {get_text('declension')}", id="btn-decl", classes="task-btn"),
                Button(f"⚔️ {get_text('conjugation')}", id="btn-conj", classes="task-btn"),
                Button(f"🔍 {get_text('analysis')}", id="btn-anal", classes="task-btn"),
                Button(f"📖 {get_text('reading')}", id="btn-read", classes="task-btn"),
                id="tasks-grid"
            ),
            id="dashboard-container"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.update_stats()

    def update_stats(self):
        with get_session() as session:
            user = session.exec(select(UserProfile)).first()
            if user:
                self.query_one("#level-val", Label).update(str(user.level))
                self.query_one("#streak-val", Label).update(str(user.streak))
                self.query_one("#xp-val", Label).update(str(user.xp))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-vocab":
            self.app.switch_screen("vocabulary")
        elif event.button.id == "btn-decl":
            self.app.switch_screen("declension")
        elif event.button.id == "btn-conj":
            self.app.switch_screen("conjugation")
        elif event.button.id == "btn-anal":
            self.app.switch_screen("analysis")
        elif event.button.id == "btn-read":
            self.app.switch_screen("reading")
