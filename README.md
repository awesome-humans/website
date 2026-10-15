# website

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
├── wrangler.jsonc     ← the Cloudflare Worker that serves the site
└── zensical.toml      ← the site configuration
```

## Licence

[Apache License 2.0](LICENSE), as in the ecosystems.
