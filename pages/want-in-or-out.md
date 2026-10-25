# Want in or out?

Citation is opt-out. Anyone can suggest a source or improve the opinions, and any listed source can ask to stop being cited. A source suggestion or an opt-out is a GitHub issue in [awesome-humans/website](https://github.com/awesome-humans/website), unless you send the opt-out by email. A change to an opinion, a template, or a skill goes to the ecosystem's own repository.

The site shows no portraits or logos. Each source appears by name, with a link to their work.

The goal is a montage of portraits for each ecosystem, and one for the site itself. Unlike citation, a portrait is opt-in: a face appears only with the person's recorded permission. Asking means the owner writes to every source on every roster and follows up each reply. That's more correspondence than one maintainer can take on yet, so portraits are on hold.

## Want in

Find your change in the table, then follow its section. Each ecosystem's pages link its repository in the header.

| Change                                                              | Repository      | Start with                                              |
| ------------------------------------------------------------------- | --------------- | ------------------------------------------------------- |
| [Suggest a source](#suggest-a-source)                               | `website`       | The suggest-source issue form                           |
| [Challenge or correct an opinion](#challenge-or-correct-an-opinion) | The ecosystem's | An issue, or a pull request for a small factual fix     |
| [Propose a new opinion](#propose-a-new-opinion)                     | The ecosystem's | A research pull request, or an issue                    |
| [Propose a house opinion](#propose-a-house-opinion)                 | The ecosystem's | A pull request with the opinion template                |
| [Fix a template or a skill](#fix-a-template-a-skill-or-the-site)    | The ecosystem's | A pull request                                          |
| [Fix the site](#fix-a-template-a-skill-or-the-site)                 | `website`       | A pull request for a small fix, otherwise a blank issue |

### Suggest a source

[Suggest a source for vetting](https://github.com/awesome-humans/website/issues/new?template=suggest-source.yml) with the issue form. It asks for the ecosystem, the source's main URL, three sample posts, and why the source qualifies. You can suggest yourself.

1. **Intake checks the suggestion.** A source already on a roster gets a reply with its current standing, and the issue closes as a duplicate.
2. **The issue moves to the ecosystem's repository,** where the `vet-source` skill checks the source against the [admission criteria](conventions/admission-criteria.md).
3. **The decision log records the outcome,** whether yes or no, in a pull request that closes the issue. The issue gets a comment with the decision.

Only published writing counts: blog posts, documentation, books, and newsletters. Videos, conference talks, and podcasts are out of scope, as material to cite and as evidence of a track record.

### Challenge or correct an opinion

Open an issue in the ecosystem's repository when an opinion is wrong, stale, or misreads its source. Name the opinion file and its section, say what's wrong, and link the evidence: the source's post, a release note, or a minimal reproduction. An opinion cites only vetted sources, so evidence from a source that isn't on the roster also needs that source [suggested for vetting](#suggest-a-source).

For a small factual fix, such as a misquote, a broken citation, or a wrong version number, open a pull request instead, with the [opinion pull request template](https://github.com/awesome-humans/.github/blob/main/PULL_REQUEST_TEMPLATE/opinion.md).

### Propose a new opinion

A new sourced opinion starts as a research topic, which saves the evidence in one pull request, and the owner promotes it into the opinions in a second. For details, see [How it works: Research is staged, never merged in place](how-it-works.md#research-is-staged-never-merged-in-place). Take one of these routes:

- **Research it yourself.** Run the ecosystem's `research-topic` skill with your coding agent, and open its pull request with the [research pull request template](https://github.com/awesome-humans/.github/blob/main/PULL_REQUEST_TEMPLATE/research.md). A topic can cite a source from outside the roster if the topic flags that source.
- **Ask the owner to research it.** Open an issue in the ecosystem's repository that names the topic and links what you've read.

Either way, the owner promotes or discards the topic with the `resolve-research` skill.

### Propose a house opinion

An opinion from your own practice, with no published source behind it, is a house opinion. Open a pull request in the ecosystem's repository with the [opinion pull request template](https://github.com/awesome-humans/.github/blob/main/PULL_REQUEST_TEMPLATE/opinion.md), and keep **Experience-based** under Provenance. If a profile's owner accepts it, they adopt it into their profile and take responsibility for it, and the Woven table's Provenance column credits you and the pull request. For the rules, see [House opinions](conventions/house-opinions.md). To keep a profile of your own, see [House profiles](house-profiles.md).

### Fix a template, a skill, or the site

- **A template or a skill:** Open a pull request in the ecosystem's repository. If the fix changes what a template recommends, it's an opinion change, so use the [opinion pull request template](https://github.com/awesome-humans/.github/blob/main/PULL_REQUEST_TEMPLATE/opinion.md).
- **The site:** The theme, the build, and the shared pages, such as this one and the [conventions](conventions/writing-style.md), live in [awesome-humans/website](https://github.com/awesome-humans/website). Open a pull request there for a small fix, or a [blank issue](https://github.com/awesome-humans/website/issues/new) for anything else.

To use a pull request template, add `template=<file>` to the new pull request's address, after `?` or `&`, and reload. Without one, you get the default template, which links the others.

### What to expect

- **CI checks every pull request:** formatting, linting, spelling, links, each file's metadata, and that every cited source is on the roster and citable. Each repository's `AGENTS.md` says how to run the same checks locally.
- **CodeRabbit reviews it.** Its findings are advisory, but answer each one: fix it, or reply with the reason you didn't.
- **The owner reviews and merges it.** CI and CodeRabbit never merge a pull request on their own.
- **The title follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/),** such as `docs: correct the EF Core version in data-access`. Every repository squash-merges a pull request, so its title becomes the commit subject and its description the commit message.
- **The prose follows the [writing style](conventions/writing-style.md),** which every repository shares.

## Opt out

[Ask to opt out](https://github.com/awesome-humans/website/issues/new?template=opt-out.yml) with the issue form, or [by email](#opt-out-by-email). An opt-out covers every ecosystem that lists you, because you opt out as a person, not per language.

### Show that you control the source

Use one of these:

- **Your GitHub account:** Comment on the issue from the GitHub account that your site links to.
- **Your domain:** Publish a page or post on the source's domain that names the issue.
- **Email:** Send the request from an address on the source's domain.

The owner checks the proof and decides. If the proof doesn't check out, you get one reply that explains these options, and the issue stays open for 30 days.

### Opt out by email

Email <contact@awesome-humans.net> from an address on the source's domain, and name the sources to remove. The owner opens the opt-out issue for you, with "email" and the date as the proof. The issue names only the source's roster ID, which the roster already shows, and never your address.

### What happens next

1. **Each ecosystem that lists you gets an issue,** linked to yours.
2. **Within 30 days, your work leaves every opinion and roster.** Each opinion that cited you is re-sourced from another vetted source, or cut back to what other sources support. Your roster ID moves to an Opted out section, so nobody suggests you again.
3. **Your issue closes** with links to every pull request, and is locked.

The pages are versioned in git, like any public repository. An opt-out removes citations of your work, but it can't remove the fact that a published opinion once linked it.

### Opt back in

Opting back in is a suggestion like any other. It goes through vetting, and your ID leaves the Opted out section when you're admitted.
