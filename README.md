# Halcyon Arts Festival

A Reflex site for the Halcyon Arts Festival at Port Merrow Bluff, June 12–14, 2027. The hero counts down to the gates. On the program, star an act and it collects on your personal schedule.

The photograph in `assets/background.jpg` is the background of every page. It is applied once, on the page root, with `background_size="cover"`, `background_position="center"`, and `background_attachment="fixed"`, so it stays put while the page scrolls. Sections sit on translucent panels so the type stays readable and the picture still shows through.

## Python version

Reflex 0.10.0 supports Python 3.14 (`requires-python >=3.11,<4`, with a Python 3.14 classifier). This project targets **Python 3.14.4**. `.python-version` is `3.14.4`.

## Run it on Ubuntu

From a terminal:

```bash
git clone https://github.com/Gooberin95/Plato9.git
cd Plato9
```

Install Python 3.14.4 and expose it as `python3.14` (skip this block if `python3.14 --version` already prints `Python 3.14.4`):

```bash
sudo apt update
sudo apt install -y curl ca-certificates
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv python install 3.14.4
mkdir -p "$HOME/.local/bin"
ln -sfn "$(uv python find 3.14.4)" "$HOME/.local/bin/python3.14"
export PATH="$HOME/.local/bin:$PATH"
python3.14 --version
```

Create a virtual environment, install Reflex, and start the app. The repo is already a Reflex project (`rxconfig.py`, the `halcyon` package, and `assets/` are included), so do **not** run `reflex init` — it will offer to overwrite these files.

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
reflex run
```

The first `reflex run` compiles the frontend and downloads Reflex's frontend toolchain, so it needs a network connection and a minute or two. When it is ready, open:

**http://localhost:3000**

The backend listens on http://localhost:8000. You do not need to open that URL. Stop the app with Ctrl+C.

## Pages

- `/` — the bluff, and a live countdown to noon UTC on Friday, June 12, 2027
- `/program` — the weekend, filtered by day and stage; star an act to keep it
- `/schedule` — the acts you starred, in weekend order
- `/artists` — twelve of the artists, with a jump to their set
- `/tickets` — day, weekend, and patron holds (a session total, not a charge)
- `/visit` — the grounds, the way in, and practical questions
- `/gallery` — six crops of the same photograph

## Deploying to Azure

The GitHub Actions workflow builds this site on every push to `main`. Deploying to Azure App Service is described in [DEPLOY.md](DEPLOY.md). Those deploy jobs stay skipped until an Azure subscription exists and the variable `AZURE_DEPLOY_ENABLED` is set to `true`.
