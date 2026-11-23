# Checks: formatting, linting, scripts, links

## Formatting and linting

- Markdown follows GFM and markdownlint, configured in `.markdownlint-cli2.jsonc`. Spelling follows cspell, configured in `cspell.jsonc` with the `en-GB` dictionary and the repository's word list in `cspell.words.txt`.
- Run `just format` to format every file, and `just check` to run every check that CI runs on a pull request: formatting, linting, types, and spelling. The link check runs only in CI. The site build runs in CI and in `just build`. Each tool is pinned, the Node ones in `package.json` and the Python ones in the dev group in `pyproject.toml`. Don't run a tool through `npx` or `uvx`, because they resolve the latest version.
- `just format` runs Prettier on Markdown, JSON, YAML, CSS, and JavaScript, taplo on TOML (configured in `.taplo.toml`), and Ruff on Python. Prettier skips the Jinja templates in `overrides/`, which it would break.
- `just lint` runs markdownlint on Markdown, stylelint on CSS (configured in `.stylelintrc.json`), ESLint on JavaScript (configured in `eslint.config.mjs`), and Ruff on Python. The CSS and JavaScript rules catch mistakes, not style: formatting is the formatters' job.
- `just lint` also checks the workflows. actionlint finds mistakes, including shellcheck on their `run:` scripts, and zizmor audits them for security problems. Without a GitHub token, zizmor skips its online audits and says so. CI passes `github.token` as `GH_TOKEN`.
- `just typecheck` runs pyright on the Python, configured in `pyproject.toml`.

## Scripts

- **The [`justfile`](../justfile) is every local and CI entry point.** Run `just` to list its recipes. Workflows call recipes, never `npm`, `uv`, or inline logic, so a step runs the same way on your machine as in CI. A new script or check gets a recipe, and the workflow calls that. `just` is a task runner, not a toolchain: it only calls npm and uv.
- Site scripts live in `scripts/` as Python, and each has a recipe. To run one directly, use `uv run scripts/<name>.py` from the repository root. Each declares its dependencies inline ([PEP 723](https://peps.python.org/pep-0723/)), with exact pins.
- A script's inline dependencies also go in the dev group in `pyproject.toml`, at the same pin, so pyright can resolve its imports.
- Python is Zensical's own language, so the site needs one toolchain. Don't add a script in an ecosystem's language here: the ecosystems dogfood their own languages in their own repositories.
- `just test-llms` asks an agent, from the fetch instruction on the Usage page, to read each opinion and template of each ecosystem in full, and to list each with its last-reviewed date and one sentence on what it recommends. It fails on any the agent didn't read in full from the site, or didn't list with the right date, and reports the tokens that reading them all used. With `--as-written`, it runs the home page's `review-project` prompt on the ecosystem's checkout instead, and reports which opinions and templates the agent picked. A run costs about a dollar an ecosystem and varies from run to run, so it isn't in `just check` or CI. Run it after you change `READING` in `scripts/stage.py` or a prompt in `pages/index.md`, with `--local` to test `build/public/` before the change deploys. The agent is Claude Code, because the script reads its transcript.
- `just skills` writes each ecosystem's consumer skills and their indexes into `build/public/`, for `npx skills add` ([README: Skills index](../README.md#skills-index)). `just build` runs it last. After you change `scripts/publish_skills.py`, run `just skills` again, then `just test-skills`. That serves `build/public/` on a local port, and runs the skills CLI, pinned in `package.json`, with `--list` against the root, each `/<id>`, and each `/<profile>`. It fails when an index doesn't list its skills, and it installs nothing.
- `just skills-drift` compares the maintenance skills the ecosystems copy from each other, and fails when the lines that differ aren't the ones `skills-drift/` records ([README: Skill drift](../README.md#skill-drift)). The `Skills drift` workflow runs it, and `just check` doesn't, because it needs `just fetch` first. Never edit a file under `skills-drift/` by hand: `just skills-drift --update` writes it.
- Exit codes: 0 for success, 1 for findings, and 2 when not run from the repository root, as in the ecosystems' scripts.

## Links

The `Markdown` workflow checks links with `lychee.toml`, and a broken link blocks the pull request. If a third-party host is down, re-run the job after it recovers. Links in `pages/` are relative to the built site, so only the strict site build checks them.
