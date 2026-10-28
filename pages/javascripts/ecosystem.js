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
// repo_url, the website repository. The theme renders the link twice, in the header
// and in the navigation drawer that narrow screens show, so this updates both.
// overrides/partials/source.html marks them with data-ah-source.
const repository = window.ahRepositories?.[segment];
if (repository) {
  for (const source of document.querySelectorAll("[data-ah-source]")) {
    source.href = `https://github.com/${repository}`;
    source.querySelector(".md-source__repository").textContent = repository;
  }
}
