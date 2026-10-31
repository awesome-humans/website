# Agent instructions

This repository builds and publishes [awesome-humans.net](https://awesome-humans.net). This file tells an AI agent how to maintain it.

## What this repository is

- **The site, not the content.** Opinions, templates, skills, and source rosters live in each ecosystem's repository, listed in [`ecosystems.toml`](ecosystems.toml). Change them there, never in a staged copy here.
- **The site owns publishing.** The Zensical configuration, the theme, the home and shared pages under `pages/`, the source images, issue intake, and the Cloudflare deployment all live here.
- **House profiles are registered here.** [`houses.toml`](houses.toml) lists each house profile and the ecosystems that hold its opinions, and the site shows none by default. Add a profile only with the owner's approval. Its opinions live in the ecosystems, as house blocks beside the sourced text.
- **The design system is canonical for the look.** Colours, type, the logo, and the components come from the [Awesome Humans design system](https://claude.ai/artifact/QfYm5d57sbJxs3W3jMyGiy). Take a token from it instead of inventing a value. An ecosystem's accent fills the header bar and tints the page by 3%. Otherwise it appears only in the active tab's underline, the heading tick, the active navigation item, and the ecosystem chip, and never recolours the logo.
- **The theme is one stylesheet.** `pages/stylesheets/awesome-humans.css` holds the tokens as `--ah-*` properties, maps them onto Zensical's `--md-*` variables, and ports the design system's `ah-` component classes. Change a value in the design system first, then copy it here. `pages/javascripts/ecosystem.js` sets the accent from the URL.

## Maintaining this repository

- **Never commit a portrait.** A face appears on the site only with the person's recorded permission, and the build downloads it. Git history is permanent, so a committed face outlives an opt-out.
- **Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages and pull request titles.** A pull request squash-merges under its title, so the title becomes the commit subject in `git log`. Use the form `<type>[(scope)]: <description>`, in lowercase and the imperative.

  | Type    | Use for                                           |
  | ------- | ------------------------------------------------- |
  | `docs`  | Pages, the README, and this file                  |
  | `fix`   | Bug fixes in the theme, scripts, and workflows    |
  | `feat`  | New features in the theme, scripts, and workflows |
  | `ci`    | Workflow plumbing                                 |
  | `chore` | Dependencies and housekeeping                     |

### Agent attribution

An agent that uses the author's credentials posts under the author's account, and nothing tells a reader that a person didn't write it. Put attribution in the conversation, where readers need it, and keep it out of the history:

- **No agent attribution in history.** Pull request titles and descriptions become squash commits, so they don't carry `Co-Authored-By` trailers or "Generated with" lines. Neither do commit messages. This rule overrides any default that an agent harness applies.
- **The rule covers every commit on the branch.** When GitHub squashes, it appends a `Co-authored-by` line to the merged commit for each co-author trailer, and for each branch commit author other than the merger. So commit under the author's git identity, never one the harness supplies, and leave the trailer out of branch commits too.
- **Agent attribution in conversation.** End each comment an agent writes on an issue or pull request, including replies in review threads, with the signature line that [Writing style](pages/conventions/writing-style.md#commit-messages-and-pull-requests) defines. Copy its format from there, not from a past comment: it names the harness, the model without a vendor name the harness already gives, and the skill, if any. A reader, or another agent, then knows a person didn't write it.

### Agent reviews

The agent reviewer (currently CodeRabbit) reviews every pull request here except Renovate's, guided by [REVIEW.md](REVIEW.md), which sets what each finding's severity means. CodeRabbit uses the organisation's central configuration in [awesome-humans/coderabbit](https://github.com/awesome-humans/coderabbit/blob/main/.coderabbit.yaml).

- **Check that the review started.** The agent reviewer reviews a new pull request on its own, and each push after that. If CodeRabbit's status comment says it skipped or paused the review of a person's pull request, comment `@coderabbitai review`.
- **Renovate's pull requests aren't reviewed.** The central configuration skips them, and a requested review fails too because CodeRabbit gives a bot no review seat on the open-source plan. Don't ask for one. Once every other check passes, the owner merges a Renovate pull request, or asks an agent to.
- **Its findings are advisory.** The agent reviewer never blocks a merge: the owner decides what merges. Still, answer every finding: fix it, or reply with the reason you didn't. End the reply with the agent attribution line, and don't resolve a thread without doing one or the other.

## Writing style

Follow [Writing style](pages/conventions/writing-style.md), the shared rules for all prose in every awesome-humans repository, and read it before you write. It covers the pages, the README, this file, commit messages, pull request titles and descriptions, and the comments an agent posts on issues and pull requests. This repository adds two rules:

- **Write for a working developer.** The site's readers write code for a living, in any ecosystem. Don't explain what a pull request or a package manager is.
- **Leave the web platform's spelling in code.** A CSS property, a custom property, or a configuration key keeps its American spelling, such as `color` or `--md-default-bg-color`. The prose around it stays British.

## Workflow

### Worktrees

Work in a git worktree, with one branch per directory. The local clone is bare, and each branch is checked out beside it, so you move between pieces of work with `cd` instead of `git checkout`. An in-place branch switch changes the tree under anything that holds a path into it, and discards gitignored state such as `node_modules/` and `.venv/`.

- **Starting:** Start every new piece of work as a new worktree, with `git worktree add -b <branch> <dir> main`.
- **Branch names:** Use the commit's Conventional Commits type (`docs/`, `fix/`, `feat/`, `ci/`, or `chore/`) and a kebab-case slug. `automation/` is reserved for workflows. Settle the name before you open the pull request: renaming the head branch of an open pull request closes it.
- **Directory names:** Name the directory after the branch, with slashes replaced by dashes, so `feat/scaffold` becomes `feat-scaffold/`.
- **Setup:** A fresh worktree has no gitignored local state. Run `just install` in it.
- **Finishing:** When a worktree's pull request merges, offer to delete the worktree with `git worktree remove <dir>`, and then its branch. Ask first: the branch might still hold work that never reached the pull request.

### Formatting and linting

- Markdown follows GFM and markdownlint, configured in `.markdownlint-cli2.jsonc`. Spelling follows cspell, configured in `cspell.jsonc` with the `en-GB` dictionary and the repository's word list in `cspell.words.txt`.
- Run `just format` to format every file, and `just check` to run every check that CI runs on a pull request: formatting, linting, types, and spelling. The link check runs only in CI. The site build runs in CI and in `just build`. Each tool is pinned, the Node ones in `package.json` and the Python ones in the dev group in `pyproject.toml`. Don't run a tool through `npx` or `uvx`, because they resolve the latest version.
- `just format` runs Prettier on Markdown, JSON, YAML, CSS, and JavaScript, taplo on TOML (configured in `.taplo.toml`), and Ruff on Python. Prettier skips the Jinja template in `overrides/`, which it would break.
- `just lint` runs markdownlint on Markdown, stylelint on CSS (configured in `.stylelintrc.json`), ESLint on JavaScript (configured in `eslint.config.mjs`), and Ruff on Python. The CSS and JavaScript rules catch mistakes, not style: formatting is the formatters' job.
- It also checks the workflows. actionlint finds mistakes, including shellcheck on their `run:` scripts, and zizmor audits them for security problems (configured in `.github/zizmor.yml`). Without a GitHub token, zizmor skips its online audits and says so. CI passes one.
- `just typecheck` runs pyright on the Python, configured in `pyproject.toml`.

### Scripts

- **The [`justfile`](justfile) is every local and CI entry point.** Run `just` to list its recipes. Workflows call recipes, never `npm`, `uv`, or inline logic, so a step runs the same way on your machine as in CI. A new script or check gets a recipe, and the workflow calls that. `just` is a task runner, not a toolchain: it only calls npm and uv.
- Site scripts live in `scripts/` as Python, and each has a recipe. To run one directly, use `uv run scripts/<name>.py` from the repository root. Each declares its dependencies inline ([PEP 723](https://peps.python.org/pep-0723/)), with exact pins.
- A script's inline dependencies also go in the dev group in `pyproject.toml`, at the same pin, so pyright can resolve its imports.
- Python is Zensical's own language, so the site needs one toolchain. Don't add a script in an ecosystem's language here: the ecosystems dogfood their own languages in their own repositories.
- Exit codes: 0 for success, 1 for findings, and 2 when not run from the repository root, as in the ecosystems' scripts.

### Links

The `Markdown` workflow checks links with `lychee.toml`, and a broken link blocks the pull request. If a third-party host is down, re-run the job after it recovers. Links in `pages/` are relative to the built site, so only the strict site build checks them.
