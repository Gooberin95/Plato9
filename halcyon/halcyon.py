"""Halcyon Arts Festival."""

import reflex as rx

from halcyon.pages import artists, gallery, index, program, tickets, visit

app = rx.App(
    html_lang="en",
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,520;9..144,650&family=Outfit:wght@360;500;640&display=swap",
        "/styles.css",
    ],
    style={
        "font_family": '"Outfit", "Avenir Next", sans-serif',
        "color": "#f6f1e7",
        "background_color": "transparent",
    },
)

app.add_page(
    index,
    route="/",
    title="Halcyon Arts Festival",
    description="Three days of painting, music, and making on Port Merrow Bluff, June 12–14, 2027.",
)
app.add_page(
    program,
    route="/program",
    title="Program · Halcyon Arts Festival",
    description="The weekend program by day and stage.",
)
app.add_page(
    artists,
    route="/artists",
    title="Artists · Halcyon Arts Festival",
    description="Painters, musicians, sculptors, and makers at Halcyon.",
)
app.add_page(
    tickets,
    route="/tickets",
    title="Passes · Halcyon Arts Festival",
    description="Day, weekend, and patron passes for Halcyon.",
)
app.add_page(
    visit,
    route="/visit",
    title="Visit · Halcyon Arts Festival",
    description="How to reach Port Merrow Bluff and where things are on the grounds.",
)
app.add_page(
    gallery,
    route="/gallery",
    title="Gallery · Halcyon Arts Festival",
    description="The grounds at last light, which is also the site background.",
)
