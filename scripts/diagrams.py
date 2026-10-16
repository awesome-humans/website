"""The How it works diagrams, drawn as inline SVG for any ecosystem.

Imported by stage.py, which replaces each <!-- diagram: <name> --> line in a staged page
with the diagram's SVG. It isn't a script of its own.

A port of dotnet's scripts/export-diagrams.cs, with neutral labels: "version refresh"
for each ecosystem's refresh-*-versions skill, and placeholders for branches, never an
ecosystem's name. Each ecosystem keeps its own diagrams for its README, where its names
belong. Keep the layout here in step with that script.

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
    step = 17
    top = y - ((len(items) - 1) * step / 2) + 4
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
        single HTML block."""
        name = self.name
        marker = (
            f'<defs><marker id="{name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"'
            ' orient="auto-start-reverse"><path class="arrowhead" d="M0 0L10 5L0 10z"/></marker></defs>'
        )
        return (
            f'<svg role="img" aria-labelledby="{name}-title {name}-desc" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(width)} {n(height)}">'
            f'<title id="{name}-title">{escape(title)}</title><desc id="{name}-desc">{escape(description)}</desc>{marker}'
            f'<rect x=".5" y=".5" width="{n(width - 1)}" height="{n(height - 1)}" rx="10" class="bg"/>'
            + "".join(self.parts)
            + "</svg>"
        )


def node(x: float, y: float, width: float, height: float, title: str, subtitle: str, cls: str = "box", title_cls: str = "tb", accent: bool = False) -> str:
    """A titled box with a subtitle and an optional brand edge on its left."""
    cy = y + height / 2
    edge_bar = f'<rect x="{n(x)}" y="{n(y)}" width="4" height="{n(height)}" rx="2" class="lane"/>' if accent else ""
    return rect(x, y, width, height, 8, cls) + edge_bar + text(x + 16, cy - 3, title, title_cls) + text(x + 16, cy + 15, subtitle, "ts")


# ---- Maintenance pipeline ----

# One skill: its lane, what starts it, the skill, the branch it works on, what the owner does
# at the human gate, and where its result lands. A report-only skill has no branch and
# opens no pull request, so it passes neither gate.
PIPELINE_LANES = [("sources", "Sources"), ("research", "Research"), ("opinions", "Opinions"), ("reports", "Reports")]
PIPELINE_ROWS = [
    ("sources", ["candidate source,", "or a standing change"], "vet-source", "vet/<source-id>", "check evidence", "roster"),
    ("research", ["a question", "on a topic"], "research-topic", "research/<topic>", "review", "research"),
    ("research", ["topic saved in", "research/"], "resolve-research", "resolve/<topic>", "approve weave", "opinions"),
    ("opinions", ["monthly harvest", "reminder issue"], "harvest-sources", "harvest/<date>", "review", "opinions"),
    ("opinions", ["release-watch PR,", "or a newer pin"], "version refresh", "refresh/<version>", "review", "opinions"),
    ("opinions", ["HOUSE-OPINIONS.md", "inbox entry"], "weave-house-opinion", "house/<slug>", "confirm wording", "opinions"),
    ("reports", ["periodic cadence"], "audit-freshness", None, "", "report"),
    ("reports", ["a project path", "or repository URL"], "verify-project", None, "", "report"),
]


def pipeline() -> str:
    d = Drawing("maintenance-pipeline")
    x_band, w_band = 12, 104
    x_bracket = 126
    x_picks_up, w_picks_up = 136, 180
    x_skill, w_skill = 342, 236
    x_agent_gate, w_agent_gate = 604, 128
    x_human_gate = 774
    x_lands_in, w_lands_in = 934, 200
    width = 1148
    row_height = 64

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
        (x_agent_gate, "agent gate"),
        (x_human_gate - 17, "human gate"),
        (x_lands_in, "lands in"),
    ]:
        d.add(text(x, 24, label, "th"))

    for key, name in PIPELINE_LANES:
        rows = [i for i, row in enumerate(PIPELINE_ROWS) if row[0] == key]
        top, bottom = ys[rows[0]], ys[rows[-1]] + row_height
        lane = "lane muted" if key == "reports" else "lane"
        d.add(
            f'<rect x="{n(x_band)}" y="{n(top)}" width="{n(w_band)}" height="{n(bottom - top)}" rx="6" class="{lane} tint"/>',
            f'<rect x="{n(x_band)}" y="{n(top)}" width="4" height="{n(bottom - top)}" rx="2" class="{lane}"/>',
            text(x_band + 14, (top + bottom) / 2 + 5, name, "tb"),
        )

    for (key, picks_up, skill, branch, human_gate, _), y0 in zip(PIPELINE_ROWS, ys):
        cy = y0 + row_height / 2
        lane = "lane muted" if key == "reports" else "lane"
        d.add(
            rect(x_picks_up, y0 + 6, w_picks_up, row_height - 12, 6, "chip"),
            lines(x_picks_up + 12, cy, picks_up),
            d.arrow(x_picks_up + w_picks_up, cy, x_skill - 2, cy),
            rect(x_skill, y0 + 4, w_skill, row_height - 8, 6, "box"),
            f'<rect x="{n(x_skill)}" y="{n(y0 + 4)}" width="4" height="{n(row_height - 8)}" rx="2" class="{lane}"/>',
            text(x_skill + 14, cy - 3, skill, "tm") + text(x_skill + 14, cy + 14, branch or "report only", "ts"),
        )
        if branch is not None:
            d.add(
                d.arrow(x_skill + w_skill, cy, x_agent_gate - 2, cy),
                rect(x_agent_gate, cy - 17, w_agent_gate, 34, 17, "check"),
                text(x_agent_gate + w_agent_gate / 2, cy - 2, "CI: metadata,", "check-t", "middle"),
                text(x_agent_gate + w_agent_gate / 2, cy + 13, "sources, links", "check-t", "middle"),
                d.arrow(x_agent_gate + w_agent_gate, cy, x_human_gate - 19, cy),
                # The human gate is a diamond the height of the agent gate's capsule.
                diamond(x_human_gate, cy, 17, "gate"),
                d.arrow(x_human_gate + 17, cy, x_lands_in - 2, cy),
                text(x_human_gate + 26, cy - 8, human_gate, "gate-t"),
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
        ("opinions", "store", ["opinions/", "templates/"], "what good looks like"),
        ("report", "ext", ["a report"], "never saved here"),
    ]:
        rows = [i for i, row in enumerate(PIPELINE_ROWS) if row[5] == key]
        top, bottom = ys[rows[0]] + 4, ys[rows[-1]] + row_height - 4
        d.add(rect(x_lands_in, top, w_lands_in, bottom - top, 6, cls))
        ty = (top + bottom) / 2 - len(title_lines) * 10 + 5
        for i, line in enumerate(title_lines):
            d.add(text(x_lands_in + 14, ty + i * 20, line, "tb" if key == "report" else "tm"))
        d.add(text(x_lands_in + 14, ty + len(title_lines) * 20, subtitle, "ts"))

    # The loop: a report's findings, with the scheduled workflows and the owner, start the
    # next run in whichever row it belongs to.
    loop_y = rows_bottom + 56
    start_x, start_width = 480, 420
    d.add(
        d.path_arrow(f"M{n(x_lands_in + w_lands_in / 2)} {n(rows_bottom - 4)}V{n(loop_y)}H{n(start_x + start_width + 2)}"),
        text(x_lands_in + w_lands_in / 2 - 8, loop_y - 8, "findings", "ts", "end"),
        rect(start_x, loop_y - 32, start_width, 64, 6, "box"),
        text(start_x + 16, loop_y - 4, "What starts a run", "tb"),
        text(start_x + 16, loop_y + 16, "findings, the release watch, the harvest reminder, you", "ts"),
        f'<path d="M{n(start_x)} {n(loop_y)}H{n(x_bracket)}V{n(ys[0] + row_height / 2)}" class="edge"/>',
        text((start_x + x_bracket) / 2, loop_y - 8, "starts the next skill", "ts", "middle"),
    )
    for y0 in ys:
        d.add(d.arrow(x_bracket, y0 + row_height / 2, x_picks_up - 1, y0 + row_height / 2))

    return d.svg(
        width,
        loop_y + 48,
        "Maintenance pipeline",
        "Swimlane diagram of how an ecosystem's repository maintains itself: vet-source, research-topic, resolve-research,"
        " harvest-sources, the version refresh, and weave-house-opinion each work on their own branch, pass CI and the"
        " owner's review, and land in the roster, research/ or the opinions and templates; audit-freshness and"
        " verify-project only report. Their findings, the release watch and the harvest reminder start the next run.",
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
    candidate_x, candidate_width = 24, 212
    vet_x, vet_y, vet_half = 308, 182, 36
    spine_x = 376
    out_x, out_width = 606, 540
    loop_x, loop_y = 1270, 412

    d.add(
        node(candidate_x, vet_y - 32, candidate_width, 64, "Candidate source", "blog, docs, book, newsletter"),
        d.arrow(candidate_x + candidate_width, vet_y, vet_x - vet_half - 2, vet_y),
        diamond(vet_x, vet_y, vet_half, "decision"),
        text(vet_x, vet_y - vet_half - 12, "vet-source", "tm", "middle"),
        text(vet_x, vet_y + 4, "criteria", "ts", "middle"),
        f'<line x1="{n(vet_x + vet_half)}" y1="{n(vet_y)}" x2="{n(spine_x)}" y2="{n(vet_y)}" class="edge"/>',
    )

    # Citable, with its markings inside.
    citable_y, citable_height = 24, 196
    d.add(
        rect(out_x, citable_y, out_width, citable_height, 8, "box"),
        f'<rect x="{n(out_x)}" y="{n(citable_y)}" width="4" height="{n(citable_height)}" rx="2" class="lane"/>',
        text(out_x + 16, citable_y + 26, "Citable", "tb"),
        text(out_x + 16, citable_y + 44, "quotable in opinions and templates, within its marking", "ts"),
    )
    for i, (marking, rule) in enumerate(MARKINGS):
        y0 = citable_y + 60 + i * 44
        d.add(rect(out_x + 16, y0, out_width - 32, 36, 6, "chip"), text(out_x + 28, y0 + 23, marking, "tm"), text(out_x + 212, y0 + 23, rule, "ts"))

    watch_y, declined_y = 244, 324
    d.add(
        node(out_x, watch_y, out_width, 56, "Watch list", "leads only, never cited", cls="ext"),
        node(out_x, declined_y, out_width, 56, "Declined", "off the roster, the decision logged", cls="ext"),
    )
    for y, label in [
        (citable_y + 32, "two years and all four criteria"),
        (watch_y + 28, "under two years, or dormant"),
        (declined_y + 28, "otherwise"),
    ]:
        d.add(d.path_arrow(f"M{n(spine_x)} {n(vet_y)}V{n(y)}H{n(out_x - 2)}"), text(spine_x + 12, y - 8, label, "ts"))

    # Standing is never permanent: citable and watch-listed sources share one path back.
    d.add(
        f'<path d="M{n(out_x + out_width)} {n(citable_y + 32)}H{n(loop_x)}V{n(loop_y)}" class="edge dash"/>',
        f'<path d="M{n(out_x + out_width)} {n(watch_y + 28)}H{n(loop_x)}" class="edge dash"/>',
        d.path_arrow(f"M{n(loop_x)} {n(loop_y)}H{n(vet_x)}V{n(vet_y + vet_half + 2)}", dash=True),
        text(out_x + out_width + 10, citable_y + 24, "dormant, weaker", "ts"),
        text(out_x + out_width + 10, watch_y + 20, "blocker clears", "ts"),
        text((vet_x + loop_x) / 2, loop_y - 8, "re-vetted: standing is never permanent", "ts", "middle"),
    )

    return d.svg(
        1290,
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
    center_y = 140
    topic_x, topic_width = 24, 196
    staged_x, staged_width = 300, 210
    resolve_x, resolve_half = 600, 36
    spine_x = 680
    out_x, out_width, out_height = 720, 360, 56
    loop_y = 292

    d.add(
        node(topic_x, center_y - 32, topic_width, 64, "research-topic", "cited, on research/<topic>", title_cls="tm"),
        d.arrow(topic_x + topic_width, center_y, staged_x - 2, center_y),
        text((topic_x + topic_width + staged_x) / 2, center_y - 8, "PR merges", "ts", "middle"),
        node(staged_x, center_y - 32, staged_width, 64, "research/<topic>.md", "on record, unresolved", cls="store", title_cls="tm"),
        d.arrow(staged_x + staged_width, center_y, resolve_x - resolve_half - 2, center_y),
        diamond(resolve_x, center_y, resolve_half, "decision"),
        text(resolve_x, center_y - resolve_half - 12, "resolve-research", "tm", "middle"),
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
        d.path_arrow(f"M{n(out_x + out_width / 2)} {n(partial_bottom)}V{n(loop_y)}H{n(resolve_x)}V{n(center_y + resolve_half + 2)}", dash=True),
        text((resolve_x + out_x + out_width / 2) / 2, loop_y - 8, "once vet-source clears its source", "ts", "middle"),
    )

    return d.svg(
        1104,
        loop_y + 28,
        "Research lifecycle",
        "Flow diagram: research-topic opens a pull request that saves research/<topic>.md; resolve-research then promotes"
        " it into the opinions and templates, discards it, or promotes part of it, deleting the topic in the same pull"
        " request. A blocked remainder stays staged and goes back through resolve-research once vet-source clears the"
        " source it waits on.",
    )


DIAGRAMS = {
    "maintenance-pipeline": pipeline,
    "source-standing": standing,
    "research-lifecycle": research,
}


def figure(name: str) -> str | None:
    """The named diagram in an .ah-diagram figure, or None for a name with no diagram."""
    draw = DIAGRAMS.get(name)
    return None if draw is None else f'<figure class="ah-diagram">{draw()}</figure>'
