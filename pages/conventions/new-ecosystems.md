# New ecosystems

These are the stages a new ecosystem goes through, from an empty repository to an established set of opinions, and what to expect in the stretch between the first research and that set. They live here once, so each ecosystem's `PLAN.md` can point to them instead of repeating them. Rust is the worked example: `awesome-humans/rust` started on 2026-10-14.

A third ecosystem is on hold until `dotnet` and `rust` have settled the multi-repository approach. For details, see the website's `PLAN.md`.

## Stages

Each stage ends with a check you can run or read. Rust's `PLAN.md` holds the full steps for each one.

1. **Scaffold the repository.** Copy the layout, `AGENTS.md`, and CI from an existing ecosystem, and port its checks. Done when `just verify` passes on empty `opinions/`, `research/`, and `templates/` directories.
2. **Vet the roster.** Run `vet-source` for each candidate in `AWESOME-HUMANS.md`. Done when every topic in the plan's first-opinions table has a Citable source expected to carry it.
3. **Settle the reference rules.** Name the repositories that count as references under Named references in `AWESOME-HUMANS.md`, and the URL form each one takes. Done before the first `research-topic` run, because every topic cites references.
4. **Add the skills.** Done when each skill's `SKILL.md` names the repository and its paths, and `skills-ref` validates it.
5. **Join the site.** Add the ecosystem to `ecosystems.toml` in this repository with `status = "soon"`. The home page shows it as coming, and only its own pull request previews build it. Done when a preview stages its pages.
6. **Research the first topics.** Run `research-topic` for each topic in the plan's table, one pull request each.
7. **Resolve them into opinions.** Run `resolve-research` for each merged topic. When the first opinion merges, set `status = "live"`. Rust went live on 2026-10-19, the day rust#18 merged `opinions/rust.md`.
8. **Delete the plan.** Once every topic in the table is promoted or discarded, delete `PLAN.md` in the pull request that resolves the last one. The ecosystem is then established.

## While research comes in

Between stages 6 and 8, the repository has more research than opinions. On 2026-10-25, Rust had one opinion, two merged topics waiting on `resolve-research`, and seven topics in open pull requests. Expect that shape, and expect these:

- **Readers and agents see only the opinions.** The site renders a merged topic with an "Unresolved research" lead, and the ecosystem's `llms.txt` lists opinions, templates, and skills, never research. A topic in an open pull request isn't on the site at all.
- **Research finds gaps in the rules.** Topics written in parallel apply an unsettled rule in different ways. Rust's open topics linked RFCs and RustSec advisories in three URL forms before rust#60 settled them. Fix the rule in its own pull request, then check each open topic against it. Don't fix a rule inside a research pull request, because the next topic won't see it.
- **Topics need sources the plan didn't expect.** `research/rust.md` needed `burntsushi`, `corrode`, and `matklad` for its idioms, none of which the plan named. Run `vet-source` for a missing source, or promote the part that's covered and leave the rest staged.
- **Resolve in the plan's order.** The table puts the foundations first, such as the language and project structure, so a later opinion can link to an earlier one instead of restating it.

## Skills on a thin corpus

Most skills work on opinions, so they have little to do before stage 7. Read their results with that in mind:

- **`audit-freshness`** reports that there's nothing to check when the repository has no opinions, and doesn't pass. It reports a research topic 90 days after its `last-reviewed` date, so a merged topic left unresolved becomes a finding.
- **`review-project`** compares a project only with the areas the opinions cover. A short report from a thin corpus means little coverage, not a compliant project.
- **`harvest-sources`** edits only opinions that exist, and turns a post on any other topic into a stub opinion. Before you add a stub, check `research/` and the open research pull requests. If a topic covers the subject, add the post to that topic instead.
- **The version refresh skill,** such as `refresh-rust-versions`, updates opinions and templates only. Research topics keep the versions they were written against until `resolve-research` updates them.
