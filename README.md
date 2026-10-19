# awesome-humans.net

The source of [awesome-humans.net](https://awesome-humans.net), an agentic take on awesome lists. It publishes the opinions, templates, skills, and source rosters of every awesome-humans ecosystem.

Each ecosystem's content lives in its own repository. This repository owns everything specific to publishing it: the [Zensical](https://zensical.org) configuration, the theme, the home and shared pages, the source images, the "Want in or out?" intake, and the Cloudflare deployment.

## Ecosystems

[`ecosystems.toml`](ecosystems.toml) lists every ecosystem the site knows. Adding one takes an entry there, which also gives it a card on the home page, and its accent colours in [`pages/stylesheets/awesome-humans.css`](pages/stylesheets/awesome-humans.css), copied from the design system, and an option in the Ecosystem dropdown of [`suggest-source.yml`](.github/ISSUE_TEMPLATE/suggest-source.yml). Once it's live, add its repository to the app token in [`intake.yml`](.github/workflows/intake.yml). Its logo, if the site shows one, goes in [`pages/assets/ecosystems/`](pages/assets/ecosystems) as `<id>.svg`, with `<id>-dark.svg` when it doesn't read on a dark ground, and its credit goes in [`overrides/partials/copyright.html`](overrides/partials/copyright.html).

| Ecosystem | Repository                                                        | Status |
| --------- | ----------------------------------------------------------------- | ------ |
| .NET      | [awesome-humans/dotnet](https://github.com/awesome-humans/dotnet) | Live   |
| Rust      | [awesome-humans/rust](https://github.com/awesome-humans/rust)     | Soon   |

## Staging contract

The site never runs an ecosystem's tooling directly. It runs the ecosystem's `stage` command from [`ecosystems.toml`](ecosystems.toml) in a checkout of its repository, with `{out}` set to the staging directory. The command writes everything under `{out}/<id>/`, and the site builds from there. The ecosystem's own CI decides how to produce the files, in its own language.

| Path in `{out}/<id>/` | Contents                                                                                                                                                                                                             |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index.md`            | The ecosystem's overview page, which the site serves at `/<id>/`                                                                                                                                                     |
| Other `*.md` pages    | Any layout under `<id>/`. A link between them is relative, and a link to the shared pages climbs out with `../`                                                                                                      |
| `assets/`             | Images and diagrams the pages use. Nothing outside `<id>/`                                                                                                                                                           |
| `nav.json`            | The section's navigation, valid against [`schemas/nav.schema.json`](schemas/nav.schema.json). The site places it under the ecosystem's name                                                                          |
| `sources.json`        | The roster, exported from `AWESOME-HUMANS.md` and valid against [`schemas/sources.schema.json`](schemas/sources.schema.json). The site combines every ecosystem's export to draw the source images and montage       |
| `llms.txt`            | A complete [llms.txt](https://llmstxt.org) for the ecosystem, served at `/<id>/llms.txt`, with no house opinions in the files it links. The site's root `llms.txt` links to each one                                 |
| `llms-<profile>.txt`  | One for each house profile the ecosystem holds opinions for, linking files with only that profile's house opinions. The site checks each profile against [`houses.toml`](houses.toml)                                |
| `raw/`                | Optional. Copies of files that differ by house profile, for the `llms` files to link, such as `raw/none/` and `raw/<profile>/`. Name a Markdown copy `*.md.txt`, because the site renders every `.md` file as a page |

### House opinions

A house opinion belongs to a house profile in [`houses.toml`](houses.toml), and the site shows it only to a reader who chooses that profile in the header. Stage it in a page as a block, which opens with `/// house | <profile>` and closes with `///`, each on its own line:

```markdown
/// house | simon-mckenna

**House:** Treat warnings as errors on every machine, not only in CI. …

///
```

The site titles the block with the profile's name, and leaves it out of search. Any other element that belongs to a profile, such as its chip in the metadata strip, carries `data-house="<profile>"` instead. For readers, see [House profiles](pages/house-profiles.md).

### Opinion metadata

Each opinion page opens with the design system's OpinionMeta strip, directly under its `h1`. Write it as one paragraph marked `{ .ah-meta }`, with a `.ah-meta__item` span for each of the opinion's targets, its last-reviewed date, and its sources:

```markdown
<span class="ah-meta__item"><span class="ah-label">Targets</span> `net10.0` `csharp-14`</span><span class="ah-meta__item"><span class="ah-label">Last reviewed</span> 2026-08-18 <span class="ah-chip ah-chip--fresh ah-chip--dot">fresh</span></span><span class="ah-meta__item"><span class="ah-label">Sources</span> [andrew-lock](../awesome-humans/citable.md#andrew-lock-citable){ .ah-chip } [ms-learn](../awesome-humans/citable.md#ms-learn-citable){ .ah-chip }</span>
{ .ah-meta }
```

- **Separate values with a space.** Two code spans with no space between them merge into one.
- **Link each source to its roster entry,** with a relative link the build can check. Give a house profile's chip `data-house="<profile>"`, as in `{ .ah-chip data-house="simon-mckenna" }`.
- **Mark the review date `fresh` or `stale`** against the ecosystem's own review tolerance, with `ah-chip--fresh` or `ah-chip--stale`. The weekly build restages every ecosystem, so the chip changes within a week of the date passing.

The command exits 0 when it staged everything, 1 when it found problems in the content, and 2 when it wasn't run from the repository root. On anything but 0, the site build stops.

The site rejects a staged directory when:

- Its JSON doesn't match its schema.
- Its `nav.json` names a page that doesn't exist.
- Its `sources.json` holds a duplicate or out-of-order `id`.
- An `llms-<profile>.txt` names a profile that `houses.toml` doesn't list for the ecosystem. A profile listed for an ecosystem that stages nothing for it only gets a warning, so a profile can be registered before its first opinion lands.

A source that appears in more than one ecosystem must use the same `id` and `kind` in each.

## Local setup

You need [just](https://just.systems/) to run the commands, [uv](https://docs.astral.sh/uv/) for the site and its scripts, and Node.js for the checks. Run `just` to list every recipe.

```sh
just install # the Node and Python tools, at the versions package-lock.json and uv.lock pin
just format  # format every file
just check   # what CI checks on a pull request: formatting, linting, types, and spelling
```

Each live ecosystem also needs its toolchain, such as the .NET SDK for `dotnet`.

## Build the site

The `Site` workflow runs the same recipes through [`build.yml`](.github/workflows/build.yml), so a local build matches CI:

```sh
just fetch # clone each live ecosystem into build/repos/, at main
just build # stage, check and merge each nav.json and sources.json, and build the site
```

`just build` runs `stage`, `nav`, `sources`, and `build-site`, which you can also run one at a time. The site lands in `build/public/`. To preview it, run `just serve` instead of `just build`.

Zensical caches each rendered page in `build/.cache/`, keyed by its content. After you change `src/`, run `just clean-cache` before you build.

To preview a change to an ecosystem before you push it, pass your checkout to `build` or `serve`, and it stages from there instead of `build/repos/`:

```sh
just serve dotnet=../../dotnet/main
```

An ecosystem that's still `soon` builds only when the `PREVIEW_ECOSYSTEM` environment variable names it, as `build.yml` sets it for that ecosystem's pull requests:

```sh
PREVIEW_ECOSYSTEM=rust just serve rust=../../rust/main
```

### How the site updates

| Trigger                                    | What runs                                                                                                        |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| A push to `main` here                      | `site.yml` builds and deploys to awesome-humans.net                                                              |
| A push to an ecosystem's `main`            | Its `site-dispatch.yml` sends `ecosystem-updated` to `site.yml`                                                  |
| Weekly, Mondays 06:00 UTC, or a manual run | `site.yml` builds and deploys, catching anything missed                                                          |
| A pull request here                        | `site.yml` builds and deploys a preview, `pr-website-<number>`                                                   |
| A pull request in an ecosystem             | Its `site-preview.yml` calls `build.yml` and `deploy.yml` with its head commit, for a preview `pr-<id>-<number>` |

Every build takes every live ecosystem at `main`, except the one a preview names. A preview also builds its ecosystem while it's `soon`, so its pull requests get the strict build before production shows it.

## Repository layout

```text
├── .github/ISSUE_TEMPLATE/ ← the Suggest a source and Opt out issue forms
├── .github/workflows/      ← build.yml and deploy.yml, which ecosystems call too, site.yml, intake.yml, and markdown.yml
├── AGENTS.md               ← how agents work in this repository
├── ecosystems.toml         ← the ecosystem registry
├── houses.toml             ← the house profile registry
├── justfile                ← every local and CI entry point: run `just` to list them
├── pages/                  ← the shared pages, the theme, and the brand assets
├── PLAN.md                 ← the organisation and website plan, deleted when it's done
├── pyproject.toml          ← the site's Python dependencies, and its package of Markdown extensions
├── schemas/                ← the staging contract's JSON schemas
├── src/                    ← the site's Markdown extensions, which zensical.toml loads
├── scripts/                ← stage, draw the How it works diagrams, merge the navigation, collate the sources, and route intake issues
├── wrangler.jsonc          ← the Cloudflare Worker that serves the site
└── zensical.toml           ← the site configuration
```

## Licence

[Apache License 2.0](LICENSE), as in the ecosystems.
