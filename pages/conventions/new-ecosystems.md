# New ecosystems

A new ecosystem goes through nine stages, from an empty repository to an established set of opinions. This page describes each stage, and what to expect while research outnumbers opinions. A new ecosystem's `PLAN.md` can link here instead of repeating the stages. Rust, started on 2026-10-14, is the worked example.

No third ecosystem starts until `dotnet` and `rust` have settled the multi-repository approach, a hold set on 2026-10-18. Problems with the approach are easier to fix across two repositories than three or more.

## Stages

Each stage ends with a check you can run or read. For the full steps, see Rust's `PLAN.md`.

1. **Scaffold the repository.** Copy the layout, `AGENTS.md`, `REVIEW.md`, and CI from an existing ecosystem. Port the checks to the ecosystem's own language, such as Go for a Kubernetes ecosystem, so the repository's own code is in the language its opinions cover. Adapt `REVIEW.md` to match, because it names the checks CI runs and the toolchain an example must build with. From then on, a pull request that changes one ecosystem's `REVIEW.md` links the matching pull request in each other ecosystem, or says why that one doesn't need the change. Done when `just verify` passes on empty `opinions/`, `research/`, and `templates/` directories.
2. **Vet the roster.** Run `vet-source` for each candidate in `AWESOME-HUMANS.md`. Done when each topic in the plan's first-opinions table has a Citable source expected to carry it.
3. **Name the references.** Under Named references in `AWESOME-HUMANS.md`, list the repositories that count as references, and the link form for each. Done before the first `research-topic` run, because most topics cite a reference.
4. **Add the skills.** Copy them from an existing ecosystem, and adapt them. Done when each skill's `SKILL.md` names the repository and its paths, and `skills-ref` validates it.
5. **Join the site.** Add the ecosystem to website's `ecosystems.toml` with `status = "soon"`. The home page then shows it as coming, and only previews of its own pull requests build it. Done when a preview stages its pages.
6. **Research the first topics.** Run `research-topic` for each topic in the plan's table, one pull request each. Done when every topic in the table has merged.
7. **Resolve them into opinions.** Run `resolve-research` for each merged topic, and set `status = "live"` when the first opinion merges. Done when the ecosystem is live. Rust went live on 2026-10-18: rust#18 merged `opinions/rust.md`, and website#91 published it the same day.
8. **Hold the checks to the opinions.** Read every check written in the ecosystem's language against its opinions and templates, and fix what doesn't follow them. The repository should follow the practices it recommends. Done when every check has been read against them, and the fixes have merged.
9. **Delete the plan.** Once every topic in the table is promoted or discarded, delete `PLAN.md` in the pull request that resolves the last one. The ecosystem is then established.

## While research outnumbers opinions

This is stages 6 to 9. On 2026-10-25, Rust had one opinion, two merged topics waiting on `resolve-research`, and seven topics in open pull requests. That's normal, and so are these:

- **Readers and agents see little of the research.** The site marks a merged topic with an "Unresolved research" lead. The ecosystem's `llms.txt` lists opinions, templates, and skills, but never research. A topic in an open pull request isn't on the site at all.
- **Research finds gaps in the rules.** Topics written in parallel apply an unsettled rule in different ways: Rust's open topics linked RFCs and RustSec advisories in three URL forms before rust#60 settled them. Fix the rule in its own pull request, then check each open topic against it. Don't fix it inside a research pull request, because the other topics won't see it.
- **Topics need sources the plan didn't expect.** The plan expected `research/rust.md` to draw its idioms from `rust-docs`, `rust-blog`, and `niko-matsakis`. It drew on `burntsushi`, `corrode`, and `matklad` instead, which were already Citable. When a source isn't on the roster, run `vet-source` for it, or promote the covered part and leave the rest staged.
- **Resolve in the plan's order.** The table puts the foundations first, such as the language and project structure, so a later opinion can link to an earlier one instead of restating it.

## Skills with few opinions

Most skills work on opinions, so before stage 7 they have little to do. Read their results with that in mind:

- **`audit-freshness`** reports nothing to check while the repository has no opinions, and fails. It flags a research topic 90 days after its `last-reviewed` date, so a merged topic left unresolved becomes a finding.
- **`review-project`** compares a project only with the areas the opinions cover. A short report from few opinions means little coverage, not a compliant project.
- **`review-opinions`** checks only opinions and templates, so before stage 7 it has little more than the template comments to read. Run a full pass when the first opinion merges, so the opinions start from citations known to hold. After that, `harvest-sources` checks the citations each harvest changes.
- **The agent reviewer** follows `REVIEW.md`, whose Important findings cover opinions, templates, skills, and checks. The one Important finding specific to research is a rule changed alongside a topic, so the owner's review carries the rest of a research pull request.
- **`harvest-sources`** edits an existing opinion when a post fits one. For a post on any other topic, it first checks `research/` and the open research pull requests, and adds the post to a topic that covers it. If none does, it adds a stub opinion.
- **The version refresh skill,** such as `refresh-rust-versions`, updates opinions and templates only. Research topics keep the versions they were written against until `resolve-research` updates them.
