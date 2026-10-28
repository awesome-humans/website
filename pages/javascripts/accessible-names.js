// Names two of the theme's controls in a way ARIA allows, so screen readers and agents
// that read the accessibility tree can tell them apart.

// The header's Navigation and Search buttons are labels with aria-label, which ARIA
// prohibits on a label. Their names move into hidden text inside the label instead.
for (const label of document.querySelectorAll(
  "label.md-header__button[aria-label]",
)) {
  const name = document.createElement("span");
  name.className = "ah-visually-hidden";
  name.textContent = label.getAttribute("aria-label");
  label.append(name);
  label.removeAttribute("aria-label");
}

// anchor_linenums in zensical.toml links each line of a code block to itself, with an
// empty link. Each one takes its line number as its name, such as "Line 3". A fence with
// linenums also gets anchors without href, which ARIA forbids naming, so they're skipped.
for (const link of document.querySelectorAll('a[href][id^="__codelineno-"]')) {
  link.setAttribute("aria-label", `Line ${link.id.split("-").at(-1)}`);
}
