"""Chrome shared by every page, including the fixed background."""

import reflex as rx

from halcyon.state import State

# Source of truth: uploads/background.jpg. Reflex serves the copy at this path.
BACKGROUND = rx.asset("uploads/background.jpg")

NAV = [
    ("Program", "/program"),
    ("Artists", "/artists"),
    ("Visit", "/visit"),
    ("Gallery", "/gallery"),
]


def fixed_background() -> rx.Component:
    """One fixed photograph behind every route."""
    return rx.box(
        aria_hidden=True,
        class_name="fixed-bg",
        style={
            "background_image": (
                "linear-gradient(180deg, rgba(12, 10, 8, 0.22), rgba(12, 10, 8, 0.5)), "
                f"url('{BACKGROUND}')"
            ),
            "background_size": "cover",
            "background_position": "center",
            "background_repeat": "no-repeat",
            "background_attachment": "fixed",
        },
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.a("Skip to content", href="#content", class_name="skip"),
        rx.link(
            rx.el.strong("Halcyon"),
            rx.el.span("Arts Festival"),
            href="/",
            class_name="brand",
            on_click=State.close_menu,
        ),
        rx.el.button(
            rx.cond(State.menu_open, "Close", "Menu"),
            type="button",
            class_name="btn btn-line menu-button",
            on_click=State.toggle_menu,
            aria_expanded=State.menu_open,
        ),
        rx.el.nav(
            *[
                rx.link(
                    label,
                    href=href,
                    class_name="nav-link",
                    on_click=State.close_menu,
                )
                for label, href in NAV
            ],
            rx.link(
                "Passes",
                href="/tickets",
                class_name="btn btn-solid",
                on_click=State.close_menu,
            ),
            class_name=rx.cond(State.menu_open, "nav-links is-open", "nav-links"),
            aria_label="Festival",
        ),
        class_name="nav",
    )


def newsletter() -> rx.Component:
    return rx.box(
        rx.el.h2("Before the gates"),
        rx.el.p(
            "One note when the program is locked, and one the week of the festival. Nothing else.",
            class_name="muted",
        ),
        rx.el.div(
            rx.input(
                placeholder="Email address",
                type="email",
                value=State.newsletter_email,
                on_change=State.set_newsletter_email,
                class_name="field",
                aria_label="Email address",
            ),
            rx.el.button(
                rx.cond(State.subscribed, "On the list", "Send me the note"),
                type="button",
                class_name="btn btn-solid",
                on_click=State.subscribe,
                disabled=State.subscribed,
            ),
            class_name="stack",
        ),
        rx.el.p(
            State.newsletter_note,
            class_name=rx.cond(
                State.subscribed,
                "note is-ok",
                rx.cond(State.newsletter_note == "", "note", "note is-bad"),
            ),
            role="status",
        ),
        class_name="panel",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.box(
                rx.el.p(
                    "June 12–14, 2027",
                    class_name="eyebrow",
                ),
                rx.el.h2("Port Merrow Bluff"),
                rx.el.p(
                    "Presented by the Port Merrow Arts Trust. The photograph behind the site is the grounds at last light.",
                    class_name="muted",
                ),
            ),
            newsletter(),
            class_name="footer-grid wrap",
        ),
        class_name="footer",
    )


def shell(*children) -> rx.Component:
    return rx.box(
        fixed_background(),
        rx.box(
            navbar(),
            rx.el.main(*children, id="content"),
            footer(),
            class_name="site",
        ),
    )
