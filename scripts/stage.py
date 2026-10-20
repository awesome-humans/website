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
own, to the shared conventions, and to each house profile's llms-<profile>.txt in it. It checks that every profile
an ecosystem staged is in houses.toml for that ecosystem, warns about a listed profile an
ecosystem staged nothing for, and writes
javascripts/houses.js, which lists them for the header's profile picker. It also fills the home page's ecosystem cards from ecosystems.toml, adds each ecosystem's logo to its card and its section index, draws the
diagrams on How it works from diagrams.py, and writes javascripts/repositories.js, which
points the header's repository link at each live ecosystem's repository under its /<id>/
pages. --local stages from a checkout on disk instead of build/repos/<id>/, to preview
an ecosystem change before pushing it.

fetch and stage cover every live ecosystem, and the one the PREVIEW_ECOSYSTEM
environment variable names, even while it's soon. build.yml sets it to the ecosystem a
pull request previews.

Exit codes: 0 done, 1 an ecosystem failed to fetch or stage, staged outside its own
directory, or staged a house profile houses.toml doesn't list for it, 2 not run from the repository root or bad arguments.
"""

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tomllib
from html import escape
from pathlib import Path

import diagrams
from ecosystems import DOCS, PREVIEW, REPOS, Ecosystem, House, built, houses, registry, report, require_root

PAGES = Path("pages")
SITE_CONFIG = Path("zensical.toml")

# The line in pages/index.md that the ecosystem cards replace.
CARDS_MARKER = "<!-- ecosystem-cards -->"

# Each ecosystem's logo, as <id>.svg, with <id>-dark.svg for the slate scheme when the
# logo doesn't read on a dark ground. It shows on the ecosystem's card and its section
# index. pages/credits.md credits each one.
LOGOS = Path("assets/ecosystems")
# A page's title, which the section index's logo follows.
TITLE = re.compile(r"^# .*\n", re.MULTILINE)

# A line in pages/how-it-works.md that a diagram from diagrams.py replaces.
DIAGRAM_PAGE = "how-it-works.md"
DIAGRAM_MARKER = re.compile(r"^<!-- diagram: ([a-z-]+) -->$", re.MULTILINE)

# The shared conventions under pages/conventions/, which the root llms.txt links to as
# raw Markdown, with what each covers.
CONVENTIONS = {
    "writing-style": ("Writing style", "the voice, spelling, and citation rules for all prose in every repository"),
    "admission-criteria": (
        "Admission criteria",
        "the track record a source needs, and the IDs and markings that limit citing it",
    ),
    "house-opinions": ("House opinions", "how a house opinion is woven into an ecosystem, and how it's marked"),
}
RAW_PAGES = "https://raw.githubusercontent.com/awesome-humans/website/main/pages/"

# The toolchains build.yml has a setup step for. A new one needs a step there too.
TOOLCHAINS = {"dotnet", "rust"}

SUMMARY = (
    "Opinionated best practices for each software ecosystem, distilled from the published"
    " writing of people and publications with a proven, multi-year track record. Each opinion"
    " states its recommendation first, then the rationale, then its sources, and targets the"
    " latest released versions."
)


def pairs(values: list[str], option: str, ecosystems: list[Ecosystem]) -> dict[str, str]:
    """Parse repeated <id>=<value> options, each naming an ecosystem the build stages."""
    ids = {ecosystem.id for ecosystem in ecosystems}
    parsed = {}
    for value in values:
        id, separator, rest = value.partition("=")
        if not separator or not rest:
            print(f"{option} {value}: expected <id>=<value>", file=sys.stderr)
            sys.exit(2)
        if id not in ids:
            print(
                f"{option} {value}: {id} isn't live in ecosystems.toml. To build a soon one, set {PREVIEW}={id}",
                file=sys.stderr,
            )
            sys.exit(2)
        parsed[id] = rest
    return parsed


def git(*args: str, cwd: Path) -> bool:
    return subprocess.run(["git", *args], cwd=cwd, check=False).returncode == 0


def fetch(ecosystems: list[Ecosystem], refs: dict[str, str]) -> int:
    errors = []
    for ecosystem in ecosystems:
        if ecosystem.toolchain not in TOOLCHAINS:
            errors.append(
                f"ecosystems.toml: {ecosystem.id} needs the {ecosystem.toolchain} toolchain, which build.yml doesn't set up"
            )
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
            errors.append(f"{ecosystem.id}: no checkout at {checkout}/. Run `just fetch` first")
            continue

        # The contract allows an ecosystem to write only under its own directory.
        before = set(os.listdir(out))
        command = [part.replace("{out}", str(out)) for part in shlex.split(ecosystem.stage)]
        print(f"Staging {ecosystem.id}: {shlex.join(command)}", flush=True)
        result = subprocess.run(command, cwd=checkout, check=False)
        if result.returncode != 0:
            errors.append(f"{ecosystem.id}: the stage command exited with {result.returncode}")
            continue

        added = set(os.listdir(out)) - before - {ecosystem.id}
        if added:
            errors.append(f"{ecosystem.id}: staged outside {ecosystem.id}/: {', '.join(sorted(added))}")
        if not (out / ecosystem.id / "index.md").is_file():
            errors.append(f"{ecosystem.id}: staged no {ecosystem.id}/index.md")

    profiles = houses(errors)
    if not errors:
        staged = check_houses(ecosystems, profiles, errors)
        write_llms(ecosystems, staged, errors)
        write_cards(errors)
        write_section_logos(ecosystems)
        write_diagrams(errors)
        write_repositories(ecosystems)
        write_houses(staged)
    return report(errors)


def check_houses(ecosystems: list[Ecosystem], profiles: list[House], errors: list[str]) -> dict[str, list[str]]:
    """Check the llms-<profile>.txt files each ecosystem staged against houses.toml, and
    return the live ecosystems of each profile, in registry order, for the profiles that have
    any. An ecosystem stages one for each profile its house blocks and regions belong to."""
    listed = {(house.id, ecosystem) for house in profiles for ecosystem in house.ecosystems}
    staged: dict[str, list[str]] = {house.id: [] for house in profiles}
    for ecosystem in ecosystems:
        for path in sorted((DOCS / ecosystem.id).glob("llms-*.txt")):
            profile = path.stem.removeprefix("llms-")
            if (profile, ecosystem.id) not in listed:
                errors.append(
                    f"{ecosystem.id}: staged house profile {profile}, which houses.toml doesn't list for {ecosystem.id}"
                )
                continue
            staged[profile].append(ecosystem.id)
    # Only a warning: a profile is registered before an ecosystem weaves its first opinion,
    # so the registration can merge first, and the ecosystem's pull request builds against it.
    for profile, ecosystem in sorted(listed):
        if ecosystem in {live.id for live in ecosystems} and ecosystem not in staged[profile]:
            print(
                f"houses.toml: {profile} lists {ecosystem}, which staged no {ecosystem}/llms-{profile}.txt",
                file=sys.stderr,
            )
    return {profile: found for profile, found in staged.items() if found}


def write_houses(staged: dict[str, list[str]]) -> None:
    """Write the house profiles with opinions on the site for javascripts/house.js, which
    adds the header's profile picker when there's at least one."""
    names = {house.id: house.name for house in houses([])}
    profiles = [{"id": profile, "name": names[profile], "ecosystems": found} for profile, found in staged.items()]
    (DOCS / "javascripts" / "houses.js").write_text(
        "// Written by scripts/stage.py from houses.toml. javascripts/house.js reads it.\n"
        f"window.ahHouses = {json.dumps(profiles)};\n",
        encoding="utf-8",
    )


def write_cards(errors: list[str]) -> None:
    """Replace the home page's marker with a card per ecosystem, as the design system's
    EcosystemCard shows: a link for a live one, and a muted card for one coming soon. Only
    a coming-soon card carries a chip, which says so in words, so the state doesn't rest on
    colour alone."""
    path = DOCS / "index.md"
    text = path.read_text(encoding="utf-8")
    if text.count(CARDS_MARKER) != 1:
        errors.append(f"{PAGES / 'index.md'}: expected one {CARDS_MARKER} line")
        return

    cards = []
    for ecosystem in registry():
        name, scope = escape(ecosystem.name), escape(ecosystem.scope)
        logo = logo_html(ecosystem.id, "")
        if ecosystem.status == "live":
            cards.append(
                f'<a class="ah-card ah-eco-{ecosystem.id}" href="{ecosystem.id}/">'
                f"{logo}<h3>{name}</h3><p>{scope}</p></a>"
            )
        else:
            cards.append(
                f'<div class="ah-card ah-card--soon ah-eco-{ecosystem.id}">'
                f'<span class="ah-chip ah-chip--eco ah-chip--dot">next</span>'
                f"{logo}<h3>{name}</h3><p>{scope}</p></div>"
            )
    block = '<div class="ah-cards">\n' + "\n".join(cards) + "\n</div>"
    path.write_text(text.replace(CARDS_MARKER, block), encoding="utf-8")


def logo_html(id: str, prefix: str) -> str:
    """The ecosystem's logo as images, with prefix leading to the site root, or nothing if
    it has none. The name beside it says which ecosystem it is, so the images are
    decorative and their alt text is empty."""
    light = LOGOS / f"{id}.svg"
    if not (PAGES / light).is_file():
        return ""
    dark = LOGOS / f"{id}-dark.svg"
    if not (PAGES / dark).is_file():
        return f'<span class="ah-eco-logo"><img src="{prefix}{light}" alt=""></span>'
    return (
        f'<span class="ah-eco-logo"><img class="ah-eco-logo--light" src="{prefix}{light}" alt="">'
        f'<img class="ah-eco-logo--dark" src="{prefix}{dark}" alt=""></span>'
    )


def write_section_logos(ecosystems: list[Ecosystem]) -> None:
    """Put each ecosystem's logo under the title of its section index, which the ecosystem
    stages from its README, so the ecosystem's own repository carries no logo."""
    for ecosystem in ecosystems:
        logo = logo_html(ecosystem.id, "../")
        if not logo:
            continue
        path = DOCS / ecosystem.id / "index.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(TITLE.sub(f"\\g<0>\n{logo}\n", text, count=1), encoding="utf-8")


def write_diagrams(errors: list[str]) -> None:
    """Replace each diagram marker on How it works with the diagram's inline SVG, which the
    theme colours, so the diagrams follow the light and dark toggle."""
    path = DOCS / DIAGRAM_PAGE
    text = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        figure = diagrams.figure(match[1])
        if figure is None:
            errors.append(f"{PAGES / DIAGRAM_PAGE}: no diagram named {match[1]} in scripts/diagrams.py")
            return match[0]
        return figure

    text, count = DIAGRAM_MARKER.subn(replace, text)
    if count == 0:
        errors.append(f"{PAGES / DIAGRAM_PAGE}: expected a <!-- diagram: <name> --> line")
    path.write_text(text, encoding="utf-8")


def write_repositories(ecosystems: list[Ecosystem]) -> None:
    """Write each live ecosystem's repository for javascripts/ecosystem.js, which loads after
    this file and before the theme reads the header's repository link."""
    repositories = {ecosystem.id: ecosystem.repository for ecosystem in ecosystems}
    (DOCS / "javascripts" / "repositories.js").write_text(
        "// Written by scripts/stage.py from ecosystems.toml. javascripts/ecosystem.js reads it.\n"
        f"window.ahRepositories = {json.dumps(repositories)};\n",
        encoding="utf-8",
    )


def write_llms(ecosystems: list[Ecosystem], staged: dict[str, list[str]], errors: list[str]) -> None:
    """Write the root llms.txt, which links to each ecosystem's own, per llmstxt.org, to the
    shared conventions, and to each house profile's."""
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
        summary = next(
            (line[2:] for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("> ")), None
        )
        if summary is None:
            errors.append(f"{path}: no summary blockquote")
            continue
        lines.append(f"- [{ecosystem.name}]({site_url}{ecosystem.id}/llms.txt): {summary}")

    lines += [
        "",
        "## Conventions",
        "",
        "Every ecosystem follows these. Read them before writing or reviewing an opinion.",
        "",
    ]
    for page, (title, covers) in CONVENTIONS.items():
        if not (PAGES / "conventions" / f"{page}.md").is_file():
            errors.append(f"{PAGES / 'conventions' / page}.md: missing, but CONVENTIONS lists it")
        lines.append(f"- [{title}]({RAW_PAGES}conventions/{page}.md): {covers}")

    if staged:
        names = {house.id: house.name for house in houses([])}
        ecosystem_names = {ecosystem.id: ecosystem.name for ecosystem in ecosystems}
        lines += [
            "",
            "## House profiles",
            "",
            (
                "The files above carry no house opinions. A house profile is one person's or organisation's"
                " preferences from experience, layered over the sourced opinions. Follow one only when the user"
                " chooses it, by reading its file for each ecosystem instead of llms.txt."
            ),
            "",
        ]
        for profile, found in staged.items():
            for ecosystem in found:
                lines.append(
                    f"- [{names[profile]}, {ecosystem_names[ecosystem]}]({site_url}{ecosystem}/llms-{profile}.txt):"
                    f" the {profile} house profile's {ecosystem_names[ecosystem]} opinions"
                )

    (DOCS / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    require_root()
    parser = argparse.ArgumentParser(description="Fetch and stage every live ecosystem.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("fetch").add_argument("--ref", action="append", default=[], metavar="ID=REF")
    commands.add_parser("stage").add_argument("--local", action="append", default=[], metavar="ID=PATH")
    args = parser.parse_args()

    ecosystems = built()
    if args.command == "fetch":
        return fetch(ecosystems, pairs(args.ref, "--ref", ecosystems))
    return stage(ecosystems, pairs(args.local, "--local", ecosystems))


if __name__ == "__main__":
    sys.exit(main())
