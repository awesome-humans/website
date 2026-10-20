---
hide:
  - toc
---

# How it works

Agent skills maintain each ecosystem's repository, and nothing becomes an opinion without passing CI, another agent's review and the repository owner's review.

## Each ecosystem is its own repository

An ecosystem's opinions, templates, skills, and source roster live in its own repository, and the `website` repository publishes them. When an ecosystem's `main` changes, it asks `website` to rebuild. A production build always uses every ecosystem's `main`, whichever repository triggered it. A pull request in an ecosystem builds a full-site preview from its own branch and every other ecosystem's `main`.

Suggestions from the site's issue forms move to the ecosystem they name. Two shared repositories serve every pull request: `.github` holds the attribution check, and `coderabbit` the review configuration.

<!-- diagram: repositories -->

## Every change is a pull request

Skills work on their own branch, and all changes arrive through a pull request. CI checks that:

- Every opinion and template has valid metadata
- Every cited source is on the roster and citable
- Every link resolves

The agent reviewer (currently CodeRabbit) also checks the change, with the owner's agent answering each finding. Its review is advisory: the owner reviews and merges the pull request.

Two skills report without modifying anything:

- `audit-freshness` finds stale review dates and lagging version pins
- `review-project` grades an external codebase against the opinions

Any of these starts the next run:

- Findings from either skill
- A scheduled release watch
- A monthly harvest reminder
- A request from the owner

<!-- diagram: maintenance-pipeline -->

## Sources need a track record

A source joins the roster on its track record: at least two years of sustained writing, with depth, accuracy, and an independent view.

A source goes on the watch list if it:

- Has less than two years of sustained writing
- Has been dormant for over a year, unless their writing clearly continues elsewhere

The watch list supplies leads, but its sources are never cited. A source is vetted again when it goes quiet, its writing weakens, or a blocker clears.

Two markings limit how an opinion can cite a roster source, and CI enforces both:

- **Corroborate:** a long track record but thin depth. An opinion can cite the source, but every claim it supports also needs an unmarked source.
- **Discovery-only:** an aggregator, such as a newsletter or a curated list of links. It's never cited, and an opinion cites the primary source it leads to instead.

<!-- diagram: source-standing -->

## Research is staged, never merged in place

A research topic saves the evidence on a subject in its own pull request. A second pull request then promotes it into the opinions and templates, or discards it, and deletes the topic. A partial promotion keeps the blocked remainder staged until `vet-source` clears its source.

<!-- diagram: research-lifecycle -->

## House opinions

House opinions are preferences from experience, which no vetted source backs. Each belongs to a house profile, owned by a person or an organisation. The site shows none by default, so every page is sourced community practice. To see a profile's house opinions, choose it in the header. Each one starts with **House:** and appears next to the sourced recommendation it changes. For how profiles work, including private ones for your own organisation, see [House profiles](house-profiles.md).
