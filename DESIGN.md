# Design

These rules set how awesome-humans.net looks. They're canonical for the look: follow them when you change the theme, a template override, or a shared page. [`pages/stylesheets/awesome-humans.css`](pages/stylesheets/awesome-humans.css) holds every value as an `--ah-*` custom property, so this file names tokens and never repeats a value. To change a value, change it in the stylesheet. To change a rule, change it here in the same pull request.

The brand is crisp and technical: a reference you trust because every claim is cited.

## Colour

- **Neutrals carry the page.** Set `--ah-ink` on `--ah-bg`. Use `--ah-surface` for the metadata strip and the hero, `--ah-code` for code blocks, and `--ah-line` for hairline borders. A border that carries a meaning takes that meaning's colour: a state chip its state, a house note `--ah-house`, and a preview note `--ah-muted`.
- **Green is the one brand hue.** `--ah-brand` is for links, the fresh state, and the hero kicker. A button is `--ah-ink` on `--ah-bg` inside a hairline, and turns `--ah-brand` on hover: no button has a brand fill. Text on a brand fill, where the theme draws one, is `--ah-on-brand`. `--ah-brand-mark` is for the logo, the focus ring, and large graphics only.
- **Each section has one accent.** An ecosystem's section takes its own token, such as `--ah-dotnet`, and every other page takes `--ah-brand`. `pages/javascripts/ecosystem.js` sets it from the URL, as `--ah-eco`.
- **The accent fills the header bar and tints the page.** The bar is `--ah-header-bg` with `--ah-header-ink` on it: the accent itself in light mode, and the accent mixed into `--ah-bg` in dark mode. The accent also tints `--ah-bg`, `--ah-surface`, and `--ah-raised`, faintly in light mode and fainter still in dark mode. Code blocks keep the plain `--ah-code`, because the syntax colours are set against it.
- **Otherwise the accent appears in five places only:** the active tab's underline, the page title with the tick under it, the active navigation link, the ecosystem chip, and an ecosystem card's top rule and hover border. Never use an ecosystem colour for links, body text, or the logo.
- **States always have a word as well as a colour.** `--ah-house` marks a house profile's opinions and the ageing state. `--ah-stale` marks stale content and "Before" code. Each has a `-tint` token, such as `--ah-house-tint`, for the background behind it.

## Diagrams

- **Each lane takes a lane token:** `--ah-lane-sources`, `--ah-lane-research`, `--ah-lane-opinions`, or `--ah-lane-reports`. Draw a solid bar in the lane's colour, and a band of the same colour mixed faintly into `--ah-bg`.
- **Lane colours never mark a gate or a state.** In a diagram, `--ah-brand` marks the CI gate and the outcome the agents work towards, and `--ah-house` marks the owner's gate. Ecosystem accents never appear in a diagram.
- **Never set a label in a lane colour.** Labels are `--ah-ink` or `--ah-muted`, and a subtitle takes `--ah-ink-2` in light mode, where muted reads too faint. A gate's label takes its gate's colour: `--ah-house` or `--ah-brand`.

## Type

- **Use IBM Plex Sans for everything read,** from the hero to small print, through `--ah-font-sans`. Headings are weight 600 with slight negative tracking. Body text is weight 400. The content column runs wide on a large screen so the widest diagram fits, so cap the measure where prose stands alone: the hero's text, and prose beside a diagram.
- **Use IBM Plex Mono for everything machine-shaped,** through `--ah-font-mono`: code, chips, and uppercase labels.
- **Serve the fonts from `pages/assets/fonts/`.** Don't load them from a font CDN.

## Space and shape

- **Space on the one scale,** from `--ah-space-1` to `--ah-space-12`, in even steps.
- **Keep corners tight.** Use `--ah-radius-xs` for chips, `--ah-radius-sm` for code, cards, notes, and buttons, and `--ah-radius-md` for the hero only.
- **Build structure from borders, not shadows.** Use `--ah-hairline` borders on `--ah-line`. Only two heavier rules exist. `--ah-tick` draws the tick under the page title, a card's top rule, and the left edge of a house or preview note. `--ah-stripe` draws the tab underline and the focus ring.
- **The header bar is the one element with a shadow.** It lifts off the page with `--ah-header-shadow`, which is deeper in dark mode because a light shadow doesn't show on a near-black page. Nothing else casts a shadow. The search button's key hint draws its hairline with an inset `box-shadow`, which is a border, not a shadow.

## Logo and icons

- **The logo is the cited human:** a person inside square brackets, which reads as both a citation and code. Use [`pages/assets/brand/mark-cited-human.svg`](pages/assets/brand/mark-cited-human.svg) in `--ah-brand-mark`, beside the name in IBM Plex Sans 600.
- **On the header bar, reverse the mark out in white,** in both themes. Its green would disappear on the green bar of a page outside an ecosystem.
- **Use Zensical's bundled Lucide icons** (`lucide/...`) at 16px to 20px in `--ah-ink-2`, stroke style only. The header's repository link is the one exception: it keeps Zensical's default Git icon unless `zensical.toml` sets another. The mark's brackets can appear as the literal text `[ ]` in the hero kicker. Don't build other icons from them.

## Imagery

- **The site shows no photographs,** and [AGENTS.md](AGENTS.md) forbids committing a portrait. Credit people by name and link their work instead.
- **No stock imagery, illustrations, or gradients.** The only images are the mark and each ecosystem's own logo, from [`pages/assets/ecosystems/`](pages/assets/ecosystems).
- **Show an ecosystem's logo as its owner supplies it,** on its card and under its section's title. Never draw it smaller than the stylesheet's `.ah-eco-logo` size, and swap to its `-dark` copy in dark mode when it has one.

## Interaction

- **Animate only colour and border changes on hover,** and keep the transition short. Nothing animates on load, and the stylesheet turns transitions off under `prefers-reduced-motion`.
- **Show focus as a solid `--ah-brand-mark` outline,** as thick as `--ah-stripe` and set slightly off the element, at a contrast of 3:1 or better on every surface in both themes. On the header bar, where the mark's green falls below 3:1, every control takes a `--ah-header-ink` outline instead, the house picker included.
- **Follow the system's colour scheme, with a manual toggle.** Light mode is Zensical's `default` scheme, and dark mode is its `slate` scheme.

## Content in the interface

- **Use sentence case** for headings, buttons, and navigation. Ecosystem names keep their own casing: .NET, C#, F#, Rust, and TypeScript.
- **Set identifiers in a chip or code,** in lowercase mono: source IDs such as `andrew-lock`, targets such as `net10.0`, and skill names. Never title-case them.
- **No emoji** in content or the interface.

For everything else about prose, see [Writing style](pages/conventions/writing-style.md).
