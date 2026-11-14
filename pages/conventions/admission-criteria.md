# Admission criteria

These are the rules every ecosystem uses to admit a source to its roster, and the reserved IDs and markings that limit how an opinion cites one. They live here once. Each ecosystem's `AWESOME-HUMANS.md` holds its roster tables, its Opted out section, its Source notes, and its decision log, and applies these rules to them.

To propose a source, [suggest it for vetting](https://github.com/awesome-humans/website/issues/new?template=suggest-source.yml). If you're a listed source and don't want your work cited, [ask to opt out](https://github.com/awesome-humans/website/issues/new?template=opt-out.yml). For how both work, see [Want in or out?](../want-in-or-out.md)

## Track record

**Scope: published writing.** A source qualifies on text a reader can check: blog posts, documentation, books, and newsletters. Videos, conference talks, and podcasts are out of scope for now, both as citable material and as evidence of a track record. A source that moves to those formats stops qualifying, and becomes a `vet-source` candidate again if the writing resumes.

A **source** is the published work of an awesome human: a person or a publication. Admission needs an **established track record**:

1. **Longevity:** At least two years of sustained publishing. A source with less goes on the watch list, however good the writing. The roster's `Since` column shows how far back each record goes.
2. **Depth:** Original insight, such as internals, measurements, or worked reasoning. Paraphrased release notes don't count. A long-lived source with thin depth is admitted with the `**Corroborate.**` marking, which limits how it's cited.
3. **Accuracy:** A history of being right, and of publishing corrections when wrong.
4. **Independence:** The content stands on its merit, not on marketing reach.

Two rules qualify these criteria:

- **An independence concern is a usage limit, not a lower rank.** A concern applies when vendor developer relations, product-team work, or project marketing produces adoption-focused content with little critical distance. The source is still admitted, and its section under the roster's Source notes says what a citation can rest on, usually how something works, not whether to adopt it.
  - Working for a vendor, or maintaining a package, isn't a concern by itself. Depth with critical distance needs no limit. Record a conflict where an opinion might recommend the source's own package or product.
  - A concern that no limit could contain leads to a decline or the watch list.
- **Dormancy blocks admission, with one exception.** A candidate who hasn't published for over a year goes on the watch list, unless the person's **writing** clearly continues elsewhere, such as official documentation, another publication, or a book. Then the track record follows the person, and the notes record the dormant channel.
  - Repository activity isn't evidence. Opinions don't cite commits, releases, or issue threads, so a busy GitHub profile beside a silent blog is still dormant.
  - Documentation written in a repository counts. The test is what was published, not where the commits landed.
  - The same rule triggers re-evaluation of admitted sources. For details, see `vet-source`.

Each roster's Watch list tracks candidates that don't qualify yet, and `vet-source` re-evaluates them. An opt-out in one ecosystem covers every ecosystem, so `vet-source` reads every roster's Opted out section before it gathers any evidence. The decision log at the end of each roster records every admission, decline, and demotion.

## Reserved IDs, markings, and references

**Reserved prefix: `house:`.** A house profile's opinions use the source ID `house:<profile>`, such as `house:simon-mckenna`. A profile's authority is its owner's experience, not a track record, so it skips the admission criteria, and every house opinion is visibly marked instead. [House opinions](house-opinions.md) is the canonical definition of the marking, of how a house opinion sits beside the sourced text, and of contributor adoption. A `house:` ID never appears in the roster tables.

**Reserved marking: `**Discovery-only.**`.** Aggregators, such as link roundups, newsletters, and curated lists, are admitted for discovery and never cited. They lead to a primary source, and the opinion cites that. CI rejects the ID of a source whose notes have this marking in any `sources:` list under `opinions/` or `templates/`. Like `**House:**`, it's a fixed string, so a check can match it exactly.

**Reserved marking: `**Corroborate.**`.** Some sources have a long track record but thin depth: SEO-shaped roundups, course funnels, community catalogues, or release paraphrase with occasional substance. They're admitted and marked. The marking limits how you cite the source, not its standing. An opinion can cite it, but never alone: every claim it supports also needs an unmarked citable source. `just validate-sources` rejects an opinion or template whose citable sources are all marked. Neither a `house:` ID nor a Discovery-only ID counts as the unmarked source.

**References: a named package's own material.** When an opinion or template names a package or tool, you can link the project's own material inline as a reference:

- Its documentation site or in-repository docs
- Its generated API documentation
- Release notes and changelogs
- Issues and pull requests
- Its design documents
- Its tests and source code
- Its page on the package registry

The standard behind a named format or protocol qualifies on the same terms, such as an RFC or the IANA time zone database. An ecosystem's `AWESOME-HUMANS.md` can name more repositories that qualify, such as a language's proposals, under a Named references section. It says there what each one is the record of, such as how a feature behaves or which versions an advisory affects.

A reference is the record of its subject: the package, the standard, or what an ecosystem names a repository for. What it supports depends on the kind of claim:

- **A reference fact rests on the reference alone.** A reference fact is a statement about the reference's subject that a reader can check against it: what the subject does, what it reports, how it's configured, what it supports, and from which version. It needs no roster source. The subject's own code and documentation are the primary evidence for it, and no roster source describes most of it.
- **Mechanics are reference facts.** Mechanics are what a subject requires of a project that already uses it. An opinion can write one as an instruction, such as the setting that stops a diagnostic the package reports, and it's still a reference fact.
- **A choice rests on a roster source.** A choice picks between alternatives a developer could reasonably weigh, such as adopting a package, turning on an optional rule, or preferring one API to another. There a reference only corroborates the roster source. A package's own material never decides whether to adopt that package.
- **A judgement is never a reference fact.** How fast, how safe, or how simple a subject is, and how it compares with another, needs a roster source even when the reference says it.
- **A reference states what the claim says.** Read it before you link it. A reference fact that its reference doesn't state is a misquoted source.

Two examples:

| Claim                                                                               | Kind           | Rests on                                    |
| ----------------------------------------------------------------------------------- | -------------- | ------------------------------------------- |
| Version an API with `Asp.Versioning`                                                | Choice         | The .NET Blog, a roster source              |
| The package reports AV0025 for a project with no `<Description>`, so set one        | Reference fact | The package's AV0025 diagnostic page        |
| Prefer `#[expect]` to `#[allow]`                                                    | Choice         | A roster source                             |
| `#[expect]` warns when the lint it names doesn't fire, and is stable from Rust 1.81 | Reference fact | RFC 2383 and its stabilization pull request |

These rules cover how you cite a reference:

- A reference needs no `vet-source` pass and never appears in `sources:`, so `just validate-sources` doesn't see it.
- Cite it in the same `Source: Title` form as anything else, as in `[xUnit.net: Testing with Native AOT]`.
- Guidance isn't a reference. A repository that publishes advice, such as a skills repository or a style guide, is a source, so propose it with `vet-source`.
- Cite a roster source's page, not its repository. A repository that publishes a roster source, such as `rust-lang/reference` for `rust-docs`, is that source.
- Don't cite an archived repository. Link where its content moved, such as `dotnet/corefx` to `dotnet/runtime`.
- Pin a link to a line of code or a test to a commit. A link to a document can follow the default branch, because the link check catches a move, but a line anchor on a branch drifts without breaking.
