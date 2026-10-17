# Plan: the awesome-humans organisation and website

This plan moves the project into the `awesome-humans` GitHub organisation. It has three parts:

- `si618/dotnet-awesome-humans` becomes `awesome-humans/dotnet`.
- `awesome-humans/rust` joins as the second ecosystem.
- A new `awesome-humans/website` repository owns everything specific to publishing awesome-humans.net.

The site takes its look from the [Awesome Humans design system](https://claude.ai/artifact/QfYm5d57sbJxs3W3jMyGiy), collates the roster of every ecosystem, and adds a "Want in or out?" section to the home page.

Written 2026-10-15. This file lives at the workspace root until `awesome-humans/website` exists. Phase 2 moves it there, and the pull request that completes phase 6 deletes it.

**Relationship to `rust/main/PLAN.md`:** That plan's Phase 0 (Organisation) and Phase 5 (Site integration) are replaced by this plan. Its Branding section is superseded by the design system, which came later (2026-10-14 21:57) and changes the approach: a green brand colour, one accent per ecosystem in four set places, and IBM Plex fonts, instead of a gradient header and system fonts. Its phases 1 to 4 and 6 stand. Trim it to point here once this plan is agreed.

## Next session

Stopped 2026-10-17, with Phases 0 to 3 and 8 done, Phase 4 parked, and Phase 5's `website` side merged (#51, #52, #55, #56). Pick up here:

1. **Merge this plan's pull request,** which also widens the intake token (see step 2).
2. **Phase 5, Want in or out?** (agent):
   - **Test the transfer again.** The duplicate path works: [#54](https://github.com/awesome-humans/website/issues/54), a suggestion of Andrew Lock, got its standing and closed. The first new suggestion, [#57](https://github.com/awesome-humans/website/issues/57) for Stephen Cleary, passed the checks, but `gh issue transfer` failed with `Resource not accessible by integration (transferIssue)`, although the app token had `issues: write` on both repositories. The owner moved it by hand to [dotnet#167](https://github.com/awesome-humans/dotnet/issues/167) and labelled it `vet-source`. This plan's pull request adds `contents: write` to the token, which is a guess. After it merges, test with the next real new suggestion. If the transfer still fails, stop transferring: open a copy in the ecosystem with a link back, then comment and close the `website` issue.
   - **dotnet#167 is a real suggestion.** On 2026-10-17 the owner accepted Stephen Cleary for vetting, so `vet-source` decides it the usual way, with a decision log entry and a pull request that closes the issue.
   - **Intake tests stay out of the decision log.** #54 and any later test suggestion exercise the plumbing only. Don't record them in `AWESOME-HUMANS.md`'s decision log, and don't open a `vet-source` pull request for them. Close each with a comment that it was a test.
   - **The `dotnet` side:** `vet-source` taking an issue; the `## Opted out` roster section and its `opted-out` standing; the roster page's two links; and dropping the portrait sentence from the roster's **Kind** bullet.
3. **Phase 8's last check** happens on its own: the next skill run that opens a pull request fills in its template and passes it with `gh pr create --body-file`. If the body drifts from the template, fix the skill.
4. **Phase 7, CodeRabbit,** needs the owner first: install the app on the organisation, and create the `coderabbit` repository.
5. **A `braces` advisory** ([GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm), high) shows in `npm audit` in both `website` and `dotnet`, through `markdownlint-cli2` and `globby`, and in `website` through `stylelint` too. It wasn't a Dependabot alert on 2026-10-17, and `markdownlint-cli2` 0.23.3 was still the latest. If one opens, check for a `markdownlint-cli2` release first, then an `overrides` entry, as #8 did for `katex`.

`gh` is signed in as `si618`, an organisation admin. It still has the `admin:org` scope added for Phase 0, which nothing needs now. The owner removes it with `gh auth refresh -h github.com --remove-scopes admin:org`.

**Agent notes:** Read the repository's `AGENTS.md` before the first commit. Commits and pull request descriptions carry no agent attribution: no `Co-Authored-By` trailer and no "Generated with" line. `npm ci` before `npm run check` in a fresh worktree. The agent can merge a pull request with `gh pr merge` when the owner asks, but can't write secrets.

## Where things stand (checked 2026-10-17)

| Item                          | State                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Organisation `awesome-humans` | Exists, with two-factor authentication required. `awesome-humans-app` (App ID `5322859`, with the cited-human logo) and Renovate are installed on all repositories. It has the `APP_ID` variable, and the `APP_PRIVATE_KEY`, `CLOUDFLARE_API_TOKEN`, and `CLOUDFLARE_ACCOUNT_ID` secrets. GitHub Actions can create pull requests. It holds `.github`, `dotnet`, `rust`, and `website`, each with private vulnerability reporting on, and its profile picture is the cited-human mark. `.github` holds the organisation profile, `SECURITY.md`, and the pull request template, and has an active `protect-main` ruleset |
| `awesome-humans/dotnet`       | Transferred 2026-10-15. The old URL redirects                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Local `.NET` clone            | At `~/Projects/github/awesome-humans/dotnet/`. `origin` points at `awesome-humans/dotnet`, and the `main` worktree is repaired and up to date                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Local `website` clone         | At `~/Projects/github/awesome-humans/website/`, with `.bare/` and a `main` worktree tracking `origin/main`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Local `.github` clone         | At `~/Projects/github/awesome-humans/.github/`, with `.bare/` and a `main` worktree tracking `origin/main`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Local Rust clone              | At `~/Projects/github/awesome-humans/rust/`, with `origin` set to `awesome-humans/rust`, which exists and is empty. It has no commits, and only an untracked `PLAN.md`                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| The site                      | Deploys from `website` since 2026-10-16. `website`'s `Site` workflow builds every live ecosystem's staged pages and deploys to production on a push to `main`, a dispatch from an ecosystem, the weekly schedule, or a manual run. Each pull request in `website` or `dotnet` gets a `website`-built preview. `dotnet` no longer holds `site/` or its own `Site` workflow                                                                                                                                                                                                                                               |
| The design system             | Tokens, the cited-human logo, eight components, and a placeholder montage. Its README names `scripts/build_montage.py` and a theme layer to copy: `stylesheets/awesome-humans.css`, `javascripts/ecosystem.js`, and `assets/brand/`                                                                                                                                                                                                                                                                                                                                                                                     |

## Decisions

These are settled unless the owner says otherwise. Each gives one line on what lost.

| Decision                      | Choice                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repository names              | `dotnet`, `rust`, `website`, and the organisation's `.github`. `website` says what the repository is, where `site` could be misread as a folder, a CI job, or the domain. Folders inside a repository keep the name `site/`, such as the .NET repository's `site/` until the cutover                                                                                                                                                                                                                                                               |
| README headings               | "Awesome Humans of" and the ecosystem's name, such as "Awesome Humans of .NET", which also titles the site's `/<id>/` page. "awesome-humans.net" for `website`, and "Awesome Humans" for the organisation profile. The `dotnet-awesome-humans template` marker keeps its old name, because projects that copied the templates carry it                                                                                                                                                                                                             |
| Site owns publishing          | Everything only the site needs lives in `website`: Zensical configuration, the theme layer, home and shared pages, the montage and source images, issue intake, Cloudflare deployment, and the root `llms.txt`. An ecosystem repository only **stages** its own pages                                                                                                                                                                                                                                                                              |
| Staging contract              | Each ecosystem has one staging command that writes `<out>/<ecosystem>/`: its pages, a `nav.json` fragment, and a `sources.json` roster export. The site validates both JSON files against schemas in `website/schemas/`. A contract keeps the site ignorant of C# or Rust tooling                                                                                                                                                                                                                                                                  |
| Ecosystem registry            | `website/ecosystems.toml` lists each ecosystem's ID, display name, repository, staging command, toolchain setup, and status (`live` or `soon`). Adding TypeScript is then one entry and one accent token. Hard-coding each ecosystem in the workflow lost                                                                                                                                                                                                                                                                                          |
| Site scripts                  | Python, run by `uv run` with [PEP 723](https://peps.python.org/pep-0723/) inline metadata and pinned dependencies. Zensical is already Python, the design system already names `build_montage.py`, and Pillow does the image work. C# or Rust here would add a second toolchain to the one repository that needs neither                                                                                                                                                                                                                           |
| Ecosystem scripts             | Each ecosystem writes its own CI and staging scripts in its own language, to dogfood its opinions: C# file-based apps in `dotnet`, and an `xtask` crate run through `just` in `rust`, as the Rust plan decides. Single-file Cargo scripts lost there because they're still unstable. Only `website` uses Python, because Zensical does                                                                                                                                                                                                             |
| How the site updates          | Four triggers, one workflow: a push to `website` `main`, a `repository_dispatch` from any ecosystem's `main`, a weekly schedule, and `workflow_dispatch`. Every build checks out every live ecosystem at `main`, so whichever repository triggers it, the result is the same                                                                                                                                                                                                                                                                       |
| Previews from ecosystems      | `website` exposes its build as a reusable workflow (`workflow_call`). An ecosystem pull request calls it with its own ref, and gets a full-site preview with only that ecosystem at the pull request's head. Previews only from the website repository lost because most content changes start in an ecosystem                                                                                                                                                                                                                                     |
| Cross-repository identity     | A GitHub App installed on the organisation, `awesome-humans-app`, sends dispatches, transfers issues, and opens pull requests. Workflows mint short-lived tokens with `actions/create-github-app-token`, pinned to a commit SHA. A personal access token lost because the site would depend on one person's account                                                                                                                                                                                                                                |
| Secrets                       | `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` become organisation secrets, limited to `website`, `dotnet`, and `rust`, so the reusable workflow can deploy previews through `secrets: inherit`                                                                                                                                                                                                                                                                                                                                                |
| Citation is opt-out           | Citing and linking published writing needs no permission, and a listed source can opt out at any time. Opting out removes the source from every ecosystem's roster and opinions within 30 days                                                                                                                                                                                                                                                                                                                                                     |
| Portraits are opt-in (parked) | Parked 2026-10-17 with Phase 4: the site shows no faces or logos. When it does, a face appears only with recorded permission, as the design system requires. A source without permission gets a generated tile: their initials inside the mark's square brackets, in `brand-mark`. Faces by default lost, because the design system says "each face needs the person's permission"                                                                                                                                                                 |
| No faces in git               | Stands while portraits are parked, as `AGENTS.md` says. Portraits are downloaded at build time from the URL in the consent register, cached in the Actions cache, and never committed. The montage and per-source images are build outputs too. Git history is permanent, and a face committed once outlives an opt-out                                                                                                                                                                                                                            |
| Publication logos (parked)    | Opt-in, like portraits. A publication gets the initials tile unless `data/consent.toml` records a grant: the publisher's written permission, or a link to brand guidelines that allow this use. Logos appear on per-source images only, never in the montage, which shows people. They're downloaded at build time and never committed. Logos by default lost because many publishers restrict them: Microsoft's trademark guidelines allow its names in text but not its logos without a licence, and a row of company logos reads as endorsement |
| Intake goes through `website` | The "Suggest a source" and "Opt out" issue forms live in `website`, with an ecosystem dropdown. A workflow transfers each suggestion to its ecosystem repository, where `vet-source` runs. Opt-outs start in `website` because one source can be in several ecosystems, and the app fans each one out to every roster that lists it. One link from the home page lost nothing, and per-repository forms would make a source ask once per ecosystem                                                                                                 |
| Fonts                         | Self-host IBM Plex Sans and Mono (SIL Open Font License) as `woff2` under `website/pages/assets/fonts/`. This keeps the current rule of no third-party request on page view. Google Fonts lost for that reason                                                                                                                                                                                                                                                                                                                                     |
| Logo                          | The cited-human mark (concept A). The owner wasn't a fan at first, but it has grown on them since it went on the app and the organisation, so Phase 3 uses it. Concepts B (prompt human) and C (the "ah" monogram) lost to it                                                                                                                                                                                                                                                                                                                      |
| Heading case                  | The section is titled "Want in or out?", in sentence case, as the design system's content rules require for headings                                                                                                                                                                                                                                                                                                                                                                                                                               |
| AI review                     | [CodeRabbit](https://coderabbit.ai) reviews every pull request in every repository, from one central configuration. Its reviews are advisory: the owner's review stays the gate, and it isn't a required check, so a rate limit on the free open-source plan can't block a merge. Below 10 stars, an agent asks for each review with `@coderabbitai review`. A per-repository configuration lost because the repositories share one writing style and one `AGENTS.md` shape                                                                        |

## Target layout of `awesome-humans/website`

```text
├── README.md                    ← what the site is, how to build it locally, the staging contract
├── AGENTS.md                    ← agent instructions; writing style, worktrees, and commits as in the ecosystems
├── PLAN.md                      ← this file, deleted when phase 6 lands
├── ecosystems.toml              ← the registry: id, name, repository, staging command, status
├── zensical.toml                ← base configuration; nav is merged in at build time
├── pyproject.toml               ← Zensical, Pillow, and the scripts' pinned dependencies (replaces requirements.txt)
├── wrangler.jsonc               ← unchanged Cloudflare configuration, moved from dotnet/site/
├── schemas/
│   ├── nav.schema.json
│   └── sources.schema.json
├── pages/                       ← shared pages, the theme layer, and brand assets
│   ├── index.md                 ← home: hero, ecosystems, usage, acknowledgement, want in or out?
│   ├── how-it-works.md
│   ├── want-in-or-out.md        ← the full suggest and opt-out policy that the home section links to
│   ├── stylesheets/awesome-humans.css
│   ├── javascripts/ecosystem.js
│   ├── javascripts/open-details.js
│   └── assets/{brand,fonts}/
├── overrides/                   ← Zensical template overrides: hero, header stripe, footer
├── scripts/
│   ├── stage.py                 ← run each ecosystem's staging command into build/docs/
│   ├── merge_nav.py             ← validate nav.json fragments and write build/zensical.toml
│   ├── collate_sources.py       ← validate sources.json files, write build/sources.json
│   └── route_issue.py           ← label, validate, and transfer intake issues
└── .github/
    ├── ISSUE_TEMPLATE/{suggest-source.yml,opt-out.yml,config.yml}
    └── workflows/
        ├── build.yml            ← reusable: stage, collate, zensical build --strict
        ├── site.yml             ← the four triggers; calls build.yml, then deploys
        ├── intake.yml           ← on issue opened or labelled: route_issue.py
        └── markdown.yml         ← Prettier, markdownlint-cli2, cspell, as in the ecosystems
```

## Phase 0: Organisation settings

The owner does these in the GitHub web UI.

1. ~~**Require two-factor authentication** for members.~~ Done 2026-10-15.
2. ~~**Create the GitHub App** `awesome-humans-app`, owned by the organisation, and install it on all repositories.~~ Done 2026-10-15. Grant only what the workflows need:
   - Contents: read and write (montage and consent pull requests)
   - Pull requests: read and write
   - Issues: read and write (transferring and labelling intake issues)
   - Actions: read
   - Metadata: read

   Store its app ID as the organisation variable `APP_ID`, and its private key as the organisation secret `APP_PRIVATE_KEY`.

   **Progress (2026-10-15):** Created with App ID `5322859`, transferred to the organisation, and installed on all repositories with the permissions above. `APP_ID` and `APP_PRIVATE_KEY` are set, and the key was tested by signing an app token. The owner uploaded the logo the same day.

   **Logo:** The app's avatar appears on every commit, comment, and pull request it makes, so give it the cited-human mark rather than GitHub's generated identicon.
   1. Download `mark-cited-human.svg` from the design system's Logos asset group.
   2. Render it as a 512×512 PNG, with one bracket width of clear space on every side, as the Logo component requires. GitHub app logos must be PNG, JPG, or GIF, and under 1 MB. Use the single `brand-mark` colour (`#109a63`) on a transparent ground. The design system rates it 3:1 on both light and dark, so it reads in either GitHub theme. Don't recolour it per ecosystem.
   3. Upload it under **General → Display information**, and set the badge background colour to `#ffffff`.
   4. Use the same PNG as the organisation's profile picture.

   **Progress (2026-10-15):** Steps 1 and 2 are done. `brand/mark-cited-human-512.png` is 512×512 and 5 KB, rendered with `resvg` from the design system's asset `7b66d8d843b3175c2778c20a279857b7`. The SVG's 32-unit viewBox already holds the clear space: the mark spans 4 to 28, a margin of a sixth on each side, so the PNG has 64 pixels on every side.

   **Logo kept (2026-10-15):** The owner wasn't a fan of the cited-human mark at first, but preferred it to the design system's alternates: B, "prompt human", is lopsided in a square frame, and C, the "ah" monogram, doesn't say "humans". Once it was on the app and the organisation, it grew on them, so A stays. A new mark would still mean changing the design system's Logo component and its asset, and rendering the app logo, the organisation picture, and `pages/assets/brand/` again. The live site uses Zensical's default book icon, so there's no existing logo to keep.

   Phase 3 step 5 brings the same SVG into `website`, so keep one copy of the rendered PNG there, in `pages/assets/brand/`, as its source of truth.

3. ~~**Add the organisation secrets** `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`, limited to `website`, `dotnet`, and `rust`.~~ Done 2026-10-15, with a new token scoped to the account and the `awesome-humans.net` zone. `dotnet`'s repository secrets were deleted, so it deploys with the organisation ones, and the old token can be revoked.
4. ~~**Allow GitHub Actions to create and approve pull requests** at the organisation level.~~ Done 2026-10-15. `dotnet-release-watch.yml` needs this, and so will the montage and consent workflows.
5. ~~**Allow reusable workflows** from repositories in the organisation, so ecosystems can call `website`'s `build.yml`.~~ Nothing to do, checked 2026-10-15: the organisation allows all actions, and the Access setting applies only to private repositories. If `website` is ever made private, set its Access to the organisation.
6. ~~**Install Renovate** on the organisation, for every repository.~~ Done 2026-10-15, as Renovate Only, scanning and alerting, on all repositories.
7. ~~**Create `awesome-humans/.github`**, holding `PULL_REQUEST_TEMPLATE.md` (moved from the .NET repository), `profile/README.md` (the organisation page), and `SECURITY.md`. Ecosystem-specific checklist lines stay in each repository's `AGENTS.md`.~~ Done 2026-10-16.

   **Progress (2026-10-16):** The owner created the repository, and its first commit (`59c9cf5`) went straight to `main`, because the repository was empty. It differs from the step above in three ways:

   - **The template is ecosystem-neutral,** not moved as it was. It names `AWESOME-HUMANS.md`, `HOUSE-OPINIONS.md`, and `AGENTS.md` in backticks, because relative links don't resolve in a pull request description, and asks for the toolchain version rather than the SDK. Its opening comment covers site and CI changes, since `website` uses it too. [awesome-humans/dotnet#142](https://github.com/awesome-humans/dotnet/pull/142) deleted `dotnet`'s copy, and the local Rust plan no longer copies one.
   - **`SECURITY.md` relies on private vulnerability reporting,** now on in every repository, with `contact@awesome-humans.net` as the fallback. It sets no response times.
   - **No lint configuration or CI.** Its files are short and rarely change, so add them only if that changes. Since 2026-10-17 it has a `protect-main` ruleset (ID `25283693`), active, which blocks deletion and force pushes and requires a pull request.

## Phase 1: Transfer `dotnet`

1. **Transfer and rename** in one step, as the repository owner:

   ```sh
   gh api repos/si618/dotnet-awesome-humans/transfer -f new_owner=awesome-humans -f new_name=dotnet
   ```

   GitHub keeps issues, pull requests, stars, and releases, and redirects the old URLs, including `git` remotes. Don't create a new `si618/dotnet-awesome-humans` later, because that breaks the redirect.

2. **Check what didn't carry over:** repository secrets and variables, the `production` and `preview` environments, branch protection, and the Renovate installation. Re-create any that are missing. The Cloudflare secrets now come from the organisation, so delete the repository copies to avoid two sources.
3. **Repair the local clone:**

   ```sh
   cd ~/Projects/github/awesome-humans/dotnet
   git --git-dir=.bare remote set-url origin https://github.com/awesome-humans/dotnet
   git --git-dir=.bare worktree repair main
   git -C main status
   ```

   Then delete `~/Projects/github/dotnet-awesome-humans/` if it still exists and holds no unpushed work.

4. **Pull request `chore/move-to-organisation`** in `dotnet`: replace every `si618/dotnet-awesome-humans` with `awesome-humans/dotnet`, including `repo_url` and `repo_name` in `site/zensical.toml`, the `Repository` constant in `scripts/build-site.cs`, the `README.md` links, skill text, and `llms.txt`. Rename `package.json` `name` to `awesome-humans-dotnet`. Find them all with `git grep -n 'si618'`.
5. **Rust:** create `awesome-humans/rust` empty, add it as the local clone's `origin`, and push once the Rust plan's phase 1 has a first commit.

**Progress (2026-10-15):** Steps 1 to 3 are done.

- **Carried over:** the `CLOUDFLARE_*` repository secrets, the `production` and `preview` environments (no secrets or rules of their own), the `protect-main` ruleset with its four required checks from GitHub Actions, and open pull request #134. The ruleset gained only a disabled `dismissal_restriction`, which GitHub adds in organisations.
- **Kept on purpose:** the repository's Cloudflare secrets stay until Phase 0 step 3 creates the organisation ones. Deleting them first would break deploys.
- **Renovate:** the organisation has no Renovate installation yet, so Renovate doesn't run on `dotnet` until Phase 0 step 6.
- **Local clone:** `~/Projects/github/dotnet-awesome-humans/` was already gone.
- **Step 4:** merged as #135 (`7547049`). The `dotnet-awesome-humans template` marker stays, because it's stamped into projects that use the templates and `verify-project` searches for it. Both followed in #137 (`8c066b9`): the README is titled "Awesome Humans of .NET", and the skills' `repo:` metadata names `awesome-humans/dotnet`. The marker is now the only use of the old name.

- **Step 5:** `awesome-humans/rust` is created, public and empty, with the same description pattern and homepage as `dotnet`. The local clone's `origin` points at it. The first push waits for the Rust plan's phase 1.
- **Rust settings match `dotnet`:** squash merge only, with the pull request's title and body as the commit; branches deleted on merge; no wiki or projects; Dependabot alerts and security updates on; topic `rust`. It has a `protect-main` ruleset (ID `25144742`) with the same rules as `dotnet`'s, but **disabled**: enforced on an empty repository, it would block the first push that creates `main`. After that push, change its required checks from `dotnet`'s job names (`format-and-lint`, `links`, `validate`, `build`) to the Rust CI's, then enable it. It has no `production` or `preview` environments; Phase 2 step 5 decides whether the preview workflow needs them.

## Phase 2: Create `website` and move the site into it

The site keeps deploying from `dotnet` until the cutover in step 6, so awesome-humans.net is never down.

1. **Create `awesome-humans/website`, keeping history.** Extract the site's history from the .NET repository with [git-filter-repo](https://github.com/newren/git-filter-repo), so `git log` and `git blame` still work in `website`:

   ```sh
   git clone --bare https://github.com/awesome-humans/dotnet /tmp/website-extract.git
   git -C /tmp/website-extract.git filter-repo \
     --path site/ --path .github/workflows/site.yml \
     --path-rename site/:
   ```

   Push the result to `awesome-humans/website`, and clone it locally as `~/Projects/github/awesome-humans/website/`, with `.bare/` and a `main` worktree. Move this `PLAN.md` into it, and the workspace's `brand/` files into `pages/assets/brand/`.

   **Progress (2026-10-15):** Done, with three changes to the steps above.

   - **Extracted in the scratchpad,** not `/tmp`. The message callback also rewrote `(#123)` to `(awesome-humans/dotnet#123)`, so pull request links in `website` still point at the .NET repository. The 10 commits keep their authors.
   - **`PLAN.md` and `brand/` wait for step 2.** `main` is protected from the start, so they go in through the scaffold pull request.
   - **The copied `Site` workflow is disabled.** Its first run failed at `setup-dotnet`, as expected, and skipped the deploy, because `website` has no Cloudflare secrets. Enable it again in step 5, when the new `site.yml` replaces it.

   `website` has `dotnet`'s settings: squash merge only, branches deleted on merge, no wiki or projects, Dependabot alerts and security updates, and topics `zensical` and `cloudflare-workers`. Its `protect-main` ruleset (ID `25145260`) is active, with `dotnet`'s rules. It requires `format-and-lint` and `links` from `markdown.yml`, and `build / build` from `site.yml` since 2026-10-15.

2. **Scaffold** the rest of the target layout: `README.md`, `AGENTS.md` (ported from the .NET repository's writing-style, worktree, commit and attribution sections), `pyproject.toml`, the prose tooling, `renovate.json`, and `ecosystems.toml` with `dotnet` as `live`, `rust` as `soon`, and `typescript` as `soon`.
   **Progress (2026-10-15):** Merged as #1 (`d8bcc51`). It adds `README.md`, `AGENTS.md`, `ecosystems.toml`, `pyproject.toml` with `uv.lock`, the prose tooling and `markdown.yml`, `lychee.toml`, `renovate.json`, `.editorconfig`, `LICENSE`, this plan, and the logo under `pages/assets/brand/`. It deletes `requirements.txt`, which `pyproject.toml` replaces. `zensical.toml` and the disabled `site.yml` are unchanged until step 5.

3. **Define the staging contract** in `schemas/` and the `README.md`.

   **Progress (2026-10-15):** Done in `website`'s `feat/staging-contract` pull request. [README.md: Staging contract](README.md#staging-contract) is now canonical. It differs from the first draft here in four ways:
   - **Everything stays under `<id>/`,** including the ecosystem's `assets/` and its own complete `llms.txt`. The site writes the root `llms.txt`, linking to each ecosystem's.
   - **Both JSON files are objects with `"version": 1`,** so the contract can change without breaking an older export.
   - **`standing` is only `citable` or `watch-list`,** the roster's two tables. The Corroborate and Discovery-only markings go in a separate `marking` field. `opted-out` isn't in the export: `data/consent.toml` is the only register of opt-outs, so the site applies them.
   - **`portrait_hint` became `github`,** a login only. A portrait URL lives in `data/consent.toml`, beside the permission it needs.

4. **Pull request `feat/staging-contract`** in `dotnet`: `build-site.cs` takes `--out <dir>` and writes `<dir>/dotnet/` with `nav.json` and `sources.json` beside the pages. It stops writing `zensical.toml`. Keep a `--standalone` flag until the cutover, so the old `site.yml` still works.
   - **Move what the site root holds today into `<dir>/dotnet/`:** the diagrams (`assets/diagrams/`) and `llms.txt`. `pages/how-it-works.md` in `website` then links to `dotnet/assets/diagrams/`, in step 5.
   - **Export `sources.json` from the roster.** The roster has no person-or-publication column, so add one to the Citable and Watch list tables, or a marking in each source's notes, and have `validate-sources.cs` check it.

   **Progress (2026-10-15):** Merged as [awesome-humans/dotnet#138](https://github.com/awesome-humans/dotnet/pull/138). It differs from the steps above in four ways:
   - **No `--standalone` flag.** With no arguments, `build-site.cs` stages the standalone site as before, so `site.yml` needs no change. The cutover removes that mode instead of a flag.
   - **The roster has a Kind column,** `person` or `publication`, which `validate-sources.cs` checks and `vet-source` sets. It holds 26 people and 14 publications. A person's name is the start of their Source link text, so `code-with-mukesh` became "Mukesh Murugan: CodeWithMukesh".
   - **Since keeps its leading year,** so `~2010s` and `~2016 (docs.microsoft.com era; MSDN before)` export as `~2010` and `~2016`.
   - **The staged output was checked against the schemas:** 42 navigation pages that all exist, 40 sorted sources, and nothing outside `dotnet/`.

5. **Build the site workflows** in `website`:
   - **`build.yml` (reusable):** inputs `ecosystem` and `ref`, both optional. It checks out `website`, then every `live` ecosystem in `ecosystems.toml` at `main`, except the named ecosystem at `ref`. It runs `stage.py`, `merge_nav.py`, `collate_sources.py`, the image scripts, and `zensical build --strict`, and uploads `public/` as an artifact.
   - **`site.yml`:** on `push` to `main`, `pull_request`, `repository_dispatch` of type `ecosystem-updated`, a weekly `schedule`, and `workflow_dispatch`. It calls `build.yml`, then keeps the deploy job from today's `site.yml`: production for `main`, dispatch and schedule; a preview alias for a pull request.
   - **In each ecosystem,** add `site-dispatch.yml`, which runs on a push to `main` and sends `ecosystem-updated` to `website` with an app token, and `site-preview.yml`, which runs on a pull request and calls `awesome-humans/website/.github/workflows/build.yml@main` with its own ecosystem and ref, then deploys a preview as `pr-<ecosystem>-<number>`.

   **Progress (2026-10-15):** Done, as #6 in `website` and [awesome-humans/dotnet#139](https://github.com/awesome-humans/dotnet/pull/139). Both previews worked, and a push to `dotnet`'s `main` dispatched a `website` build. The `Site` workflow is enabled again. It differs from the steps above in five ways:
   - **`deploy.yml` is reusable too.** `site.yml` and each ecosystem's `site-preview.yml` call it with `secrets: inherit`, so the Wrangler steps exist once.
   - **`stage.py` fetches the ecosystems itself,** with a shallow `git fetch` of `main` or the named ref into `build/repos/<id>/`. One checkout step per ecosystem would need a workflow edit for each new ecosystem. It also copies `pages/`, and writes the root `llms.txt` from each ecosystem's summary.
   - **No image scripts yet.** Phase 4 adds them to `build.yml`. `collate_sources.py` already writes `build/sources.json` for them.
   - **Production deploys stay off until the cutover.** `site.yml` deploys only pull request previews, as `pr-website-<number>`, so a dispatch can't replace the live site early. Step 6 drops that condition.
   - **Checked against production:** a local build differs from `dotnet`'s standalone build only in the diagram paths, now under `/dotnet/assets/diagrams/`, and in the root `llms.txt`, which now links to `/dotnet/llms.txt`.

6. **Cut over** in one sitting, in this order. Until step 6.3 merges, nothing changes on awesome-humans.net.
   1. **Compare.** Stage and build both ways locally, and diff the outputs. The expected differences are the diagrams, under `/dotnet/assets/diagrams/`, the root `llms.txt`, and the new `dotnet/` files `llms.txt`, `nav.json`, and `sources.json`, plus `assets/brand/`. On 2026-10-15 nothing else differed:

      ```sh
      # in dotnet/main
      dotnet run scripts/build-site.cs
      uvx --with-requirements site/requirements.txt zensical build --strict -f site/build/zensical.toml
      # in a website worktree
      uv run scripts/stage.py fetch && uv run scripts/stage.py stage
      uv run scripts/merge_nav.py && uv run scripts/collate_sources.py
      uv run zensical build --strict -f build/zensical.toml
      diff -rq ../../dotnet/main/site/build/public build/public
      ```

   2. **Swap `dotnet`'s required check.** Its `protect-main` ruleset requires `build`, from the old `site.yml`. Replace it with `build / build`, from `site-preview.yml`, through `gh api` on the ruleset (integration ID `15368`, GitHub Actions). Do this first, or the next step's pull request can't merge.
   3. **`dotnet` `chore/remove-site`:** delete `site/` and `.github/workflows/site.yml`, and drop `build-site.cs`'s no-argument mode, so `--out` is required. Then update what names them:
      - `README.md` and `AGENTS.md`, to describe staging only. AGENTS.md's Site section names `site/pages`, `site/wrangler.jsonc`, and the `Site` workflow.
      - `npm run verify` in `package.json`, to stage into a temporary directory with `--out`.
      - The `site/build` entries in `.gitignore`, `.markdownlint-cli2.jsonc`, `cspell.jsonc`, and `lychee.toml`.

      Merging it dispatches a `website` build, which doesn't deploy yet, so the live site stays as it was.

   4. **`website` `feat/cutover`:** in `site.yml`, drop the deploy job's `if: github.event_name == 'pull_request'`, so `main`, dispatches, and the schedule deploy to production. Update README.md's note, which says only previews deploy. Merging it deploys awesome-humans.net from `website`.
   5. **Check** awesome-humans.net: the home page, `/dotnet/`, a few opinion pages, `/how-it-works/` with its diagrams, `/llms.txt`, and `/dotnet/llms.txt`. The Worker name in `wrangler.jsonc` doesn't change, so the domain and routes stay as they are. To roll back, revert the `website` pull request and redeploy with Wrangler's `rollback`.
   6. **Tidy:** remove README.md's note that the repository is being set up, and update "Where things stand".

   **Progress (2026-10-16):** Done, in the order above.

   - **6.1:** The diff matched the expected differences exactly. The only changed pages were `/dotnet/` and `/how-it-works/`, both for the diagram paths.
   - **6.2:** The owner swapped the check with `gh api -X PUT` on ruleset `20728052`. `protect-main` now requires `format-and-lint`, `links`, `validate`, and `build / build`.
   - **6.3:** Merged as [awesome-humans/dotnet#140](https://github.com/awesome-humans/dotnet/pull/140). `npm run verify` stages into `artifacts/site/`, which `.gitignore` already covers, and the staged `dotnet/` output was byte-identical to before.
   - **6.4:** Merged as #9. Its push to `main` deployed production.
   - **6.5:** All 44 built pages returned 200 on awesome-humans.net, apart from `/404.html`, which redirects. The diagrams load from `/dotnet/assets/diagrams/`, and `/llms.txt` is the new root version.
   - **Also:** #8 and [awesome-humans/dotnet#141](https://github.com/awesome-humans/dotnet/pull/141) closed the `katex` alerts in both repositories with an `overrides` entry. `micromark-extension-math` allows only `katex` `^0.16`, so no bump could fix it.

## Phase 3: Apply the design system

Branch `feat/design-system` in `website`. The design system is the reference: copy values exactly, and don't approximate the marks.

1. **Tokens to CSS:** Write `stylesheets/awesome-humans.css`. It maps each token in `tokens.json` onto Zensical's `--md-*` variables for `[data-md-color-scheme="default"]` (light) and `[data-md-color-scheme="slate"]` (dark):
   - `bg` → `--md-default-bg-color`
   - `ink` → `--md-default-fg-color`
   - `brand` → `--md-typeset-a-color`
   - `surface` → `--md-code-bg-color`
   - …and so on for the rest.

   Spacing, radius, and border tokens become `--ah-*` custom properties.

2. **Ecosystem accent:** `ecosystem.js` sets `data-ecosystem` on `<html>` from the first path segment, and `ah-eco-brand` outside an ecosystem. The accent (`dotnet`, `rust`, or `typescript`) appears only in the four places the design system allows: the 2px header stripe, the 3px tick above `h1`, the active nav link, and the ecosystem chip. Links stay `brand` everywhere.
3. **Components:** Implement the `ah-` classes from the design system's `bundle.css` for Hero, SiteHeader, EcosystemCard, OpinionMeta, Chip, Admonition, CodeCompare, and Logo. Use Zensical template overrides in `overrides/` for the header and hero, and attribute lists (`{ .ah-meta }`) for content components.
4. **Ecosystem pages:** OpinionMeta needs each opinion's `targets:`, `last_reviewed:`, and `sources:`. Extend the staging contract so ecosystems emit the strip as a `{ .ah-meta }` paragraph, and make that change in `dotnet`'s `build-site.cs` and the Rust `xtask build-site`.
5. **Brand assets:** Download `mark-cited-human.svg` and `favicon.svg` from the design system's asset store into `pages/assets/brand/`. Set them as `theme.logo` and `theme.favicon`.
6. **Fonts:** Add the self-hosted IBM Plex `woff2` files and the `@font-face` rules. Keep `font = false` in `zensical.toml`.
7. **Home page:** Use the hero (headline under 18 characters, lede under 46) and replace the Ecosystems list with EcosystemCards, with Rust and TypeScript as `ah-card--soon` until they go live.
8. **Check** text contrast of 4.5:1 in both themes on every component, a focus ring of 3:1, `prefers-reduced-motion`, no horizontal scroll at 360px, and `zensical build --strict`.

**Progress (2026-10-17):** Steps 1 to 3 and 5 to 8 are done in `feat/design-system`. Step 4 is done in [dotnet#159](https://github.com/awesome-humans/dotnet/pull/159), and README.md's [Opinion metadata](README.md#opinion-metadata) section adds the strip to the staging contract. The strip also carries the design system's freshness chip: `fresh`, or `stale` past the ecosystem's review tolerance, which is 180 days for `dotnet`. The Rust `xtask build-site` doesn't exist yet, so Phase 6 builds the strip into it from the contract. The work differs from the steps above in six ways:

- **The design system has no theme layer to copy.** Its README names `stylesheets/awesome-humans.css`, `javascripts/ecosystem.js`, and `assets/brand/`, but it holds only `tokens.json`, `components/bundle.css`, and the assets. So `pages/stylesheets/awesome-humans.css` is written from those two files, with the tokens renamed `--ah-*`, and replaces `extra.css`.
- **No template overrides.** The `modern` variant already keeps the header and tabs on the page background. CSS draws the stripe on `.md-header::after`, the tick on `h1`, and the accent on the active tab and navigation link. The hero is HTML in `pages/index.md`, through `md_in_html`.
- **The design system's favicon is broken.** Its asset (`e5b0a59c…`) colours its paths with a class but has no `<style>`, so the brackets don't draw. `pages/assets/brand/favicon.svg` uses the same paths with the colours inline, switching to `#3DD392` in dark mode. Fix the asset in the design system too.
- **No montage yet.** The design system's montage uses generated placeholder faces, and the hero credit says the faces are cited sources, so the hero ships without one until Phase 4 builds the real montage.
- **`stage.py` writes the ecosystem cards** from `ecosystems.toml`, which gained a `scope` line per ecosystem, so a status change there updates the home page. Each card's chip says `live` or `next`, so the state doesn't rest on colour.
- **The fonts are IBM's Latin-1 subsets,** with IBM's own `unicode-range`: six faces, 136 KB in all, under `pages/assets/fonts/` with the OFL.

The checks: every token pair passes in both themes, at 4.5:1 for text and 3:1 for the focus ring and accents. Firefox screenshots at 1280px and 360px, light and dark, of the home page, an opinion page, the roster, and How it works show no horizontal page scroll, and a scratch page showed the admonitions, CodeCompare, and the `{ .ah-meta }` strip. `dotnet` doesn't use the `house` and `preview` admonitions or the CodeCompare fences yet, so those styles wait for content that uses them.

## Phase 4: Collate sources and generate their images

**Parked 2026-10-17.** The owner judged that collecting, recording, and honouring portrait and logo permissions is too much to maintain, so the site shows no faces or logos. Step 7 was done before the phase was parked. Steps 1 to 6 stay here for reference, and Phase 5 no longer depends on them: without portraits, an opt-out only affects citations, which the ecosystems' rosters handle. A first cut of steps 1 and 2, [#49](https://github.com/awesome-humans/website/pull/49), was closed without merging. `collate_sources.py` still writes `build/sources.json`, which Phase 5's intake reads.

Branch `feat/source-images` in `website`.

1. **`data/consent.toml`**, one table per source that has said anything. A source without a table counts as `portrait = "unknown"`:

   ```toml
   [andrew-lock]
   portrait = "granted"            # granted | declined | unknown
   portrait_url = "https://…"      # the image the person chose; falls back to the GitHub avatar of sources.json's github
   citation = "allowed"            # allowed | opted-out
   evidence = "https://github.com/awesome-humans/website/issues/12"
   recorded = 2026-11-02
   ```

   A publication uses `logo` and `logo_url` instead of `portrait` and `portrait_url`, with `evidence` linking the written permission or the brand guidelines that allow the use:

   ```toml
   [jetbrains-dotnet]
   logo = "granted"                # granted | declined | unknown
   logo_url = "https://…"
   evidence = "https://…"          # the permission, or the brand guidelines' page
   recorded = 2026-11-02
   ```

   Every change to this file goes through a pull request that links its evidence: an issue, or for an email, an anonymised note and the date.

2. **`collate_sources.py`:** Merge every ecosystem's `sources.json` by ID, since one person can be in several rosters. Apply `consent.toml`, and write `build/sources.json`, which the other scripts and the pages read.
   - **Drop a source** whose `citation` is `opted-out` from every page and image at once. The ecosystems remove it from their opinions within 30 days, and until then the source keeps its standing in their `sources.json`.
   - **Fail the build** if an ID has a different `kind` in two ecosystems, or if `consent.toml` gives a `logo` to a person or a `portrait` to a publication.
3. **`fetch_portraits.py`:** For each `portrait = "granted"` or `logo = "granted"` source only, download `portrait_url` or `logo_url` (or the GitHub avatar of a person's `github` login). Cap the size at 2 MB, accept only JPEG, PNG, or WebP, and store the files in an Actions cache keyed by the URL. Nothing is written into the repository.
4. **`build_source_images.py`:** For every source in `build/sources.json`, write `build/docs/assets/sources/<id>.webp` and `<id>-dark.webp` at 96px and 192px:
   - **With a portrait:** greyscale, then duotone in `ink` and `brand-mark` for light, and `brand` on black for dark.
   - **Without one:** the initials tile.
   - **For a publication:** its logo, in full colour on a `surface` ground, if `consent.toml` grants one. Otherwise the initials tile. Never a scraped logo.

   The roster pages show these beside each source.

5. **`build_montage.py`:** Port the design system's montage: a grid of permitted portraits only, with a duotone in `ink` and green using multiply for light, and green on black using screen for dark. Write it as `montage.webp` and `montage-dark.webp`, at 22% and 14% opacity in CSS, masked away from the headline.
   - With fewer than eight permitted portraits, build no montage, and the hero shows its plain `surface` ground. A montage of three faces singles people out.
   - The hero credit line links to a "Faces in the montage" list on the acknowledgement page, so every face can be attributed.
6. **Collecting portrait permissions:** After the theme is live, the owner writes once to each citable person in the roster, through a channel the roster already links. The message asks whether they'd like their portrait in the montage, and which image to use. A yes is recorded as an issue comment or an email note in `consent.toml`. Silence stays `unknown`, which means no face.
7. ~~**Neutral How it works diagrams:**~~ Done 2026-10-16, in #21 and [awesome-humans/dotnet#149](https://github.com/awesome-humans/dotnet/pull/149). `pages/how-it-works.md` showed `dotnet`'s own diagrams today, from `/dotnet/assets/diagrams/`. They name `refresh-dotnet-versions`, use .NET purple and lane colours from outside the design system, and follow the system's dark setting rather than the site's toggle, because they're `<img>` SVGs. Write `scripts/build_diagrams.py`, a port of `dotnet`'s `export-diagrams.cs`, that draws the three diagrams for any ecosystem:
   - **Neutral labels:** "version refresh" for each ecosystem's `refresh-*-versions` skill, and placeholders such as `<topic>`, never an ecosystem's name or branch.
   - **Design-system colours:** `brand` for the accent, `house` for the owner's gates, and `muted`, `line`, and `surface` for the rest, so no ecosystem accent appears outside its four places.
   - **The site's theme:** inline the SVGs in the page, or key their colours to `[data-md-color-scheme]`, so the toggle switches them and they can use IBM Plex.
   - **Each ecosystem keeps its own diagrams** for its README, where its own names belong. Do this before Rust goes live in Phase 6, so the page never shows one ecosystem's pipeline as everyone's.

   **Progress (2026-10-16):** The port is `scripts/diagrams.py`, a module rather than a script: `stage.py` replaces each `<!-- diagram: <name> -->` line on How it works with the diagram's inline SVG, as it fills the home page cards. The SVG carries classes only, and the `.ah-diagram` rules in `awesome-humans.css` colour it from the tokens. `dotnet`'s `export-diagrams.cs` moved to the same tokens and IBM Plex for its README, with the .NET accent dropped. Both dropped the pipeline's "hands off" column for larger type. Rust's `xtask` should start from the same palette and layout.

## Phase 5: Want in or out?

Branch `feat/want-in-or-out` in `website`.

### On the home page

Add this after `## Acknowledgement` in `pages/index.md`, and keep the full policy in `want-in-or-out.md`:

```markdown
## Want in or out?

- **Suggest a source.** Know a person or publication with at least two years of accurate, independent writing about an ecosystem we cover? [Suggest them for vetting](https://github.com/awesome-humans/website/issues/new?template=suggest-source.yml). Every suggestion goes through the same [admission criteria](dotnet/awesome-humans/index.md#admission-criteria), and the decision log records the outcome, whether yes or no.
- **Opt out.** If you're a listed source and don't want your work cited, [ask to opt out](https://github.com/awesome-humans/website/issues/new?template=opt-out.yml), or email <contact@awesome-humans.net> if you'd rather not ask in public. Citations of your work go within 30 days.

For how we handle both, see [Want in or out?](want-in-or-out.md)
```

Each ecosystem's roster page carries the same two links, with `&ecosystem=<name>` prefilled.

**Progress (2026-10-17):** `feat/want-in-or-out` adds the two issue forms, a `config.yml` whose contact link points at the email option, `pages/want-in-or-out.md`, which the home section, the forms, and the organisation profile link to instead of a navigation tab, and this section on the home page. The labels `intake`, `suggest-source`, `opt-out`, and `verified` exist in `website`. Cloudflare Email Routing already forwards `contact@awesome-humans.net`, which the owner tested. The Ecosystem dropdown lists all three ecosystems by name, and `route_issue.py` should fail on a name `ecosystems.toml` doesn't have, so the two can't drift.

**Progress (2026-10-17), intake:** `feat/intake` adds `intake.yml` and `route_issue.py`. A suggestion is checked when it's opened or edited: a field that isn't a URL gets one comment, kept up to date; a source already on that ecosystem's roster, matched by URL or name, gets its standing and closes as a duplicate; a `soon` ecosystem keeps it in `website` with a comment; otherwise it moves to the ecosystem's repository, labelled `vet-source`. A source on another ecosystem's roster isn't a duplicate, because vetting is per ecosystem. A `verified` opt-out opens one issue per live ecosystem that lists the source, unless one is already open, and comments with any name it couldn't match. The script reads each roster from the published `/<id>/sources.json`, so intake needs no build. The app token covers `website` and `dotnet`, and each ecosystem's repository joins it as it goes live. `dotnet` has the `vet-source` and `opt-out` labels.

**Progress (2026-10-17), first runs:** #54 tested the duplicate path, and #55 and #56 fixed what it found: the roster check now runs before the URL checks, the form's own labels no longer cancel a route, and the comment names the roster table. #57 tested the transfer, which failed for the app token. See [Next session](#next-session).

### Suggest a source

1. **`suggest-source.yml` issue form** with these fields:
   - Ecosystem (a dropdown from `ecosystems.toml`)
   - Name
   - Main URL
   - Three sample posts
   - Writing since (year)
   - Why they qualify
   - Relationship to the source: self, colleague, or reader
   - A required checkbox confirming the suggester has read the admission criteria, and knows that videos and podcasts are out of scope

   It applies the labels `intake` and `suggest-source`.

2. **`intake.yml` with `route_issue.py`:** On a new `suggest-source` issue:
   - Check that the URL fields are URLs.
   - Check `build/sources.json` and the rosters for an existing ID or URL. If found, comment with the source's current standing, and close as duplicate.
   - Otherwise, transfer the issue to the chosen ecosystem repository with the app token, and label it `vet-source`.
3. **In each ecosystem:** Extend `vet-source` to accept an issue number as input. It reads the form fields, runs the usual vetting, records the decision in `AWESOME-HUMANS.md`'s decision log in a pull request that closes the issue, and comments the outcome on the issue. A self-suggestion is fine, and the decision log notes it.

### Opt out

An opt-out removes citations only, because the site shows no portraits while Phase 4 is parked. The ecosystems' rosters are the record: `website` keeps no register of its own.

1. **`opt-out.yml` issue form** with these fields:
   - The source IDs or names
   - How the requester shows they control the source: a comment from the GitHub account linked from the source's site, a page or post on the source's domain naming the issue, or an email from the source's domain to `contact@awesome-humans.net`

   It applies the labels `intake` and `opt-out`. The form's intro links the email option for anyone who'd rather not ask in public.

2. **The private channel:** Cloudflare Email Routing forwards `contact@awesome-humans.net`, which `SECURITY.md` already names, to the owner. For an emailed request, the owner opens the opt-out issue themselves, with "email" and the date as the proof, and no address or name beyond the source ID. The ID is public already, in the roster.
3. **Verification** is a human step. An agent can check that the claimed proof exists, but the owner decides, and labels the issue `verified`. An unverifiable request gets one reply explaining the three options, and stays open for 30 days.
4. **Once verified:**
   - **The app opens an issue** in each ecosystem whose `sources.json` lists the ID, linking the `website` issue. `intake.yml` runs it on the `verified` label.
   - **In each ecosystem:** The source moves to a new `## Opted out` roster section, which keeps the ID reserved so it's never suggested again, and exports as `standing = "opted-out"` in `sources.json`. The decision log records the date and the `website` issue. `validate-sources` fails on any opinion that still cites the ID. Opinions that rested on it are re-sourced with `research-topic`, or reduced to what other citable sources support. The site build never waits on this: the policy promises removal within 30 days, not at the next build.
   - **Close** the `website` issue with links to every pull request, and lock it.
5. **Reversal:** Opting back in is a suggestion like any other. It goes through vetting, and leaves the `## Opted out` section only on admission.
6. **`sources.schema.json`** gains the `opted-out` standing, reversing Phase 2's choice to leave opt-outs out of the export, so `route_issue.py` can turn away a suggestion of an opted-out source. Its descriptions stop naming `data/consent.toml` and portraits.

### Policy page

`want-in-or-out.md` sets out the principle that citations are opt-out. It also covers:

- What counts as proof of control
- The 30-day deadline for citations
- That the site shows no faces or logos
- That opting out removes citations of the source's work, but can't remove the fact that a published opinion once linked it. Pages are versioned in git, like any public repository

## Phase 6: Rust joins

1. Follow `rust/main/PLAN.md` phases 1 to 4.
2. Add `cargo xtask build-site --out <dir>`, implementing the staging contract including `sources.json` and the OpinionMeta strip, plus `site-dispatch.yml` and `site-preview.yml`.
3. When the Rust plan's phase 6 has its first opinions, set `rust` to `live` in `ecosystems.toml`. The root `llms.txt` then links `/rust/llms.txt`, the Rust EcosystemCard becomes a link, and "Rust and TypeScript are next" becomes "TypeScript is next".
4. **Rust logo and trademark:** As in the Rust plan, use the official CC-BY logo only on the Rust section index and its EcosystemCard, credited in the footer. Add the footer line "Not affiliated with or endorsed by the Rust Project or the Rust Foundation", and never call the section "official". Add an equivalent .NET line, since the same reasoning applies to Microsoft's marks.
5. Delete this `PLAN.md`, and trim the Rust plan's superseded sections.

## Phase 7: CodeRabbit reviews

[CodeRabbit](https://coderabbit.ai) reviews pull requests in `.github`, `dotnet`, `rust`, `website`, and `coderabbit`. All of them are public, so the [open-source plan](https://docs.coderabbit.ai/management/plans) covers them at no cost, with Team features. Phase 7 is independent of the others, so it can run at any time.

**Limits (checked 2026-10-16):** 1 to 10 pull request reviews an hour per developer, scaled by the repository's stars, 100 to 300 files per review, and 25 chat messages an hour. **A repository with fewer than 10 stars gets no automatic reviews:** someone has to comment `@coderabbitai review`, or select **Trigger review** in CodeRabbit's status comment. On 2026-10-16, `dotnet` had 1 star and the others none, so every review starts by hand until a repository passes 10.

1. **Install the app** (owner, web UI): sign in at [app.coderabbit.ai](https://app.coderabbit.ai) with GitHub, add the `awesome-humans` organisation, and install the CodeRabbit app on all repositories, as for Renovate in Phase 0 step 6.
2. **Create `awesome-humans/coderabbit`** (owner, web UI), public and empty. CodeRabbit reads an organisation's [central configuration](https://docs.coderabbit.ai/configuration/central-configuration) only from a repository with that exact name, so it can't live in `.github`. A repository without its own `.coderabbit.yaml` uses the central one.
3. **Write the central `.coderabbit.yaml`** (agent), first commit straight to `main`, as `.github`'s was:
   - **Language:** `en-GB`, to match the repositories' spelling rule.
   - **Tone and noise:** the `chill` profile, no poem, and no review of draft pull requests.
   - **Advisory only:** `request_changes_workflow: false`, so CodeRabbit comments but never blocks.
   - **Skip generated files:** lock files, `.github/state/`, `assets/diagrams/`, `build/`, `artifacts/`, and `pages/assets/fonts/`.
   - **Path instructions:** for `opinions/` and `templates/`, check that every claim cites a source on the roster and that the metadata is complete. For all Markdown, apply `AGENTS.md: Writing style`.
   - **Guidelines:** CodeRabbit reads `**/AGENTS.md` by default ([Code guidelines](https://docs.coderabbit.ai/knowledge-base/code-guidelines)), so each repository's own rules apply without more configuration.
   - **Renovate:** check whether the schema can skip or shorten reviews of `renovate[bot]`'s pull requests, which only bump pins.
4. **Per-repository overrides,** only if one is needed: a repository's own `.coderabbit.yaml` with `inheritance: true`, which merges onto the central file instead of replacing it ([Configuration inheritance](https://docs.coderabbit.ai/configuration/configuration-inheritance)).
5. **Tell the agents** in each repository's `AGENTS.md`: when a pull request is ready and its checks pass, comment `@coderabbitai review`, because a repository under 10 stars isn't reviewed automatically. Its findings are advisory. Fix each one or reply with the reason, ending the reply with the agent attribution line, and don't resolve a thread without doing either. Once a repository passes 10 stars, the comment is no longer needed, but it does no harm.
6. **Check** with a small pull request in each repository. Comment `@coderabbitai configuration` to see the resolved settings and confirm they come from `awesome-humans/coderabbit/.coderabbit.yaml`. Add `coderabbit` to `cspell.words.txt` wherever a check flags it.

## Phase 8: Pull request templates

The organisation's one pull request template, in `awesome-humans/.github`, fits only a proposed opinion or template change. Six skills in `dotnet` have `change-flow: branch-pr`, and each describes its own pull request body in prose, so the bodies drift between runs and between ecosystems. Give each kind of change its own template, and have each skill name the one it fills in. Phase 8 is independent of the others, so it can run at any time.

**How GitHub picks a template:** Several templates can live in a `PULL_REQUEST_TEMPLATE/` folder, and the `template` query parameter on a compare URL chooses one, such as `?template=source.md` ([Creating a pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)). Unlike issue forms, pull requests have no template chooser, so a person only sees the default `PULL_REQUEST_TEMPLATE.md` unless a link sets the parameter. An agent fills the template in and passes `--body-file`. `gh pr create --template <file>` only works interactively: without a terminal, `gh` refuses to run without `--body`.

1. **Check the organisation fallback first** (agent): with a throwaway branch in `rust`, which has no template of its own, confirm that the folder form in `.github` applies to other repositories, that `?template=` finds those files, and that `gh pr create --template` lists them. The docs only state that a single default template falls back. If the folder doesn't fall back, keep the default in `.github`, and put the skill templates in each ecosystem repository's own `.github/PULL_REQUEST_TEMPLATE/`.
2. **Write the templates** (agent), in `awesome-humans/.github` unless step 1 rules it out:

   | Template                   | Used by                                                              | Asks for                                                                                                                                                                               |
   | -------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `PULL_REQUEST_TEMPLATE.md` | A person, for anything else                                          | What changed and why. It links each template below by its `?template=` URL, so a person can switch                                                                                     |
   | `opinion.md`               | A person proposing an opinion, `harvest-sources`, `resolve-research` | Today's template: the opinion, the provenance, and the checklist. `harvest-sources` adds which posts it read; `resolve-research` names the topic it resolves or discards               |
   | `source.md`                | `vet-source`                                                         | The decision (admit, watch-list, decline, promote, or demote), the evidence for each admission criterion, the decision log line, and, for a demotion, each claim re-sourced or dropped |
   | `version-refresh.md`       | Each `refresh-<ecosystem>-versions` skill                            | The versions before and after (framework, toolchain band, and each package pin), the opinions changed and verified unchanged, whether the samples built and tested, and the TODOs      |
   | `research.md`              | `research-topic`                                                     | The question, the recommendation, the sources cited, and what `resolve-research` should do with it                                                                                     |
   | `house-opinion.md`         | `weave-house-opinion`                                                | The house opinion, the files it changes, the sourced position it overrides, and the `HOUSE-OPINIONS.md` entry. Fold it into `opinion.md` if the two turn out nearly the same           |

   Keep ecosystem-specific lines, such as a toolchain name, out of the templates. As now, those stay in each repository's `AGENTS.md`. Renovate's pull requests don't use a template.

3. **Point each skill at its template** (agent), in `dotnet` now and in `rust` as its skills are written: the skill's "Open a pull request" step names the template, and the agent fills in every section. A section that doesn't apply says so, instead of being deleted.
4. **A person suggesting a source** keeps using `website`'s `suggest-source` issue form. `source.md` is for the pull request that records a `vet-source` decision, by an agent or by a contributor who did the vetting.
5. **Check** with one pull request per template, opened through its `?template=` URL, and one opened by a skill with `gh pr create`.

**Progress (2026-10-17):**

- **Step 1:** The folder falls back. A test file pushed straight to `.github`'s `main` (`106e320`, removed in `20cd476`) showed up in the GraphQL `pullRequestTemplates` list for `rust`, `dotnet`, `website`, and `.github`, beside the default template. `rust` saw it although it's empty, so the throwaway branch wasn't needed. GitHub reads templates only from the default branch. The `?template=` link wasn't checked, because comparing `main` with itself shows no pull request form, so step 5 checks it.
- **Step 2:** [.github#1](https://github.com/awesome-humans/.github/pull/1) adds the five templates and makes the default one ask what changed and why, listing the others. `house-opinion.md` stays separate from `opinion.md`, because it asks for the position it overrides and the Woven table row. `opinion.md` has a **Skill run** section for `harvest-sources` and `resolve-research`.
- **Step 3:** [dotnet#166](https://github.com/awesome-humans/dotnet/pull/166) names a template in each of the six `branch-pr` skills, and repoints the three links to the default template at `opinion.md`. One rule in `dotnet`'s `AGENTS.md` says how to fill a template in, so the skills don't each repeat it. `rust` copies that rule and the template names as its skills are written.
- **Step 5:** On a throwaway `chore/template-check` branch in `website`, since deleted, the owner opened the compare page signed in. With no parameter it filled in the organisation's default template, and `?template=opinion.md` and `?template=source.md` filled in those templates from the folder. The other three sit in the same folder, so they weren't opened one by one. `gh pr create --template --dry-run` failed without a terminal, which is why the skills use `--body-file`. The skill half of the check waits for the next skill run.

## Exploration: house opinion profiles

This isn't a phase yet. It's open question 5, written down far enough to judge whether it's feasible.

**The idea:** The site shows no house opinions by default, so every page is sourced community practice only. A reader, or an agent, can choose a **house profile**: a named set of house opinions per ecosystem, owned by a person (such as `simon-mckenna`) or an organisation. Choosing one layers its opinions over the defaults.

### What stands in the way today

- **Weaving is destructive.** `HOUSE-OPINIONS.md` rule 4 says a house opinion wins a conflict, and cuts the sourced position to a one-line note. With the house opinion removed, there's no full community default left to show. Four house opinions are woven into `dotnet` today: in `testing.md`, `ci.md` (two), and `project-structure.md`, plus the templates `Directory.Build.props` and `example.slnx`.
- **There's only one owner.** `house` is a single reserved ID, and its authority is ownership of the repository.
- **Templates are copy-paste files.** A house opinion inside `Directory.Build.props` has no page around it to hide.

### What would make it feasible

1. **Separate house opinions from sourced ones.** A house opinion becomes a block next to the sourced recommendation it changes, never a rewrite of it. In each opinion file, that's an admonition:

   ```markdown
   !!! house "simon-mckenna"
   **House:** Treat warnings as errors everywhere, not only in CI. …
   ```

   The sourced text above it stays whole. Rule 4 changes from "cut the sourced position" to "keep both, and the profile decides which a reader sees". The `**House:**` marking and the `house` colour token in the design system stay as they are.

2. **Namespace the ID.** The ID becomes `house:<profile>` in `sources:`. Profiles are listed in a registry, `website/houses.toml`, with each profile's ID, display name, kind (`person` or `organisation`), ecosystems, and where its opinions live. `none` is the default.
3. **Templates use region markers** like `# house:simon-mckenna begin` and `# house:simon-mckenna end`, in the file's comment syntax. Staging writes one copy of each template per profile, removing every region that doesn't belong to it. The default copy has no house regions at all.
4. **Validators enforce the pairing.** Every house block names a registered profile, and every `house:<profile>` in `sources:` has a block.

### How a reader or agent chooses a profile

- **On the site:** A profile picker in the header sets `data-house` on `<html>`, remembered in `localStorage` and overridable with `?house=<profile>`. CSS shows only the matching house blocks. Without JavaScript, the reader sees the default. This is one build, with every block in the page and the choice made in the browser. A separate build per profile (`/dotnet/house/simon-mckenna/…`) lost, because it multiplies pages, search results, and preview time by the number of profiles.
- **For agents:** `llms.txt` stays the default. Each profile gets `llms-<profile>.txt`, linking per-profile raw Markdown with the other profiles' blocks removed, and per-profile templates. `verify-project` takes an optional profile.
- **In search:** The index holds house blocks too, so a search result may land on a block that's hidden. Label hits by profile, or leave house blocks out of the index.

### Organisation profiles

- **Hosted profiles:** An organisation's profile hosted on awesome-humans.net carries the site's name. Admit one only by the owner's approval, recorded in `houses.toml`, as contributor opinions are adopted today.
- **Private overlays:** The more useful case is likely an organisation keeping its own profile private. It holds a `house/<ecosystem>.md` overlay in its own repository, and points its agents at the default `llms.txt` plus that overlay. That needs only a documented overlay format, and nothing hosted. Ship this before hosted organisation profiles.

### Cost and timing

- **Changes to the content model:** `HOUSE-OPINIONS.md`, the `weave-house-opinion` skill, `validate-sources`, the staging contract, and the four woven `dotnet` opinions. Unweaving those means restoring each full sourced position from git history or from `research-topic`.
- **Site work:** the picker, the CSS, and per-profile `llms.txt` and templates. This is small next to phase 3.
- **Timing:** Rust starts with an empty `HOUSE-OPINIONS.md`, so the cheapest time to decide is before Rust weaves its first house opinion. Prototype in `dotnet` with the four existing opinions first.

## Open questions

1. **Shared skills and scripts (deferred):** Many skills (`vet-source`, `audit-freshness`, `research-topic`, and the others), the prose tooling configuration, and the shared text in `AGENTS.md`, the admission criteria, and the house-opinion mechanism will exist as near-copies in every ecosystem repository. Consolidating them into a shared repository, or into `website`, may cut the drift. **Decide once the Rust ecosystem is up and running**, when there are two real copies to compare. Until then, keep the copies, and note each divergence in the Rust repository's pull requests.
2. ~~**The opt-out address:**~~ Settled 2026-10-17: `contact@awesome-humans.net`, already named in `SECURITY.md`, forwarded to the owner. One inbox is less to maintain than a separate opt-out address.
3. ~~**The montage threshold:**~~ Parked with Phase 4.
4. **Opted-out sources across ecosystems:** One person can be in several rosters. Should an opt-out given for one ecosystem apply to all of them? This plan assumes it does, because people opt out as people, not per language.
5. **House opinion profiles:** Should the site default to no house opinions, and let readers and agents choose a profile per person or organisation, such as `simon-mckenna`? It looks feasible. The main cost is changing house opinions from rewriting the sourced text to a separate block beside it. See [Exploration: house opinion profiles](#exploration-house-opinion-profiles). **Decide before the Rust repository weaves its first house opinion**, and prototype it with the four that `dotnet` has woven.
