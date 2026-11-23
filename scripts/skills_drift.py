# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Check that the skills the ecosystems copy from each other differ only where recorded.

    uv run scripts/skills_drift.py [--local <id>=<path>]...
    uv run scripts/skills_drift.py --update [--local <id>=<path>]... [<skill>]...

Each ecosystem keeps its own copy of the maintenance skills, such as vet-source, and most
of each copy is the same text. A change to that text belongs in every copy, and nothing
else says so when it lands in one. This compares each copy with the first live ecosystem's,
line by line, and fails when the lines that differ aren't the ones skills-drift/ records.

skills-drift/<id>/<skill>.diff holds the differences between the first live ecosystem's
copy of a skill and <id>'s: each run of lines that differ, with no line numbers, so a
change made to both copies alike moves nothing. Before it compares, it writes each
ecosystem's id, name, and repository as <id>, <name>, and <repository>, so a line that
differs only by those isn't a difference. The skills it checks are the ones with a file
there.

--update writes the files from the copies as they are, and adds a file for each skill
named. Run it when a difference belongs to the ecosystem, such as its own example, and
read the change to the file before you commit it.

It reads each copy from build/repos/<id>/, where `just fetch` leaves it, or from the
checkout --local names, as `just stage` does.

Exit codes: 0 the copies differ only as recorded, or --update wrote the files, 1 they
differ in another way, or a copy is missing, 2 not run from the repository root, or a
malformed --local.
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

from ecosystems import REPOS, Ecosystem, live, report, require_root

RECORDED = Path("skills-drift")
# The line between two runs of differing lines in a recorded file. A line from a skill
# starts with - or +, so it's never this.
BREAK = "@@"


def checkouts(values: list[str], ecosystems: list[Ecosystem]) -> dict[str, Path]:
    """Where each ecosystem's checkout is: build/repos/<id>/, or the path --local gives it."""
    found = {ecosystem.id: REPOS / ecosystem.id for ecosystem in ecosystems}
    for value in values:
        id, separator, path = value.partition("=")
        if not separator or not path or id not in found:
            print(
                f"--local {value}: expected <id>=<path>, for an ecosystem that's live in ecosystems.toml",
                file=sys.stderr,
            )
            sys.exit(2)
        found[id] = Path(path)
    return found


def neutral(text: str, ecosystem: Ecosystem) -> list[str]:
    """A skill's lines, with the ecosystem's own repository, name, and id written as placeholders."""
    text = text.replace(ecosystem.repository, "<repository>").replace(ecosystem.name, "<name>")
    return re.sub(rf"(?<![A-Za-z0-9]){re.escape(ecosystem.id)}(?![A-Za-z0-9])", "<id>", text).splitlines()


def differences(first: list[str], other: list[str]) -> list[str]:
    """Each run of lines that differ, as the first copy's lines with - and the other's with +."""
    matcher = difflib.SequenceMatcher(None, first, other, autojunk=False)
    return [
        "\n".join([f"-{line}" for line in first[i1:i2]] + [f"+{line}" for line in other[j1:j2]])
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    ]


def written(first: Ecosystem, other: Ecosystem, skill: str, runs: list[str]) -> str:
    """A recorded file's text."""
    header = [f"--- {first.repository}: skills/{skill}/SKILL.md", f"+++ {other.repository}: skills/{skill}/SKILL.md"]
    return "\n".join(header + [f"{BREAK}\n{run}" for run in runs]) + "\n"


def recorded(text: str) -> list[str]:
    """The runs a recorded file holds."""
    return [run.strip("\n") for run in f"\n{text}".split(f"\n{BREAK}\n")[1:]]


def indented(run: str) -> str:
    return "\n".join(f"    {line}" for line in run.splitlines())


def main() -> int:
    require_root()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--local", action="append", default=[], metavar="ID=PATH")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("skills", nargs="*", metavar="SKILL")
    args = parser.parse_args()
    if args.skills and not args.update:
        parser.error("name a skill only with --update, which adds a file for it")

    ecosystems = live()
    paths = checkouts(args.local, ecosystems)
    first, others = ecosystems[0], ecosystems[1:]
    errors: list[str] = []
    drifted = False
    for other in others:
        directory = RECORDED / other.id
        skills = sorted({path.stem for path in directory.glob("*.diff")} | set(args.skills))
        if not skills:
            errors.append(f"{directory}/: records no skill. To add one, run `just skills-drift --update <skill>`")
        for skill in skills:
            copies = []
            for ecosystem in (first, other):
                copy = paths[ecosystem.id] / "skills" / skill / "SKILL.md"
                if copy.is_file():
                    copies.append(neutral(copy.read_text(encoding="utf-8"), ecosystem))
                else:
                    errors.append(f"{copy}: missing. Run `just fetch` first, or pass --local {ecosystem.id}=<path>")
            if len(copies) < 2:
                continue

            runs = differences(*copies)
            path = directory / f"{skill}.diff"
            text = written(first, other, skill, runs)
            if args.update:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
                print(f"{path}: recorded {len(runs)} differences")
                continue
            before = path.read_text(encoding="utf-8")
            if before == text:
                print(f"{skill}: {first.id} and {other.id} differ in the {len(runs)} places recorded")
                continue

            drifted = True
            known = recorded(before)
            new = [run for run in runs if run not in known]
            gone = [run for run in known if run not in runs]
            lines = [f"{path}: {skill} differs between {first.id} and {other.id} in a way this file doesn't record."]
            lines += [f"  A new difference:\n{indented(run)}" for run in new]
            lines += [f"  A recorded difference that's gone:\n{indented(run)}" for run in gone]
            if not new and not gone:
                lines.append("  The same differences, in another order or under another header.")
            errors.append("\n".join(lines))

    if drifted:
        errors.append(
            "Make the same change to the other ecosystem's copy, so the copies agree again."
            " If the difference belongs to one ecosystem, such as its own example, record it with"
            " `just skills-drift --update`, and commit the changed file."
        )
    return report(errors)


if __name__ == "__main__":
    sys.exit(main())
