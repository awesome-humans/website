# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Publish each ecosystem's consumer skills in build/public/, for `npx skills add`.

    uv run scripts/publish_skills.py

A consumer skill is one a project runs on its own code, such as review-project. Each
ecosystem names its own in the `skills` key of ecosystems.toml. For each one, this writes
an archive of the skill. The archive of the first skill an ecosystem lists also holds every
opinion and template the ecosystem's llms.txt links, and its roster, so an agent reads them from disk and
fetches nothing. Each other skill reads that copy, from the directory beside its own, so a
project holds each opinion once. It publishes the skill as
<verb>-<id>-<rest>, such as review-dotnet-project, because two ecosystems' skills are
installed side by side, and one named review-project would overwrite the other.

It writes a discovery index, which the skills CLI reads from
<address>/.well-known/agent-skills/index.json, at four kinds of address:

- /                        Every ecosystem's skills, with no house opinions.
- /<id>/                   One ecosystem's.
- /<profile>/              Every ecosystem's, with that profile's house opinions where an
                           ecosystem holds any, and the default copy where it doesn't.
- /<id>/<profile>/         One ecosystem's, for a profile it holds opinions for.

A profile's address is its id alone, as raw/<profile>/ is. So this fails when a profile's
id is also a page or a directory at either place, and ecosystems.py rejects a profile
named after an ecosystem.

Run it after `zensical build`, which drops every path that starts with a dot, and from
what `just stage` left in build/docs/. An archive's bytes depend only on the files in it,
so its digest changes only when a skill, an opinion, or a template does, and `skills
check` in a project reports an update only then.

build.yml uploads build/public/ with its hidden files, so that the indexes deploy. So this
also fails on any path there that starts with a dot and isn't one it wrote: nothing else
hidden reaches the site.

Exit codes: 0 done, 1 a skill, an llms.txt, or a file one links is missing or malformed, or
build/public/ holds a hidden path this didn't write, 2 not run from the repository root, or
nothing is staged or built.
"""

import gzip
import hashlib
import io
import json
import re
import shutil
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

# A link in an llms.txt, and the heading of the section it's under, as in test_llms.py.
LINK = re.compile(r"^- \[(?P<title>.+?)\]\((?P<url>[^)\s]+)\)")
SECTION = re.compile(r"^## (?P<title>.+)$")
# The sections an ecosystem's llms.txt lists its opinions and templates under.
KINDS = ("opinions", "templates")
# The section an ecosystem's llms.txt lists its roster and its house opinions record under.
# research-topic scans the roster, so each goes beside the opinions, in references/.
OPTIONAL = "Optional"
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

{where}

- **Read them from {directory},** with a file-reading tool. Where another paragraph says to read an opinion or a template from the site or the repository, read this copy's. Don't use a copy the target holds.
- **Read every opinion that covers something the project uses,** and every template the project has a file for, not only the ones the task names.
- **Read each one from its first line to its last.** A search for its headings, or a read of one section, isn't reading it: a rule's exception is often in another section.
- **Say which opinions and templates you read in full,** and which you skipped.
- **Check that the copy is current** with `npx skills check`, and update it with `npx skills update`. Each opinion gives its `last-reviewed` date.
- {other}
"""
# Where the files are, for the skill that carries them, and for one that reads another's.
CARRIES = (
    "This copy of the skill carries every {name} opinion and template, as [{repository}](https://github.com/{repository})"
    " published them, {profile}. The opinions are in [references/opinions/](references/opinions/), and the templates in"
    " [references/templates/](references/templates/), beside this file, with the roster of vetted sources in"
    " [references/AWESOME-HUMANS.md](references/AWESOME-HUMANS.md). In this skill, `opinions/`, `templates/`, and"
    ' `AWESOME-HUMANS.md` mean those, and "this repository" means {repository}.'
)
SHARES = (
    "This skill reads the {name} opinions and templates that the `{holder}` skill carries, as"
    " [{repository}](https://github.com/{repository}) published them, {profile}. That skill installs beside this one, so"
    " the opinions are in [../{holder}/references/opinions/](../{holder}/references/opinions/), and the templates in"
    " [../{holder}/references/templates/](../{holder}/references/templates/), relative to this file's directory, with"
    " the roster of vetted sources in [../{holder}/references/AWESOME-HUMANS.md](../{holder}/references/AWESOME-HUMANS.md)."
    ' In this skill, `opinions/`, `templates/`, and `AWESOME-HUMANS.md` mean those, and "this repository" means'
    " {repository}."
    "\n\n**If `../{holder}/` is missing, stop.** Tell the user to run `npx skills add {address} --skill {holder}`, and"
    " never work from what you remember of an opinion."
)


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
            title = section["title"]
            kind = OPTIONAL if title == OPTIONAL else next((kind for kind in KINDS if title.endswith(f" {kind}")), "")
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
        name = link["title"] if kind == "templates" else staged.name.removesuffix(".txt")
        path = PurePosixPath("references", name) if kind == OPTIONAL else PurePosixPath("references", kind, name)
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
    ecosystem: Ecosystem,
    skill: str,
    profile: str,
    files: dict[str, tuple[str, Path]],
    site_url: str,
    errors: list[str],
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
    # An ecosystem's first skill carries the files, and each other skill reads that one's copy,
    # so a project holds every opinion once however many skills it installs.
    holder = consumer_name(ecosystem.skills[0], ecosystem.id)
    prefix = "" if name == holder else f"../{holder}/"
    local = {raw["path"]: f"{prefix}{path}" for path, (url, _) in files.items() if (raw := RAW.search(url))}

    def carried(link: re.Match[str]) -> str:
        target = link["target"]
        raw = RAW.search(target) if target.startswith(f"{site_url}{ecosystem.id}/") else None
        return f"]({local[raw['path']] if raw and raw['path'] in local else target})"

    body = MARKDOWN_LINK.sub(carried, body)

    if profile == NO_PROFILE:
        carries = "with no house opinions"
        other = (
            "**This copy has no house opinions, so it can't follow a house profile.** If the user or the project names"
            " one, say so before you do anything else, and give the command that installs that profile's copy:"
            f" `npx skills add {site_url}{ecosystem.id}/<profile>`. If the site has no skills at that address, the"
            f" profile holds no {ecosystem.name} opinions, and this copy is the right one. Then carry on with the"
            " sourced text alone, unless the user stops you."
        )
    else:
        carries = f"with the `{profile}` house profile's opinions"
        other = (
            f"**This copy holds the `{profile}` profile's house blocks and regions, and no other profile's.** If the"
            " user names no profile, skip every house block, and compare each template with its house regions removed."
        )
    scope = ecosystem.id if profile == NO_PROFILE else f"{ecosystem.id}/{profile}"
    where = (CARRIES if name == holder else SHARES).format(
        name=ecosystem.name,
        repository=ecosystem.repository,
        profile=carries,
        holder=holder,
        address=f"{site_url}{scope}",
    )
    directory = "this skill's directory" if name == holder else f"the `{holder}` skill's directory"
    section = BUNDLE.format(where=where, repository=ecosystem.repository, directory=directory, other=other)
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
    scope = PurePosixPath(ecosystem.id) if profile == NO_PROFILE else PurePosixPath(ecosystem.id, profile)
    published: list[Published] = []
    for skill in ecosystem.skills:
        if not (written := skill_text(ecosystem, skill, profile, files, site_url, errors)):
            continue
        name, description, text = written
        contents = {"SKILL.md": text.encode("utf-8")}
        if skill == ecosystem.skills[0]:
            contents |= {path: staged.read_bytes() for path, (_, staged) in files.items()}
        data = archive(contents)
        path = scope / WELL_KNOWN / f"{name}.tar.gz"
        (PUBLIC / path).parent.mkdir(parents=True, exist_ok=True)
        (PUBLIC / path).write_bytes(data)
        published.append(Published(name, description, path, f"sha256:{hashlib.sha256(data).hexdigest()}"))
    return published


def write_index(scope: PurePosixPath, skills: list[Published]) -> Path:
    """Write the index at an address, and return its file. Each archive's address starts at
    the site's root, so the index also works on a preview, which has another host."""
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
    return path


def unexpected(written: set[Path]) -> list[str]:
    """Every hidden path in build/public/ that this run didn't write. The site artifact
    includes hidden files for the indexes' sake, so anything else hidden would deploy too."""
    found: list[str] = []
    for path in sorted(PUBLIC.rglob("*")):
        relative = path.relative_to(PUBLIC)
        if not any(part.startswith(".") for part in relative.parts):
            continue
        inside = path.is_dir() and any(file.is_relative_to(path) for file in written)
        if path not in written and not inside:
            found.append(f"{path}: a hidden path that isn't part of a skills index, which the site would deploy")
    return found


def main() -> int:
    require_root()
    if not PUBLIC.is_dir() or not DOCS.is_dir():
        print(f"No {PUBLIC}/ or no {DOCS}/. Run `just build` first.", file=sys.stderr)
        return 2
    with SITE_CONFIG.open("rb") as file:
        site_url = tomllib.load(file)["project"]["site_url"]

    # An index from an earlier run, for a skill or a profile that has since gone.
    # Its .well-known/ goes too once it's empty, or the check below would call it a leak.
    for stale in sorted(PUBLIC.rglob(WELL_KNOWN)):
        shutil.rmtree(stale)
        if not any(stale.parent.iterdir()):
            stale.parent.rmdir()

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
    # A profile's address is its id, under the root and under each ecosystem. A page or a
    # directory of the same name there would share the address with the profile's skills.
    for profile, found in house.items():
        for scope in (PurePosixPath(profile), *(PurePosixPath(id, profile) for id in found)):
            taken = PUBLIC / scope
            if taken.is_file() or (taken.is_dir() and any(not path.name.startswith(".") for path in taken.iterdir())):
                errors.append(f"{taken}: a page has the address of the house profile {profile}'s skills")
    if errors:
        return report(errors)

    written = {
        PUBLIC / skill.path for found in (default, *house.values()) for skills in found.values() for skill in skills
    }
    for id, skills in default.items():
        written.add(write_index(PurePosixPath(id), skills))
    for profile, found in house.items():
        for id, skills in found.items():
            written.add(write_index(PurePosixPath(id, profile), skills))
        # A project with several ecosystems installs from one address. An ecosystem with
        # no opinions for the profile gives its default copy, which is all the profile has there.
        every = [skill for id in default for skill in found.get(id, default[id])]
        written.add(write_index(PurePosixPath(profile), every))
    if default:
        written.add(write_index(PurePosixPath(), [skill for skills in default.values() for skill in skills]))
    return report(unexpected(written))


if __name__ == "__main__":
    sys.exit(main())
