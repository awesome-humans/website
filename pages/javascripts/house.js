// Lets a reader choose a house profile, a named set of house opinions, from a picker in
// the header. The site shows none by default: stylesheets/awesome-humans.css hides every
// element with data-house, and this script shows the chosen profile's, and sets
// data-house on <html>. Local storage remembers the choice. ?house=<profile> sets it, and
// ?house=none clears it. houses.js, which stage.py writes from houses.toml, lists the
// profiles. Without JavaScript, or with no profiles, the reader sees the default and no picker.
// A block, so these names stay out of the global scope, which the theme's own scripts share.
{
  const houses = window.ahHouses ?? [];
  const none = "none";
  const key = "ah.house";

  function stored() {
    try {
      return localStorage.getItem(key);
    } catch {
      // Storage can be blocked. The reader then sees the default on every page.
      return null;
    }
  }

  function store(profile) {
    try {
      if (profile === none) {
        localStorage.removeItem(key);
      } else {
        localStorage.setItem(key, profile);
      }
    } catch {
      // As above: the choice lasts for this page only.
    }
  }

  // Shows the profile's house content and hides every other profile's. An unknown profile,
  // such as one removed from houses.toml since the reader chose it, falls back to the default.
  function apply(profile) {
    const chosen = houses.some((house) => house.id === profile)
      ? profile
      : none;
    if (chosen === none) {
      delete document.documentElement.dataset.house;
    } else {
      document.documentElement.dataset.house = chosen;
    }
    for (const element of document.querySelectorAll(
      ".md-typeset [data-house]",
    )) {
      element.classList.toggle(
        "ah-house--on",
        element.dataset.house === chosen,
      );
    }
    return chosen;
  }

  const requested = new URLSearchParams(location.search).get("house");
  if (requested === none || houses.some((house) => house.id === requested)) {
    store(requested);
  }
  const current = apply(requested ?? stored() ?? none);

  // The picker sits in the header, before the search box, on every page.
  const header = document.querySelector(".md-header__inner");
  if (houses.length > 0 && header) {
    const select = document.createElement("select");
    select.className = "ah-house-picker";
    select.setAttribute("aria-label", "House profile");
    select.title = "Show a house profile's opinions beside the sourced ones";
    select.append(new Option("No house opinions", none));
    for (const house of houses) {
      select.append(new Option(`House: ${house.name}`, house.id));
    }
    select.value = current;
    // A ?house= left in the address would undo the change on reload, so it follows the picker.
    select.addEventListener("change", () => {
      store(select.value);
      apply(select.value);
      const url = new URL(location.href);
      if (url.searchParams.has("house")) {
        if (select.value === none) {
          url.searchParams.delete("house");
        } else {
          url.searchParams.set("house", select.value);
        }
        history.replaceState(history.state, "", url);
      }
    });
    header.insertBefore(
      select,
      header.querySelector(".md-search") ??
        header.querySelector(".md-header__source"),
    );
  }
}
