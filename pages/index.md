<!-- The hero and the ecosystem cards are the design system's Hero and EcosystemCard,
     written as HTML. The hero's h1 is the page title and ends with a full stop. -->
<!-- markdownlint-disable MD026 MD033 MD041 -->

<section class="ah-hero" markdown>

<p class="ah-hero__kicker">[ ] awesome-humans.net</p>

# Awesome lists, distilled.

Like a curated awesome-* list, but instead of links you get the guidance itself: opinions distilled from people with a proven track record, each one cited, kept current, and ready for your coding agent.

<div class="ah-row"><a class="ah-btn ah-btn--primary" href="dotnet/">Browse .NET</a><a class="ah-btn" href="how-it-works/">How it works</a></div>

</section>

This project shows you what good code looks like today, and keeps that answer current as each ecosystem changes. Recommendations come from awesome humans: people and publications with at least two years of accurate, independent writing on the subject.

Every opinion states its recommendation first, cites its sources, and targets the latest released versions.

## Ecosystems

<!-- ecosystem-cards -->

Each ecosystem has the same parts:

- **Opinions:** One topic per page, each with its recommendation, rationale, and sources.
- **Templates:** Copy-paste-ready files that encode the opinions.
- **Skills:** Agent skills that check a project against the opinions and keep the opinions current.
- **Awesome humans:** The roster of sources that the opinions cite.

## Usage

- **Point your agent at it.** Tell your coding agent to follow the opinions when it writes code. For example: "Follow the conventions in <https://awesome-humans.net/llms.txt> when you write .NET code." That file links the raw Markdown of every opinion, template, and skill.
- **Check an existing project.** Clone the repository, and ask your agent to run [`verify-project`](dotnet/skills/verify-project.md) on a local path or a repository URL. It reports each deviation from the opinions with a severity and a one-line fix, and applies the fixes only if you ask. To narrow the review, say so in the request, such as "focus on testing".
- **Start a project from the templates.** Copy the [.NET templates](dotnet/templates/index.md) into a new project, and trim what you don't need.
- **Read the opinions.** Each page gives the recommendation, the rationale, and the sources behind it.

For how sources are vetted and how the opinions stay current, see [How it works](how-it-works.md).

## Acknowledgement

Agents build and maintain this project, but it wouldn't exist without the people whose writing it draws on. Every opinion cites their work. Thank you to all of these awesome humans, and to everyone who supports them.
