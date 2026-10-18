"""The ecosystem and house profile registries, and the staging paths that the site scripts share.

Imported by stage.py, merge_nav.py, and collate_sources.py, which run from the
repository root. It isn't a script of its own.
"""

import json
import re
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REGISTRY = Path("ecosystems.toml")
HOUSES = Path("houses.toml")
PROFILE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
BUILD = Path("build")
DOCS = BUILD / "docs"
REPOS = BUILD / "repos"
SCHEMAS = Path("schemas")


@dataclass(frozen=True)
class Ecosystem:
    id: str
    name: str
    repository: str
    toolchain: str
    stage: str
    status: str
    scope: str


@dataclass(frozen=True)
class House:
    id: str
    name: str
    kind: str
    ecosystems: list[str]
    approved: date


def houses(errors: list[str]) -> list[House]:
    """Every house profile, in registry order, recording a malformed entry as an error."""
    with HOUSES.open("rb") as file:
        found = [House(**entry) for entry in tomllib.load(file).get("house", [])]
    ids = {ecosystem.id for ecosystem in registry()}
    for house in found:
        if not PROFILE.fullmatch(house.id):
            errors.append(f"{HOUSES}: {house.id} isn't a profile id: use lowercase words joined by hyphens")
        if house.kind not in ("person", "organisation"):
            errors.append(f"{HOUSES}: {house.id} has kind {house.kind}, not person or organisation")
        for ecosystem in house.ecosystems:
            if ecosystem not in ids:
                errors.append(f"{HOUSES}: {house.id} lists {ecosystem}, which isn't in {REGISTRY}")
    if len({house.id for house in found}) != len(found):
        errors.append(f"{HOUSES}: a profile id appears more than once")
    return found


def require_root() -> None:
    """Exit with 2 unless run from the repository root, as every site script does."""
    if not REGISTRY.is_file():
        print(f"No {REGISTRY} here. Run this script from the repository root.", file=sys.stderr)
        sys.exit(2)


def registry() -> list[Ecosystem]:
    """Every ecosystem, live or soon, in registry order, which is the order the site shows them in."""
    with REGISTRY.open("rb") as file:
        return [Ecosystem(**entry) for entry in tomllib.load(file)["ecosystem"]]


def live() -> list[Ecosystem]:
    """The live ecosystems, in registry order."""
    return [ecosystem for ecosystem in registry() if ecosystem.status == "live"]


def load_json(path: Path, errors: list[str]) -> dict | None:
    """Read a staged JSON file, recording a missing or malformed one as an error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path}: missing")
    except json.JSONDecodeError as error:
        errors.append(f"{path}: not valid JSON: {error}")
    return None


def validate(document: dict, schema: str, path: Path, errors: list[str]) -> bool:
    """Validate a staged document against one of the contract's schemas."""
    # Imported here so that a script without jsonschema in its inline metadata can
    # still use the rest of this module.
    from jsonschema import Draft202012Validator

    validator = Draft202012Validator(json.loads((SCHEMAS / schema).read_text(encoding="utf-8")))
    found = sorted(validator.iter_errors(document), key=lambda error: list(error.absolute_path))
    for error in found:
        location = "/".join(str(part) for part in error.absolute_path) or "(root)"
        errors.append(f"{path}: {location}: {error.message}")
    return not found


def report(errors: list[str]) -> int:
    """Print the errors, and return the exit code: 0 for none, 1 for findings."""
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0
