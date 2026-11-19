# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Publish each ecosystem's consumer skills in build/public/, for `npx skills add`.

    uv run scripts/publish_skills.py

A consumer skill is one a project runs on its own code, such as review-project. Each
ecosystem names its own in the `skills` key of ecosystems.toml. For each one, this writes
an archive that holds the skill and every opinion and template the ecosystem's llms.txt
links, so an agent reads them from disk and fetches nothing. It publishes the skill as
<verb>-<id>-<rest>, such as review-dotnet-project, because two ecosystems' skills are
installed side by side, and one named review-project would overwrite the other.

It writes a discovery index, which the skills CLI reads from
<address>/.well-known/agent-skills/index.json, at four kinds of address:

- /                        Every ecosystem's skills, with no house opinions.
- /<id>/                   One ecosystem's.
- /house/<profile>/        Every ecosystem's, with that profile's house opinions where an
                           ecosystem holds any, and the default copy where it doesn't.
- /<id>/house/<profile>/   One ecosystem's, for a profile it holds opinions for.

Run it after `zensical build`, which drops every path that starts with a dot, and from
what `just stage` left in build/docs/. An archive's bytes depend only on the files in it,
so its digest changes only when a skill, an opinion, or a template does, and `skills
check` in a project reports an update only then.

Exit codes: 0 done, 1 a skill, an llms.txt, or a file one links is missing or malformed,
2 not run from the repository root, or nothing is staged or built.
"""

import gzip
import hashlib
import io
import json
import re
import sys
import tarfile
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ecosystems import BUILD, DOCS, NO_PROFILE, Ecosystem, built, report, require_root

PUBLIC = BUILD / "public"
SITE_CONFIG = Path("zensical.toml")
# Where the skills CLI looks for an index, under the address it's given.
WELL_KNOWN = ".well-known/agent-skills"
# The index format the skills CLI reads: https://github.com/vercel-labs/skills.
SCHEMA = "https://schemas.agentskills.io/discovery/0.2.0/schema.json"
# The path under an ecosystem, or under the root, that scopes an install to a house profile.
HOUSE = "house"

# A link in an llms.txt, and the heading of the section it's under, as in test_llms.py.
LINK = re.compile(r"^- \[(?P<title>.+?)\]\((?P<url>[^)\s]+)\)")
SECTION = re.compile(r"^## (?P<title>.+)$")
# The sections an ecosystem's llms.txt lists its opinions and templates under.
KINDS = ("opinions", "templates")
# A skill's frontmatter, and the two fields the index needs from it.
FRONTMATTER = re.compile(r"\A---\n(?P<fields>.*?\n)---\n", re.DOTALL)
NAME = re.compile(r"^name: *(?P<value>.+)$", re.MULTILINE)
DESCRIPTION = re.compile(r"^description: *(?P<value>.+)$", re.MULTILINE)
# What the skills CLI accepts as a name, and the longest description it accepts.
VALID_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
# A Markdown link's target.
MARKDOWN_LINK = re.compile(r"\]\((?P<target>[^)\s]+)\)")
# A copy's path under raw/<profile>/, which is the same for every profile's copy of a file.
RAW = re.compile(r"/raw/[^/]+/(?P<path>.+)$")

# What a published skill says about the files it carries. It goes before the skill's first
# section, as stage.py puts the reading rules into each llms.txt, and its two reading rules
# are the ones from READING there that still apply once nothing is fetched. Keep them in step.
# A skill written for its own repository says "this repository" and `opinions/`, and its
# staged copy says to read each file from the site, so this section says which copy wins.
BUNDLE = """## Where the opinions and templates are

This copy of the skill carries every {name} opinion and template, as [{repository}](https://github.com/{repository}) published them, {profile}. The opinions are in [references/opinions/](references/opinions/), and the templates in [references/templates/](references/templates/), beside this file. In this skill, `opinions/` and `templates/` mean those two directories, and "this repository" means {repository}.

- **Read them from this skill's directory,** with a file-reading tool. Where another paragraph says to read an opinion or a template from the site or the repository, read this copy's. Don't use a copy the target holds.
- **Read every opinion that covers something the project uses,** and every template the project has a file for, not only the ones the task names.
- **Say which opinions and templates you read in full,** and which you skipped.
- **Check that the copy is current** with `npx skills check`, and update it with `npx skills update`. Each opinion gives its `last-reviewed` date.
- {other}
"""


@dataclass(frozen=True)
class Published:
    """One skill's archive, as an index lists it."""

    name: str
    description: str
    # The archive's path under build/public/.
    path: PurePosixPath
    digest: str


def consumer_name(skill: str, id: str) -> str:
    """The name a skill is published under: its first word, the ecosystem, then the rest."""
    verb, _, rest = skill.partition("-")
    return "-".join(part for part in (verb, id, rest) if part)


def linked(llms: Path, site_url: str, errors: list[str]) -> dict[str, tuple[str, Path]]:
    """The opinions and templates an llms.txt links, by the path each takes in an archive,
    with the address it's linked at and its staged file."""
    found: dict[str, tuple[str, Path]] = {}
    kind = ""
    for line in llms.read_text(encoding="utf-8").splitlines():
        if section := SECTION.match(line):
            kind = next((kind for kind in KINDS if section["title"].endswith(f" {kind}")), "")
            continue
        if not kind or not (link := LINK.match(line)):
            continue
        url = link["url"]
        if not url.startswith(site_url):
            errors.append(f"{llms}: {url} isn't on the site, so no skill can carry it")
            continue
        staged = DOCS / url.removeprefix(site_url)
        # An opinion keeps its file name, without the .txt its copy on the site adds. A
        # template's link text is its path in a project, such as projects/Domain.fs.
        name = staged.name.removesuffix(".txt") if kind == "opinions" else link["title"]
        path = PurePosixPath("references", kind, name)
        if ".." in path.parts or PurePosixPath(name).is_absolute():
            errors.append(f"{llms}: {name} isn't a path inside a skill")
        elif not staged.is_file():
            errors.append(f"{llms}: links {url}, but nothing staged {staged}")
        elif str(path) in found:
            errors.append(f"{llms}: links {path} twice")
        else:
            found[str(path)] = (url, staged)
    if not any(path.startswith("references/opinions/") for path in found):
        errors.append(f"{llms}: links no opinions")
    return found


def skill_text(
    ecosystem: Ecosystem, skill: str, profile: str, files: dict[str, tuple[str, Path]], site_url: str, errors: list[str]
) -> tuple[str, str, str] | None:
    """A skill's published name, description, and text: renamed, with the section on the
    files it carries, and with each link to one of them pointing at the copy beside it."""
    staged = DOCS / ecosystem.id / "raw" / NO_PROFILE / "skills" / skill / "SKILL.md.txt"
    if not staged.is_file():
        errors.append(f"{ecosystem.id}: ecosystems.toml lists the skill {skill}, but nothing staged {staged}")
        return None
    text = staged.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER.match(text)
    description = DESCRIPTION.search(frontmatter["fields"]) if frontmatter else None
    if not frontmatter or not description or NAME.search(frontmatter["fields"]) is None:
        errors.append(f"{staged}: no frontmatter with a name and a description")
        return None
    name = consumer_name(skill, ecosystem.id)
    if not VALID_NAME.fullmatch(name) or len(name) > MAX_NAME:
        errors.append(f"{staged}: {name} isn't a name the skills CLI accepts")
        return None
    summary = description["value"].strip()
    if len(summary) > MAX_DESCRIPTION:
        errors.append(f"{staged}: the description is over {MAX_DESCRIPTION} characters, the most an index entry holds")
        return None

    fields = NAME.sub(f"name: {name}", frontmatter["fields"], count=1)
    body = text[frontmatter.end() :]
    # A skill is staged once, linking the default copy of each file, so match a link to the
    # file this archive carries by its path under raw/<profile>/, not by its whole address.
    local = {raw["path"]: path for path, (url, _) in files.items() if (raw := RAW.search(url))}

    def carried(link: re.Match[str]) -> str:
        target = link["target"]
        raw = RAW.search(target) if target.startswith(f"{site_url}{ecosystem.id}/") else None
        return f"]({local[raw['path']] if raw and raw['path'] in local else target})"

    body = MARKDOWN_LINK.sub(carried, body)

    if profile == NO_PROFILE:
        carries = "with no house opinions"
        other = (
            "**To follow a house profile, install its copy of this skill,** from"
            f" `{site_url}{ecosystem.id}/{HOUSE}/<profile>`. This copy has no house blocks or regions to keep."
        )
    else:
        carries = f"with the `{profile}` house profile's opinions"
        other = (
            f"**This copy holds the `{profile}` profile's house blocks and regions, and no other profile's.** If the"
            " user names no profile, skip every house block, and compare each template with its house regions removed."
        )
    section = BUNDLE.format(name=ecosystem.name, repository=ecosystem.repository, profile=carries, other=other)
    heading = re.search(r"^## ", body, re.MULTILINE)
    at = heading.start() if heading else len(body)
    body = body[:at].rstrip("\n") + "\n\n" + section + "\n" + body[at:]
    return name, summary, f"---\n{fields}---\n{body.rstrip('\n')}\n"


def archive(files: dict[str, bytes]) -> bytes:
    """A .tar.gz whose bytes depend only on the files' names and contents."""
    tarball = io.BytesIO()
    with tarfile.open(fileobj=tarball, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for name, data in sorted(files.items()):
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(data))
    packed = io.BytesIO()
    with gzip.GzipFile(fileobj=packed, mode="wb", mtime=0, filename="") as file:
        file.write(tarball.getvalue())
    return packed.getvalue()


def publish(ecosystem: Ecosystem, profile: str, site_url: str, errors: list[str]) -> list[Published]:
    """Write the archive of each of an ecosystem's consumer skills, with one profile's copy
    of the opinions and templates, and return them for the indexes."""
    llms = DOCS / ecosystem.id / ("llms.txt" if profile == NO_PROFILE else f"llms-{profile}.txt")
    if not llms.is_file():
        errors.append(f"{ecosystem.id}: staged no {llms.name}")
        return []
    files = linked(llms, site_url, errors)
    scope = PurePosixPath(ecosystem.id) if profile == NO_PROFILE else PurePosixPath(ecosystem.id, HOUSE, profile)
    published: list[Published] = []
    for skill in ecosystem.skills:
        if not (written := skill_text(ecosystem, skill, profile, files, site_url, errors)):
            continue
        name, description, text = written
        contents = {"SKILL.md": text.encode("utf-8")}
        contents |= {path: staged.read_bytes() for path, (_, staged) in files.items()}
        data = archive(contents)
        path = scope / WELL_KNOWN / f"{name}.tar.gz"
        (PUBLIC / path).parent.mkdir(parents=True, exist_ok=True)
        (PUBLIC / path).write_bytes(data)
        published.append(Published(name, description, path, f"sha256:{hashlib.sha256(data).hexdigest()}"))
    return published


def write_index(scope: PurePosixPath, skills: list[Published]) -> None:
    """Write the index at an address. Each archive's address starts at the site's root, so
    the index also works on a preview, which has another host."""
    entries = [
        {
            "name": skill.name,
            "type": "archive",
            "description": skill.description,
            "url": f"/{skill.path}",
            "digest": skill.digest,
        }
        for skill in skills
    ]
    path = PUBLIC / scope / WELL_KNOWN / "index.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"$schema": SCHEMA, "skills": entries}, indent=2) + "\n", encoding="utf-8")
    print(f"/{path.relative_to(PUBLIC)}: {', '.join(skill.name for skill in skills)}")


def main() -> int:
    require_root()
    if not PUBLIC.is_dir() or not DOCS.is_dir():
        print(f"No {PUBLIC}/ or no {DOCS}/. Run `just build` first.", file=sys.stderr)
        return 2
    with SITE_CONFIG.open("rb") as file:
        site_url = tomllib.load(file)["project"]["site_url"]

    errors: list[str] = []
    ecosystems = [ecosystem for ecosystem in built() if ecosystem.skills]
    # Each ecosystem's skills by profile. An ecosystem staged an llms-<profile>.txt for each
    # profile it holds opinions for, and stage.py checked each against houses.toml.
    default: dict[str, list[Published]] = {}
    house: dict[str, dict[str, list[Published]]] = {}
    for ecosystem in ecosystems:
        default[ecosystem.id] = publish(ecosystem, NO_PROFILE, site_url, errors)
        for llms in sorted((DOCS / ecosystem.id).glob("llms-*.txt")):
            profile = llms.stem.removeprefix("llms-")
            house.setdefault(profile, {})[ecosystem.id] = publish(ecosystem, profile, site_url, errors)
    if errors:
        return report(errors)

    for id, skills in default.items():
        write_index(PurePosixPath(id), skills)
    for profile, found in house.items():
        for id, skills in found.items():
            write_index(PurePosixPath(id, HOUSE, profile), skills)
        # A project with several ecosystems installs from one address. An ecosystem with
        # no opinions for the profile gives its default copy, which is all the profile has there.
        write_index(PurePosixPath(HOUSE, profile), [skill for id in default for skill in found.get(id, default[id])])
    if default:
        write_index(PurePosixPath(), [skill for skills in default.values() for skill in skills])
    return 0


if __name__ == "__main__":
    sys.exit(main())
