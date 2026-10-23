"""Serve the Reflex backend and the prebuilt frontend on one port.

GitHub Actions runs ``reflex export`` and puts the static frontend in
``.web/build/client``. App Service's Python image has no Node.js or Bun, so
this process must not call ``reflex run`` — that command rebuilds the
frontend. ``REFLEX_SKIP_COMPILE`` keeps startup on the Python side, and
``REFLEX_MOUNT_FRONTEND_COMPILED_APP`` attaches the exported files to the
same ASGI server.

The listen port is ``PORT``, then ``WEBSITES_PORT``, then 8000. The exported
client is built against ``http://localhost:8000``. In the browser, Reflex
rewrites that localhost host to the page's host. On Azure's HTTPS front end
the socket uses port 443, so staging and production can share one build.
"""

from __future__ import annotations

import os
import sys

from reflex_base import constants
from reflex_base.environment import environment


def _port() -> int:
    raw = os.environ.get("PORT") or os.environ.get("WEBSITES_PORT") or "8000"
    try:
        port = int(raw)
    except ValueError:
        print(f"PORT must be an integer, got {raw!r}.", file=sys.stderr)
        raise SystemExit(1) from None
    if not 1 <= port <= 65535:
        print(f"PORT {port} is outside 1-65535.", file=sys.stderr)
        raise SystemExit(1)
    return port


def main() -> None:
    environment.REFLEX_ENV_MODE.set(constants.Env.PROD)
    environment.REFLEX_SKIP_COMPILE.set(True)
    environment.REFLEX_MOUNT_FRONTEND_COMPILED_APP.set(True)
    # The disk state manager is one process. B1 is a small box.
    os.environ["GRANIAN_WORKERS"] = os.environ.get("GRANIAN_WORKERS", "1")

    from reflex.utils.prerequisites import get_web_dir
    from reflex.utils.exec import get_app_instance, run_granian_backend_prod

    static_dir = get_web_dir() / constants.Dirs.STATIC
    if not static_dir.is_dir():
        print(
            f"Missing production frontend at {static_dir}. "
            "Build it with: reflex export --env prod --frontend-only --no-zip",
            file=sys.stderr,
        )
        raise SystemExit(1)

    port = _port()
    target = get_app_instance()
    print(f"Serving {target} on 0.0.0.0:{port} from {static_dir}", flush=True)
    run_granian_backend_prod(
        host="0.0.0.0",
        port=port,
        loglevel=constants.LogLevel.INFO,
        app_target=target,
    )


if __name__ == "__main__":
    main()


