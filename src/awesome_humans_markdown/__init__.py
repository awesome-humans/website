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

title_text unwraps the link that the toc extension's anchorlink puts around each page
title. A section heading links to itself, as in "On this page", but the title isn't in
that list, and a link to the top of the page adds nothing. The h1 keeps its id, which
the theme's toc template looks for to leave the title out.
"""

import re
import xml.etree.ElementTree as etree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor

TAB_LENGTH = 4
MARKER = re.compile(r"( *)([-*+]|\d{1,9}[.)])( {1,4}|$)(.*)")
FENCE = re.compile(r" *(`{3,}|~{3,})")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


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
    """Add the ah-date class to each table cell whose whole text is an ISO 8601 date."""

    def run(self, root: etree.Element) -> None:
        for cell in root.iter("td"):
            if len(cell) == 0 and DATE.fullmatch((cell.text or "").strip()):
                cell.set("class", "ah-date")


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
        # After toc (5), which wraps each heading's contents in its anchorlink.
        md.treeprocessors.register(TitleTextTreeprocessor(md), "title_text", 4)


def makeExtension(**kwargs) -> ListIndentExtension:
    return ListIndentExtension(**kwargs)
