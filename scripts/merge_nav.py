# /// script
# requires-python = ">=3.14"
# dependencies = ["jsonschema==4.26.0"]
# ///
"""Validate each staged nav.json, and write build/zensical.toml with the full navigation.

    uv run scripts/merge_nav.py

Run it after stage.py. The navigation is the site's own pages, then each live
ecosystem's section under its name from ecosystems.toml, in registry order. Each
section's paths gain the ecosystem's directory as a prefix. zensical.toml stays the
base configuration, and the copy in build/ adds only the nav, so Zensical then
builds from build/:

    uv run zensical build --strict -f build/zensical.toml

Exit codes: 0 written, 1 a nav.json is missing, invalid, or names a page that
wasn't staged, 2 not run from the repository root.
"""

import json
import sys
import tomllib
from pathlib import Path

from ecosystems import BUILD, DOCS, live, load_json, report, require_root, validate

SITE_CONFIG = Path("zensical.toml")

# The site's own pages, ahead of the ecosystems.
SITE_NAV: list[dict] = [
    {"Home": "index.md"},
    {"How it works": "how-it-works.md"},
    {"Want in or out?": "want-in-or-out.md"},
]


def prefixed(items: list[dict], prefix: str, directory: Path, errors: list[str], path: Path) -> list[dict]:
    """The section's items with each page under the ecosystem's directory, checking that it exists."""
    result = []
    for item in items:
        ((title, value),) = item.items()
        if isinstance(value, list):
            result.append({title: prefixed(value, prefix, directory, errors, path)})
        else:
            if not (directory / value).is_file():
                errors.append(f"{path}: {title}: {value} wasn't staged")
            result.append({title: prefix + value})
    return result


def toml(item: dict) -> str:
    """One nav entry as a TOML inline table. JSON's string escapes are valid TOML."""
    ((title, value),) = item.items()
    if isinstance(value, list):
        return f"{{ {json.dumps(title, ensure_ascii=False)} = [{', '.join(toml(child) for child in value)}] }}"
    return f"{{ {json.dumps(title, ensure_ascii=False)} = {json.dumps(value, ensure_ascii=False)} }}"


def main() -> int:
    require_root()
    errors: list[str] = []
    nav = list(SITE_NAV)

    for ecosystem in live():
        directory = DOCS / ecosystem.id
        path = directory / "nav.json"
        document = load_json(path, errors)
        if document is not None and validate(document, "nav.schema.json", path, errors):
            nav.append({ecosystem.name: prefixed(document["nav"], f"{ecosystem.id}/", directory, errors, path)})

    config = SITE_CONFIG.read_text(encoding="utf-8")
    with SITE_CONFIG.open("rb") as file:
        if "nav" in tomllib.load(file)["project"]:
            errors.append(f"{SITE_CONFIG}: has a nav of its own. merge_nav.py writes the navigation, so remove it")

    table = "[project]\n"
    if table not in config:
        errors.append(f"{SITE_CONFIG}: no [project] table to add the navigation to")
    if errors:
        return report(errors)

    entries = ",\n  ".join(toml(item) for item in nav)
    merged = config.replace(table, f"{table}nav = [\n  {entries},\n]\n", 1)

    # Parse the result, so a quoting mistake fails here instead of in Zensical.
    if tomllib.loads(merged)["project"]["nav"] != nav:
        return report([f"{BUILD / SITE_CONFIG}: the written navigation doesn't read back as written"])

    BUILD.mkdir(exist_ok=True)
    (BUILD / SITE_CONFIG).write_text(merged, encoding="utf-8")
    sections = len(nav) - len(SITE_NAV)
    print(f"Wrote {BUILD / SITE_CONFIG} with {sections} ecosystem section{'' if sections == 1 else 's'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
