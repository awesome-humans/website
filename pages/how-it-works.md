---
hide:
  - toc
---

# How it works

Agent skills maintain each ecosystem's repository, and nothing becomes an opinion without passing CI and the owner's review. The diagrams below are an overview. Where one disagrees with a skill or the roster's admission criteria, follow the skill or the criteria, which each ecosystem's pages link to.

## Every change is a pull request

Each skill works on its own branch, and its changes land through a pull request. CI checks the metadata on every opinion and template, that every cited source is on the roster and citable, and that every link resolves. The owner then reviews and merges it.

Two skills only report: `audit-freshness` finds stale review dates and lagging version pins, and `review-project` grades an external codebase against the opinions. Their findings, a scheduled release watch, and a monthly harvest reminder start the next run.

<!-- diagram: maintenance-pipeline -->

## Sources need a track record

A source joins the roster on its track record: at least two years of sustained writing, with depth, accuracy, and an independent view. A source with less than two years, or dormant for over a year, goes on the watch list, which supplies leads but is never cited. A source is vetted again when it goes quiet or a blocker clears.

Two markings limit how an opinion can cite a roster source, and CI enforces both:

- **Corroborate:** a long track record but thin depth. An opinion can cite the source, but every claim it supports also needs an unmarked source.
- **Discovery-only:** an aggregator, such as a newsletter or a curated list of links. It's never cited, and an opinion cites the primary source it leads to instead.

<!-- diagram: source-standing -->

## Research is staged, never merged in place

A research topic saves the evidence on a subject in its own pull request. A second pull request then promotes it into the opinions and templates, or discards it, and deletes the topic either way. A topic on disk is unresolved.

<!-- diagram: research-lifecycle -->

## House opinions

House opinions are preferences from experience, which no vetted source backs. Each belongs to a house profile, owned by a person or an organisation. The site shows none by default, so every page is sourced community practice. Choose a profile in the header to see its house opinions, each marked **House:** beside the sourced text it changes. For how profiles work, including private ones for your own organisation, see [House profiles](house-profiles.md).
