# Review instructions

These instructions tune automated pull request review in this repository. The agent reviewer (currently CodeRabbit) reads them, and so can any other agent asked to review a pull request here. They add to [AGENTS.md](AGENTS.md), which stays the source of every rule.

This repository builds and deploys awesome-humans.net from every ecosystem's staged pages. A finding matters when it would break the build or the deployment, publish something it shouldn't, or misstate a shared convention that every repository links.

## What Important means here

Reserve Important for these. Everything else is Nit at most.

- **A portrait or personal data.** A committed image of a person's face, or a person's details beyond what the source roster already publishes. A face reaches the site only through the build, with recorded permission.
- **A broken staging contract.** A change to `scripts/stage.py`, `scripts/merge_nav.py`, `scripts/collate_sources.py`, or `schemas/` that an ecosystem's staged `nav.json`, `sources.json`, or `llms.txt` written to the [staging contract](README.md#staging-contract) would no longer pass, without the matching change in `README.md` and each ecosystem.
- **A house opinion shown by default.** A page, stylesheet, or script change that shows a `data-house` element, or puts house opinions in `llms.txt`, for a reader who chose no profile. Also a profile added to `houses.toml` without the owner's approval date.
- **A shared convention changed by accident.** An edit under `pages/conventions/` that changes what a rule requires while presenting itself as a wording fix. Every ecosystem's `AGENTS.md` and CodeRabbit's central configuration read these pages, so name the rule and quote the old and new requirement.
- **An unsafe workflow.** A `pull_request_target` job that checks out or runs the pull request's code, a secret passed to a step or a reusable workflow that doesn't need it, a Cloudflare deployment reachable from an untrusted ref, or an action pinned to a tag instead of a commit SHA. Issue intake in `intake.yml` treats issue text as untrusted input.
- **A wrong script.** In `scripts/`, logic that passes input it should reject, a change to the exit codes (0 success, 1 findings, 2 wrong directory), or an inline dependency whose pin differs from the dev group in `pyproject.toml`.
- **A design system departure.** A colour, font, or spacing value in `pages/stylesheets/awesome-humans.css` that isn't an `--ah-*` token from the design system, or an ecosystem accent used outside the header stripe, the heading tick, the active navigation item, and the ecosystem chip.

## Cap the nits

Report at most five Nits per review, the ones a reader would notice first. Writing-style findings, from [Writing style](pages/conventions/writing-style.md) and `AGENTS.md`, are Nit at most.

## Do not report

- Anything CI already enforces: Prettier, taplo, Ruff, markdownlint, stylelint, ESLint, actionlint, zizmor, pyright, cspell, links, and the strict site build.
- Generated files and copied fonts: `package-lock.json`, `uv.lock`, and `pages/assets/fonts/`.
- Content that belongs to an ecosystem: an opinion, template, skill, or roster entry seen in a staged copy. Report it in that ecosystem's repository instead.
- Wording, spelling, or titles inside a third-party quotation or link, and the web platform's American spelling in code, such as `color`.
- An issue the pull request didn't introduce or make worse. Report one as pre-existing only when the changed lines depend on it.

## Always check

- A new script has a `justfile` recipe, and the workflow calls the recipe instead of `npm`, `uv`, or inline logic.
- A new or renamed page under `pages/` is in the navigation in `scripts/merge_nav.py`. A page under `pages/conventions/` is also in `CONVENTIONS` in `scripts/stage.py`, so the root `llms.txt` links it.
- A change to `ecosystems.toml` keeps an ecosystem that has no opinions yet at `soon`.

## Evidence

Cite `file:line` for every finding about this repository's behaviour, not an inference from a name. A finding about an ecosystem's staged output names the ecosystem and the file.
