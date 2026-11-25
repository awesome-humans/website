# Usage

Try the opinions and skills from the site without installing anything, or install the skills in your project.

## Try it without installing

Nothing to install. Your coding agent fetches the opinions and skills from the site each time. Each prompt asks for raw text, so your agent reads the rules in full and not a summary of them.

- **Check an existing project.** Ask your agent to run `review-project`, for [.NET](dotnet/skills/review-project.md) or [Rust](rust/skills/review-project.md):

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its review-project skill on <repository>
  ```

  To narrow the review, say what to include or leave out, and optionally name a house profile:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its review-project skill on <repository>, focus on logging and testing, skip CI, use the simon-mckenna house profile
  ```

  Name the topics your ecosystem's opinions cover. For a Rust project:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its review-project skill on <repository>, focus on panics and lints, skip the edition
  ```

- **Research a topic.** Ask your agent to run `research-topic`, for [.NET](dotnet/skills/research-topic.md) or [Rust](rust/skills/research-topic.md), which answers from the opinions and the vetted sources, citing each claim:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its research-topic skill to research how to pin dependency versions
  ```

  The question can be about one ecosystem, such as a .NET feature or a Rust tool:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its research-topic skill to research whether to turn on runtime async
  ```

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its research-topic skill to research whether to adopt cargo-nextest
  ```

To have your agent follow the opinions every time it writes code, [install the skills](#install-it-in-your-project). If your agent can't install skills, end the prompt with "then follow its conventions when writing code" instead. It picks the ecosystem from your project's files, such as `Cargo.toml` or a `.csproj`, but you need to repeat the prompt in each session.

## Install it in your project

Install the skills in your project. Your agent then reads the opinions and templates from the project's own copy, with nothing to fetch.

Each ecosystem installs three skills, named for the ecosystem:

| .NET                                                         | Rust                                                     | What your agent does with it                                                |
| ------------------------------------------------------------ | -------------------------------------------------------- | --------------------------------------------------------------------------- |
| [`follow-dotnet-opinions`](dotnet/skills/follow-opinions.md) | [`follow-rust-opinions`](rust/skills/follow-opinions.md) | Applies the opinions and templates while it writes or changes code          |
| [`research-dotnet-topic`](dotnet/skills/research-topic.md)   | [`research-rust-topic`](rust/skills/research-topic.md)   | Answers a question from the opinions and vetted sources, citing each claim  |
| [`review-dotnet-project`](dotnet/skills/review-project.md)   | [`review-rust-project`](rust/skills/review-project.md)   | Checks a project against the opinions and templates, and reports deviations |

Choose one address to suit your needs:

- **Every ecosystem:**

  ```sh
  npx skills add https://awesome-humans.net
  ```

- **One ecosystem:** add its path. This installs the three .NET skills alone.

  ```sh
  npx skills add https://awesome-humans.net/dotnet
  ```

- **A [house profile](house-profiles.md):** add the profile's name, after the site or after an ecosystem. The skills then hold that profile's house opinions. An ecosystem has a profile's address only when the profile holds opinions there. After the site, the profile's name installs every ecosystem's skills, with the default copy for an ecosystem the profile doesn't cover.

  ```sh
  npx skills add https://awesome-humans.net/simon-mckenna
  npx skills add https://awesome-humans.net/dotnet/simon-mckenna
  ```

The CLI asks which skills to install. Keep the `follow-<ecosystem>-opinions` skill selected, because it carries the opinions and templates the other two read.

Each command installs into the project you run it in, and records what it installed in `skills-lock.json`.

`npx skills check` tells you when an opinion has changed, and `npx skills update` fetches it.

### Install it for every project on your machine

```sh
npx skills add https://awesome-humans.net/dotnet --global
```

- **A collaborator or a CI agent doesn't get the skills.** When they need them, install in the project.
- **Choose the default opinions or a house profile.** Their skills have the same names, so a second install replaces the first.
- **Add `--global` to the other commands too.** `npx skills check --global` tells you when an opinion has changed, `npx skills update --global` fetches it, and `npx skills remove awesome-humans.net --global` uninstalls.
