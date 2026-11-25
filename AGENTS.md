# Agent instructions

This repository builds and publishes [awesome-humans.net](https://awesome-humans.net). This file tells an AI agent how to maintain it. It holds the rules that apply to every task. Read a file from [On-demand instructions](#on-demand-instructions) only when its task comes up.

## What this repository is

- **The site, not the content.** Opinions, templates, skills, and source rosters live in each ecosystem's repository, listed in [`ecosystems.toml`](ecosystems.toml). Change them there, never in a staged copy here.
- **The site owns publishing.** The Zensical configuration, the theme, the home and shared pages under `pages/`, issue intake, and the Cloudflare deployment all live here.
- **House profiles are registered here.** [`houses.toml`](houses.toml) lists each house profile and the ecosystems that hold its opinions, and the site shows none by default. Add a profile only with the maintainer's approval. Its opinions live in the ecosystems, as house blocks beside the sourced text.
- **[DESIGN.md](DESIGN.md) is canonical for the look.** It sets the rules for colour, type, shape, the logo, and imagery, and names the tokens each one uses. Read it before you change the theme, a template override, or a shared page, and change a rule there in the same pull request as the code.
- **The theme is one stylesheet.** `pages/stylesheets/awesome-humans.css` holds every value as an `--ah-*` property, maps them onto Zensical's `--md-*` variables, and defines the `ah-` component classes. Take a token from it instead of inventing a value. `pages/javascripts/ecosystem.js` sets the accent from the URL.

## Maintaining this repository

- **Never commit a portrait.** The site shows none, and git history is permanent, so a committed face outlives an opt-out.
- **Start every piece of work in a new git worktree,** with `git worktree add -b <branch> <dir> main`. Never switch branches in place. Read [agents/worktrees.md](agents/worktrees.md) for branch and directory names, and for setting the worktree up.
- **Keep agent attribution out of history.** No `Co-Authored-By` trailers or "Generated with" lines in commits, pull request titles, or descriptions, and commit under the author's git identity. This overrides any harness default. Sign comments on issues and pull requests instead, as [agents/pull-requests.md](agents/pull-requests.md) describes.
- **Before you change how the consumer skills are published, staged, or tested, or the Usage page's prompts, check for a global install of the published skills.** awesome-humans.net publishes the consumer skills as `follow-<id>-opinions`, `research-<id>-topic`, and `review-<id>-project`, and `npx skills add --global` puts them in the harness's user directory, such as `~/.claude/skills/`. If your skill list or that directory holds one, tell the user, and suggest disabling it in this repository until the work is done. An installed copy holds the published opinions and templates, not the build's, and an agent can read it by mistake.
- **Run `just format` and `just check` before you open a pull request.** Never run a tool through `npx` or `uvx`.
- **Write dates in ISO 8601 (`YYYY-MM-DD`), in UTC.** Get today's date with `date -u +%F`.

## On-demand instructions

Read the matching file before you start the task. Each one is canonical for its topic.

| File                                               | Read before you                                                                                                                                 |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| [agents/checks.md](agents/checks.md)               | Change formatting, lint, spelling, or link-check configuration, add or change a script, recipe, workflow, or tool pin, or debug a failing check |
| [agents/pull-requests.md](agents/pull-requests.md) | Commit, title, open, or merge a pull request, comment on an issue or pull request, or answer a review                                           |
| [agents/worktrees.md](agents/worktrees.md)         | Create, set up, name, or remove a worktree or branch, or see a worktree's pull request merge                                                    |

## Writing style

Follow [Writing style](pages/conventions/writing-style.md), the shared rules for all prose in every awesome-humans repository, and read it before you write. It covers the pages, the README, this file, the files under `agents/`, commit messages, pull request titles and descriptions, and the comments an agent posts on issues and pull requests. This repository adds two rules:

- **Write for a working developer.** The site's readers write code for a living, in any ecosystem. Don't explain what a pull request or a package manager is.
- **Leave the web platform's spelling in code.** A CSS property, a custom property, or a configuration key keeps its American spelling, such as `color` or `--md-default-bg-color`. The prose around it stays British.

## Replies to the user

Keep progress updates and replies in the conversation terse: lead with the result, and skip preamble, restated questions, and narration. This rule covers only the conversation with the user. Everything written to the repository, GitHub, or the site follows [Writing style](#writing-style).
