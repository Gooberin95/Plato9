# Halcyon Arts Festival

A Reflex site for the Halcyon Arts Festival at Port Merrow Bluff, June 12–14, 2027.

Every page uses one shared fixed background: `uploads/background.jpg`, served at `/uploads/background.jpg`. The photograph stays fixed while the page scrolls.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
reflex run --env prod --single-port
```

Open the URL printed in the log. Pages: home, program, artists, passes, visit, and gallery.
