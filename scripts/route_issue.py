# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Route an intake issue from the Suggest a source or Opt out form.

    uv run scripts/route_issue.py suggest <number> [--dry-run]
    uv run scripts/route_issue.py opt-out <number> [--dry-run]

intake.yml runs it with GH_TOKEN set to the app's token. It reads the issue with gh,
and each live ecosystem's roster from its published sources.json.

suggest checks a new or edited suggestion. A field that isn't a URL gets one comment,
which the script updates on each edit. A source already on the chosen ecosystem's
roster gets its standing, and the issue closes. Otherwise the issue moves to the
ecosystem's repository, labelled vet-source. An ecosystem that isn't live yet keeps the
suggestion here, with a comment.

opt-out runs when the owner labels an opt-out verified. It opens an issue in each live
ecosystem whose roster lists one of the sources, unless one is already open there, and
comments on the opt-out with what it opened and what it couldn't match.

--dry-run prints what it would do instead of doing it. The issue text is untrusted, so
it only ever reaches gh as an argument or a file, never through a shell.

Exit codes: 0 routed, or nothing to do, 1 the issue names an ecosystem that
ecosystems.toml doesn't have, or gh or a roster failed, 2 not run from the repository
root or bad arguments.
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from urllib.parse import urlsplit

from ecosystems import Ecosystem, live, registry, require_root

REPOSITORY = "awesome-humans/website"
SITE = "https://awesome-humans.net"

# Marks the one comment suggest keeps up to date, so an edit doesn't add another.
MARKER = "<!-- route-issue -->"

# An issue form renders each field as a level-3 heading, then its value. An empty
# optional field reads "_No response_".
FIELD = re.compile(r"^### (.+?)\n+(.*?)(?=^### |\Z)", re.MULTILINE | re.DOTALL)
NO_RESPONSE = "_No response_"
URL = re.compile(r"^https?://[^\s/]+\.[^\s]+$")


class RouteError(Exception):
    pass


def fields(body: str) -> dict[str, str]:
    """The form's fields, by label, with empty ones as empty strings."""
    found = {label.strip(): value.strip() for label, value in FIELD.findall(body)}
    return {label: "" if value == NO_RESPONSE else value for label, value in found.items()}


def gh(*args: str, dry_run: bool = False, writes: bool = False) -> str:
    """Run gh, and return its output. With --dry-run, print a write instead of running it."""
    if dry_run and writes:
        print("would run: gh " + " ".join(args))
        return ""
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RouteError(f"gh {args[0]} {args[1]} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def roster(ecosystem: Ecosystem) -> list[dict]:
    """An ecosystem's sources, from the sources.json the site publishes."""
    url = f"{SITE}/{ecosystem.id}/sources.json"
    # The site's host refuses urllib's default user agent.
    request = urllib.request.Request(url, headers={"User-Agent": "awesome-humans-intake"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)["sources"]
    except (OSError, ValueError, KeyError) as error:
        raise RouteError(f"{url}: {error}") from error


def normalise(url: str) -> str:
    """A URL reduced to its host and path, so http, www, and a trailing slash don't matter."""
    parts = urlsplit(url.strip().lower())
    host = parts.netloc.removeprefix("www.")
    return host + parts.path.rstrip("/")


def comment(number: int | str, body: str, *, repository: str = REPOSITORY, dry_run: bool) -> None:
    gh("issue", "comment", str(number), "-R", repository, "--body", body, dry_run=dry_run, writes=True)


def upsert_comment(number: int, body: str, *, dry_run: bool) -> None:
    """Write the marked comment, replacing the previous one, so an edit doesn't add another."""
    body = f"{MARKER}\n{body}"
    comments = json.loads(gh("api", f"repos/{REPOSITORY}/issues/{number}/comments", "--paginate", "--slurp"))
    existing = [c for page in comments for c in page if c["body"].startswith(MARKER)]
    if existing:
        endpoint = f"repos/{REPOSITORY}/issues/comments/{existing[-1]['id']}"
        gh("api", "-X", "PATCH", endpoint, "-f", f"body={body}", dry_run=dry_run, writes=True)
    else:
        comment(number, body, dry_run=dry_run)


def suggest(number: int, issue: dict, dry_run: bool) -> int:
    form = fields(issue["body"])
    name = form.get("Ecosystem", "")
    ecosystem = next((e for e in registry() if e.name == name), None)
    if ecosystem is None:
        raise RouteError(f"#{number} names the ecosystem {name!r}, which ecosystems.toml doesn't have")

    problems = []
    main_url = form.get("Main URL", "")
    if not URL.match(main_url):
        problems.append(f"**Main URL** isn't a URL: `{main_url}`")
    samples = [line.strip() for line in form.get("Three sample posts", "").splitlines() if line.strip()]
    not_urls = [line for line in samples if not URL.match(line)]
    if not_urls:
        problems.append("**Three sample posts** has lines that aren't URLs: " + ", ".join(f"`{s}`" for s in not_urls))
    elif len(samples) < 3:
        problems.append(f"**Three sample posts** has {len(samples)}, and needs three, one URL per line.")
    if problems:
        lines = "\n".join(f"- {problem}" for problem in problems)
        upsert_comment(
            number, f"This suggestion can't be routed yet:\n\n{lines}\n\nEdit the issue to fix it.", dry_run=dry_run
        )
        return 0

    if ecosystem.status != "live":
        upsert_comment(
            number,
            f"Thanks. {ecosystem.name} isn't live yet, so this suggestion stays here until its roster opens.",
            dry_run=dry_run,
        )
        return 0

    target = normalise(main_url)
    suggested_name = form.get("Name", "").casefold()
    for source in roster(ecosystem):
        if normalise(source["url"]) == target or source["name"].casefold() == suggested_name:
            standing = source["standing"].replace("-", " ")
            upsert_comment(
                number,
                f"`{source['id']}` is already on the {ecosystem.name} roster, on the {standing}. "
                f"See [{source['name']}]({SITE}/{ecosystem.id}/awesome-humans/). "
                "If you think its standing should change, say so here, and the owner can reopen this issue.",
                dry_run=dry_run,
            )
            gh("issue", "close", str(number), "-R", REPOSITORY, "--reason", "not planned", dry_run=dry_run, writes=True)
            gh("issue", "edit", str(number), "-R", REPOSITORY, "--add-label", "duplicate", dry_run=dry_run, writes=True)
            return 0

    moved = gh("issue", "transfer", str(number), ecosystem.repository, dry_run=dry_run, writes=True)
    if not dry_run:
        gh("issue", "edit", moved, "--add-label", "vet-source", dry_run=dry_run, writes=True)
        print(f"Moved #{number} to {moved}")
    return 0


def opt_out(number: int, issue: dict, dry_run: bool) -> int:
    form = fields(issue["body"])
    wanted = [line.strip(" -*`\t") for line in form.get("Sources", "").splitlines()]
    wanted = [entry for entry in wanted if entry]
    url = f"https://github.com/{REPOSITORY}/issues/{number}"

    matched: set[str] = set()
    opened = []
    for ecosystem in live():
        ids = []
        for source in roster(ecosystem):
            keys = {source["id"], source["name"].casefold()}
            hits = [entry for entry in wanted if entry.casefold() in keys]
            if hits and source["standing"] != "opted-out":
                ids.append(source["id"])
                matched.update(hits)
        if not ids:
            continue

        search = ("--state", "open", "--search", f'"{url}" in:body', "--json", "url", "--jq", ".[0].url // empty")
        existing = gh("issue", "list", "-R", ecosystem.repository, *search)
        if existing:
            opened.append(f"- {ecosystem.name}: already open, {existing}")
            continue
        listed = ", ".join(f"`{id}`" for id in ids)
        body = (
            f"{url} asks to stop citing {listed}, and the owner verified it.\n\n"
            "Within 30 days of the verification, in one pull request:\n\n"
            "- Move each source to the roster's `## Opted out` section, and log the date and this issue in the decision log.\n"
            "- Re-source each opinion or template that cites it with `research-topic`, "
            "or cut it back to what other citable sources support.\n"
        )
        # The body holds only roster ids and the issue's URL, never the requester's text.
        title = f"Opt out: {', '.join(ids)}"
        args = ("issue", "create", "-R", ecosystem.repository, "--title", title, "--body", body, "--label", "opt-out")
        created = gh(*args, dry_run=dry_run, writes=True)
        opened.append(f"- {ecosystem.name}: {created or '(dry run)'}")

    unmatched = [entry for entry in wanted if entry not in matched]
    lines = opened or ["- No live ecosystem's roster lists these sources."]
    if unmatched:
        lines.append("\nNot on any live roster, so the owner needs to check: " + ", ".join(f"`{e}`" for e in unmatched))
    comment(number, "Opened the opt-out in each ecosystem:\n\n" + "\n".join(lines), dry_run=dry_run)
    return 0


def main() -> int:
    require_root()
    parser = argparse.ArgumentParser(description="Route an intake issue from the Suggest a source or Opt out form.")
    parser.add_argument("form", choices=["suggest", "opt-out"])
    parser.add_argument("number", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        issue = json.loads(gh("issue", "view", str(args.number), "-R", REPOSITORY, "--json", "body,state"))
        if issue["state"] != "OPEN":
            print(f"#{args.number} is closed, so there's nothing to route")
            return 0
        route = suggest if args.form == "suggest" else opt_out
        return route(args.number, issue, args.dry_run)
    except RouteError as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
