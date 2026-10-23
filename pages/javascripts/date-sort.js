// Lets a reader sort a table by a date column, such as a roster's decision log or the
// Woven table of house opinions. A column qualifies when every body cell holds only a
// date, which the date_cells extension in src/ marks with ah-date, so a column with a
// placeholder, such as the watch list's Since, stays in source order. A column already in
// date order, such as a decision log, which runs newest first, starts marked with that
// order, so each click reverses it. Otherwise the first click sorts newest first. ISO
// 8601 dates sort as text, trimmed as date_cells trims them, and rows with the same date
// keep their source order. The theme draws the arrow from role and aria-sort on the header.
// A block, so these names stay out of the global scope, which the theme's own scripts share.
{
  function sortable(table, index) {
    const rows = [...table.tBodies[0].rows];
    return (
      rows.length > 1 &&
      rows.every((row) => row.cells[index]?.classList.contains("ah-date"))
    );
  }

  function dates(table, index) {
    return [...table.tBodies[0].rows].map((row) =>
      row.cells[index].textContent.trim(),
    );
  }

  // The order the column is already in, as an aria-sort value.
  function sourceOrder(table, index) {
    const values = dates(table, index);
    const pairs = values.slice(1).map((value, i) => [values[i], value]);
    if (pairs.every(([a, b]) => a.localeCompare(b) >= 0)) {
      return "descending";
    }
    if (pairs.every(([a, b]) => a.localeCompare(b) <= 0)) {
      return "ascending";
    }
    return "none";
  }

  function sort(table, header, index) {
    const descending = header.getAttribute("aria-sort") !== "descending";
    for (const other of table.tHead.rows[0].cells) {
      if (other.hasAttribute("aria-sort")) {
        other.setAttribute("aria-sort", "none");
      }
    }
    header.setAttribute("aria-sort", descending ? "descending" : "ascending");

    const body = table.tBodies[0];
    const rows = [...body.rows].sort((a, b) => {
      const order = a.cells[index].textContent
        .trim()
        .localeCompare(b.cells[index].textContent.trim());
      return descending ? -order : order;
    });
    body.append(...rows);
  }

  function addDateSort() {
    for (const table of document.querySelectorAll(".md-typeset table")) {
      if (!table.tHead || table.tBodies.length !== 1) {
        continue;
      }
      for (const [index, header] of [...table.tHead.rows[0].cells].entries()) {
        if (!sortable(table, index)) {
          continue;
        }
        const button = document.createElement("button");
        button.type = "button";
        button.className = "ah-sort";
        button.append(...header.childNodes);
        header.append(button);
        // On the header, which the theme gives a pointer, so a click anywhere in it sorts.
        header.addEventListener("click", () => sort(table, header, index));
        header.setAttribute("role", "columnheader");
        header.setAttribute("aria-sort", sourceOrder(table, index));
      }
    }
  }

  addEventListener("DOMContentLoaded", addDateSort);
}
