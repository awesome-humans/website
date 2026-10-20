# Every local and CI entry point (AGENTS.md: Scripts). CI calls these recipes, never npm or
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

# Export the site's build dependencies from uv.lock as a CycloneDX SBOM, which Credits and
# licences links. Run after stage, which recreates build/docs/
sbom:
    uv export --format cyclonedx1.5 --preview-features sbom-export --no-dev --frozen --quiet -o build/docs/sbom.cdx.json

# Build build/public/ from what's staged, failing on any broken link or anchor
build-site:
    uv run zensical build --strict -f build/zensical.toml

# Stage, merge, and build the site, each <id>=<path> from that checkout. Run fetch first
build *locals:
    just stage "$@"
    just nav
    just sources
    just sbom
    just build-site

# Stage, merge, and serve the site locally, each <id>=<path> from that checkout. Run fetch first
serve *locals:
    just stage "$@"
    just nav
    just sources
    just sbom
    uv run zensical serve -f build/zensical.toml

# Delete Zensical's page cache, which keeps stale pages after a change to src/
clean-cache:
    rm -rf build/.cache

# Route an issue that a form opened: <form> is suggest or opt-out
route-issue form number *flags:
    uv run scripts/route_issue.py "$@"
