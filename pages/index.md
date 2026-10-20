<!-- The hero and the ecosystem cards are the design system's Hero and EcosystemCard,
     written as HTML. The hero's h1 is the page title and ends with a full stop. -->
<!-- markdownlint-disable MD026 MD033 MD041 -->

<section class="ah-hero" markdown>

# Awesome lists, distilled.

An agentic take on awesome lists (such as [awesome-dotnet](https://github.com/quozd/awesome-dotnet) and [awesome-rust](https://github.com/rust-unofficial/awesome-rust)):<br>
distilled, opinionated guidance, thanks to awesome humans.

<div class="ah-row">
<a class="ah-btn" href="how-it-works/">How it works</a>
<a class="ah-btn" href="dotnet/">Browse .NET</a>
</div>

</section>

This project documents current best practice in code and updates it as ecosystems evolve. Opinions come from awesome humans: people and publications with at least two years of accurate, independent writing on the subject.

Every opinion states its recommendation first, cites its sources, and targets the latest released versions.

## Ecosystems

<!-- ecosystem-cards -->

Each ecosystem includes:

- **Opinions:** One topic per page, with its recommendation, rationale, and sources.
- **Templates:** Files that encode the opinions.
- **Skills:** Agent skills that check a project against the opinions and keep the opinions current.
- **Awesome humans:** The roster of sources that the opinions cite.

## Usage

- **Point your agent at it.** Tell your coding agent to follow the opinions when it writes code:

  ```text
  Follow the conventions at awesome-humans.net when writing .NET code
  ```

- **Check an existing project.** Ask your coding agent to run [`review-project`](dotnet/skills/review-project.md):

  ```text
  Use the review-project skill at awesome-humans.net on <repository>
  ```

  To narrow the review, say what to include or leave out, such as "focus on testing, skip CI".

- **Start a project from the templates.** Copy the [.NET templates](dotnet/templates/index.md) into a new project, trimming what you don't need.

- **Read the opinions.** Each page gives its recommendation, with the rationale and sources behind it.

To understand how sources are vetted and how opinions stay current, see [How it works](how-it-works.md).

## Acknowledgement

Agents build and maintain this project, but it wouldn't exist without the people whose writing it draws on. Every opinion cites their work. Thank you to all of these awesome humans, and to everyone who supports them.

## Want in or out?

- **Suggest a source.** Know a person or publication with at least two years of accurate, independent writing about an ecosystem we cover? [Suggest them for vetting](https://github.com/awesome-humans/website/issues/new?template=suggest-source.yml). Every suggestion goes through the same [admission criteria](conventions/admission-criteria.md), and the decision log records the outcome, whether yes or no.
- **Opt out.** If you're a listed source and don't want your work cited, [ask to opt out](https://github.com/awesome-humans/website/issues/new?template=opt-out.yml), or email <contact@awesome-humans.net> if you'd rather not ask in public. Citations of your work go within 30 days.

For how we handle both, see [Want in or out?](want-in-or-out.md)
