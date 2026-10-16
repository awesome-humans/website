# Agent instructions

This repository builds and publishes [awesome-humans.net](https://awesome-humans.net). This file tells an AI agent how to maintain it.

## What this repository is

- **The site, not the content.** Opinions, templates, skills, and source rosters live in each ecosystem's repository, listed in [`ecosystems.toml`](ecosystems.toml). Change them there, never in a staged copy here.
- **The site owns publishing.** The Zensical configuration, the theme, the home and shared pages under `pages/`, the source images, issue intake, and the Cloudflare deployment all live here.
- **The design system is canonical for the look.** Colours, type, the logo, and the components come from the [Awesome Humans design system](https://claude.ai/artifact/QfYm5d57sbJxs3W3jMyGiy). Take a token from it instead of inventing a value. An ecosystem's accent appears only in the header stripe, the heading tick, the active navigation item, and the ecosystem chip, and never recolours the logo.
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
- **Agent attribution in conversation.** End each comment an agent writes on an issue or pull request, including replies in review threads, with a line such as `Written by an agent: <harness>, <model>.` A reader, or another agent, then knows a person didn't write it.

## Writing style

These rules cover all prose in this repository: the pages, the README, this file, commit messages, pull request titles and descriptions, and the comments an agent posts on issues and pull requests. They match the ecosystems' rules, so the whole site reads in one voice.

The voice follows the [Google developer documentation style guide](https://developers.google.com/style): conversational but direct, plain, and easy to scan. When a question comes up, use [Google's own order of precedence](https://developers.google.com/style#how-to-use):

1. The rules in this section.
2. The Google developer documentation style guide.
3. For a technical term that neither settles, the [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/), which Google names as its technical reference.

Apart from spelling, which [Spelling](#spelling) covers, this repository departs from Google's guide in one place: write dates as ISO 8601 (`2026-10-15`).

### Voice

- **Write for a working developer.** The site's readers write code for a living. Don't explain what a pull request or a package manager is.
- **Address the reader as "you", and use the imperative for instructions.**
- **Use active voice and present tense.**
- **Use common contractions.** _It's_, _don't_, _isn't_, _can't_, and _you're_ read naturally. Prefer the negative contractions: a reader scanning the page can miss _not_, but rarely misreads _don't_. Avoid rare ones, such as _it'll_ or _should've_.
- **Use plain words.** Write _use_, not _utilize_; _about_, not _with regard to_; _for example_, not _e.g._; _that is_, not _i.e._ Use _can_ for ability and _might_ for possibility. Reserve _must_ for a hard requirement.
- **Drop filler from instructions.** Don't write _please_, _simply_, _easy_, _quickly_, or _let's_, and don't open with a placeholder such as _please note_ or _at this time_. Avoid exclamation marks.
- **Write for a global audience.** Avoid figurative language, idioms, and cultural references. [Stock phrases](#stock-phrases) lists the ones that got into the ecosystems.

### Content

- **Lead with what matters.** Put the recommendation or the action first in a section, a paragraph, and a sentence. Put the reason after it.
- **Put a condition before the instruction it limits.** Write "For details, see [README.md](README.md)", not "See [README.md](README.md) for details". A reader the condition excludes can then skip the instruction.
- **Make link text say where the link goes.** Use the target's title. Never use _here_, _this page_, or a bare URL.
- **Make every sentence carry a fact the reader can act on or check.** A measured number beats an adjective.
- **Cut what doesn't add a fact.** Delete a sentence that restates the one before it, or that comments on the text instead of the subject.
- **Keep sentences short.** Aim for about 20 words. Split any sentence over 35 words at the clause that does separate work.
- **Keep paragraphs short.** Three or four sentences is plenty. Break up a longer one, or turn it into a list.
- **Make it scannable.** Use a numbered list for steps that happen in order, a bulleted list for items that don't, and a table when the same attributes repeat across items. Use sentence-style capitalisation for headings, and keep headings short and specific.
- **Use the serial comma.** Write "opinions, templates, and skills".
- **Write a range with _to_, not an en dash.** Write "versions 8 to 10".

### Rhythm

Agents write most of the prose here, and it goes wrong in rhythm more than vocabulary. Four patterns are fine occasionally and read as machine-written in bulk:

- **Em dashes.** Use at most one per sentence, and only for a real turn. A colon, a comma, or a full stop usually works better.
- **"X, not Y" contrasts.** Keep one when the rejected option is the one a reader would otherwise choose. Cut it when nobody would choose the alternative.
- **Parenthetical asides.** If an aside carries real content, make it a sentence. If it restates the sentence it's attached to, delete it.
- **Lists of three.** A real list can have any length. Don't pad a list to three items because three sounds complete.

### Stock phrases

Replace each with the plain statement it stands for.

| Avoid                                              | Write instead                                   |
| -------------------------------------------------- | ----------------------------------------------- |
| load-bearing                                       | what depends on it                              |
| belt and braces                                    | the second check, and what it catches           |
| earns its keep, earns its place                    | the benefit, measured                           |
| escape hatch                                       | the setting or API that opts out                |
| bites                                              | the failure, and when it happens                |
| for free                                           | without extra code, or what's actually included |
| reach for                                          | use                                             |
| worth noting                                       | (delete it, and state the fact)                 |
| _honest_, _genuinely_, _quietly_ (as intensifiers) | (delete them)                                   |

### Spelling

- **Use British spelling, except where a platform names the word.** Write _defence_, _modelling_, _catalogue_, _behaviour_, and _colour_. Never anglicise an API, a CSS property, or a configuration key, such as `color` or `--md-default-bg-color`.
- **`npm run spell` checks spelling.** When it flags a correctly spelled name or term, add the word to `cspell.words.txt` in the same commit. Never add an American spelling there. In Markdown, it skips link text, inline code, and double-quoted text.

### Scope of these rules

- **They're review guidance, not a build check,** except spelling, which `npm run spell` enforces.
- **They apply only to prose written here.** A third-party title and its URL keep the author's wording and spelling.

## Workflow

### Worktrees

Work in a git worktree, with one branch per directory. The local clone is bare, and each branch is checked out beside it, so you move between pieces of work with `cd` instead of `git checkout`. An in-place branch switch changes the tree under anything that holds a path into it, and discards gitignored state such as `node_modules/` and `.venv/`.

- **Starting:** Start every new piece of work as a new worktree, with `git worktree add -b <branch> <dir> main`.
- **Branch names:** Use the commit's Conventional Commits type (`docs/`, `fix/`, `feat/`, `ci/`, or `chore/`) and a kebab-case slug. `automation/` is reserved for workflows. Settle the name before you open the pull request: renaming the head branch of an open pull request closes it.
- **Directory names:** Name the directory after the branch, with slashes replaced by dashes, so `feat/scaffold` becomes `feat-scaffold/`.
- **Setup:** A fresh worktree has no gitignored local state. Run `uv sync` and `npm install` in it.
- **Finishing:** When a worktree's pull request merges, offer to delete the worktree with `git worktree remove <dir>`, and then its branch. Ask first: the branch might still hold work that never reached the pull request.

### Formatting and linting

- Markdown follows GFM and markdownlint, configured in `.markdownlint-cli2.jsonc`. Spelling follows cspell, configured in `cspell.jsonc` with the `en-GB` dictionary and the repository's word list in `cspell.words.txt`.
- Run `npm run format` to format, and `npm run check` to check formatting, lint, and spelling together. All three use the versions pinned in `package.json`. Don't run `npx prettier`, `npx markdownlint-cli2`, or `npx cspell` directly, because they resolve the latest version.
- Prettier formats Markdown, JSON, YAML, CSS, and JavaScript. It skips the Jinja template in `overrides/`, which it would break. It doesn't format TOML, so `.editorconfig` holds TOML and Python to their indentation.

### Scripts

- Site scripts live in `scripts/` as Python, run with `uv run scripts/<name>.py` from the repository root. Each declares its dependencies inline ([PEP 723](https://peps.python.org/pep-0723/)), with exact pins.
- Ruff formats and lints the Python in `scripts/` and `src/`, configured in `pyproject.toml`. Run `uv run ruff format` to format, and `uv run ruff check` to lint. CI runs both as checks.
- Python is Zensical's own language, so the site needs one toolchain. Don't add a script in an ecosystem's language here: the ecosystems dogfood their own languages in their own repositories.
- Exit codes: 0 for success, 1 for findings, and 2 when not run from the repository root, as in the ecosystems' scripts.

### Links

The `Markdown` workflow checks links with `lychee.toml`, and a broken link blocks the pull request. If a third-party host is down, re-run the job after it recovers. Links in `pages/` are relative to the built site, so only the strict site build checks them.
