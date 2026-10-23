#!/usr/bin/env bash
# Assemble the directory Azure App Service should receive.
# The frontend must already be exported to .web/build/client.
# Dependencies are not copied. Oryx installs requirements.txt on the server.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$ROOT/deploy-package}"

if [[ ! -d "$ROOT/.web/build/client" ]]; then
  echo "Missing $ROOT/.web/build/client." >&2
  echo "Run: reflex export --env prod --frontend-only --no-zip" >&2
  exit 1
fi

rm -rf "$DEST"
mkdir -p "$DEST/.web/build" "$DEST/.web/backend"

cp "$ROOT/requirements.txt" "$ROOT/rxconfig.py" "$ROOT/startup.sh" "$ROOT/serve_prod.py" "$DEST/"
chmod +x "$DEST/startup.sh"

if [[ -d "$ROOT/assets" ]]; then
  mkdir -p "$DEST/assets"
  cp -a "$ROOT/assets/." "$DEST/assets/"
  rm -rf "$DEST/assets/external"
fi

# Top-level Python packages. Hidden dirs, the frontend tree, and tooling stay out
# so Oryx does not treat this zip as a Node app.
for dir in "$ROOT"/*/; do
  name="$(basename "$dir")"
  case "$name" in
    assets | deploy-package | node_modules | reflex.lock | scripts) continue ;;
  esac
  if [[ "$name" == .* ]]; then
    continue
  fi
  if [[ ! -f "$dir/__init__.py" && ! -f "$dir/${name}.py" ]]; then
    continue
  fi
  mkdir -p "$DEST/$name"
  while IFS= read -r -d '' file; do
    rel="${file#"$dir"}"
    case "$rel" in
      */__pycache__/* | __pycache__/* | *.pyc | *.pyo) continue ;;
    esac
    mkdir -p "$DEST/$name/$(dirname "$rel")"
    cp "$file" "$DEST/$name/$rel"
  done < <(find "$dir" -type f -print0)
done

# Only the static client. .web/package.json and node_modules must not be deployed.
cp -a "$ROOT/.web/build/client" "$DEST/.web/build/client"
if [[ -f "$ROOT/.web/backend/bundled_libraries.json" ]]; then
  cp "$ROOT/.web/backend/bundled_libraries.json" "$DEST/.web/backend/"
fi
if [[ -f "$ROOT/.web/routes.json" ]]; then
  cp "$ROOT/.web/routes.json" "$DEST/.web/"
fi

if [[ -f "$DEST/package.json" || -f "$DEST/.web/package.json" || -d "$DEST/node_modules" ]]; then
  echo "The deploy package contains a Node manifest. Oryx would try to build it." >&2
  exit 1
fi

echo "Packaged $DEST"


