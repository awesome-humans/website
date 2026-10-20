# Credits and licences

Awesome Humans is an independent project. It isn't affiliated with or endorsed by the .NET Foundation, Microsoft, the Rust Project, or the Rust Foundation. It names their languages and platforms to describe what its guidance covers.

## The site

The site's source, and every ecosystem's opinions, templates, and skills, are licensed under the [Apache License 2.0](https://github.com/awesome-humans/website/blob/main/LICENSE). Each cited source keeps the rights to its own work, which the site quotes and links. To stop being cited, see [Want in or out?](want-in-or-out.md).

## Logos

- **.NET:** the [.NET logo](https://github.com/dotnet/brand) is copyright the .NET authors, used per the .NET brand guidelines.
- **Rust:** the [Rust logo](https://github.com/rust-lang/rust-artwork) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), unchanged.

## Fonts and software

- **IBM Plex Sans and IBM Plex Mono:** copyright IBM Corp., licensed under the [SIL Open Font License 1.1](https://github.com/awesome-humans/website/blob/main/pages/assets/fonts/OFL.txt). The site serves a Latin-1 subset.
- **[Zensical](https://zensical.org):** builds the site, under the MIT License.

## Software bill of materials

[`sbom.cdx.json`](sbom.cdx.json) lists the Python packages that build the site, with their versions and hashes, in [CycloneDX 1.5](https://cyclonedx.org/docs/1.5/json/). Each build exports it from the site's lock file, so it always matches the published site. It leaves out the tools that only check the source, such as the formatters and lint tools.
