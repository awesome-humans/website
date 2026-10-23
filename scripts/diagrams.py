"""The How it works diagrams, drawn as inline SVG for any ecosystem.

Imported by stage.py, which replaces each <!-- diagram: <name> --> line in a staged page
with the diagram's SVG. It isn't a script of its own.

A port of dotnet's scripts/export-diagrams.cs, with neutral labels: "version refresh"
for each ecosystem's refresh-*-versions skill, and placeholders for branches, never an
ecosystem's name. Each ecosystem keeps its own diagrams for its README, where its names
belong. Keep the layout here in step with that script, with two differences: columns
here fit IBM Plex, which the site always loads, where the script leaves room for wider
fallback fonts, and the skill column fits "version refresh" rather than an ecosystem's
longer skill name.

Each diagram is data at the top of its function, rows or nodes with their labels, and
layout code below. The SVG carries classes and no colours or fonts: the .ah-diagram rules
in awesome-humans.css colour them from the theme's tokens, so the theme toggle switches
them and the text is IBM Plex.
"""

from html import escape

# ---- SVG helpers ----


def n(value: float) -> str:
    """A coordinate with at most two decimals, as the C# script's "0.##" format writes it."""
    return f"{value:.2f}".rstrip("0").rstrip(".")


def text(x: float, y: float, value: str, cls: str = "t", anchor: str = "start") -> str:
    return f'<text x="{n(x)}" y="{n(y)}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>'


def lines(x: float, y: float, items: list[str], cls: str = "t") -> str:
    """Lines of text, vertically centred on y."""
    step = 19
    top = y - ((len(items) - 1) * step / 2) + 5
    return "".join(text(x, top + i * step, item, cls) for i, item in enumerate(items))


def rect(x: float, y: float, width: float, height: float, radius: float, cls: str) -> str:
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(width)}" height="{n(height)}" rx="{n(radius)}" class="{cls}"/>'


def diamond(cx: float, cy: float, half: float, cls: str) -> str:
    return f'<path d="M{n(cx)} {n(cy - half)}L{n(cx + half)} {n(cy)}L{n(cx)} {n(cy + half)}L{n(cx - half)} {n(cy)}z" class="{cls}"/>'


def edge(dash: bool) -> str:
    return "edge dash" if dash else "edge"


class Drawing:
    """One diagram's elements. Its arrowhead marker takes the diagram's name, because the
    page holds every diagram and an id must be unique in it."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.parts: list[str] = []

    def add(self, *parts: str) -> None:
        self.parts.extend(parts)

    def arrow(self, x1: float, y1: float, x2: float, y2: float, dash: bool = False) -> str:
        return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" class="{edge(dash)}" marker-end="url(#{self.name}-arrow)"/>'

    def path_arrow(self, d: str, dash: bool = False) -> str:
        return f'<path d="{d}" class="{edge(dash)}" marker-end="url(#{self.name}-arrow)"/>'

    def svg(self, width: float, height: float, title: str, description: str) -> str:
        """The drawing as one line of accessible SVG, so Markdown passes it through as a
        single HTML block. It grows to its own width and no further, so every diagram's
        text renders at one size, and shrinks on a narrower page."""
        name = self.name
        marker = (
            f'<defs><marker id="{name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"'
            ' orient="auto-start-reverse"><path class="arrowhead" d="M0 0L10 5L0 10z"/></marker></defs>'
        )
        return (
            f'<svg role="img" aria-labelledby="{name}-title {name}-desc" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(width)} {n(height)}" style="max-width: {n(width)}px">'
            f'<title id="{name}-title">{escape(title)}</title><desc id="{name}-desc">{escape(description)}</desc>{marker}'
            f'<rect x=".5" y=".5" width="{n(width - 1)}" height="{n(height - 1)}" rx="10" class="bg"/>'
            + "".join(self.parts)
            + "</svg>"
        )


def node(
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    subtitle: str,
    cls: str = "box",
    title_cls: str = "tb",
    accent: bool = False,
) -> str:
    """A titled box with a subtitle and an optional brand edge on its left."""
    cy = y + height / 2
    edge_bar = f'<rect x="{n(x)}" y="{n(y)}" width="4" height="{n(height)}" rx="2" class="accent"/>' if accent else ""
    return (
        rect(x, y, width, height, 8, cls)
        + edge_bar
        + text(x + 16, cy - 4, title, title_cls)
        + text(x + 16, cy + 17, subtitle, "ts")
    )


# ---- Maintenance pipeline ----

# One skill: its lane, what starts it, the skill, the branch it works on, what the owner does
# at the human gate, and where its result lands. A report-only skill has no branch and
# opens no pull request, so it passes neither gate.
PIPELINE_LANES = [("sources", "Sources"), ("research", "Research"), ("opinions", "Opinions"), ("reports", "Reports")]
PIPELINE_ROWS = [
    (
        "sources",
        ["candidate source,", "or a change in standing"],
        "vet-source",
        "vet/<source-id>",
        "check evidence",
        "roster",
    ),
    ("research", ["a question", "about <topic>"], "research-topic", "research/<topic>", "review", "research"),
    ("research", ["topic saved in", "research/"], "resolve-research", "resolve/<topic>", "approve weave", "opinions"),
    ("opinions", ["monthly harvest", "reminder issue"], "harvest-sources", "harvest/<date>", "review", "opinions"),
    ("opinions", ["release-watch PR,", "or a newer pin"], "version refresh", "refresh/<version>", "review", "opinions"),
    (
        "opinions",
        ["HOUSE-OPINIONS.md", "inbox entry"],
        "weave-house-opinion",
        "house/<slug>",
        "confirm wording",
        "opinions",
    ),
    ("reports", ["periodic cadence"], "audit-freshness", None, "", "report"),
    ("reports", ["a project path", "or repository URL"], "review-project", None, "", "report"),
]


def pipeline() -> str:
    d = Drawing("maintenance-pipeline")
    x_band, w_band = 12, 96
    x_bracket = 118
    x_picks_up, w_picks_up = 128, 192
    x_skill, w_skill = 344, 204
    x_agent_gate, w_agent_gate = 572, 116
    gate_half = 20
    x_human_gate = 732
    x_lands_in, w_lands_in = 878, 184
    width = 1074
    row_height = 66

    # Rows stack with a gap between lanes.
    ys: list[float] = []
    y, previous = 44.0, None
    for row in PIPELINE_ROWS:
        if previous is not None and row[0] != previous:
            y += 18
        ys.append(y)
        y += row_height + 8
        previous = row[0]
    rows_bottom = ys[-1] + row_height

    for x, label in [
        (x_band, "lane"),
        (x_picks_up, "picks up"),
        (x_skill, "skill"),
        (x_agent_gate, "agent checks"),
        (x_human_gate - gate_half, "human gate"),
        (x_lands_in, "lands in"),
    ]:
        d.add(text(x, 24, label, "th"))

    for key, name in PIPELINE_LANES:
        rows = [i for i, row in enumerate(PIPELINE_ROWS) if row[0] == key]
        top, bottom = ys[rows[0]], ys[rows[-1]] + row_height
        d.add(
            f'<rect x="{n(x_band)}" y="{n(top)}" width="{n(w_band)}" height="{n(bottom - top)}" rx="6" class="lane {key} tint"/>',
            f'<rect x="{n(x_band)}" y="{n(top)}" width="4" height="{n(bottom - top)}" rx="2" class="lane {key}"/>',
            text(x_band + 14, (top + bottom) / 2 + 6, name, "tb"),
        )

    for (key, picks_up, skill, branch, human_gate, _), y0 in zip(PIPELINE_ROWS, ys):
        cy = y0 + row_height / 2
        d.add(
            rect(x_picks_up, y0 + 6, w_picks_up, row_height - 12, 6, "chip"),
            lines(x_picks_up + 12, cy, picks_up),
            d.arrow(x_picks_up + w_picks_up, cy, x_skill - 2, cy),
            rect(x_skill, y0 + 4, w_skill, row_height - 8, 6, "box"),
            f'<rect x="{n(x_skill)}" y="{n(y0 + 4)}" width="4" height="{n(row_height - 8)}" rx="2" class="lane {key}"/>',
            text(x_skill + 14, cy - 4, skill, "tm") + text(x_skill + 14, cy + 16, branch or "report only", "ts"),
        )
        if branch is not None:
            d.add(
                d.arrow(x_skill + w_skill, cy, x_agent_gate - 2, cy),
                rect(x_agent_gate, cy - gate_half, w_agent_gate, gate_half * 2, 6, "check"),
                text(x_agent_gate + w_agent_gate / 2, cy - 3, "CI checks,", "check-t", "middle"),
                text(x_agent_gate + w_agent_gate / 2, cy + 13, "agent review", "check-t", "middle"),
                d.arrow(x_agent_gate + w_agent_gate, cy, x_human_gate - gate_half - 2, cy),
                # The human gate is a diamond the height of the agent checks' box.
                diamond(x_human_gate, cy, gate_half, "gate"),
                d.arrow(x_human_gate + gate_half, cy, x_lands_in - 2, cy),
                text(x_human_gate + gate_half + 8, cy - 9, human_gate, "gate-t"),
            )
        else:
            d.add(
                d.arrow(x_skill + w_skill, cy, x_lands_in - 2, cy, dash=True),
                text((x_agent_gate + x_lands_in) / 2, cy - 8, "no pull request", "ts", "middle"),
            )

    # Each destination is one store spanning the rows that land in it.
    for key, cls, title_lines, subtitle in [
        ("roster", "store", ["AWESOME-HUMANS.md"], "the roster"),
        ("research", "store", ["research/"], "staged, unresolved"),
        ("opinions", "store", ["opinions/", "templates/"], "distilled guidance"),
        ("report", "ext", ["a report"], "never saved here"),
    ]:
        rows = [i for i, row in enumerate(PIPELINE_ROWS) if row[5] == key]
        top, bottom = ys[rows[0]] + 4, ys[rows[-1]] + row_height - 4
        d.add(rect(x_lands_in, top, w_lands_in, bottom - top, 6, cls))
        ty = (top + bottom) / 2 - len(title_lines) * 11 + 5
        for i, line in enumerate(title_lines):
            d.add(text(x_lands_in + 14, ty + i * 22, line, "tb" if key == "report" else "tm"))
        d.add(text(x_lands_in + 14, ty + len(title_lines) * 22, subtitle, "ts"))

    # The loop: a report's findings, with the scheduled workflows and the owner, start the
    # next run in whichever row it belongs to.
    loop_y = rows_bottom + 56
    start_x, start_width = 440, 372
    d.add(
        d.path_arrow(
            f"M{n(x_lands_in + w_lands_in / 2)} {n(rows_bottom - 4)}V{n(loop_y)}H{n(start_x + start_width + 2)}"
        ),
        text(x_lands_in + w_lands_in / 2 - 8, loop_y - 8, "findings", "ts", "end"),
        rect(start_x, loop_y - 34, start_width, 68, 6, "box"),
        text(start_x + 16, loop_y - 5, "What starts a run", "tb"),
        text(start_x + 16, loop_y + 17, "findings, the release watch, the harvest reminder, you", "ts"),
        f'<path d="M{n(start_x)} {n(loop_y)}H{n(x_bracket)}V{n(ys[0] + row_height / 2)}" class="edge"/>',
        text((start_x + x_bracket) / 2, loop_y - 8, "starts the next skill", "ts", "middle"),
    )
    for y0 in ys:
        d.add(d.arrow(x_bracket, y0 + row_height / 2, x_picks_up - 1, y0 + row_height / 2))

    return d.svg(
        width,
        loop_y + 50,
        "Maintenance pipeline",
        "Swimlane diagram of how an ecosystem's repository maintains itself: vet-source, research-topic, resolve-research,"
        " harvest-sources, the version refresh, and weave-house-opinion each work on their own branch, pass the CI"
        " checks, get an agent review, pass the owner's review, and land in the roster, research, or the opinions and"
        " templates; audit-freshness and review-project only report. Their findings, the release watch, and the harvest reminder start the next run.",
    )


# ---- Source standing ----

# Each marking a citable source can carry, and what it lets a citation rest on.
MARKINGS = [
    ("unmarked", "may carry a claim alone"),
    ("**Corroborate.**", "cited, never as the only source on a claim"),
    ("**Discovery-only.**", "never cited, only followed to its primary source"),
]


def standing() -> str:
    d = Drawing("source-standing")
    # The candidate sits above vet-source, and each marking's rule sits under it, so the
    # diagram is narrow enough for its text to render at the pipeline's size.
    candidate_x, candidate_y, candidate_width = 20, 20, 212
    vet_x, vet_y, vet_half = 126, 196, 38
    spine_x = 256
    out_x, out_width = 462, 372
    loop_x = 966

    d.add(
        node(candidate_x, candidate_y, candidate_width, 64, "Candidate source", "blog, docs, book, newsletter"),
        d.arrow(vet_x, candidate_y + 64, vet_x, vet_y - vet_half - 2),
        diamond(vet_x, vet_y, vet_half, "decision"),
        text(vet_x + 12, candidate_y + 64 + 40, "vet-source", "tm"),
        text(vet_x, vet_y + 4, "criteria", "ts", "middle"),
        f'<line x1="{n(vet_x + vet_half)}" y1="{n(vet_y)}" x2="{n(spine_x)}" y2="{n(vet_y)}" class="edge"/>',
    )

    # Citable, with its markings inside.
    citable_y, chip_height = 20, 52
    citable_height = 64 + len(MARKINGS) * (chip_height + 8) + 8
    d.add(
        rect(out_x, citable_y, out_width, citable_height, 8, "box"),
        f'<rect x="{n(out_x)}" y="{n(citable_y)}" width="4" height="{n(citable_height)}" rx="2" class="accent"/>',
        text(out_x + 16, citable_y + 27, "Citable", "tb"),
        text(out_x + 16, citable_y + 48, "quotable in opinions and templates, within its marking", "ts"),
    )
    for i, (marking, rule) in enumerate(MARKINGS):
        y0 = citable_y + 64 + i * (chip_height + 8)
        d.add(
            rect(out_x + 16, y0, out_width - 32, chip_height, 6, "chip"),
            text(out_x + 28, y0 + 22, marking, "tm"),
            text(out_x + 28, y0 + 42, rule, "ts"),
        )

    watch_y = citable_y + citable_height + 24
    declined_y = watch_y + 84
    loop_y = declined_y + 60 + 36
    d.add(
        node(out_x, watch_y, out_width, 60, "Watch list", "leads only, never cited", cls="ext"),
        node(out_x, declined_y, out_width, 60, "Declined", "off the roster, the decision logged", cls="ext"),
    )
    for y, label in [
        (citable_y + 32, "two years and all four criteria"),
        (watch_y + 30, "under two years, or dormant"),
        (declined_y + 30, "otherwise"),
    ]:
        d.add(d.path_arrow(f"M{n(spine_x)} {n(vet_y)}V{n(y)}H{n(out_x - 2)}"), text(spine_x + 12, y - 8, label, "ts"))

    # Standing is never permanent: citable and watch-listed sources share one path back.
    d.add(
        f'<path d="M{n(out_x + out_width)} {n(citable_y + 32)}H{n(loop_x)}V{n(loop_y)}" class="edge dash"/>',
        f'<path d="M{n(out_x + out_width)} {n(watch_y + 30)}H{n(loop_x)}" class="edge dash"/>',
        d.path_arrow(f"M{n(loop_x)} {n(loop_y)}H{n(vet_x)}V{n(vet_y + vet_half + 2)}", dash=True),
        text(out_x + out_width + 10, citable_y + 24, "dormant, weaker", "ts"),
        text(out_x + out_width + 10, watch_y + 22, "blocker clears", "ts"),
        text((vet_x + loop_x) / 2, loop_y - 8, "re-vetted: standing is never permanent", "ts", "middle"),
    )

    return d.svg(
        loop_x + 20,
        loop_y + 28,
        "Source standing",
        "Flow diagram: vet-source sorts a candidate source into citable, with two years of writing and all four criteria;"
        " the watch list, under two years or dormant; or declined. A citable source is unmarked, marked Corroborate and"
        " never the only citation on a claim, or marked Discovery-only and never cited. Citable and watch-listed sources"
        " go back through vet-source when they go dormant, drop in quality, or clear a blocker.",
    )


# ---- Research lifecycle ----

OUTCOMES = [
    ("Promote", "opinions and templates updated, topic deleted"),
    ("Discard", "nothing woven, topic deleted"),
    ("Partial promotion", "the rest woven, the blocked remainder stays staged"),
]


def research() -> str:
    d = Drawing("research-lifecycle")
    # research-topic sits above the topic it saves, so the diagram is narrow enough for its
    # text to render at the pipeline's size.
    center_y = 182
    topic_x, topic_y, topic_width = 20, 20, 212
    resolve_x, resolve_half = 320, 38
    spine_x = 404
    out_x, out_width, out_height = 428, 356, 60
    loop_y = 328

    d.add(
        node(topic_x, topic_y, topic_width, 64, "research-topic", "cited, on research/<topic>", title_cls="tm"),
        d.arrow(topic_x + topic_width / 2, topic_y + 64, topic_x + topic_width / 2, center_y - 34),
        text(topic_x + topic_width / 2 + 12, center_y - 60, "PR merges", "ts"),
        node(
            topic_x,
            center_y - 32,
            topic_width,
            64,
            "research/<topic>.md",
            "on record, unresolved",
            cls="store",
            title_cls="tm",
        ),
        d.arrow(topic_x + topic_width, center_y, resolve_x - resolve_half - 2, center_y),
        diamond(resolve_x, center_y, resolve_half, "decision"),
        text(resolve_x, center_y - resolve_half - 14, "resolve-research", "tm", "middle"),
        text(resolve_x, center_y + 4, "own PR", "ts", "middle"),
        f'<line x1="{n(resolve_x + resolve_half)}" y1="{n(center_y)}" x2="{n(spine_x)}" y2="{n(center_y)}" class="edge"/>',
    )
    for i, (name, detail) in enumerate(OUTCOMES):
        y0 = center_y - out_height - 16 - out_height / 2 + i * (out_height + 16)
        cy = y0 + out_height / 2
        d.add(
            d.path_arrow(f"M{n(spine_x)} {n(center_y)}V{n(cy)}H{n(out_x - 2)}"),
            node(out_x, y0, out_width, out_height, name, detail, cls="box" if i == 0 else "ext", accent=i == 0),
        )

    # The remainder waits for vet-source, then goes round again.
    partial_bottom = center_y + out_height + 16 + out_height / 2
    d.add(
        d.path_arrow(
            f"M{n(out_x + out_width / 2)} {n(partial_bottom)}V{n(loop_y)}H{n(resolve_x)}V{n(center_y + resolve_half + 2)}",
            dash=True,
        ),
        text((resolve_x + out_x + out_width / 2) / 2, loop_y - 8, "once vet-source clears its source", "ts", "middle"),
    )

    return d.svg(
        out_x + out_width + 20,
        loop_y + 28,
        "Research lifecycle",
        "Flow diagram: research-topic opens a pull request that saves research/<topic>.md; resolve-research then promotes"
        " it into the opinions and templates, discards it, or promotes part of it, deleting the topic in the same pull"
        " request. A blocked remainder stays staged and goes back through resolve-research once vet-source clears the"
        " source it waits on.",
    )


# ---- Repositories ----

# What passes between the ecosystems and website: its direction, and its label. Each
# arrow runs between the ecosystems' column and website's left edge.
LINKS = [
    ("to-site", "dispatch when main changes"),
    ("to-ecosystem", "checks out main, runs stage"),
    ("to-site", "pull request: preview build"),
    ("to-ecosystem", "suggestions, as vet-source issues"),
]


def repositories() -> str:
    d = Drawing("repositories")
    # The site's own diagram, with no counterpart in an ecosystem's README: an ecosystem
    # never draws the repositories around it.
    top, height = 44, 220
    eco_x, eco_width = 20, 256
    site_x, site_width = 540, 250
    out_x, out_width = 930, 210
    shared_y = 340

    d.add(
        text(eco_x, 24, "content", "th"),
        text(site_x, 24, "publishing", "th"),
        text(out_x, 24, "the site", "th"),
        rect(eco_x, top, eco_width, height, 8, "chip"),
        node(
            eco_x + 16,
            top + 16,
            eco_width - 32,
            64,
            "awesome-humans/dotnet",
            "opinions, skills, the roster",
            title_cls="tm",
        ),
        node(
            eco_x + 16,
            top + 92,
            eco_width - 32,
            64,
            "awesome-humans/rust",
            "opinions, skills, the roster",
            title_cls="tm",
        ),
        lines(eco_x + 16, top + 192, ["one for each ecosystem", "in ecosystems.toml"], "ts"),
        rect(site_x, top, site_width, height, 8, "box"),
        f'<rect x="{n(site_x)}" y="{n(top)}" width="4" height="{n(height)}" rx="2" class="accent"/>',
        text(site_x + 16, top + 30, "awesome-humans/website", "tm"),
        lines(
            site_x + 16,
            top + 120,
            [
                "stages every ecosystem,",
                "then builds the site:",
                "theme, shared pages,",
                "source images, intake",
                "",
                "rebuilds weekly too",
            ],
            "ts",
        ),
    )
    for i, (direction, label) in enumerate(LINKS):
        y = top + 36 + i * 52
        if direction == "to-site":
            d.add(d.arrow(eco_x + eco_width, y, site_x - 2, y))
        else:
            d.add(d.arrow(site_x, y, eco_x + eco_width + 2, y))
        d.add(text((eco_x + eco_width + site_x) / 2, y - 8, label, "ts", "middle"))

    # The site and its readers, who reach back through the issue forms.
    readers_y = top + 140
    d.add(
        node(out_x, top, out_width, 80, "awesome-humans.net", "and a preview per PR", accent=True),
        d.arrow(site_x + site_width, top + 40, out_x - 2, top + 40),
        text((site_x + site_width + out_x) / 2, top + 32, "deploys", "ts", "middle"),
        node(out_x, readers_y, out_width, 80, "Readers", "developers and agents", cls="ext"),
        d.arrow(out_x + out_width / 2, top + 80, out_x + out_width / 2, readers_y - 2),
        text(out_x + out_width / 2 + 12, top + 116, "reads", "ts"),
        d.arrow(out_x, readers_y + 40, site_x + site_width + 2, readers_y + 40),
        text((site_x + site_width + out_x) / 2, readers_y + 32, "issue forms", "ts", "middle"),
        text((site_x + site_width + out_x) / 2, readers_y + 60, "suggest, opt out", "ts", "middle"),
    )

    # The shared repositories serve every repository's pull requests.
    bracket_y = 300
    github_x, github_width = 20, 380
    coderabbit_x, coderabbit_width = 420, 370
    eco_mid, site_mid = eco_x + eco_width / 2, site_x + site_width / 2
    d.add(
        node(
            github_x,
            shared_y,
            github_width,
            64,
            "awesome-humans/.github",
            "attribution check, profile, PR template",
            title_cls="tm",
        ),
        node(
            coderabbit_x,
            shared_y,
            coderabbit_width,
            64,
            "awesome-humans/coderabbit",
            "one review configuration for all",
            title_cls="tm",
        ),
        f'<path d="M{n(github_x + github_width / 2)} {n(shared_y)}V{n(bracket_y)}" class="edge"/>',
        f'<path d="M{n(coderabbit_x + coderabbit_width / 2)} {n(shared_y)}V{n(bracket_y)}" class="edge"/>',
        f'<path d="M{n(eco_mid)} {n(bracket_y)}H{n(site_mid)}" class="edge"/>',
        d.arrow(eco_mid, bracket_y, eco_mid, top + height + 2),
        d.arrow(site_mid, bracket_y, site_mid, top + height + 2),
        text((eco_mid + site_mid) / 2, bracket_y + 22, "every repository's pull requests", "ts", "middle"),
    )

    return d.svg(
        out_x + out_width + 20,
        shared_y + 84,
        "Repositories",
        "Block diagram of the awesome-humans repositories. Each ecosystem, such as dotnet and rust, holds its own opinions,"
        " skills and roster. When its main changes, it dispatches to website, which checks out every ecosystem at main,"
        " runs its stage command, builds the site and deploys awesome-humans.net. An ecosystem's pull request builds a"
        " preview through website's build. Readers' suggestions arrive through website's issue forms and move to the"
        " ecosystem as vet-source issues. The .github repository supplies the attribution check and coderabbit the review"
        " configuration for every repository's pull requests.",
    )


DIAGRAMS = {
    "repositories": repositories,
    "maintenance-pipeline": pipeline,
    "source-standing": standing,
    "research-lifecycle": research,
}


def figure(name: str) -> str | None:
    """The named diagram in an .ah-diagram figure, or None for a name with no diagram."""
    draw = DIAGRAMS.get(name)
    return None if draw is None else f'<figure class="ah-diagram">{draw()}</figure>'
