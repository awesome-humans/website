# Usage

Try the opinions and skills from the site without installing anything, or install the skills in your project.

## Try it without installing

Nothing to install. Your coding agent fetches the opinions and skills from the site each time. Each prompt asks for raw text, so your agent reads the rules in full and not a summary of them.

- **Follow the opinions.** Tell your agent to follow them when it writes code:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then follow its conventions when writing code
  ```

  The agent picks the ecosystem from your project's files, such as `Cargo.toml` or a `.csproj`.

- **Check an existing project.** Ask your agent to run `review-project`, for [.NET](dotnet/skills/review-project.md) or [Rust](rust/skills/review-project.md):

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its review-project skill on <repository>
  ```

  To narrow the review, say what to include or leave out, and optionally name a house profile:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its review-project skill on <repository>, focus on logging and testing, skip CI, use the simon-mckenna house profile
  ```

- **Research a topic.** Ask your agent to run `research-topic`, for [.NET](dotnet/skills/research-topic.md) or [Rust](rust/skills/research-topic.md), which answers from the opinions and the vetted sources, citing each claim:

  ```text
  Fetch awesome-humans.net/llms.txt and every file it links as raw text, then use its research-topic skill to research how to pin dependency versions
  ```

## Install it in your project

Install the skills in your project. Your agent then reads the opinions and templates from the project's own copy, with nothing to fetch.

Each ecosystem installs three skills, such as `follow-dotnet-opinions`, `research-dotnet-topic`, and `review-dotnet-project`. Your agent follows the opinions as it writes code, answers a question from them, and checks a project against them.

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

Each command installs into the project you run it in, and records what it installed in `skills-lock.json`. To install for every project on your machine, add `--global`.

`npx skills check` tells you when an opinion has changed, and `npx skills update` fetches it.
