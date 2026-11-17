# Worktrees

Work in a git worktree, with one branch per directory. The local clone is bare, and each branch is checked out beside it, so you move between pieces of work with `cd` instead of `git checkout`. An in-place branch switch changes the tree under anything that holds a path into it, and discards gitignored state such as `node_modules/` and `.venv/`.

- **Starting:** Start every new piece of work as a new worktree, with `git worktree add -b <branch> <dir> main`.
- **Branch names:** Use the commit's Conventional Commits type (`docs/`, `fix/`, `feat/`, `ci/`, or `chore/`) and a kebab-case slug. `automation/` is reserved for workflows. Settle the name before you open the pull request: renaming the head branch of an open pull request closes it.
- **Directory names:** Name the directory after the branch, with slashes replaced by dashes, so `feat/scaffold` becomes `feat-scaffold/`.
- **Setup:** A fresh worktree has no gitignored local state. Run `just install` in it.
- **Finishing:** When a worktree's pull request merges, offer to delete the worktree with `git worktree remove <dir>`, and then its branch. Ask first: the branch might still hold work that never reached the pull request.
