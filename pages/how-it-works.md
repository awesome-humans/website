---
hide:
  - toc
---

# How it works

Agent skills maintain each ecosystem's repository, and nothing reaches an opinion without passing CI and the owner's review. The diagrams below are an overview. Where one disagrees with a skill or the roster's admission criteria, follow the skill or the criteria, which each ecosystem's pages link to.

## Every change is a pull request

Each skill works on its own branch, and its changes land through a pull request. CI checks the metadata on every opinion and template, that every cited source is on the roster and citable, and that every link resolves. The owner then reviews and merges it.

Two skills only report: `audit-freshness` finds stale review dates and lagging version pins, and `verify-project` grades an external codebase against the opinions. Their findings, a scheduled release watch, and a monthly harvest reminder start the next run.

<!-- diagram: maintenance-pipeline -->

## Sources need a track record

A source joins the roster on its track record: at least two years of sustained writing, with depth, accuracy, and an independent view. A source with less than two years, or dormant for over a year, goes on the watch list, which supplies leads but is never cited. Two markings limit what a citable source can support. A source is vetted again when it goes quiet or a blocker clears.

<!-- diagram: source-standing -->

## Research is staged, never merged in place

A research topic saves the evidence on a subject in its own pull request. A second pull request then promotes it into the opinions and templates, or discards it, and deletes the topic either way. A topic on disk is unresolved.

<!-- diagram: research-lifecycle -->

## House opinions

Each repository's owner outranks the roster. The owner's preferences are recorded separately, and marked **House:** wherever they appear, so you can tell community practice from local convention.
