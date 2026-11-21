# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Check that the skills CLI lists the skills at each index in build/public/.

    uv run scripts/test_skills.py

publish_skills.py writes the indexes, and a project reads them with `npx skills add`. This
serves build/public/ on a local port, and runs the pinned skills CLI with `--list` against
each address that has an index: the root, each ecosystem, and each house profile. It fails
when the CLI can't read an index, when an archive doesn't match its digest, or when a skill
the index names isn't listed. It also checks that a path with no index is refused, so an
install there can't widen to the root's skills.

It installs nothing. Run `just build` first, or `just skills` after a change to
publish_skills.py.

Exit codes: 0 every index lists its skills, 1 one doesn't, 2 not run from the repository
root, nothing built, or the skills CLI isn't installed.
"""

import functools
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from ecosystems import BUILD, report, require_root

PUBLIC = BUILD / "public"
WELL_KNOWN = ".well-known/agent-skills"
# The terminal colours the CLI writes even when its output isn't a terminal.
COLOUR = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
# A path under the site that has no index, to check that the CLI refuses it.
NO_INDEX = "conventions"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass


def serve() -> str:
    """Serve build/public/ on a free local port, and return its address."""
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(PUBLIC)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}"


def listed(address: str) -> str:
    """What the CLI prints for `skills add <address> --list`, without colours."""
    result = subprocess.run(
        ["npm", "exec", "--no", "--", "skills", "add", address, "--list"],
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
        # The CLI reports each run to its maker unless told not to, and prompts unless CI is set.
        env={**os.environ, "DISABLE_TELEMETRY": "1", "DO_NOT_TRACK": "1", "CI": "1"},
    )
    return COLOUR.sub("", result.stdout + result.stderr)


def main() -> int:
    require_root()
    indexes = sorted(PUBLIC.rglob(f"{WELL_KNOWN}/index.json"))
    if not indexes:
        print(f"No skills index under {PUBLIC}/. Run `just build` first.", file=sys.stderr)
        return 2
    if shutil.which("npm") is None or not Path("node_modules/skills").is_dir():
        print("The skills CLI isn't installed. Run `just install` first.", file=sys.stderr)
        return 2

    origin = serve()
    errors: list[str] = []
    for index in indexes:
        scope = index.relative_to(PUBLIC).as_posix().removesuffix(f"{WELL_KNOWN}/index.json").rstrip("/")
        expected = [skill["name"] for skill in json.loads(index.read_text(encoding="utf-8"))["skills"]]
        output = listed(f"{origin}/{scope}".rstrip("/"))
        # The CLI prints each skill's name on a line of its own.
        names = {line.strip("│ ").strip() for line in output.splitlines()}
        missing = [name for name in expected if name not in names]
        print(f"/{scope}: {', '.join(expected)}" + (f", but not listed: {', '.join(missing)}" if missing else ""))
        if missing:
            errors.append(f"/{scope}: the skills CLI didn't list {', '.join(missing)}:\n{output.strip()}")

    refused = listed(f"{origin}/{NO_INDEX}")
    if "SKILLS_WELLKNOWN_SCOPE_NOT_FOUND" not in refused:
        errors.append(f"/{NO_INDEX}: has no index, but the skills CLI didn't refuse it:\n{refused.strip()}")
    else:
        print(f"/{NO_INDEX}: refused, as a path with no index")
    return report(errors)


if __name__ == "__main__":
    sys.exit(main())
