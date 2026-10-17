# /// script
# requires-python = ">=3.14"
# dependencies = ["jsonschema==4.26.0"]
# ///
"""Validate each staged sources.json, apply data/consent.toml, and write build/sources.json.

    uv run scripts/collate_sources.py

Run it after stage.py. Each ecosystem's export must match the schema and hold its
ids sorted and unique. A source in more than one ecosystem must have the same kind
in each, because a person can have a portrait and a publication a logo. The combined
file lists each source once, with what each ecosystem's roster says about it. The
image scripts read it to draw the source images and the montage.

consent.toml decides what the combined file says about each source's image. A source
with a granted portrait or logo gets an image entry, with the URL to download it from.
A source that opted out of citation is left out of the file altogether.

Exit codes: 0 written, 1 an export is missing, invalid, unsorted, or disagrees with
another ecosystem on a source's kind, or consent.toml is invalid, 2 not run from the
repository root.
"""

import datetime
import json
import sys
import tomllib
from itertools import pairwise
from pathlib import Path

from ecosystems import BUILD, DOCS, live, load_json, report, require_root, validate

OUTPUT = BUILD / "sources.json"
CONSENT = Path("data/consent.toml")

# What a source is, as opposed to what one ecosystem's roster says about it.
IDENTITY = ("id", "name", "kind")

# The image each kind of source can have: its consent.toml key, and that key's URL.
IMAGES = {"person": ("portrait", "portrait_url"), "publication": ("logo", "logo_url")}
IMAGE_STATES = ("granted", "declined", "unknown")
CITATION_STATES = ("allowed", "opted-out")
REQUIRED = ("evidence", "recorded")


def load_consent(errors: list[str]) -> dict[str, dict]:
    """Read consent.toml, checking what can be checked without the rosters."""
    try:
        with CONSENT.open("rb") as file:
            consent = tomllib.load(file)
    except FileNotFoundError:
        errors.append(f"{CONSENT}: missing")
        return {}
    except tomllib.TOMLDecodeError as error:
        errors.append(f"{CONSENT}: not valid TOML: {error}")
        return {}

    for previous, current in pairwise(consent):
        if current < previous:
            errors.append(f"{CONSENT}: {current} is out of order, after {previous}")

    known = {key for keys in IMAGES.values() for key in keys} | {"citation", *REQUIRED}
    for id, entry in consent.items():
        if not isinstance(entry, dict):
            errors.append(f"{CONSENT}: {id} must be a table")
            continue
        for key in sorted(entry.keys() - known):
            errors.append(f"{CONSENT}: {id}.{key} isn't a consent key")
        for key in REQUIRED:
            if key not in entry:
                errors.append(f"{CONSENT}: {id} needs {key}")
        # A datetime is a date too, so compare the type itself.
        if "recorded" in entry and type(entry["recorded"]) is not datetime.date:
            errors.append(f"{CONSENT}: {id}.recorded must be a TOML date, such as 2026-11-02")
        for state, _ in IMAGES.values():
            if entry.get(state, "unknown") not in IMAGE_STATES:
                errors.append(f"{CONSENT}: {id}.{state} must be one of {', '.join(IMAGE_STATES)}")
        for key in ("evidence", *(url for _, url in IMAGES.values())):
            if key in entry and not str(entry[key]).startswith("https://"):
                errors.append(f"{CONSENT}: {id}.{key} must be an https:// URL")
        if entry.get("citation", "allowed") not in CITATION_STATES:
            errors.append(f"{CONSENT}: {id}.citation must be one of {', '.join(CITATION_STATES)}")
    return consent


def apply_consent(combined: dict[str, dict], consent: dict[str, dict], errors: list[str]) -> None:
    """Drop the sources that opted out, and give each granted image its download URL."""
    for id, entry in consent.items():
        opted_out = entry.get("citation") == "opted-out"
        source = combined.get(id)
        if source is None:
            # A roster drops an opted-out source within 30 days, and its table stays as the
            # record. Any other unknown id is a typo, which would silently show nothing.
            if not opted_out:
                errors.append(f"{CONSENT}: {id} isn't in any ecosystem's roster")
            continue
        if opted_out:
            del combined[id]
            continue

        state, url = IMAGES[source["kind"]]
        for kind, keys in IMAGES.items():
            if kind != source["kind"]:
                for key in keys:
                    if key in entry:
                        errors.append(f"{CONSENT}: {id} is a {source['kind']}, so it can't have {key}")
        if entry.get(state) != "granted":
            continue

        logins = sorted({roster["github"] for roster in source["ecosystems"].values() if "github" in roster})
        if url in entry:
            source["image"] = {"kind": state, "url": entry[url]}
        elif state == "portrait" and len(logins) == 1:
            source["image"] = {"kind": state, "url": f"https://github.com/{logins[0]}.png"}
        elif state == "portrait" and logins:
            errors.append(f"{CONSENT}: {id} has a GitHub login in more than one roster, so it needs {url}")
        else:
            errors.append(f"{CONSENT}: {id} grants a {state}, so it needs {url}")


def main() -> int:
    require_root()
    errors: list[str] = []
    combined: dict[str, dict] = {}

    for ecosystem in live():
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

    consent = load_consent(errors)
    if errors:
        return report(errors)

    apply_consent(combined, consent, errors)
    if errors:
        return report(errors)

    BUILD.mkdir(exist_ok=True)
    document = {"version": 1, "sources": [combined[id] for id in sorted(combined)]}
    OUTPUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(combined)} sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
