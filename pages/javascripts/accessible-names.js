// Names the code line links, so screen readers and agents that read the accessibility
// tree can tell them apart. anchor_linenums in zensical.toml links each line of a code
// block to itself, with an empty link. Each one takes its line number as its name, such
// as "Line 3". A fence with linenums also gets anchors without href, which ARIA forbids
// naming, so they're skipped.
for (const link of document.querySelectorAll('a[href][id^="__codelineno-"]')) {
  link.setAttribute("aria-label", `Line ${link.id.split("-").at(-1)}`);
}
