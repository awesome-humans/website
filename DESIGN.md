# Design

These rules set how awesome-humans.net looks. They're canonical for the look: follow them when you change the theme, a template override, or a shared page. [`pages/stylesheets/awesome-humans.css`](pages/stylesheets/awesome-humans.css) holds every value as an `--ah-*` custom property, so this file names tokens and never repeats a value. To change a value, change it in the stylesheet. To change a rule, change it here in the same pull request.

The brand is crisp and technical: a reference you trust because every claim is cited.

## Colour

- **Neutrals carry the page.** Set `--ah-ink` on `--ah-bg`. Use `--ah-surface` for the metadata strip and the hero, `--ah-code` for code blocks, and `--ah-line` for every border.
- **Green is the one brand hue.** `--ah-brand` is for links, the fresh state, the hero kicker, and primary buttons. `--ah-brand-mark` is for the logo, the focus ring, and large graphics only.
- **Each section has one accent.** An ecosystem's section takes its own token, such as `--ah-dotnet`, and every other page takes `--ah-brand`. `pages/javascripts/ecosystem.js` sets it from the URL, as `--ah-eco`.
- **The accent fills the header bar and tints the page.** The bar is `--ah-header-bg` with `--ah-header-ink` on it: the accent itself in light mode, and 28% of it on `--ah-bg` in dark mode. The accent tints `--ah-bg`, `--ah-surface`, and `--ah-raised` by 3%, or 2% in dark mode. Code blocks keep the plain `--ah-code`, because the syntax colours are set against it.
- **Otherwise the accent appears in four places only:** the active tab's underline, the heading tick above `h1`, the active navigation link, and the ecosystem chip. Never use an ecosystem colour for links, body text, or the logo.
- **States always have a word as well as a colour.** `--ah-house` marks a house profile's opinions and the ageing state. `--ah-stale` marks stale content and "Before" code.

## Diagrams

- **Each lane takes a lane token:** `--ah-lane-sources`, `--ah-lane-research`, `--ah-lane-opinions`, or `--ah-lane-reports`. Draw a 4px bar, and a band of the same colour at 14% on `--ah-bg`.
- **Lane colours never mark a gate or a state.** In a diagram, `--ah-brand` marks the CI gate and the outcome the agents work towards, and `--ah-house` marks the owner's gate. Ecosystem accents never appear in a diagram.
- **Set every label in `--ah-ink` or `--ah-muted`,** never in a lane colour.

## Type

- **Use IBM Plex Sans for everything read,** from the hero to small print, through `--ah-font-sans`. Headings are weight 600 with slight negative tracking. Body text is weight 400 at 16px on a 26px line. Keep running text near 70 characters wide.
- **Use IBM Plex Mono for everything machine-shaped,** through `--ah-font-mono`: code, chips, and uppercase labels.
- **Serve the fonts from `pages/assets/fonts/`.** Don't load them from a font CDN.

## Space and shape

- **Space in steps of 4px,** from `--ah-space-1` to `--ah-space-12`.
- **Keep corners tight.** Use `--ah-radius-xs` for chips, `--ah-radius-sm` for code, cards, notes, and buttons, and `--ah-radius-md` for the hero only.
- **Build structure from borders, not shadows.** Use `--ah-hairline` borders on `--ah-line`. The heading tick (`--ah-tick`) and the tab underline (`--ah-stripe`) are the only heavy rules.
- **The header bar is the one element with a shadow.** It lifts off the page with `--ah-header-shadow`, which is deeper in dark mode because a light shadow doesn't show on a near-black page. Don't add a shadow anywhere else.

## Logo and icons

- **The logo is the cited human:** a person inside square brackets, which reads as both a citation and code. Use [`pages/assets/brand/mark-cited-human.svg`](pages/assets/brand/mark-cited-human.svg) in `--ah-brand-mark`, beside the name in IBM Plex Sans 600.
- **On the header bar, reverse the mark out in `--ah-header-ink`.** Its green would disappear on the green bar of a page outside an ecosystem.
- **Use Zensical's bundled Lucide icons** (`lucide/...`) at 16px to 20px in `--ah-ink-2`, stroke style only. The mark's brackets can appear as the literal text `[ ]` in the hero kicker. Don't build other icons from them.

## Imagery

- **The site shows no photographs,** and [AGENTS.md](AGENTS.md) forbids committing a portrait. Credit people by name and link their work instead.
- **No stock imagery, illustrations, or gradients.**

## Interaction

- **Animate only colour and border changes on hover,** in 150ms or less. Nothing animates on load, and the stylesheet turns transitions off under `prefers-reduced-motion`.
- **Show focus as a solid 2px `--ah-brand-mark` outline,** offset by 2px, at a contrast of 3:1 or better on every surface in both themes. On the header bar, where the mark's green falls below 3:1, use a `--ah-header-ink` outline instead.
- **Follow the system's colour scheme, with a manual toggle.** Light mode is Zensical's `default` scheme, and dark mode is its `slate` scheme.

## Content in the interface

- **Use sentence case** for headings, buttons, and navigation. Ecosystem names keep their own casing: .NET, C#, F#, Rust, and TypeScript.
- **Set identifiers in a chip or code,** in lowercase mono: source IDs such as `andrew-lock`, targets such as `net10.0`, and skill names. Never title-case them.
- **No emoji** in content or the interface.

For everything else about prose, see [Writing style](pages/conventions/writing-style.md).
