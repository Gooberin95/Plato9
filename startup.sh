#!/usr/bin/env bash
# App Service startup command: startup.sh
# Oryx has already activated the virtualenv, so `python` is the app interpreter.
# Do not call `reflex run` here. That rebuilds the frontend and needs Node or Bun.
set -euo pipefail

if [[ -n "${APP_PATH:-}" && -d "${APP_PATH}" ]]; then
  cd "${APP_PATH}"
fi

exec python serve_prod.py


