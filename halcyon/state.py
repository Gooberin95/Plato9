"""Session state for filters, the pass hold, the clock, and a personal schedule."""

import asyncio
from datetime import datetime, timezone

import reflex as rx

from halcyon.data import (
    ARTISTS,
    EVENTS,
    GATES_OPEN,
    MOMENTS,
    PASSES,
    ZONES,
    Artist,
    Moment,
    PassOption,
    ProgramEvent,
    Zone,
)


class State(rx.State):
    """One state shared by every page."""

    menu_open: bool = False
    day: str = "Friday"
    stage: str = "All"
    discipline: str = "All"
    selected_name: str = ""
    zone_name: str = "Meadow"
    pass_id: str = "weekend"
    quantity: int = 1
    buyer_name: str = ""
    buyer_email: str = ""
    held: bool = False
    hold_message: str = ""
    moment_index: int = 0
    lightbox_open: bool = False
    newsletter_email: str = ""
    subscribed: bool = False
    newsletter_note: str = ""
    starred: list[str] = []
    clock_days: str = "—"
    clock_hours: str = "—"
    clock_minutes: str = "—"
    clock_seconds: str = "—"
    gates_open: bool = False
    _clock_on: bool = False

    events: list[ProgramEvent] = EVENTS
    artists: list[Artist] = ARTISTS
    zones: list[Zone] = ZONES
    moments: list[Moment] = MOMENTS

    @rx.event
    def set_buyer_name(self, value: str):
        self.buyer_name = value

    @rx.event
    def set_buyer_email(self, value: str):
        self.buyer_email = value

    @rx.event
    def set_newsletter_email(self, value: str):
        self.newsletter_email = value
        self.subscribed = False
        self.newsletter_note = ""

    @rx.event
    def set_lightbox_open(self, open: bool):
        self.lightbox_open = open

    def _write_clock(self) -> None:
        remaining = GATES_OPEN - datetime.now(timezone.utc)
        total = int(remaining.total_seconds())
        if total <= 0:
            self.gates_open = True
            self.clock_days = "0"
            self.clock_hours = "00"
            self.clock_minutes = "00"
            self.clock_seconds = "00"
            return
        self.gates_open = False
        self.clock_days = str(total // 86400)
        self.clock_hours = f"{(total % 86400) // 3600:02d}"
        self.clock_minutes = f"{(total % 3600) // 60:02d}"
        self.clock_seconds = f"{total % 60:02d}"

    @rx.event
    def open_home(self):
        """Start the hero countdown. One loop per session."""
        self._write_clock()
        if self._clock_on:
            return
        self._clock_on = True
        return State.run_clock

    @rx.event(background=True)
    async def run_clock(self):
        try:
            while True:
                await asyncio.sleep(1)
                async with self:
                    self._write_clock()
        finally:
            async with self:
                self._clock_on = False

    @rx.event
    def toggle_star(self, event_id: str):
        if event_id in self.starred:
            self.starred = [item for item in self.starred if item != event_id]
            return
        self.starred = [*self.starred, event_id]

    @rx.event
    def toggle_menu(self):
        self.menu_open = not self.menu_open

    @rx.event
    def close_menu(self):
        self.menu_open = False

    @rx.event
    def choose_day(self, day: str):
        self.day = day

    @rx.event
    def choose_stage(self, stage: str):
        self.stage = stage

    @rx.event
    def choose_discipline(self, discipline: str):
        self.discipline = discipline

    @rx.event
    def open_artist(self, name: str):
        self.selected_name = name

    @rx.event
    def close_artist(self, open: bool):
        if not open:
            self.selected_name = ""

    @rx.event
    def show_on_program(self):
        artist = self.selected_artist
        self.day = artist.day
        self.stage = artist.stage
        self.selected_name = ""
        return rx.redirect("/program")

    @rx.event
    def choose_zone(self, name: str):
        self.zone_name = name

    @rx.event
    def choose_pass(self, pass_id: str):
        self.pass_id = pass_id
        self.held = False
        self.hold_message = ""

    @rx.event
    def more_passes(self):
        if self.quantity < 8:
            self.quantity += 1
        self.held = False
        self.hold_message = ""

    @rx.event
    def fewer_passes(self):
        if self.quantity > 1:
            self.quantity -= 1
        self.held = False
        self.hold_message = ""

    @rx.event
    def reserve(self):
        name = self.buyer_name.strip()
        email = self.buyer_email.strip()
        if len(name) < 2:
            self.held = False
            self.hold_message = "Add the name that should be on the passes."
            return
        domain = email.split("@")[-1] if "@" in email else ""
        if "@" not in email or "." not in domain or email.startswith("@"):
            self.held = False
            self.hold_message = "Add an email we can send the hold to."
            return
        self.held = True
        noun = "pass" if self.quantity == 1 else "passes"
        self.hold_message = (
            f"Held {self.quantity} {self.pass_name} {noun} for {name}. "
            "This hold stays in your browser session. No card is charged."
        )

    @rx.event
    def revise_hold(self):
        self.held = False
        self.hold_message = ""

    @rx.event
    def open_moment(self, index: int):
        self.moment_index = index
        self.lightbox_open = True

    @rx.event
    def shift_moment(self, step: int):
        count = len(self.moments)
        self.moment_index = (self.moment_index + step) % count

    @rx.event
    def subscribe(self):
        email = self.newsletter_email.strip()
        domain = email.split("@")[-1] if "@" in email else ""
        if "@" not in email or "." not in domain or email.startswith("@"):
            self.subscribed = False
            self.newsletter_note = "Add a complete email address."
            return
        self.subscribed = True
        self.newsletter_note = "You're on the list. We'll write before the gates open."

    @rx.var
    def schedule(self) -> list[ProgramEvent]:
        chosen = set(self.starred)
        return [event for event in self.events if event.id in chosen]

    @rx.var
    def schedule_count(self) -> int:
        return len(self.starred)

    @rx.var
    def visible_events(self) -> list[ProgramEvent]:
        return [
            event
            for event in self.events
            if event.day == self.day and (self.stage == "All" or event.stage == self.stage)
        ]

    @rx.var
    def visible_artists(self) -> list[Artist]:
        if self.discipline == "All":
            return self.artists
        return [artist for artist in self.artists if artist.discipline == self.discipline]

    @rx.var
    def selected_artist(self) -> Artist:
        for artist in self.artists:
            if artist.name == self.selected_name:
                return artist
        return self.artists[0]

    @rx.var
    def artist_open(self) -> bool:
        return self.selected_name != ""

    @rx.var
    def active_zone(self) -> Zone:
        for zone in self.zones:
            if zone.name == self.zone_name:
                return zone
        return self.zones[0]

    @rx.var
    def selected_pass(self) -> PassOption:
        for option in PASSES:
            if option.id == self.pass_id:
                return option
        return PASSES[1]

    @rx.var
    def pass_name(self) -> str:
        return self.selected_pass.name

    @rx.var
    def total_label(self) -> str:
        return f"${self.selected_pass.price * self.quantity}"

    @rx.var
    def active_moment(self) -> Moment:
        return self.moments[self.moment_index]
