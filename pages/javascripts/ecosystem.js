// Sets data-ecosystem on <html> from the first path segment, such as dotnet in
// /dotnet/opinions/csharp/, so stylesheets/awesome-humans.css gives the page that
// ecosystem's accent. A segment with no accent there, such as how-it-works, keeps brand.
// A preview serves the site at its root too, so the first segment is the same there.
const [segment] = location.pathname.split("/").filter(Boolean);
if (segment) {
  document.documentElement.dataset.ecosystem = segment;
}

// Points the header's repository link at the ecosystem's own repository under /<id>/,
// from repositories.js, which stage.py writes. Every other page keeps zensical.toml's
// repo_url, the website repository. This runs before the theme reads the link.
const repository = window.ahRepositories?.[segment];
const source = document.querySelector('[data-md-component="source"]');
if (repository && source) {
  source.href = `https://github.com/${repository}`;
  source.querySelector(".md-source__repository").textContent = repository;
}

// The theme caches one repository's stars and forks in session storage, whichever
// repository they came from. Drop them when the link names a different repository, so
// the theme fetches that one's.
if (source) {
  try {
    const key = `${__md_scope.pathname}.__source`;
    if (sessionStorage.getItem("ah.source") !== source.href) {
      sessionStorage.removeItem(key);
      sessionStorage.setItem("ah.source", source.href);
    }
  } catch {
    // Storage can be blocked. The theme then fetches the facts on every page.
  }
}
