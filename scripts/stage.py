# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Fetch every live ecosystem, and stage it with the shared pages into build/docs/.

    uv run scripts/stage.py fetch [--ref <id>=<ref>]...
    uv run scripts/stage.py stage [--local <id>=<path>]...

fetch clones each live ecosystem in ecosystems.toml into build/repos/<id>/, at main
or at the ref --ref names. A pull request's preview passes its head commit this way.
In GitHub Actions, it also writes the toolchains the ecosystems need to the step's
outputs, so build.yml sets up only those.

stage copies pages/ into build/docs/, runs each ecosystem's stage command with {out}
set to build/docs/, and writes the root llms.txt, which links to each ecosystem's
own. It also fills the home page's ecosystem cards from ecosystems.toml. --local stages from a checkout on disk instead of build/repos/<id>/, to preview
an ecosystem change before pushing it.

Exit codes: 0 done, 1 an ecosystem failed to fetch or stage, or staged outside its
own directory, 2 not run from the repository root or bad arguments.
"""

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import tomllib
from html import escape
from pathlib import Path

from ecosystems import DOCS, REPOS, Ecosystem, live, registry, report, require_root

PAGES = Path("pages")
SITE_CONFIG = Path("zensical.toml")

# The line in pages/index.md that the ecosystem cards replace.
CARDS_MARKER = "<!-- ecosystem-cards -->"

# The toolchains build.yml has a setup step for. A new one needs a step there too.
TOOLCHAINS = {"dotnet"}

SUMMARY = (
    "Opinionated best practices for each software ecosystem, distilled from the published"
    " writing of people and publications with a proven, multi-year track record. Each opinion"
    " states its recommendation first, then the rationale, then its sources, and targets the"
    " latest released versions."
)


def pairs(values: list[str], option: str, ecosystems: list[Ecosystem]) -> dict[str, str]:
    """Parse repeated <id>=<value> options, each naming a live ecosystem."""
    ids = {ecosystem.id for ecosystem in ecosystems}
    parsed = {}
    for value in values:
        id, separator, rest = value.partition("=")
        if not separator or not rest:
            print(f"{option} {value}: expected <id>=<value>", file=sys.stderr)
            sys.exit(2)
        if id not in ids:
            print(f"{option} {value}: {id} isn't a live ecosystem in ecosystems.toml", file=sys.stderr)
            sys.exit(2)
        parsed[id] = rest
    return parsed


def git(*args: str, cwd: Path) -> bool:
    return subprocess.run(["git", *args], cwd=cwd).returncode == 0


def fetch(ecosystems: list[Ecosystem], refs: dict[str, str]) -> int:
    errors = []
    for ecosystem in ecosystems:
        if ecosystem.toolchain not in TOOLCHAINS:
            errors.append(f"ecosystems.toml: {ecosystem.id} needs the {ecosystem.toolchain} toolchain, which build.yml doesn't set up")
            continue

        # A shallow fetch of one ref, which can be a branch or a commit SHA. GitHub
        # serves a pull request's head commit by SHA, including one from a fork.
        directory = REPOS / ecosystem.id
        shutil.rmtree(directory, ignore_errors=True)
        directory.mkdir(parents=True)
        ref = refs.get(ecosystem.id, "main")
        url = f"https://github.com/{ecosystem.repository}"
        if not (
            git("init", "--quiet", cwd=directory)
            and git("fetch", "--quiet", "--depth", "1", url, ref, cwd=directory)
            and git("checkout", "--quiet", "--detach", "FETCH_HEAD", cwd=directory)
        ):
            errors.append(f"{ecosystem.id}: couldn't fetch {ref} from {url}")
            continue
        print(f"Fetched {ecosystem.repository} at {ref} into {directory}/")

    if output := os.environ.get("GITHUB_OUTPUT"):
        toolchains = sorted({ecosystem.toolchain for ecosystem in ecosystems})
        with open(output, "a", encoding="utf-8") as file:
            file.write(f"toolchains={' '.join(toolchains)}\n")
            # setup-dotnet reads the SDK version from the ecosystem's own global.json.
            for ecosystem in ecosystems:
                if ecosystem.toolchain == "dotnet":
                    file.write(f"dotnet-global-json={REPOS / ecosystem.id / 'global.json'}\n")
                    break

    return report(errors)


def stage(ecosystems: list[Ecosystem], local: dict[str, str]) -> int:
    errors = []
    shutil.rmtree(DOCS, ignore_errors=True)
    shutil.copytree(PAGES, DOCS)
    out = DOCS.resolve()

    for ecosystem in ecosystems:
        checkout = Path(local[ecosystem.id]) if ecosystem.id in local else REPOS / ecosystem.id
        if not checkout.is_dir():
            errors.append(f"{ecosystem.id}: no checkout at {checkout}/. Run `uv run scripts/stage.py fetch` first")
            continue

        # The contract allows an ecosystem to write only under its own directory.
        before = set(os.listdir(out))
        command = [part.replace("{out}", str(out)) for part in shlex.split(ecosystem.stage)]
        print(f"Staging {ecosystem.id}: {shlex.join(command)}", flush=True)
        result = subprocess.run(command, cwd=checkout)
        if result.returncode != 0:
            errors.append(f"{ecosystem.id}: the stage command exited with {result.returncode}")
            continue

        added = set(os.listdir(out)) - before - {ecosystem.id}
        if added:
            errors.append(f"{ecosystem.id}: staged outside {ecosystem.id}/: {', '.join(sorted(added))}")
        if not (out / ecosystem.id / "index.md").is_file():
            errors.append(f"{ecosystem.id}: staged no {ecosystem.id}/index.md")

    if not errors:
        write_llms(ecosystems, errors)
        write_cards(errors)
    return report(errors)


def write_cards(errors: list[str]) -> None:
    """Replace the home page's marker with a card per ecosystem, as the design system's
    EcosystemCard shows: a link for a live one, and a muted card for one coming soon. The
    chip says which in words, so the state doesn't rest on colour alone."""
    path = DOCS / "index.md"
    text = path.read_text(encoding="utf-8")
    if text.count(CARDS_MARKER) != 1:
        errors.append(f"{PAGES / 'index.md'}: expected one {CARDS_MARKER} line")
        return

    cards = []
    for ecosystem in registry():
        name, scope = escape(ecosystem.name), escape(ecosystem.scope)
        if ecosystem.status == "live":
            cards.append(
                f'<a class="ah-card ah-eco-{ecosystem.id}" href="{ecosystem.id}/">'
                f'<span class="ah-chip ah-chip--eco ah-chip--dot">live</span>'
                f"<h3>{name}</h3><p>{scope}</p></a>"
            )
        else:
            cards.append(
                f'<div class="ah-card ah-card--soon ah-eco-{ecosystem.id}">'
                f'<span class="ah-chip ah-chip--eco ah-chip--dot">next</span>'
                f"<h3>{name}</h3><p>{scope}</p></div>"
            )
    block = '<div class="ah-cards">\n' + "\n".join(cards) + "\n</div>"
    path.write_text(text.replace(CARDS_MARKER, block), encoding="utf-8")


def write_llms(ecosystems: list[Ecosystem], errors: list[str]) -> None:
    """Write the root llms.txt, which links to each ecosystem's own, per llmstxt.org."""
    with SITE_CONFIG.open("rb") as file:
        site_url = tomllib.load(file)["project"]["site_url"]

    lines = [
        "# Awesome Humans",
        "",
        f"> {SUMMARY}",
        "",
        "Each ecosystem has its own llms.txt, which links to its opinions, templates, and skills as raw Markdown.",
        "",
        "## Ecosystems",
        "",
    ]
    for ecosystem in ecosystems:
        # The ecosystem's own summary is the blockquote at the top of its llms.txt.
        path = DOCS / ecosystem.id / "llms.txt"
        if not path.is_file():
            errors.append(f"{ecosystem.id}: staged no {ecosystem.id}/llms.txt")
            continue
        summary = next((line[2:] for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("> ")), None)
        if summary is None:
            errors.append(f"{path}: no summary blockquote")
            continue
        lines.append(f"- [{ecosystem.name}]({site_url}{ecosystem.id}/llms.txt): {summary}")

    (DOCS / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    require_root()
    parser = argparse.ArgumentParser(description="Fetch and stage every live ecosystem.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("fetch").add_argument("--ref", action="append", default=[], metavar="ID=REF")
    commands.add_parser("stage").add_argument("--local", action="append", default=[], metavar="ID=PATH")
    args = parser.parse_args()

    ecosystems = live()
    if args.command == "fetch":
        return fetch(ecosystems, pairs(args.ref, "--ref", ecosystems))
    return stage(ecosystems, pairs(args.local, "--local", ecosystems))


if __name__ == "__main__":
    sys.exit(main())
