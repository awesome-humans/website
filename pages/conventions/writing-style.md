# Writing style

These rules cover all prose in every awesome-humans repository: opinions, research topics, skills, template comments, the site's pages, and root documents such as `AGENTS.md` and `README.md`. They also cover commit messages, pull request titles and descriptions, and the comments an agent posts on issues and pull requests. They live here once, so the whole site reads in one voice.

Each repository's `AGENTS.md` adds what only it can say: who its reader is, the platform's spelling exception and its examples, and, in an ecosystem, Writing style for opinions. Read both before you write.

The voice follows the [Google developer documentation style guide](https://developers.google.com/style): conversational but direct, plain, and easy to scan. Start with its [highlights](https://developers.google.com/style/highlights). The rules below adapt it to awesome-humans. When a question comes up, use [Google's own order of precedence](https://developers.google.com/style#reference-hierarchy):

1. The rules on this page, and the repository's own in its `AGENTS.md`. Where the repository's rule is narrower, it wins.
2. The Google developer documentation style guide.
3. For a technical term that neither settles, the [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/), which Google names as its technical reference.

Apart from spelling, which [Spelling](#spelling) covers, awesome-humans departs from Google's guide in two places:

- **Pre-release features:** Google says not to pre-announce. An ecosystem's opinion can still carry a clearly marked "Coming next" note about a preview or nightly-only feature, where the ecosystem's `AGENTS.md` allows it.
- **Dates:** Write dates as ISO 8601 (`2026-10-19`), in UTC. Google accepts any unambiguous format. The rule covers every date in a repository, commit, or pull request, such as `last-reviewed`, a decision-log row, a "read" note, a "Review by" marking, and a harvest window. CI, GitHub, and the site builds run in UTC, so a date in a timezone ahead of UTC can read as a future date. An agent gets the date with `date -u +%F`. Leave an existing date as written.

## Voice

- **Write for a working developer.** Each repository's `AGENTS.md` says what its reader already knows. Don't explain that.
- **Address the reader as "you", and use the imperative for instructions.** Write "Set `persist-credentials` to `false`", not "The developer should set `persist-credentials`" or "One might disable persisted credentials".
- **Use active voice and present tense.** Write "The analyzer reports `CA1307`", not "`CA1307` will be reported by the analyzer".
- **Use common contractions.** _It's_, _don't_, _isn't_, _can't_, and _you're_ read naturally. Prefer the negative contractions: a reader scanning the page can miss _not_, but rarely misreads _don't_. Avoid rare ones, such as _it'll_ or _should've_.
- **Use plain words.** Write _use_, not _utilize_; _about_, not _with regard to_; _for example_, not _e.g._; _that is_, not _i.e._ Use _can_ for ability and _might_ for possibility. Reserve _must_ for a hard requirement.
- **Drop filler from instructions.** Don't write _please_, _simply_, _easy_, _quickly_, or _let's_, and don't open with a placeholder such as _please note_ or _at this time_. Avoid exclamation marks.
- **Write for a global audience.** Avoid figurative language, idioms, and cultural references. They don't translate, and a reader whose first language isn't English can take them literally. [Stock phrases](#stock-phrases) lists the ones that got in.

## Content

- **Lead with what matters.** Put the recommendation or the action first in a section, a paragraph, and a sentence. Put the reason after it.
- **Put a condition before the instruction it limits.** Write "For details, see `testing.md`", not "See `testing.md` for details", and "To publish a crate, run `cargo publish`", not the reverse. A reader the condition excludes can then skip the instruction. The condition is the only thing that goes ahead of the action. The reason still follows it.
- **Make link text say where the link goes.** Use the target's title, as [Citations and labels](#citations-and-labels) describes. Never use _here_, _this page_, or a bare URL. A pull request description has two exceptions, which [Commit messages and pull requests](#commit-messages-and-pull-requests) describes.
- **Make every sentence carry a fact the reader can act on or check.** Name the exact type, member, lint, key, diagnostic ID, and version (`CA1307`, `clippy::large_futures`, `[workspace.lints]`, .NET 10, Rust 1.99) instead of describing it. A measured number beats an adjective: "5.5 ms to 0.826 ms", not "much faster".
- **Cut what doesn't add a fact.** Delete a sentence that restates the one before it. Delete one that comments on the text instead of the subject, such as "which is worth noticing" or "the part that matters".
- **Keep sentences short.** Aim for about 20 words. Split any sentence over 35 words at the clause that does separate work.
- **Keep paragraphs short.** Three or four sentences is plenty. Break up a longer one, or turn it into a list.
- **Make it scannable.** Use a numbered list for steps that happen in order, a bulleted list for items that don't, and a table when the same attributes repeat across items. Use sentence-style capitalisation for headings, and keep headings short and specific.
- **Use the serial comma.** Write "opinions, templates, and skills".
- **Write a range with _to_, not an en dash.** Write "22.2% to 22.3%" and "versions 8 to 10". Use a hyphen only where a compound modifier needs one, as in "a long-running service".

## Order

A page that's read from top to bottom follows its topic. A list that a reader looks up follows the alphabet.

- **Group an opinion's sections by topic.** Put related sections next to each other, with the foundations first: hosting before hardening, for example. Don't sort the sections alphabetically. That would put "Open redirects" between "OpenAPI" and "Rate limiting", away from the rest of security.
- **Add a new section to its group, not to the end of the page.** If no group fits, start one where a reader would expect it. A page loses its order one appended section at a time.
- **Sort a template's interchangeable entries within their group.** Package versions, package references, and lints don't change meaning when reordered, so sort them by name, ignoring case. A group is an MSBuild `ItemGroup`, or a run of TOML keys between blank lines. A comment stays with the entry below it. Each ecosystem's CI checks this order.
- **Order by meaning where order is meaning.** F# compiles files in the order the project lists them, and an `.editorconfig` section groups its settings under the comment that explains them. Leave those in that order.

Each repository's `AGENTS.md` sets the order of its own indexes, such as a README's list of opinions.

## Rhythm

Agents write most of the prose here, and it goes wrong in rhythm more than vocabulary. The well-known tells (_delve_, _leverage_, _seamless_, _robust_, _comprehensive_, _in today's_, a "here is" lead-in, an "in conclusion" wrap-up) don't appear here, so don't hunt for them. Four patterns are fine occasionally and read as machine-written in bulk:

- **Em dashes.** Use at most one per sentence, and only for a real turn. A colon, a comma, or a full stop usually works better.
- **"X, not Y" contrasts.** Keep one when the rejected option is the one a reader would otherwise choose: "Pin to commit SHAs, not mutable tags". Cut it when nobody would choose the alternative: "a build artefact, not an afterthought".
- **Parenthetical asides.** If an aside carries real content, make it a sentence. If it restates the sentence it's attached to, delete it.
- **Lists of three.** A real list can have any length. Don't pad a list to three items because three sounds complete.

## Stock phrases

A few agent idioms did get in. Replace each with the plain statement it stands for: the failure a check catches, the claim an opinion rests on, or the cost a feature repays.

| Avoid                                              | Write instead                                   |
| -------------------------------------------------- | ----------------------------------------------- |
| load-bearing                                       | what depends on it                              |
| belt and braces                                    | the second check, and what it catches           |
| earns its keep, earns its place                    | the benefit, measured                           |
| escape hatch                                       | the setting or API that opts out                |
| bites                                              | the failure, and when it happens                |
| for free                                           | without extra code, or what's actually included |
| pull the other way                                 | the opposing claim, and who makes it            |
| reach for                                          | use                                             |
| worth noting                                       | (delete it, and state the fact)                 |
| _honest_, _genuinely_, _quietly_ (as intensifiers) | (delete them)                                   |

A literal use isn't an idiom. _Silently_ for a failure that raises no error stays, and so does _drift_ for two copies that diverge.

## Citations and labels

- **House:** Cite as `Source: Title`, never the reverse. The source comes first, whether it's a person or a publication: `[Toub: Performance Improvements in .NET 10]` and `[The Cargo Book: Workspaces]`, not `[Workspaces: The Cargo Book]`.
- **A description-list line uses the same colon:** `**Label:** definition`. Don't use an em dash as the separator.
- **Leave a source's own title as written.** A colon inside a title stays (`[Avalonia 12: Ready for What's Next]`), and an internal reference keeps its section (`[AGENTS.md: Metadata]`).

## Commit messages and pull requests

Every repository squash-merges a pull request with its title as the commit subject and its description as the commit body. GitHub renders the description as Markdown, but `git log` shows the same text as plain text, which GitHub wraps at 72 characters when it builds the commit. Write the description so it reads well both ways.

- **Title the pull request as a [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) subject.** Use the form `<type>[(scope)]: <description>`, in lowercase and the imperative, so it completes "If applied, this commit will". Each repository's `AGENTS.md` lists its types, and a skill that sets its own title says so. Keep it under 72 characters, counting the `(#123)` that GitHub appends.
- **Describe the change as a reader sees it, not file by file.** The diff already lists the files. Say what's different afterwards, and what you ran to check it.
- **Say why.** State the problem or the decision in the present tense, as the code stands without the change. It's the part of the commit that `git blame` can't recover.
- **Use only the Markdown that reads as plain text.** Paragraphs, `##` headings, `-` lists, `**Label:**` leads, and inline code read the same in both. Leave out tables, checkboxes, nested lists, and inline `[text](url)` links: GitHub's wrapping breaks a table row or a link across lines.
- **Link with references.** Write an issue or pull request as `#93`, or `awesome-humans/rust#20` in another repository, and a commit as its short SHA. GitHub links them in the pull request and the commit, and they read as plain text. For any other link, use a reference-style link, `[text][1]`, with `[1]: https://…` on its own line after the last section and before the trailers.
- **End with trailers.** The last paragraph holds one trailer per line, as `Token: value`, which is a Conventional Commits footer and a git trailer at once. Put it after any link definitions because git reads trailers only from the last paragraph. Use `Closes: #93` for an issue the change finishes, `Refs: #93` for one it only relates to, and `Link: https://…` for background, such as a discussion or a specification. Each issue gets its own line. The description still has to make sense without opening any of them.
- **Delete the template's comment.** A template's `<!-- … -->` guidance would become part of the commit. The required `attribution / check` fails a description that still has one, or that has a table, a checkbox, or an inline link.
- **Keep agent attribution out.** A description and its trailers never carry a `Co-authored-by` line or a "Generated with" footer. Each repository's `AGENTS.md` explains why, and where agent attribution goes instead.
- **Sign an agent's comment with one italic line.** It names the harness, the model, and the skill running, if any: `_Written by an agent: Claude Code, Opus 5.5, running review-project._` Leave out a vendor name the harness already gives, so write `Opus 5.5`, not `Claude Opus 5.5`.

For example:

```markdown
## What changed

The home page, Want in or out?, and the suggest-source form link the shared admission criteria. Checked with `just check` and the preview.

## Why

The three links point at `dotnet`'s copy of the criteria, so a Rust suggestion is checked against the wrong page.

Closes: #93
Refs: awesome-humans/rust#20
```

To read a commit's message rendered as Markdown in a terminal, pipe it through a renderer such as [Glow](https://github.com/charmbracelet/glow): `git show -s --format='# %s%n%n%b' <sha> | glow -`.

## Spelling

- **Use British spelling, except where a platform names the word.** Write _defence_, _modelling_, _catalogue_, _behaviour_, and _colour_. This overrides Google's American spelling and its dictionary, Merriam-Webster.
- **Use the platform's spelling for its own concept,** so prose and identifiers match and a search for one finds the other. Each repository's `AGENTS.md` gives its platform's examples.
- **Don't extend the exception to words that only share a stem with an API.** "A behaviour change in SQLite" keeps its British spelling, even though a library has a `Behavior` type. Never anglicise an API name, a CSS property, or a configuration key, such as `color`.
- **`just spell` checks spelling.** When it flags a correctly spelled name or term, add the word to the repository's `cspell.words.txt` in the same commit. Never add an American spelling there. In Markdown, it skips link text, inline code, and double-quoted text, so a cited title or a quotation keeps its spelling. For a title outside those, such as an italic book title, put `<!-- cspell:ignore <word> -->` above the paragraph.

## Scope of these rules

- **They're review guidance, not a build check.** Whether a contrast is justified can't be decided by counting. Read for these patterns in review, and don't add a check that fails a build over them. Spelling is one exception: a misspelled word is wrong whatever its context, so `just spell` fails the build over it. A template's sorted entries are the other, because sorting by name needs no judgement.
- **They apply only to prose written here.** A third-party title and its URL keep the author's wording and spelling, American or British, so Andrew Lock's "Adding Localisation to an ASP.NET Core application" stays as written. Correcting a source misquotes it, and correcting a URL breaks it.
- **They don't apply to other people's code.** `review-project` reviews a codebase against an ecosystem's opinions. Spelling and wording in someone else's identifiers, comments, or documentation is never a finding.
