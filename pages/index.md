<!-- The hero and the ecosystem cards are the stylesheet's ah-hero and ah-card components,
     written as HTML. The hero's h1 is the page title and ends with a full stop.
     scripts/stage.py replaces each marker from ecosystems.toml. -->
<!-- markdownlint-disable MD026 MD033 MD041 -->

<section class="ah-hero" markdown>

# Awesome lists, distilled.

An agentic take on awesome lists (such as [awesome-dotnet](https://github.com/quozd/awesome-dotnet) and [awesome-rust](https://github.com/rust-unofficial/awesome-rust)):<br>
distilled, opinionated guidance, thanks to awesome humans.

<div class="ah-row">
<a class="ah-btn" href="usage/">Usage</a>
<a class="ah-btn" href="how-it-works/">How it works</a>
<!-- ecosystem-buttons -->
</div>

</section>

This project documents current best practice in code and updates it as ecosystems evolve. Opinions come from awesome humans: people and publications with at least two years of accurate, independent writing on the subject.

Every opinion states its recommendation first, cites its sources, and targets the latest released versions.

**Agents:** Fetch [`/llms.txt`](llms.txt) and every file it links as raw text. It links every ecosystem's opinions, templates, and skills.

## Ecosystems

<!-- ecosystem-cards -->

Each ecosystem includes:

- **Awesome humans:** The roster of sources that the opinions cite.
- **Opinions:** One topic per page, with its recommendation, rationale, and sources.
- **Templates:** Files that encode the opinions.
- **Skills:** Agent skills that check a project against the opinions and keep the opinions current.

## Usage

- **Try it once.** Ask your coding agent to check a project against the opinions. It reports what it finds, and changes nothing unless you ask for fixes:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its review-project skill on <repository>
  ```

- **Use it in your project.** Install the skills, so your agent reads the opinions from the project's own copy:

  ```sh
  npx skills add https://awesome-humans.net
  ```

[Usage](usage.md) has the prompts for following the opinions and researching a topic, and the addresses for one ecosystem or a house profile.

To understand how sources are vetted and how opinions stay current, see [How it works](how-it-works.md).

## Acknowledgement

Agents build and maintain this project, so the [usual disclaimers](credits.md#disclaimer) apply, but it wouldn't exist without the people whose writing it draws on. Every opinion cites their work. Thank you to all of these awesome humans, and to everyone who supports them.

## Want in or out?

- **Suggest a source.** Know a person or publication with at least two years of accurate, independent writing about an ecosystem we cover? [Suggest them for vetting](https://github.com/awesome-humans/website/issues/new?template=suggest-source.yml). Every new source goes through the same [admission criteria](conventions/admission-criteria.md), and the decision log records every outcome.
- **Improve an opinion.** Challenge or correct one, propose a new one, or fix a template, a skill, or the site. [Want in](want-in-or-out.md#want-in) says which repository it goes to, and whether to start with an issue or a pull request.
- **Opt out.** If you're a listed source and don't want your work cited, [ask to opt out](https://github.com/awesome-humans/website/issues/new?template=opt-out.yml), or email <contact@awesome-humans.net> if you'd rather not ask in public. Once the maintainer verifies that you control the source, we remove citations of your work within 30 days.

For how we handle each of these, see [Want in or out?](want-in-or-out.md)
