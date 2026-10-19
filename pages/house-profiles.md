<!-- data-house-picker shows the header's profile picker here, though the page has no house content. -->

# House profiles { data-house-picker }

Every page on this site is sourced community practice, unless you choose a house profile. A house profile is a named set of house opinions, owned by a person or an organisation: their preferences from experience, which no vetted source backs. Choosing one shows its house opinions beside the sourced text they change.

## Choose a profile

- **On the site:** Choose a profile from the picker in the header, which shows on this page and on each page with house opinions. Your browser remembers the choice. To link to a page with a profile chosen, add `?house=<profile>` to its URL, such as `?house=simon-mckenna`. To clear the choice, choose **No house opinions**, or add `?house=none`.
- **For an agent:** Point it at an ecosystem's `llms-<profile>.txt` instead of its `llms.txt`, such as `/dotnet/llms-simon-mckenna.txt`. The root [`llms.txt`](llms.txt) lists every profile's files. Each ecosystem's `llms.txt` carries no house opinions.
- **With `review-project`:** Name the profile when you run the skill. Without one, it checks sourced practice only.

Search covers the sourced text only, so a result never lands on a house opinion you can't see.

## What a house opinion looks like

In an ecosystem's repository, a house opinion is a block beside the sourced recommendation it changes. It opens with `/// house | <profile>`, starts with `**House:**`, and closes with `///`:

```markdown
/// house | simon-mckenna

**House:** Treat warnings as errors on every machine, not only in CI. …

///
```

A template marks a house opinion as a region between `house:<profile> begin` and `house:<profile> end` comment lines, in the file's own comment syntax. The site shows each template without its regions, and each profile's copy below it. The file's `sources:` list names the profile as `house:<profile>`.

The sourced text stays whole. With a profile chosen, you see both, and the house opinion wins where they conflict. Each ecosystem's `HOUSE-OPINIONS.md` records every house opinion woven in, and the profile it belongs to. For how an opinion gets woven in, and the rules for marking it, see [House opinions](conventions/house-opinions.md).

## Hosted profiles

The site registers each profile in [`houses.toml`](https://github.com/awesome-humans/website/blob/main/houses.toml), with the ecosystems that hold its opinions. The header's picker lists them. A hosted profile carries the site's name, so the repository owner approves each one, as for a contributor's opinion.

## Keep your own profile private

An organisation can keep its house opinions in its own repository, with nothing hosted here. Write one overlay file per ecosystem, `house/<ecosystem>.md`, and point your agents at the ecosystem's default `llms.txt` and then at the overlay.

The overlay uses the same blocks, grouped under a heading per opinion file they change:

```markdown
# House overlay: acme, .NET

## opinions/testing.md

/// house | acme

**House:** Name test classes `<Type>Should`, as in `BasketShould`. …

///
```

Tell your agents to read each block as a house opinion on the opinion file its heading names, and to follow the block where it conflicts with that file.
