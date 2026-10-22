"""Pages for the Halcyon Arts Festival."""

import reflex as rx

from halcyon.data import DAYS, DISCIPLINES, FAQS, PASSES, STAGES, ZONES, Artist, Moment, ProgramEvent
from halcyon.state import State
from halcyon.ui import BACKGROUND, shell


def index() -> rx.Component:
    return shell(
        rx.el.section(
            rx.box(
                rx.el.p("June 12–14, 2027 · Port Merrow Bluff", class_name="kicker"),
                rx.el.h1(
                    "Halcyon",
                    rx.el.br(),
                    rx.el.em("field notes"),
                    class_name="display",
                ),
                rx.el.p(
                    "Three days of painting, music, and making on the bluff above the tide. Eighty-six artists, three stages, and a workshop tent that smells like clay and indigo.",
                    class_name="lede",
                ),
                rx.el.div(
                    rx.link("Get passes", href="/tickets", class_name="btn btn-solid"),
                    rx.link("See the program", href="/program", class_name="btn btn-line"),
                    class_name="actions",
                ),
                rx.el.p(
                    rx.el.span(rx.el.strong("86"), " artists"),
                    rx.el.span(rx.el.strong("3"), " stages"),
                    rx.el.span(rx.el.strong("14"), " acres"),
                    rx.el.span(rx.el.strong("Free"), " under 12"),
                    class_name="stats",
                ),
                class_name="hero-copy",
            ),
            class_name="hero wrap",
        ),
        rx.el.section(
            rx.el.div(
                rx.box(
                    rx.el.p("See", class_name="eyebrow"),
                    rx.el.h3("Work hung for the weekend"),
                    rx.el.p(
                        "Canvases in Lantern Hall, bronze birds in the oaks, and driftwood arches you can walk through. Nothing is for sale on the grass.",
                        class_name="muted",
                    ),
                ),
                rx.box(
                    rx.el.p("Hear", class_name="eyebrow"),
                    rx.el.h3("The tide stage, after six"),
                    rx.el.p(
                        "A choir with a pump organ, a fiddle band, and a guitar duo that closes Sunday. The stage faces the water on purpose.",
                        class_name="muted",
                    ),
                ),
                rx.box(
                    rx.el.p("Make", class_name="eyebrow"),
                    rx.el.h3("A cup or a stained hem"),
                    rx.el.p(
                        "Estuary clay on Saturday. Indigo on Friday. If the cup survives the kiln, collect it before the grounds close.",
                        class_name="muted",
                    ),
                ),
                class_name="grid-3",
            ),
            class_name="section wrap panel",
        ),
    )


def _event_row(event: ProgramEvent) -> rx.Component:
    return rx.el.article(
        rx.el.time(event.time),
        rx.box(
            rx.el.h3(event.title, class_name="artist-name"),
            rx.el.p(event.detail, class_name="muted"),
        ),
        rx.el.span(event.stage, class_name="stage"),
        class_name="event",
    )


def program() -> rx.Component:
    return shell(
        rx.el.section(
            rx.el.p("Program", class_name="kicker"),
            rx.el.h1("What happens, and where"),
            rx.el.p(
                "Pick a day, then a stage. All times are local to Port Merrow. Workshops keep a standing line; a seat is not reserved with the pass.",
                class_name="lede",
            ),
            rx.el.div(
                *[
                    rx.el.button(
                        day,
                        type="button",
                        class_name=rx.cond(State.day == day, "chip is-on", "chip"),
                        on_click=State.choose_day(day),
                    )
                    for day in DAYS
                ],
                class_name="filters",
                role="group",
                aria_label="Day",
            ),
            rx.el.div(
                *[
                    rx.el.button(
                        stage,
                        type="button",
                        class_name=rx.cond(State.stage == stage, "chip is-on", "chip"),
                        on_click=State.choose_stage(stage),
                    )
                    for stage in STAGES
                ],
                class_name="filters",
                role="group",
                aria_label="Stage",
            ),
            rx.cond(
                State.visible_events.length() == 0,
                rx.el.p(
                    "Nothing on that stage this day. Try All stages.",
                    class_name="muted",
                ),
                rx.foreach(State.visible_events, _event_row),
            ),
            class_name="section wrap panel",
        ),
    )


def _artist_card(artist: Artist) -> rx.Component:
    return rx.el.button(
        rx.el.span(artist.discipline, class_name="discipline"),
        rx.el.span(artist.name, class_name="artist-name"),
        rx.el.span(artist.appearance, class_name="muted"),
        type="button",
        class_name="artist",
        on_click=State.open_artist(artist.name),
    )


def artists() -> rx.Component:
    return shell(
        rx.el.section(
            rx.el.p("Artists", class_name="kicker"),
            rx.el.h1("Who is on the bluff"),
            rx.el.p(
                "Twelve of the eighty-six, the ones who anchor the weekend. Open a name for the short version, then jump to their place in the program.",
                class_name="lede",
            ),
            rx.el.div(
                *[
                    rx.el.button(
                        discipline,
                        type="button",
                        class_name=rx.cond(
                            State.discipline == discipline, "chip is-on", "chip"
                        ),
                        on_click=State.choose_discipline(discipline),
                    )
                    for discipline in DISCIPLINES
                ],
                class_name="filters",
                role="group",
                aria_label="Discipline",
            ),
            rx.el.div(
                rx.foreach(State.visible_artists, _artist_card),
                class_name="artist-grid",
            ),
            rx.dialog.root(
                rx.dialog.content(
                    rx.el.p(State.selected_artist.discipline, class_name="discipline"),
                    rx.dialog.title(State.selected_artist.name),
                    rx.dialog.description(State.selected_artist.bio),
                    rx.el.p(State.selected_artist.appearance, class_name="muted"),
                    rx.el.div(
                        rx.el.button(
                            "Show on the program",
                            type="button",
                            class_name="btn btn-solid",
                            on_click=State.show_on_program,
                        ),
                        rx.dialog.close(
                            rx.el.button("Close", type="button", class_name="btn btn-line")
                        ),
                        class_name="actions",
                    ),
                    class_name="sheet",
                ),
                open=State.artist_open,
                on_open_change=State.close_artist,
            ),
            class_name="section wrap panel",
        ),
    )


def _pass_card(option) -> rx.Component:
    return rx.el.button(
        rx.el.span(option.name, class_name="pass-name"),
        rx.el.span(f"${option.price}", class_name="pass-price"),
        rx.el.span(option.detail, class_name="muted"),
        type="button",
        class_name=rx.cond(State.pass_id == option.id, "pass is-on", "pass"),
        on_click=State.choose_pass(option.id),
        aria_pressed=State.pass_id == option.id,
    )


def tickets() -> rx.Component:
    return shell(
        rx.el.section(
            rx.box(
                rx.el.p("Passes", class_name="kicker"),
                rx.el.h1("Hold a pass"),
                rx.el.p(
                    "Choose a pass and how many. The hold is for this session only — a way to see the total, not a payment.",
                    class_name="lede",
                ),
                rx.el.div(
                    *[_pass_card(option) for option in PASSES],
                    class_name="stack",
                ),
                class_name="panel",
            ),
            rx.box(
                rx.cond(
                    State.held,
                    rx.box(
                        rx.el.p("Held", class_name="eyebrow"),
                        rx.el.h2(State.total_label, class_name="total"),
                        rx.el.p(State.hold_message, class_name="note is-ok", role="status"),
                        rx.el.button(
                            "Change this hold",
                            type="button",
                            class_name="btn btn-line",
                            on_click=State.revise_hold,
                        ),
                        class_name="stack",
                    ),
                    rx.box(
                        rx.el.p("Quantity", class_name="eyebrow"),
                        rx.el.div(
                            rx.el.button(
                                "Fewer",
                                type="button",
                                class_name="btn btn-line",
                                on_click=State.fewer_passes,
                                disabled=State.quantity <= 1,
                            ),
                            rx.el.span(State.quantity, aria_live="polite"),
                            rx.el.button(
                                "More",
                                type="button",
                                class_name="btn btn-line",
                                on_click=State.more_passes,
                                disabled=State.quantity >= 8,
                            ),
                            class_name="stepper",
                        ),
                        rx.el.p(State.total_label, class_name="total"),
                        rx.el.p(
                            State.quantity,
                            " × ",
                            State.pass_name,
                            class_name="muted",
                        ),
                        rx.input(
                            placeholder="Name on the passes",
                            value=State.buyer_name,
                            on_change=State.set_buyer_name,
                            class_name="field",
                            aria_label="Name on the passes",
                        ),
                        rx.input(
                            placeholder="Email for the hold",
                            type="email",
                            value=State.buyer_email,
                            on_change=State.set_buyer_email,
                            class_name="field",
                            aria_label="Email for the hold",
                        ),
                        rx.el.button(
                            "Hold these passes",
                            type="button",
                            class_name="btn btn-solid",
                            on_click=State.reserve,
                        ),
                        rx.el.p(
                            State.hold_message,
                            class_name="note is-bad",
                            role="status",
                        ),
                        class_name="stack",
                    ),
                ),
                class_name="panel",
            ),
            class_name="section wrap grid-2",
        ),
    )


def visit() -> rx.Component:
    return shell(
        rx.el.section(
            rx.box(
                rx.el.p("The grounds", class_name="kicker"),
                rx.el.h1("A small map"),
                rx.el.p(
                    "Select a part of the bluff. This is a plan, not a satellite photo — the real one is the picture behind the page.",
                    class_name="lede",
                ),
                rx.el.div(
                    *[
                        rx.el.button(
                            zone.name,
                            type="button",
                            class_name=rx.cond(
                                State.zone_name == zone.name,
                                "zone wide is-on" if zone.wide else "zone is-on",
                                "zone wide" if zone.wide else "zone",
                            ),
                            on_click=State.choose_zone(zone.name),
                            aria_pressed=State.zone_name == zone.name,
                        )
                        for zone in ZONES
                    ],
                    class_name="grounds",
                ),
                class_name="panel",
            ),
            rx.box(
                rx.el.p("Selected", class_name="eyebrow"),
                rx.el.h2(State.active_zone.name),
                rx.el.p(State.active_zone.note, class_name="lede"),
                rx.el.h3("Getting here"),
                rx.el.p(
                    "Ferry from Eastwick, eighteen minutes, then the bluff path or the shuttle. The train stops at Port Merrow; the harbor bus meets the evening arrivals. Bikes lock at the north gate.",
                    class_name="muted",
                ),
                rx.el.h3("Hours"),
                rx.el.p(
                    "Friday noon to 11pm. Saturday 10am to midnight. Sunday 10am to midnight, with quiet hour until 11.",
                    class_name="muted",
                ),
                class_name="panel stack",
            ),
            class_name="section wrap grid-2",
        ),
        rx.el.section(
            rx.el.h2("Before you come"),
            rx.accordion.root(
                *[
                    rx.accordion.item(header=question, content=answer, value=f"faq-{index}")
                    for index, (question, answer) in enumerate(FAQS)
                ],
                type="single",
                collapsible=True,
                variant="soft",
                width="100%",
            ),
            class_name="section wrap panel stack",
        ),
    )


def _moment_card(moment: Moment, index: int) -> rx.Component:
    return rx.el.button(
        rx.el.img(
            src=BACKGROUND,
            alt="",
            style={"object_position": moment.position},
        ),
        rx.el.span(moment.title),
        type="button",
        class_name="moment",
        on_click=State.open_moment(index),
    )


def gallery() -> rx.Component:
    return shell(
        rx.el.section(
            rx.el.p("Gallery", class_name="kicker"),
            rx.el.h1("The same hour, six ways"),
            rx.el.p(
                "Every frame is the grounds at last light — the photograph this site uses as its background — cropped to the place the weekend actually happens.",
                class_name="lede",
            ),
            rx.el.div(
                rx.foreach(State.moments, _moment_card),
                class_name="moment-grid",
            ),
            rx.dialog.root(
                rx.dialog.content(
                    rx.el.img(
                        src=BACKGROUND,
                        alt=State.active_moment.title,
                        style={
                            "object_position": State.active_moment.position,
                            "height": "18rem",
                        },
                    ),
                    rx.dialog.title(State.active_moment.title),
                    rx.dialog.description(State.active_moment.caption),
                    rx.el.div(
                        rx.el.button(
                            "Previous",
                            type="button",
                            class_name="btn btn-line",
                            on_click=State.shift_moment(-1),
                        ),
                        rx.el.button(
                            "Next",
                            type="button",
                            class_name="btn btn-line",
                            on_click=State.shift_moment(1),
                        ),
                        rx.dialog.close(
                            rx.el.button("Close", type="button", class_name="btn btn-solid")
                        ),
                        class_name="actions",
                    ),
                    class_name="sheet",
                ),
                open=State.lightbox_open,
                on_open_change=State.set_lightbox_open,
            ),
            class_name="section wrap panel",
        ),
    )
