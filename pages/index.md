<!-- The hero and the ecosystem cards are the design system's Hero and EcosystemCard,
     written as HTML. The hero's h1 is the page title and ends with a full stop. -->
<!-- markdownlint-disable MD026 MD033 MD041 -->

<section class="ah-hero" markdown>

# Awesome lists, distilled.

An agentic take on awesome lists ([awesome-dotnet](https://github.com/quozd/awesome-dotnet), [awesome-rust](https://github.com/rust-unofficial/awesome-rust)): distilled guidance, thanks to awesome humans.

<div class="ah-row">
<a class="ah-btn" href="how-it-works/">How it works</a>
<a class="ah-btn" href="dotnet/">Browse .NET</a>
</div>

</section>

It shows you what good code looks like today, and keeps that answer current as ecosystems change. Recommendations come from awesome humans: people and publications with at least two years of accurate, independent writing on the subject.

Every opinion states its recommendation first, cites its sources, and targets the latest released versions.

## Ecosystems

<!-- ecosystem-cards -->

Each ecosystem has the same parts:

- **Opinions:** One topic per page, each with its recommendation, rationale, and sources.
- **Templates:** Files that encode the opinions.
- **Skills:** Agent skills that check a project against the opinions and keep the opinions current.
- **Awesome humans:** The roster of sources that the opinions cite.

## Usage

- **Point your agent at it.** Tell your coding agent to follow the opinions when it writes code:

  ```text title="Prompt"
  Follow the conventions at awesome-humans.net when writing .NET code
  ```

- **Check an existing project.** Ask your coding agent to run [`verify-project`](dotnet/skills/verify-project.md):

  ```text title="Prompt"
  Use the verify project skill at awesome-humans.net against <repo>
  ```

  To narrow the review, say so in the request, such as "focus on testing".

- **Start a project from the templates.** Copy the [.NET templates](dotnet/templates/index.md) into a new project, and trim what you don't need.

- **Read the opinions.** Each page gives the recommendation, the rationale, and the sources behind it.

To understand how sources are vetted and how the opinions stay current, see [How it works](how-it-works.md).

## Acknowledgement

Agents build and maintain this project, but it wouldn't exist without the people whose writing it draws on. Every opinion cites their work. Thank you to all of these awesome humans, and to everyone who supports them.
