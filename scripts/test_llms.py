# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run an agent from the home page's review-project prompt, and report what it read.

    uv run scripts/test_llms.py [--local] [--budget <usd>] [<id>]...

For each live ecosystem, or each one named, it starts an agent in an empty directory with
the review-project prompt from pages/index.md, aimed at the ecosystem's own checkout in
build/repos/<id>/. Run `just fetch` first. Then it reads the agent's transcript and reports:

- Whether the agent got the root llms.txt and the ecosystem's in full, or as a summary.
- Which opinions and templates it fetched from the site, and whether each came in full.
  A file counts as in full when 95% of its longer lines appear in what the agent's tools
  returned.
- Which of them it read from the checkout instead, which holds house opinions.
- The turns, the largest context, the tokens across every turn, and the cost.

The checkout holds the opinions and templates the site links, so an agent that reads the
project's copy shows up here, and one that follows the reading rules doesn't.

--local tests a change before it deploys. It serves build/public/, which `just build`
writes, on a local port, with the site's address in each llms.txt changed to that port.

The agent is Claude Code in print mode, with read-only tools: no other harness writes a
transcript this script reads. An agent run costs about a dollar and its reading varies from
run to run, so this isn't in `just check` or CI. Run it after a change to the reading rules
in stage.py, to the prompts in pages/index.md, or to a review-project skill. Each
transcript and answer stays in build/llms-test/.

Exit codes: 0 every agent read each llms.txt and at least one opinion in full, from the
site, 1 one didn't, or the agent failed, 2 not run from the repository root, bad arguments,
or nothing to test against.
"""

import argparse
import functools
import http.server
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import tomllib
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ecosystems import BUILD, REPOS, Ecosystem, built, require_root

PAGES = Path("pages")
PUBLIC = BUILD / "public"
RESULTS = BUILD / "llms-test"
SITE_CONFIG = Path("zensical.toml")

# The prompt this tests is the home page's own, so the test follows a change to it.
PROMPT = re.compile(r"^\s*(?P<prompt>Fetch \S+/llms\.txt .* review-project skill on <repository>)$", re.MULTILINE)
# A link in an llms.txt, and the heading of the section it's under.
LINK = re.compile(r"^- \[(?P<title>.+?)\]\((?P<url>[^)\s]+)\)")
SECTION = re.compile(r"^## (?P<title>.+)$")
# The sections an ecosystem's llms.txt lists its opinions and templates under.
KINDS = ("opinions", "templates")
# A copy's path under raw/<profile>/, which is the file's path in the ecosystem's repository.
RAW = re.compile(r"/raw/[^/]+/(?P<path>.+)$")

# A file is read in full when this share of its longer lines is in a tool's result. A
# summary scores near zero, and a full copy scores 1, so the exact share matters little.
FULL = 0.95
LONG_LINE = 25

# Tools that read and never write, so an agent can't change the checkout it reviews.
TOOLS = [
    "Read",
    "Grep",
    "Glob",
    "WebFetch",
    *(
        f"Bash({command}:*)"
        for command in ("cat", "cd", "curl", "diff", "echo", "find", "grep", "head", "ls", "mkdir", "sort")
    ),
    *(f"Bash({command}:*)" for command in ("tail", "wc", "git log", "git rev-parse", "git status", "git ls-files")),
]
# Tool calls that fetch from the site, as opposed to reading the checkout.
FETCHES = re.compile(r"\b(curl|wget)\b")


@dataclass
class Linked:
    """A file an llms.txt links, as the site serves it."""

    title: str
    url: str
    kind: str
    lines: list[str]


@dataclass
class Transcript:
    """What one agent run fetched and read, and what it cost."""

    fetched: str = ""
    returned: str = ""
    local_reads: set[str] = field(default_factory=set[str])
    answer: str = ""
    failed: str = ""
    turns: int = 0
    peak: int = 0
    tokens: int = 0
    cost: float = 0.0


class Rewriting(http.server.SimpleHTTPRequestHandler):
    """Serve the built site, with the deployed site's address in each llms.txt changed to
    this server's, so an agent that follows the links stays on the local build."""

    site_url = ""
    origin = ""

    def do_GET(self) -> None:
        path = Path(self.translate_path(self.path))
        if not (path.is_file() and path.name.startswith("llms") and path.suffix == ".txt"):
            super().do_GET()
            return
        body = path.read_text(encoding="utf-8").replace(self.site_url, self.origin).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        pass


def serve(site_url: str) -> str:
    """Serve build/public/ on a free local port, and return its address."""
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Rewriting, directory=str(PUBLIC)))
    origin = f"http://127.0.0.1:{server.server_address[1]}/"
    Rewriting.site_url, Rewriting.origin = site_url, origin
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return origin


def get(url: str) -> str | None:
    request = urllib.request.Request(url, headers={"User-Agent": "awesome-humans-test-llms"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError, TimeoutError:
        return None


def long_lines(text: str) -> list[str]:
    return [stripped for line in text.splitlines() if len(stripped := line.strip()) > LONG_LINE]


def linked(url: str, title: str, kind: str, errors: list[str]) -> Linked | None:
    text = get(url)
    if text is None:
        errors.append(f"{url}: couldn't fetch it")
        return None
    return Linked(title, url, kind, long_lines(text))


def links(llms: str, errors: list[str]) -> list[Linked]:
    """The opinions and templates an ecosystem's llms.txt links, each fetched."""
    found: list[Linked] = []
    kind = ""
    for line in (get(llms) or "").splitlines():
        if section := SECTION.match(line):
            kind = next((kind for kind in KINDS if section["title"].endswith(f" {kind}")), "")
        elif kind and (link := LINK.match(line)) and (file := linked(link["url"], link["title"], kind, errors)):
            found.append(file)
    return found


def result_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        blocks: list[Any] = content
        return "\n".join(block.get("text", "") for block in blocks if isinstance(block, dict))
    return ""


def read_transcript(path: Path, target: Path) -> Transcript:
    """Sort an agent's stream-json transcript into what it asked the site for, what its
    tools returned, and which of the target's files it read."""
    transcript = Transcript()
    # A Read of the target's own file, by tool call, so its result doesn't count as the site's.
    local: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = event.get("message", {})
        if event.get("type") == "assistant":
            if not event.get("parent_tool_use_id"):
                usage = message.get("usage", {})
                context = sum(
                    usage.get(key, 0)
                    for key in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
                )
                transcript.peak = max(transcript.peak, context)
            for block in message.get("content", []):
                if block.get("type") != "tool_use":
                    continue
                call = block.get("input", {})
                read = Path(call.get("file_path", ""))
                if block.get("name") == "Read" and read.is_relative_to(target):
                    local.add(block["id"])
                    transcript.local_reads.add(read.relative_to(target).as_posix())
                elif block.get("name") == "WebFetch" or FETCHES.search(call.get("command", "")):
                    transcript.fetched += json.dumps(call) + "\n"
        elif event.get("type") == "user" and isinstance(message.get("content"), list):
            for block in message["content"]:
                if block.get("type") == "tool_result" and block.get("tool_use_id") not in local:
                    transcript.returned += result_text(block.get("content")) + "\n"
        elif event.get("type") == "result":
            transcript.answer = event.get("result") or ""
            transcript.turns = event.get("num_turns", 0)
            transcript.cost = event.get("total_cost_usd", 0.0)
            if event.get("is_error") or event.get("subtype") != "success":
                transcript.failed = event.get("subtype", "error")
            for usage in event.get("modelUsage", {}).values():
                transcript.tokens += sum(
                    usage.get(key, 0)
                    for key in ("inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens")
                )
    if not transcript.turns and not transcript.failed:
        transcript.failed = "no result"
    return transcript


def in_full(file: Linked, transcript: Transcript) -> bool:
    if not file.lines:
        return file.url in transcript.fetched
    return sum(line in transcript.returned for line in file.lines) / len(file.lines) >= FULL


def asked_for(file: Linked, transcript: Transcript) -> bool:
    """Whether a fetch named the file: by its address, or by its path under raw/<profile>/,
    which is what's left when the agent keeps the rest in a shell variable."""
    raw = RAW.search(file.url)
    return file.url in transcript.fetched or (raw is not None and raw["path"] in transcript.fetched)


def repository_path(file: Linked) -> str:
    raw = RAW.search(file.url)
    return raw["path"].removesuffix(".txt") if raw and raw["path"].endswith(".md.txt") else raw["path"] if raw else ""


def run(ecosystem: Ecosystem, prompt: str, budget: str) -> Path:
    """Run the agent from an empty directory, so the checkout is only its target, and
    return its transcript."""
    target = (REPOS / ecosystem.id).resolve()
    RESULTS.mkdir(parents=True, exist_ok=True)
    transcript = RESULTS / f"{ecosystem.id}.jsonl"
    command = [
        "claude",
        "--print",
        prompt.replace("<repository>", str(target)),
        "--output-format",
        "stream-json",
        "--verbose",
        # No user settings, plugins, or MCP servers, which would change what's measured.
        "--setting-sources",
        "project",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--max-budget-usd",
        budget,
        "--add-dir",
        str(target),
        "--allowedTools",
        *TOOLS,
    ]
    print(f"{ecosystem.id}: running the agent on {target}/", flush=True)
    with tempfile.TemporaryDirectory() as empty, transcript.open("w", encoding="utf-8") as output:
        subprocess.run(command, cwd=empty, stdin=subprocess.DEVNULL, stdout=output, check=False)
    return transcript


def report(ecosystem: Ecosystem, origin: str, transcript: Transcript, errors: list[str]) -> None:
    """Print what the agent read, and record each way it read less than the site serves."""
    id = ecosystem.id
    print(
        f"{id}: {transcript.turns} turns, largest context {transcript.peak:,} tokens,"
        f" {transcript.tokens:,} tokens in all, ${transcript.cost:.2f}"
    )
    if transcript.failed:
        errors.append(f"{id}: the agent stopped with {transcript.failed}. See {RESULTS / f'{id}.jsonl'}")
        return

    for url in (f"{origin}llms.txt", f"{origin}{id}/llms.txt"):
        if index := linked(url, url, "", errors):
            full = in_full(index, transcript)
            print(f"  {url}: {'in full' if full else 'as a summary, or not at all'}")
            if not full:
                errors.append(f"{id}: the agent didn't get {url} in full")

    files = links(f"{origin}{id}/llms.txt", errors)
    for kind in KINDS:
        of_kind = [file for file in files if file.kind == kind]
        full = [file for file in of_kind if in_full(file, transcript)]
        summarised = [file for file in of_kind if file not in full and asked_for(file, transcript)]
        local = [file for file in of_kind if repository_path(file) in transcript.local_reads]
        unread = [file for file in of_kind if file not in full and file not in summarised and file not in local]
        print(f"  {kind}: {len(full)} of {len(of_kind)} read in full from the site")
        for label, group in (("As a summary", summarised), ("From the checkout", local), ("Not read", unread)):
            if group:
                print(f"    {label}: {', '.join(file.title for file in group)}")
        if summarised:
            errors.append(f"{id}: the agent got {len(summarised)} of the {kind} as a summary")
        if local:
            errors.append(f"{id}: the agent read {len(local)} of the {kind} from the checkout, not the site")
        if kind == "opinions" and of_kind and not full:
            errors.append(f"{id}: the agent read no opinion in full from the site")

    answer = RESULTS / f"{id}.md"
    answer.write_text(transcript.answer, encoding="utf-8")
    print(f"  Its answer is in {answer}")


def main() -> int:
    require_root()
    parser = argparse.ArgumentParser(description="Run an agent from the review-project prompt, and report its reading.")
    parser.add_argument("--local", action="store_true", help="test build/public/ instead of the deployed site")
    parser.add_argument("--budget", default="5", metavar="USD", help="the most one agent run can cost")
    parser.add_argument("ids", nargs="*", metavar="ID", help="an ecosystem to test. The default is every live one")
    args = parser.parse_args()

    ecosystems = built()
    if unknown := set(args.ids) - {ecosystem.id for ecosystem in ecosystems}:
        print(f"{', '.join(sorted(unknown))}: not live in ecosystems.toml", file=sys.stderr)
        return 2
    ecosystems = [ecosystem for ecosystem in ecosystems if not args.ids or ecosystem.id in args.ids]
    if missing := [ecosystem.id for ecosystem in ecosystems if not (REPOS / ecosystem.id).is_dir()]:
        print(f"No checkout of {', '.join(missing)} in {REPOS}/. Run `just fetch` first", file=sys.stderr)
        return 2
    if shutil.which("claude") is None:
        print("The agent is Claude Code, and `claude` isn't on the path", file=sys.stderr)
        return 2

    with SITE_CONFIG.open("rb") as file:
        site_url: str = tomllib.load(file)["project"]["site_url"]
    host = site_url.removeprefix("https://").rstrip("/")
    prompt = PROMPT.search((PAGES / "index.md").read_text(encoding="utf-8"))
    if prompt is None or f"{host}/llms.txt" not in prompt["prompt"]:
        print(f"{PAGES / 'index.md'}: no review-project prompt that fetches {host}/llms.txt", file=sys.stderr)
        return 2

    origin, address = site_url, host
    if args.local:
        if not (PUBLIC / "llms.txt").is_file():
            print(f"No {PUBLIC / 'llms.txt'}. Run `just build` first", file=sys.stderr)
            return 2
        origin = serve(site_url)
        address = origin.rstrip("/")
    if get(f"{origin}llms.txt") is None:
        print(f"Couldn't fetch {origin}llms.txt", file=sys.stderr)
        return 2

    errors: list[str] = []
    for ecosystem in ecosystems:
        transcript = run(ecosystem, prompt["prompt"].replace(host, address), args.budget)
        report(ecosystem, origin, read_transcript(transcript, (REPOS / ecosystem.id).resolve()), errors)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
