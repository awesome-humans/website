# Plan: the awesome-humans organisation and website

This plan moves the project into the `awesome-humans` GitHub organisation. It has three parts:

- `si618/dotnet-awesome-humans` becomes `awesome-humans/dotnet`.
- `awesome-humans/rust` joins as the second ecosystem.
- A new `awesome-humans/website` repository owns everything specific to publishing awesome-humans.net.

The site takes its look from the [Awesome Humans design system](https://claude.ai/artifact/QfYm5d57sbJxs3W3jMyGiy), collates the roster of every ecosystem, generates the images of the cited sources, and adds a "Want in or out?" section to the home page.

Written 2026-10-15. This file lives at the workspace root until `awesome-humans/website` exists. Phase 2 moves it there, and the pull request that completes phase 6 deletes it.

**Relationship to `rust/main/PLAN.md`:** That plan's Phase 0 (Organisation) and Phase 5 (Site integration) are replaced by this plan. Its Branding section is superseded by the design system, which came later (2026-10-14 21:57) and changes the approach: a green brand colour, one accent per ecosystem in four set places, and IBM Plex fonts, instead of a gradient header and system fonts. Its phases 1 to 4 and 6 stand. Trim it to point here once this plan is agreed.

## Next session

Stopped 2026-10-15, with Phase 1 and Phase 2 steps 1 to 4 done, Phase 2 step 5 half done, and Phase 0 down to step 7. Pick up here:

1. **Phase 2 step 5, after `website`'s `feat/site-workflows` pull request merges:**
   - Enable the `Site` workflow, which is still disabled from step 1: `gh workflow enable site.yml -R awesome-humans/website`.
   - Add `build / build` to the `protect-main` ruleset's required checks, once it has run on `main`.
   - Open `dotnet`'s `feat/site-workflows` pull request, with `site-dispatch.yml` and `site-preview.yml`.
2. **Phase 0 step 7, in the web UI:** create the `.github` repository.
3. **Renovate's first run:** it was installed 2026-10-15. Check for its Dependency Dashboard issue, and for the `katex` security fix on `website`.

`gh` is signed in as `si618`, an organisation admin, with the `admin:org` scope added for Phase 0. Remove it with `gh auth refresh -h github.com --remove-scopes admin:org` once Phase 0 is done.

## Where things stand (checked 2026-10-15)

| Item                          | State                                                                                                                                                                                                                                                                             |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Organisation `awesome-humans` | Exists, with two-factor authentication required. `awesome-humans-app` (App ID `5322859`) is installed on all repositories, with the `APP_ID` variable and `APP_PRIVATE_KEY` secret set. It holds `dotnet`, `rust`, and `website`, and its profile picture is the cited-human mark |
| `awesome-humans/dotnet`       | Transferred 2026-10-15. The old URL redirects                                                                                                                                                                                                                                     |
| Local `.NET` clone            | At `~/Projects/github/awesome-humans/dotnet/`. `origin` points at `awesome-humans/dotnet`, and the `main` worktree is repaired and up to date                                                                                                                                     |
| Local `website` clone         | At `~/Projects/github/awesome-humans/website/`, with `.bare/` and a `main` worktree tracking `origin/main`                                                                                                                                                                        |
| Local Rust clone              | At `~/Projects/github/awesome-humans/rust/`, with `origin` set to `awesome-humans/rust`, which exists and is empty. It has no commits, and only an untracked `PLAN.md`                                                                                                            |
| The site                      | Built from the .NET repository: `site/`, `scripts/build-site.cs` (hard-codes `Ecosystem = "dotnet"`), and `.github/workflows/site.yml`, which deploys to Cloudflare with Wrangler                                                                                                 |
| The design system             | Tokens, the cited-human logo, eight components, and a placeholder montage. Its README names `scripts/build_montage.py` and a theme layer to copy: `stylesheets/awesome-humans.css`, `javascripts/ecosystem.js`, and `assets/brand/`                                               |

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
| Citation is opt-out           | Citing and linking published writing needs no permission, and a listed source can opt out at any time. Opting out removes the portrait at the next build, and the source from every ecosystem's opinions within 30 days                                                                                                                                                                                                                                                                                                                            |
| Portraits are opt-in          | A face appears only with recorded permission, as the design system requires. A source without permission gets a generated tile: their initials inside the mark's square brackets, in `brand-mark`. Faces by default lost, because the design system says "each face needs the person's permission"                                                                                                                                                                                                                                                 |
| No faces in git               | Portraits are downloaded at build time from the URL in the consent register, cached in the Actions cache, and never committed. The montage and per-source images are build outputs too. Git history is permanent, and a face committed once outlives an opt-out                                                                                                                                                                                                                                                                                    |
| Publication logos             | Opt-in, like portraits. A publication gets the initials tile unless `data/consent.toml` records a grant: the publisher's written permission, or a link to brand guidelines that allow this use. Logos appear on per-source images only, never in the montage, which shows people. They're downloaded at build time and never committed. Logos by default lost because many publishers restrict them: Microsoft's trademark guidelines allow its names in text but not its logos without a licence, and a row of company logos reads as endorsement |
| Intake goes through `website` | The "Suggest a source" and "Opt out" issue forms live in `website`, with an ecosystem dropdown. A workflow transfers each suggestion to its ecosystem repository, where `vet-source` runs. Opt-outs stay in `website` because they cross ecosystems. One link from the home page lost nothing, and per-repository forms would scatter the opt-out register                                                                                                                                                                                         |
| Fonts                         | Self-host IBM Plex Sans and Mono (SIL Open Font License) as `woff2` under `website/pages/assets/fonts/`. This keeps the current rule of no third-party request on page view. Google Fonts lost for that reason                                                                                                                                                                                                                                                                                                                                     |
| Logo                          | The cited-human mark (concept A). The owner wasn't a fan at first, but it has grown on them since it went on the app and the organisation, so Phase 3 uses it. Concepts B (prompt human) and C (the "ah" monogram) lost to it                                                                                                                                                                                                                                                                                                                      |
| Heading case                  | The section is titled "Want in or out?", in sentence case, as the design system's content rules require for headings                                                                                                                                                                                                                                                                                                                                                                                                                               |

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
├── data/
│   └── consent.toml             ← portrait and logo permissions, and opt-outs; the only register of each
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
│   ├── collate_sources.py       ← validate sources.json files, apply consent.toml, write build/sources.json
│   ├── fetch_portraits.py       ← download permitted portraits into the cache
│   ├── build_source_images.py   ← per-source images: portrait or initials tile, light and dark
│   ├── build_montage.py         ← the hero montage, light and dark, from permitted portraits only
│   └── route_issue.py           ← label, validate, and transfer intake issues
└── .github/
    ├── ISSUE_TEMPLATE/{suggest-source.yml,opt-out.yml,config.yml}
    └── workflows/
        ├── build.yml            ← reusable: stage, collate, images, zensical build --strict
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
7. **Create `awesome-humans/.github`**, holding `PULL_REQUEST_TEMPLATE.md` (moved from the .NET repository), `profile/README.md` (the organisation page), and `SECURITY.md`. Ecosystem-specific checklist lines stay in each repository's `AGENTS.md`.

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

   `website` has `dotnet`'s settings: squash merge only, branches deleted on merge, no wiki or projects, Dependabot alerts and security updates, and topics `zensical` and `cloudflare-workers`. Its `protect-main` ruleset (ID `25145260`) is active, with `dotnet`'s rules. It requires `format-and-lint` and `links` from `markdown.yml`. Add `build` once `build.yml` runs.

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

   **Progress (2026-10-15):** The `website` half is in `website`'s `feat/site-workflows` pull request. It differs from the steps above in five ways:
   - **`deploy.yml` is reusable too.** `site.yml` and each ecosystem's `site-preview.yml` call it with `secrets: inherit`, so the Wrangler steps exist once.
   - **`stage.py` fetches the ecosystems itself,** with a shallow `git fetch` of `main` or the named ref into `build/repos/<id>/`. One checkout step per ecosystem would need a workflow edit for each new ecosystem. It also copies `pages/`, and writes the root `llms.txt` from each ecosystem's summary.
   - **No image scripts yet.** Phase 4 adds them to `build.yml`. `collate_sources.py` already writes `build/sources.json` for them.
   - **Production deploys stay off until the cutover.** `site.yml` deploys only pull request previews, as `pr-website-<number>`, so a dispatch can't replace the live site early. Step 6 drops that condition.
   - **Checked against production:** a local build differs from `dotnet`'s standalone build only in the diagram paths, now under `/dotnet/assets/diagrams/`, and in the root `llms.txt`, which now links to `/dotnet/llms.txt`.

6. **Cut over** in one sitting:
   1. Merge the `website` scaffold, and check that a `website` preview matches production.
   2. Merge `chore/remove-site` in `dotnet`: delete `site/` and `site.yml`, drop `build-site.cs`'s no-argument mode, and change `README.md`, `AGENTS.md`, and `npm run verify` to describe staging only.
   3. Run `site.yml` on `main` by `workflow_dispatch`, and check awesome-humans.net.

   The Cloudflare Worker name in `wrangler.jsonc` doesn't change, so the domain and routes stay as they are.

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

## Phase 4: Collate sources and generate their images

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

## Phase 5: Want in or out?

Branch `feat/want-in-or-out` in `website`.

### On the home page

Add this after `## Acknowledgement` in `pages/index.md`, and keep the full policy in `want-in-or-out.md`:

```markdown
## Want in or out?

- **Suggest a source.** Know a person or publication with at least two years of accurate, independent writing about an ecosystem we cover? [Suggest them for vetting](https://github.com/awesome-humans/website/issues/new?template=suggest-source.yml). Every suggestion goes through the same [admission criteria](dotnet/awesome-humans/index.md#admission-criteria), and the decision log records the outcome, whether yes or no.
- **Opt out.** If you're a listed source and don't want your work cited or your face shown, [ask to opt out](https://github.com/awesome-humans/website/issues/new?template=opt-out.yml), or email <opt-out@awesome-humans.net> if you'd rather not ask in public. Your portrait goes at the next build, and citations of your work within 30 days.

For how we handle both, see [Want in or out?](want-in-or-out.md)
```

Each ecosystem's roster page carries the same two links, with `&ecosystem=<name>` prefilled.

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

1. **`opt-out.yml` issue form** with these fields:
   - The source IDs or names
   - What to remove: the portrait only, or the portrait and all citations
   - How the requester shows they control the source: a comment from the GitHub account linked from the source's site, a page or post on the source's domain naming the issue, or an email from the source's domain to the opt-out address

   It applies the labels `intake` and `opt-out`. The form's intro links the email option for anyone who'd rather not ask in public.

2. **The private channel:** Use Cloudflare Email Routing on awesome-humans.net to forward `opt-out@awesome-humans.net` to the owner. The owner records an emailed request as a `consent.toml` change, with the date and "email" as evidence, but no address or name beyond the source ID.
3. **Verification** is a human step. An agent can check that the claimed proof exists, but the owner decides. An unverifiable request gets one reply explaining the three options, and stays open for 30 days.
4. **Once verified:**
   - **Portrait:** A pull request sets `portrait = "declined"`. The next build drops the face from the montage and the source images. A portrait opt-out needs nothing from the ecosystems.
   - **Citation:** The same pull request sets `citation = "opted-out"`, and the app opens an issue in each ecosystem whose `sources.json` lists the ID.
   - **In each ecosystem:** The source moves to a new `## Opted out` roster section, which keeps the ID reserved so it's never suggested again. `validate-sources` fails on any opinion that still cites the ID. Opinions that rested on it are re-sourced with `research-topic`, or reduced to what other citable sources support. Merging this unblocks the site build, which `collate_sources.py` fails until then.
   - **Close** the issue with links to every pull request, and lock it.
5. **Reversal:** Opting back in is a suggestion like any other. It goes through vetting, and leaves the `## Opted out` section only on admission.

### Policy page

`want-in-or-out.md` sets out the two principles: citations are opt-out and portraits are opt-in. It also covers:

- What counts as proof of control
- The 30-day deadline for citations
- That no portrait is ever committed to the repository
- That opting out removes citations of the source's work, but can't remove the fact that a published opinion once linked it. Pages are versioned in git, like any public repository

## Phase 6: Rust joins

1. Follow `rust/main/PLAN.md` phases 1 to 4.
2. Add `cargo xtask build-site --out <dir>`, implementing the staging contract including `sources.json` and the OpinionMeta strip, plus `site-dispatch.yml` and `site-preview.yml`.
3. When the Rust plan's phase 6 has its first opinions, set `rust` to `live` in `ecosystems.toml`. The root `llms.txt` then links `/rust/llms.txt`, the Rust EcosystemCard becomes a link, and "Rust and TypeScript are next" becomes "TypeScript is next".
4. **Rust logo and trademark:** As in the Rust plan, use the official CC-BY logo only on the Rust section index and its EcosystemCard, credited in the footer. Add the footer line "Not affiliated with or endorsed by the Rust Project or the Rust Foundation", and never call the section "official". Add an equivalent .NET line, since the same reasoning applies to Microsoft's marks.
5. Delete this `PLAN.md`, and trim the Rust plan's superseded sections.

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
2. **The opt-out address:** Is `opt-out@awesome-humans.net` acceptable, and should it forward to the owner's personal address or to a shared inbox?
3. **The montage threshold:** Is eight permitted portraits the right minimum before the hero shows a montage?
4. **Opted-out sources across ecosystems:** One person can be in several rosters. Should an opt-out given for one ecosystem apply to all of them? This plan assumes it does, because people opt out as people, not per language.
5. **House opinion profiles:** Should the site default to no house opinions, and let readers and agents choose a profile per person or organisation, such as `simon-mckenna`? It looks feasible. The main cost is changing house opinions from rewriting the sourced text to a separate block beside it. See [Exploration: house opinion profiles](#exploration-house-opinion-profiles). **Decide before the Rust repository weaves its first house opinion**, and prototype it with the four that `dotnet` has woven.
