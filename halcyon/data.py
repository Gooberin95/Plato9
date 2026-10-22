"""Festival copy. Original to this site."""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class PassOption:
    id: str
    name: str
    price: int
    detail: str


@dataclass
class ProgramEvent:
    day: str
    time: str
    stage: str
    title: str
    detail: str
    id: str = ""


# Noon UTC on opening day. The countdown and the program both use this instant.
GATES_OPEN = datetime(2027, 6, 12, 12, 0, tzinfo=timezone.utc)


@dataclass
class Artist:
    name: str
    discipline: str
    bio: str
    appearance: str
    day: str
    stage: str


@dataclass
class Zone:
    name: str
    note: str
    wide: bool = False


@dataclass
class Moment:
    title: str
    caption: str
    position: str


DAYS = ["Friday", "Saturday", "Sunday"]
STAGES = ["All", "Meadow", "Lantern Hall", "Tide Stage", "Workshops"]
DISCIPLINES = ["All", "Painting", "Music", "Sculpture", "Performance", "Craft"]

PASSES = [
    PassOption(
        "day",
        "Day",
        48,
        "One calendar day. Every stage, and a workshop seat while there is room.",
    ),
    PassOption(
        "weekend",
        "Weekend",
        120,
        "Friday noon through Sunday night. The pass most people carry.",
    ),
    PassOption(
        "patron",
        "Patron",
        280,
        "The whole weekend, Saturday's noon meal, and your name in the printed program.",
    ),
]

EVENTS = [
    ProgramEvent(
        "Friday",
        "12:00",
        "Meadow",
        "Gates open",
        "The north path is staffed. Water is free from the oak casks.",
    ),
    ProgramEvent(
        "Friday",
        "14:00",
        "Meadow",
        "June Pell: harbor studies",
        "Oil sketches painted from a folding stool, one tide at a time.",
    ),
    ProgramEvent(
        "Friday",
        "15:30",
        "Workshops",
        "Hester Quinn: indigo",
        "Dip linen in a cold vat. Aprons provided. Closed shoes, please.",
    ),
    ProgramEvent(
        "Friday",
        "17:00",
        "Lantern Hall",
        "Idris Vale on wind and bronze",
        "How the bird sculptures are balanced so they turn and do not fall.",
    ),
    ProgramEvent(
        "Friday",
        "21:00",
        "Tide Stage",
        "Black Kettle Band",
        "Fiddle, frame drum, and songs about weather that actually arrives.",
    ),
    ProgramEvent(
        "Saturday",
        "11:00",
        "Workshops",
        "Atelier Sable: estuary clay",
        "Throw a cup. If it survives the firing, it is yours on Sunday.",
    ),
    ProgramEvent(
        "Saturday",
        "13:00",
        "Lantern Hall",
        "Priya Lang: portraits in public",
        "Sit for twenty minutes. Leave with a drawing, or don't sit and watch.",
    ),
    ProgramEvent(
        "Saturday",
        "16:30",
        "Meadow",
        "Leo Park, from the oak",
        "A solo aerial piece. The grass below is kept clear.",
    ),
    ProgramEvent(
        "Saturday",
        "20:30",
        "Tide Stage",
        "The Low Choir",
        "Four voices and a pump organ. The set ends when the lanterns are lit.",
    ),
    ProgramEvent(
        "Sunday",
        "10:00",
        "Meadow",
        "Quiet hour",
        "No amplified sound until 11. Coffee is at the food grove.",
    ),
    ProgramEvent(
        "Sunday",
        "11:00",
        "Lantern Hall",
        "Maren Sol: skies without a horizon",
        "A talk beside three large canvases hung for the day only.",
    ),
    ProgramEvent(
        "Sunday",
        "15:00",
        "Meadow",
        "Amos Reed: walk the arches",
        "Driftwood arches from the north gate to the tide stairs.",
    ),
    ProgramEvent(
        "Sunday",
        "19:00",
        "Meadow",
        "Naomi Cho: paper boats",
        "A dusk procession down to the water. Hold a boat if one is offered.",
    ),
    ProgramEvent(
        "Sunday",
        "21:15",
        "Tide Stage",
        "The Night Orchard",
        "Electric guitar, mostly quiet. The last set before the grounds close.",
    ),
]


def _event_id(event: ProgramEvent) -> str:
    slug = []
    for character in f"{event.day}-{event.time}-{event.title}".lower():
        slug.append(character if character.isalnum() else "-")
    compact = "".join(slug)
    while "--" in compact:
        compact = compact.replace("--", "-")
    return compact.strip("-")


for _event in EVENTS:
    _event.id = _event_id(_event)

ARTISTS = [
    Artist(
        "June Pell",
        "Painting",
        "Pell paints the harbor from a skiff at dawn, then finishes the studies on the bluff where the light is less honest. She keeps the horizon low and the water busy.",
        "Friday, 14:00, Meadow",
        "Friday",
        "Meadow",
    ),
    Artist(
        "Black Kettle Band",
        "Music",
        "Three players from the east shore. The songs are about ferries, fog, and the year the breakwater failed. They do not play over conversation.",
        "Friday, 21:00, Tide Stage",
        "Friday",
        "Tide Stage",
    ),
    Artist(
        "Hester Quinn",
        "Craft",
        "Quinn dyes with indigo, rust, and whatever the oak galls give her. The vats at Halcyon are the same ones she uses in the town dye house.",
        "Friday, 15:30, Workshops",
        "Friday",
        "Workshops",
    ),
    Artist(
        "Idris Vale",
        "Sculpture",
        "Cast-bronze birds, balanced to turn in a modest wind and to stop in a strong one. Vale will tell you the stop matters more than the spin.",
        "Friday, 17:00, Lantern Hall",
        "Friday",
        "Lantern Hall",
    ),
    Artist(
        "Atelier Sable",
        "Craft",
        "Two potters, one kiln, clay dug from the estuary below the bluff. Cups thrown on Saturday can be collected Sunday if they survive.",
        "Saturday, 11:00, Workshops",
        "Saturday",
        "Workshops",
    ),
    Artist(
        "Priya Lang",
        "Painting",
        "Lang draws portraits in one sitting and does not revise them. The rule is twenty minutes, then the sitter stands up.",
        "Saturday, 13:00, Lantern Hall",
        "Saturday",
        "Lantern Hall",
    ),
    Artist(
        "Leo Park",
        "Performance",
        "Park works alone, from a rig in the oak at the north edge of the meadow. The piece is short. The tree is old. Both are treated carefully.",
        "Saturday, 16:30, Meadow",
        "Saturday",
        "Meadow",
    ),
    Artist(
        "The Low Choir",
        "Music",
        "Four voices and a pump organ that travels in a crate. They sing in a close interval and leave a long pause before the last chord.",
        "Saturday, 20:30, Tide Stage",
        "Saturday",
        "Tide Stage",
    ),
    Artist(
        "Maren Sol",
        "Painting",
        "Large skies, small figures, and no horizon line to settle on. The canvases in Lantern Hall go back to the studio on Sunday night.",
        "Sunday, 11:00, Lantern Hall",
        "Sunday",
        "Lantern Hall",
    ),
    Artist(
        "Amos Reed",
        "Sculpture",
        "Reed builds arches from driftwood collected after winter storms. You can walk through them. Please do not climb.",
        "Sunday, 15:00, Meadow",
        "Sunday",
        "Meadow",
    ),
    Artist(
        "Naomi Cho",
        "Performance",
        "Cho's procession starts in the meadow and ends at the tide stairs. The boats are paper. The water takes them.",
        "Sunday, 19:00, Meadow",
        "Sunday",
        "Meadow",
    ),
    Artist(
        "The Night Orchard",
        "Music",
        "A guitar duo that plays as if the amplifier might be asked to leave. They close the festival.",
        "Sunday, 21:15, Tide Stage",
        "Sunday",
        "Tide Stage",
    ),
]

ZONES = [
    Zone(
        "North gate",
        "Passes are scanned here. The bike racks, the shuttle stop, and the first water cask are just inside. The path from the ferry takes about twelve minutes on foot.",
        wide=True,
    ),
    Zone(
        "Meadow",
        "The open grass between the oaks. Painting, aerial work, and Sunday's procession happen here. The ground is packed where the chairs go and left long at the edges.",
    ),
    Zone(
        "Lantern Hall",
        "A timber hall with a ramp at the west door. Talks and the portrait sittings are inside. It is the rain plan for anything that cannot bear weather.",
    ),
    Zone(
        "Workshops",
        "Three oak tents south of the hall. Indigo, clay, and a quiet table for mending. Space is first come; a day pass is enough.",
    ),
    Zone(
        "Tide Stage",
        "A low platform facing the water. Music only. The sightline is clear from the grass; you do not need a seat.",
    ),
    Zone(
        "Food grove",
        "Eight kitchens, one of them a nut-free window marked with a yellow board. Saturday's patron meal is served at noon from the long table.",
        wide=True,
    ),
]

FAQS = [
    (
        "Are children free?",
        "Guests 12 and under are free with a ticketed adult. Sunday morning is quiet hour until 11, with no amplified sound.",
    ),
    (
        "Can I bring a dog?",
        "On a leash, on the outer path. Not in Lantern Hall, the food grove, or the workshop tents.",
    ),
    (
        "What if it rains?",
        "The program moves under the hall and the oak tents. Passes are not refunded for weather. They can be transferred to a friend or held for the next Halcyon.",
    ),
    (
        "Is the bluff accessible?",
        "The meadow path is packed gravel. Lantern Hall has a ramp and an accessible toilet. A shuttle runs from the ferry every twenty minutes and can take a wheelchair.",
    ),
    (
        "Can I camp?",
        "Not on the bluff. Port Merrow has inns, and the visit desk keeps a short list of rooms that still answer the phone in June.",
    ),
]

MOMENTS = [
    Moment(
        "Lantern line",
        "The string of lanterns between the oaks, before they are lit.",
        "18% 42%",
    ),
    Moment(
        "Last light on the water",
        "The tide stage faces this. Sunday's last set plays into it.",
        "72% 38%",
    ),
    Moment(
        "Easels in the grass",
        "A painting row on the meadow, left up until the dew comes.",
        "40% 78%",
    ),
    Moment(
        "The evening walk",
        "The path most people take from the hall down toward the music.",
        "62% 62%",
    ),
    Moment(
        "Sculpture among the oaks",
        "Where Vale's birds and Reed's arches share the tree line.",
        "28% 58%",
    ),
    Moment(
        "The sky the painters argue about",
        "Honey over teal. Sol says there is no horizon. Pell says there is, and it is low.",
        "80% 18%",
    ),
]
