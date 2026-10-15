// Sets data-ecosystem on <html> from the first path segment, such as dotnet in
// /dotnet/opinions/csharp/, so stylesheets/awesome-humans.css gives the page that
// ecosystem's accent. A segment with no accent there, such as how-it-works, keeps brand.
// A preview serves the site at its root too, so the first segment is the same there.
const [segment] = location.pathname.split("/").filter(Boolean);
if (segment) {
  document.documentElement.dataset.ecosystem = segment;
}
