"""Markdown extensions for the awesome-humans.net site.

list_indent reads list nesting the way Prettier writes it and GitHub renders it: a
list item's content lines up under the text after its marker, two columns deep for
"- " and three for "1. ". Python-Markdown nests only in steps of tab_length, which is
4, so without this a fenced code block, a paragraph, or a nested list under a list item
drops out of the item on the site, and an ordered list nested three columns deep splits
its parent list in two. Before parsing, the extension re-indents each list to 4 columns
per level, and keeps any indentation past an item's content column.
"""

import re

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

TAB_LENGTH = 4
MARKER = re.compile(r"( *)([-*+]|\d{1,9}[.)])( {1,4}|$)(.*)")
FENCE = re.compile(r" *(`{3,}|~{3,})")


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
                if re.fullmatch(re.escape(marker[0]) + "{%d,} *" % len(marker), stripped):
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
                spaces, bullet, gap, rest = marker.groups()
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


class ListIndentExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        # After normalize_whitespace (30), which expands tabs, and before
        # superfences' fenced_code_block (25), which reads fences by indentation.
        md.preprocessors.register(ListIndentPreprocessor(md), "list_indent", 28)


def makeExtension(**kwargs) -> ListIndentExtension:
    return ListIndentExtension(**kwargs)
