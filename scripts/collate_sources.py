# /// script
# requires-python = ">=3.14"
# dependencies = ["jsonschema==4.26.0"]
# ///
"""Validate each staged sources.json, and combine them into build/sources.json.

    uv run scripts/collate_sources.py

Run it after stage.py. Each ecosystem's export must match the schema and hold its
ids sorted and unique. A source in more than one ecosystem must have the same kind
in each, because a person can have a portrait and a publication a logo. The combined
file lists each source once, with what each ecosystem's roster says about it. The
image scripts read it to draw the source images and the montage.

Exit codes: 0 written, 1 an export is missing, invalid, unsorted, or disagrees with
another ecosystem on a source's kind, 2 not run from the repository root.
"""

import json
import sys
from itertools import pairwise

from ecosystems import BUILD, DOCS, built, load_json, report, require_root, validate

OUTPUT = BUILD / "sources.json"

# What a source is, as opposed to what one ecosystem's roster says about it.
IDENTITY = ("id", "name", "kind")


def main() -> int:
    require_root()
    errors: list[str] = []
    combined: dict[str, dict] = {}

    for ecosystem in built():
        path = DOCS / ecosystem.id / "sources.json"
        document = load_json(path, errors)
        if document is None or not validate(document, "sources.schema.json", path, errors):
            continue

        ids = [source["id"] for source in document["sources"]]
        for previous, current in pairwise(ids):
            if current == previous:
                errors.append(f"{path}: {current} appears more than once")
            elif current < previous:
                errors.append(f"{path}: {current} is out of order, after {previous}")

        for source in document["sources"]:
            entry = combined.setdefault(source["id"], {key: source[key] for key in IDENTITY} | {"ecosystems": {}})
            if entry["kind"] != source["kind"]:
                first = next(iter(entry["ecosystems"]))
                errors.append(f"{path}: {source['id']} is a {source['kind']} here, but a {entry['kind']} in {first}")
            entry["ecosystems"][ecosystem.id] = {key: value for key, value in source.items() if key not in IDENTITY}

    if errors:
        return report(errors)

    BUILD.mkdir(exist_ok=True)
    document = {"version": 1, "sources": [combined[id] for id in sorted(combined)]}
    OUTPUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(combined)} sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
