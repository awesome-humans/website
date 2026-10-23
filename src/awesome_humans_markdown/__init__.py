"""Markdown extensions for the awesome-humans.net site.

list_indent reads list nesting the way Prettier writes it and GitHub renders it: a
list item's content lines up under the text after its marker, two columns deep for
"- " and three for "1. ". Python-Markdown nests only in steps of tab_length, which is
4, so without this a fenced code block, a paragraph, or a nested list under a list item
drops out of the item on the site, and an ordered list nested three columns deep splits
its parent list in two. Before parsing, the extension re-indents each list to 4 columns
per level, and keeps any indentation past an item's content column.

date_cells marks a table cell that holds only an ISO 8601 date with the ah-date class,
which the theme keeps on one line. A browser otherwise breaks a date at its hyphens in
a narrow column, as in a roster's decision log or the Woven table of house opinions.
It also marks a cell that holds only an id in code, such as a house profile, with the
ah-id class, which the theme keeps on one line for the same reason.

path_breaks lets a path in a table cell's link text, such as
templates/projects/Example.Library.Tests.csproj in the Woven table, break after each
slash. Without it, the path can't break at all, and its column takes the width.

house_blocks ties each house block, which an ecosystem writes as "/// house | <profile>",
to its profile. It sets data-house to the profile, which javascripts/house.js shows only
to a reader who chooses it, and titles the block with the profile's name from houses.toml.
Every element with data-house, such as a profile's chip in an opinion's metadata strip,
also gets data-search-exclude, so a search never lands on a house opinion the reader
can't see.

title_text unwraps the link that the toc extension's anchorlink puts around each page
title. A section heading links to itself, as in "On this page", but the title isn't in
that list, and a link to the top of the page adds nothing. The h1 keeps its id, which
the theme's toc template looks for to leave the title out.
"""

import re
import tomllib
import xml.etree.ElementTree as etree
from pathlib import Path

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import HTML_PLACEHOLDER_RE

TAB_LENGTH = 4
MARKER = re.compile(r"( *)([-*+]|\d{1,9}[.)])( {1,4}|$)(.*)")
FENCE = re.compile(r" *(`{3,}|~{3,})")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
ID = re.compile(r"[\w.-]+")
PATH = re.compile(r"\S+/\S+")

# The house profile registry. The site builds from the repository root.
HOUSES = Path("houses.toml")


class ListIndentPreprocessor(Preprocessor):
    """Re-indent list content from marker-aligned columns to TAB_LENGTH steps."""

    def run(self, lines: list[str]) -> list[str]:
        out: list[str] = []
        # The content column of each open list item, outermost first.
        items: list[int] = []
        # An open fence: its marker, the content column it's measured from, and the
        # column that maps to.
        fence: tuple[str, int, int] | None = None
        previous_blank = True

        for line in lines:
            stripped = line.lstrip(" ")
            indent = len(line) - len(stripped)

            if fence:
                marker, source, target = fence
                text = line[min(indent, source) :] if stripped else ""
                out.append(" " * target + text if stripped else "")
                if re.fullmatch(re.escape(marker[0]) + f"{{{len(marker)},}} *", stripped):
                    fence = None
                previous_blank = False
                continue

            if not stripped:
                out.append("")
                previous_blank = True
                continue

            marker = MARKER.fullmatch(line)
            # A line indented less than an item's content column closes the item,
            # unless it continues a paragraph without a blank line (a lazy line).
            if previous_blank or marker:
                while items and indent < items[-1]:
                    items.pop()

            base = items[-1] if items else 0
            target = TAB_LENGTH * len(items) + max(0, indent - base)

            if marker:
                _, bullet, gap, rest = marker.groups()
                width = len(bullet) + max(1, len(gap))
                out.append(" " * target + bullet + " " + rest if rest else " " * target + bullet)
                items.append(indent + width)
                previous_blank = False
                continue

            if items:
                out.append(" " * target + stripped)
            else:
                out.append(line)

            opening = FENCE.match(line)
            if opening:
                fence = (opening.group(1), base, TAB_LENGTH * len(items))
            previous_blank = False

        return out


class DateCellTreeprocessor(Treeprocessor):
    """Add the ah-date class to each table cell whose whole text is an ISO 8601 date, and
    the ah-id class to each that holds only an id in code."""

    def run(self, root: etree.Element) -> None:
        for cell in root.iter("td"):
            if len(cell) == 0 and DATE.fullmatch((cell.text or "").strip()):
                cell.set("class", "ah-date")
            elif (
                len(cell) == 1
                and not (cell.text or "").strip()
                and not (cell[0].tail or "").strip()
                and cell[0].tag == "code"
                and ID.fullmatch(self.code_text(cell[0]))
            ):
                cell.set("class", "ah-id")

    def code_text(self, code: etree.Element) -> str:
        """The text of inline code, which inlinehilite leaves in the HTML stash until after
        the tree is built."""
        text = code.text or ""
        placeholder = HTML_PLACEHOLDER_RE.fullmatch(text)
        if placeholder is None:
            return text
        stashed = self.md.htmlStash.rawHtmlBlocks[int(placeholder.group(1))]
        return stashed if isinstance(stashed, str) else ""


class PathBreakTreeprocessor(Treeprocessor):
    """Add a <wbr> after each slash in a table cell's link text that is a path."""

    def run(self, root: etree.Element) -> None:
        for cell in root.iter("td"):
            for link in cell.iter("a"):
                text = link.text or ""
                if len(link) == 0 and PATH.fullmatch(text):
                    first, *rest = text.split("/")
                    link.text = f"{first}/"
                    for index, part in enumerate(rest):
                        wbr = etree.SubElement(link, "wbr")
                        wbr.tail = part if index == len(rest) - 1 else f"{part}/"


class HouseTreeprocessor(Treeprocessor):
    """Set data-house on each house block, title it, and keep house content out of search."""

    def __init__(self, md: Markdown, names: dict[str, str]) -> None:
        super().__init__(md)
        self.names = names

    def run(self, root: etree.Element) -> None:
        for element in root.iter():
            classes = element.get("class", "").split()
            if element.tag == "div" and "admonition" in classes and "house" in classes:
                title = next((child for child in element if "admonition-title" in child.get("class", "")), None)
                if title is not None and len(title) == 0:
                    profile = (title.text or "").strip()
                    element.set("data-house", profile)
                    title.text = f"House opinion · {self.names.get(profile, profile)}"
            if element.get("data-house") is not None:
                element.set("data-search-exclude", "")


def house_names() -> dict[str, str]:
    """Each house profile's display name, by id. A build without houses.toml titles a block by its id."""
    try:
        with HOUSES.open("rb") as file:
            return {house["id"]: house["name"] for house in tomllib.load(file).get("house", [])}
    except FileNotFoundError:
        return {}


class TitleTextTreeprocessor(Treeprocessor):
    """Replace the anchorlink in each h1 with its contents."""

    def run(self, root: etree.Element) -> None:
        for heading in root.iter("h1"):
            if len(heading) == 1 and "toclink" in heading[0].get("class", "").split():
                link = heading[0]
                heading.remove(link)
                heading.text = link.text
                heading.extend(link)


class ListIndentExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        # After normalize_whitespace (30), which expands tabs, and before
        # superfences' fenced_code_block (25), which reads fences by indentation.
        md.preprocessors.register(ListIndentPreprocessor(md), "list_indent", 28)
        # Tables are built by the block parser, so any priority after it works.
        md.treeprocessors.register(DateCellTreeprocessor(md), "date_cells", 5)
        md.treeprocessors.register(PathBreakTreeprocessor(md), "path_breaks", 5)
        # After attr_list (8), which sets data-house on a chip.
        md.treeprocessors.register(HouseTreeprocessor(md, house_names()), "house_blocks", 6)
        # After toc (5), which wraps each heading's contents in its anchorlink.
        md.treeprocessors.register(TitleTextTreeprocessor(md), "title_text", 4)


def makeExtension(**kwargs) -> ListIndentExtension:
    return ListIndentExtension(**kwargs)
