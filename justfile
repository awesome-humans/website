# Every local and CI entry point (agents/checks.md: Scripts). CI calls these recipes, never npm or
# uv directly, so a step runs the same way on every machine. Run `just` to list them.

set shell := ["bash", "-euo", "pipefail", "-c"]

# Recipes read their arguments as "$1" and "$@", never as {{ }}, which would paste a
# caller's input into the script as code.
set positional-arguments

# List the recipes
default:
    @just --list

# Install the Node and Python tools at the versions package-lock.json and uv.lock pin
install: install-node install-python

# Install the Node tools at the versions package-lock.json pins
install-node:
    npm ci

# Install the site's Python environment and its Python tools at the versions uv.lock pins
install-python:
    uv sync --locked

# Format every file
format:
    npm run format

# Run every check CI runs on a pull request, except the link check and the site build
check: format-check lint typecheck spell

# Check that the formatters leave every file unchanged
format-check:
    npm run format:check

# Lint Markdown, CSS, JavaScript, Python, and the workflows
lint:
    npm run lint

# Check the Python types with pyright
typecheck:
    npm run typecheck

# Check spelling with cspell
spell:
    npm run spell

# Clone each live ecosystem into build/repos/, at main, or <ecosystem> at <ref>
fetch ecosystem="" ref="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -n "$1" ] && [ -n "$2" ]; then
        uv run scripts/stage.py fetch --ref "$1=$2"
    elif [ -n "$1$2" ]; then
        echo "Pass both an ecosystem and a ref, or neither." >&2
        exit 2
    else
        uv run scripts/stage.py fetch
    fi

# Stage the shared pages and every ecosystem into build/docs/, each <id>=<path> from that checkout
stage *locals:
    #!/usr/bin/env bash
    set -euo pipefail
    args=()
    for local in "$@"; do
        args+=(--local "$local")
    done
    uv run scripts/stage.py stage "${args[@]}"

# Check each staged nav.json, and write build/zensical.toml
nav:
    uv run scripts/merge_nav.py

# Check each staged sources.json, and write build/sources.json
sources:
    uv run scripts/collate_sources.py

# Build build/public/ from what's staged, failing on any broken link or anchor
build-site:
    uv run zensical build --strict -f build/zensical.toml

# Write each ecosystem's consumer skills, and their indexes for `npx skills add`, into build/public/
skills:
    uv run scripts/publish_skills.py

# Check that the pinned skills CLI lists every skill at each index in build/public/. Run build first
test-skills:
    uv run scripts/test_skills.py

# Check that the skills the ecosystems copy differ only where skills-drift/ records. --local <id>=<path>
# reads that checkout, and --update records the differences as they are. Run fetch first
skills-drift *args:
    uv run scripts/skills_drift.py "$@"

# Stage, merge, and build the site, each <id>=<path> from that checkout. Run fetch first
build *locals:
    just stage "$@"
    just nav
    just sources
    just build-site
    just skills

# Stage, merge, and serve the site locally, each <id>=<path> from that checkout. Run fetch first
serve *locals:
    just stage "$@"
    just nav
    just sources
    uv run zensical serve -f build/zensical.toml

# `just --list` shows only the last comment line, so the flags come first:
#   --local       tests build/public/ instead of the deployed site.
#   --as-written  runs the home page's review-project prompt on the ecosystem's checkout. Run fetch first.
#   --installed   adds the ecosystem's skills to a scratch project, as `npx skills add` does, and
#                 reviews the ecosystem's templates with the review skill it added. Run fetch first.
# Ask an agent to read each ecosystem's opinions and templates, and fail unless it read each in full
test-llms *args:
    uv run scripts/test_llms.py "$@"

# Delete Zensical's page cache, which keeps stale pages after a change to src/
clean-cache:
    rm -rf build/.cache

# Route an issue that a form opened: <form> is suggest or opt-out
route-issue form number *flags:
    uv run scripts/route_issue.py "$@"
