# awesome-humans.net

The source of [awesome-humans.net](https://awesome-humans.net), which publishes the opinions, templates, skills, and source rosters of every awesome-humans ecosystem.

Each ecosystem's content lives in its own repository. This repository owns everything specific to publishing it: the [Zensical](https://zensical.org) configuration, the theme, the home and shared pages, the source images, the "Want in or out?" intake, and the Cloudflare deployment.

> [!NOTE]
> This repository is being set up. Until the cutover, awesome-humans.net still builds and deploys from [awesome-humans/dotnet](https://github.com/awesome-humans/dotnet), and the copied `Site` workflow here is disabled. For the steps and their state, see [PLAN.md](PLAN.md).

## Ecosystems

[`ecosystems.toml`](ecosystems.toml) lists every ecosystem the site knows. Adding one takes an entry there and an accent token in the theme.

| Ecosystem  | Repository                                                        | Status |
| ---------- | ----------------------------------------------------------------- | ------ |
| .NET       | [awesome-humans/dotnet](https://github.com/awesome-humans/dotnet) | Live   |
| Rust       | [awesome-humans/rust](https://github.com/awesome-humans/rust)     | Soon   |
| TypeScript | Not created yet                                                   | Soon   |

## Staging contract

The site never runs an ecosystem's tooling directly. It runs the ecosystem's `stage` command from [`ecosystems.toml`](ecosystems.toml) in a checkout of its repository, with `{out}` set to the staging directory. The command writes everything under `{out}/<id>/`, and the site builds from there. The ecosystem's own CI decides how to produce the files, in its own language.

| Path in `{out}/<id>/` | Contents                                                                                                                                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index.md`            | The ecosystem's overview page, which the site serves at `/<id>/`                                                                                                                                               |
| Other `*.md` pages    | Any layout under `<id>/`. A link between them is relative, and a link to the shared pages climbs out with `../`                                                                                                |
| `assets/`             | Images and diagrams the pages use. Nothing outside `<id>/`                                                                                                                                                     |
| `nav.json`            | The section's navigation, valid against [`schemas/nav.schema.json`](schemas/nav.schema.json). The site places it under the ecosystem's name                                                                    |
| `sources.json`        | The roster, exported from `AWESOME-HUMANS.md` and valid against [`schemas/sources.schema.json`](schemas/sources.schema.json). The site combines every ecosystem's export to draw the source images and montage |
| `llms.txt`            | A complete [llms.txt](https://llmstxt.org) for the ecosystem, served at `/<id>/llms.txt`. The site's root `llms.txt` links to each one                                                                         |

The command exits 0 when it staged everything, 1 when it found problems in the content, and 2 when it wasn't run from the repository root. On anything but 0, the site build stops.

The site rejects a staged directory whose JSON doesn't match its schema, whose `nav.json` names a page that doesn't exist, or whose `sources.json` holds a duplicate or out-of-order `id`. A source that appears in more than one ecosystem must use the same `id` and `kind` in each.

## Local setup

You need [uv](https://docs.astral.sh/uv/) for the site and its scripts, and Node.js for the prose checks.

```sh
uv sync       # the site's Python environment, from pyproject.toml
npm install   # Prettier, markdownlint, and cspell, at the versions in package.json
npm run check # formatting, Markdown lint, and spelling
```

## Repository layout

```text
├── AGENTS.md          ← how agents work in this repository
├── ecosystems.toml    ← the ecosystem registry
├── pages/             ← the shared pages, the theme, and the brand assets
├── PLAN.md            ← the organisation and website plan, deleted when it's done
├── pyproject.toml     ← the site's Python dependencies
├── schemas/           ← the staging contract's JSON schemas
├── wrangler.jsonc     ← the Cloudflare Worker that serves the site
└── zensical.toml      ← the site configuration
```

## Licence

[Apache License 2.0](LICENSE), as in the ecosystems.
